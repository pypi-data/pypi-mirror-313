import hmac
import json
import hashlib

def sign(data, secret):
    return hmac.new(secret.encode('utf-8'), json.dumps(data, separators=(',', ':')).encode('utf-8'),digestmod=hashlib.sha1).hexdigest()