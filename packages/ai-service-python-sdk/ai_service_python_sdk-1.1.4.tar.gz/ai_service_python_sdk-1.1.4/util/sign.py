import hashlib
import hmac


def build_sign_string(method, path, body, query_params):
    sign = method + '\n'
    sign += md5(body) + '\n'
    sign += path
    return sign


def create_sign(sign, secret):
    key = secret.encode(encoding='utf-8')
    sha = hmac.new(key, sign.encode(encoding='utf-8'), digestmod=hashlib.sha256).hexdigest()
    return sha


def md5(msg):
    hl = hashlib.md5()
    hl.update(msg.encode(encoding='utf-8'))
    return hl.hexdigest()
