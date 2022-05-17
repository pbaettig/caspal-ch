from os.path import join
import re


DEFAULT_INDEX_DOCUMENT = 'index.html'


def file_suffix(uri):
    ms = re.findall(r'\.(\w+)$', uri)
    if not ms:
        return None

    return ms[0]

def get_request(event):
    rs = event.get('Records', [])
    if len(rs) < 1:
        return

    return rs[0].get('cf', {}).get('request', {})


def lambda_handler(event, context):
    request = get_request(event)
    uri = request.get('uri')
    print(f'got request for {uri}: ', end='')
    
    if not uri or uri == '/':
        print('no need to rewrite')
        return request

    suffix = file_suffix(uri)
    print(suffix)
    if not suffix:
        request['uri'] = join(uri, DEFAULT_INDEX_DOCUMENT)
        print(f'rewrite to {request["uri"]}')
    return request