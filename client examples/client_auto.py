#test tokens:

#expired_token: b0ad8b2122d5f9bdec6024290240b253e53734f44badf3a0dbe9e5a5f6224c8b
#active_token: 6b264705db27f7c52c883bb687e8ecf7f9a92fde2af5ed85705760fce39804ce
#non-expirable_token: admin1

import urllib.request
import json
import sys

if len(sys.argv) < 2:
    print('Call me like this:', sys.argv[0], 'url_to_stream1', '[url_to_stream2] ...')
    exit()

body = \
{
    'auth_token' : 'admin1', #test token
    'streams' : sys.argv[1:]
} 

myurl = "http://127.0.0.1:1234/api/"
req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
response = urllib.request.urlopen(req, jsondataasbytes)

print (response.read().decode())
