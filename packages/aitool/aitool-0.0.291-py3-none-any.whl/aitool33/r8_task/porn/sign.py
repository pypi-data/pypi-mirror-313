# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
import hmac
from hashlib import sha1
import codecs
import base64

AUTH_PREFIX_V1 = "VARCH1-HMAC-SHA1"
DEFAULT_TTL = 3600 # in seconds
SEP = ":"


def sign_rpc_request(ak, sk, method='', caller='', extra={}, ttl=0):
    """ sign_rpc_request

            ak: access_key
            sk: secret_key
    """
    if ttl <= 0:
        ttl = DEFAULT_TTL
    deadline = str(int(time.time())+ttl)

    arr = ['method='+method, 'caller='+caller, 'deadline='+deadline]
    arr.extend([k+'='+extra[k] for k in sorted(extra.keys())])


    raw = '&'.join(arr)
    hashed = hmac.new(codecs.encode(sk), codecs.encode(raw), sha1)
    dig = hashed.digest()
    ciphertext = base64.standard_b64encode(dig)
    return SEP.join([AUTH_PREFIX_V1, ak, deadline, codecs.decode(ciphertext)])

def sign_http_request(ak, sk, method, url, ttl=0):
    """ sign_http_request
    """
    # TODO(kuangchanglang): python 3 support
    if sys.version_info.major == 2:
        from urlparse import urlparse, parse_qsl
    else:
        from urllib.parse import urlparse, parse_qsl
    q = urlparse(url)
    m = method+q.path
    caller = ''
    extra = dict(parse_qsl(q.query))
    return sign_rpc_request(ak, sk, method=m, caller=caller, extra=extra,
                            ttl=ttl)

if __name__ == '__main__':
    ak = '123'
    sk = '467'
    method = 'MGetPlayInfosV2'
    caller = 'content.arch.dianch'
    extra = {
        'vid': 'v09044b10000bnvdeqc1psvnipk18shg',
        'a': 'b',
        '1': '333'
    }
    print(sign_rpc_request(ak, sk, method, caller, extra=extra))

    url = 'http://127.0.0.1:9998/v1/api/get_video_info?vid=v09044b10000bnvdeqc1psvnipk18shg&a=b&1=333'
    print(sign_http_request(ak, sk, 'GET', url))
