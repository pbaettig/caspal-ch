
from main import *


def test_parse_accept_language():
    cases = [
        (
            'de;q=0.7, *;q=0.5, fr-CH, fr;q=0.9, en;q=0.8', 
            [('fr-ch', 1.0), ('fr', 0.9), ('en', 0.8), ('de', 0.7), ('*', 0.5)],
        )
    ]
    for test_input, expected_output in cases:
        out = parse_accept_language(test_input)
        for i in range(len(out)):
            assert out[i] == expected_output[i]

def test_determine_language():
    cases = [
        (
           [('fr-ch', 1.0), ('fr', 0.9), ('en', 0.8), ('de', 0.7), ('*', 0.5)],
           Language.EN
        ),
        (
            [],
            Language.EN
        ),
        (
            [('fr', 0.9), ('de', 0.8), ('en', 0.7)],
           Language.DE
        )
    ]
    for test_input, expected_output in cases:
        out = determine_language(test_input)
        assert out == expected_output

def test_lambda_handler():
    cases = [
        (('/', 'de-CH'), '/de/index.html'),
        (('/', 'en'), '/en/index.html'),
        (('/page/123', 'de;q=0.8, *;q=0.5, fr-CH, fr;q=0.9, en;q=0.7'), '/de/page/123/index.html'),
        (('/file.txt', 'de-CH'), '/file.txt'),
        (('/cv', 'en'), '/en/cv/index.html'),
        (('/bubu/', 'fr'), '/en/bubu/index.html'),
        (('/de/bubu/page.html', 'fr'), '/de/bubu/page.html'),
        (('/404.html', 'en-US'), '/en/404.html'),
        (('/404.html', ''), '/en/404.html'),
        (('/404.html', 'de-AT'), '/de/404.html'),
        (('/de/404.html', 'de-AT'), '/de/404.html'),
        (('/en/projects', 'de-AT'), '/en/projects/index.html'),
        (('/projects', 'de-AT'), '/de/projects/index.html'),
    ]

    def event(uri, lang):
        return {
            "Records": [
                {
                    "cf": {
                        "config": {
                            "distributionId": "EXAMPLE"
                        },
                        "request": {
                            "uri": uri,
                            "method": "GET",
                            "clientIp": "2001:cdba::3257:9652",
                            "headers": {
                                "accept-language": [
                                    {
                                        "key": "Accept-Language",
                                        "value": lang
                                    }
                                ],
                                "user-agent": [
                                    {
                                        "key": "User-Agent",
                                        "value": "test-agent"
                                    }
                                ],
                            }
                        }
                    }
                }
            ]
        }
    def event_uri(event):
        return event['Records'][0]['cf']['request']['uri']

    for (test_uri, test_lang), expected_output in cases:
        e = event(test_uri, test_lang)
        lambda_handler(e, None)
        assert event_uri(e) == expected_output

def test_uri():
    u = Uri('/')
    assert u.expanded == '/index.html'
    assert u.language is None
    u.language = Language.DE
    assert u.expanded == '/de/index.html'
    u.language = None
    assert u.expanded == '/index.html' 

    assert u.document == 'index.html'
    assert u.document_suffix == 'html'



if __name__ == '__main__':
    lambda_handler(
        {
            "Records": [
                {
                "cf": {
                    "config": {
                    "distributionId": "EXAMPLE"
                    },
                    "request": {
                        "uri": "/cv/",
                        "method": "GET",
                        "clientIp": "2001:cdba::3257:9652",
                        "headers": {
                            "accept-language": [
                            {
                                "key": "Accept-Language",
                                "value": "de;q=0.81, *;q=0.5, fr-CH, fr;q=0.9, en;q=0.8"
                            }
                            ],
                            "user-agent": [
                            {
                                "key": "User-Agent",
                                "value": "test-agent"
                            }
                            ],
                            "authorization": [
                            {
                                "key": "Authorization",
                                "value": "Basic cGFzY2FsOnBhc3N3b3Jk"
                            }
                            ]
                        }
                    }
                }
                }
            ]
        }, None)