from functools import partial
from operator import itemgetter
from os.path import join
import re
from typing import List, Optional, Tuple
from pprint import pprint
from enum import Enum
from random import random
from fnmatch import fnmatch


class Language(Enum):
    '''
    Languages supported by the origin
    '''
    EN = 'en'
    DE = 'de'


# Name of the default index document
DEFAULT_INDEX_DOCUMENT = 'index.html'

# List of all Language values
LANGUAGE_VALUES = [l.value for l in Language]

# Regex to match Accept-Language values in the *;q= form
Q_RE = re.compile(r'([^,\s]+)q=([\d\.]+)')

EXCLUDES = []


class Uri:
    def __init__(self, uri):
        self.original = uri
        self._original_uri_split = uri.split('/')
        self._expanded_uri_split = self._expand_uri(
            self._original_uri_split).split('/')

    def _expand_uri(self, us):
        print(us[-1])
        if us[-1] == '':
            # uri ends in a / (e.g. /projects/)
            us[-1] = DEFAULT_INDEX_DOCUMENT
        elif not fnmatch(us[-1], '*.*'):
            print('why though?')
            # uri ends in a document that does not have an
            # extension (e.g. /projects/file)
            us.append(DEFAULT_INDEX_DOCUMENT)

        return '/'.join(us)

    def _get_lang(self) -> Optional[Language]:
        if len(self._expanded_uri_split) < 2:
            return None

        l = self._expanded_uri_split[1].lower()
        if not l in LANGUAGE_VALUES:
            return None

        return Language(l)

    @property
    def expanded(self):
        return '/'.join(self._expanded_uri_split)

    @property
    def language(self) -> Optional[Language]:
        return self._get_lang()

    @language.setter
    def language(self, lang: Language):

        if self._get_lang():
            if lang is not None:
                self._expanded_uri_split[1] = lang.value
            else:
                del self._expanded_uri_split[1]
        else:
            if lang is not None:
                self._expanded_uri_split.insert(1, lang.value)

    @property
    def document(self):
        '''
        document requested in `uri`, if any
        '''
        if self.expanded.endswith('/'):
            return None
        return self._expanded_uri_split[-1]

    @property
    def document_suffix(self):
        '''
        file suffix for the requested resource or None
        '''
        d = self.document
        if not d:
            return ''

        ms = re.findall(r'\.(\w+)$', d)
        if not ms:
            return ''

        return ms[0]


def get_request(event):
    '''
    get the request object from the CloudFront event
    '''
    rs = event.get('Records', [])
    if len(rs) < 1:
        return

    return rs[0].get('cf', {}).get('request', {})


def parse_accept_language(h: str) -> List[Tuple[str, float]]:
    '''
    parse the Accept-Language header into a sorted list of tuples consisting
    of the language and a weight. The weight is 1.0 if none was provided.
    '''

    def must_float(n):
        try:
            return float(n)
        except ValueError:
            return 0.0

    vs = [v.strip() for v in h.split(',')]
    if not vs:
        return []

    langs = []
    for v in vs:
        v = v.lower()
        l, q = '', ''
        mt = Q_RE.match(v)
        if mt:
            l, q = mt.groups()

            l = l.rstrip(';')
            q = must_float(q)
        else:
            l, q = v, 1.0

        langs.append((l, q))

    langs.sort(key=itemgetter(1), reverse=True)
    return langs


def determine_language(parsed_lang_header: List[Tuple[str, float]]) -> Language:
    '''
    determine the language to use from the parsed Accept-Language header values
    '''

    if not parsed_lang_header:
        return Language.EN
    for lang, _ in parsed_lang_header:
        if 'en' in lang:
            return Language.EN
        if 'de' in lang:
            return Language.DE

    return Language.EN


def lambda_handler(event, context):
    request = get_request(event)
    request_uri = Uri(request['uri'])

    headers = {k: v[0]['value'] for k, v in request.get('headers', {}).items()}
    al = headers.get('accept-language')
    if al:
        lang = determine_language(parse_accept_language(al))
    else:
        lang = Language.EN

    # if no language was provided in the URI (e.g. /index.html)
    # and the request is for a page (document_suffix=htm*) we add
    # the language determined earlier
    if not request_uri.language and request_uri.document_suffix.startswith('htm'):
        request_uri.language = lang

    request['uri'] = request_uri.expanded
    return request
