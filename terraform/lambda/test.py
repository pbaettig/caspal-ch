from main import lambda_handler
from main import file_suffix

for uri in ['/abcd/def/12.txt', '/', '/cv', '/cv/']:
    print(f'{uri}: -> {file_suffix(uri)}')

lambda_handler(
    {
        "Records": [
            {
            "cf": {
                "config": {
                "distributionId": "EXAMPLE"
                },
                "request": {
                    "uri": "/bubu/",
                    "method": "GET",
                    "clientIp": "2001:cdba::3257:9652",
                    "headers": {
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