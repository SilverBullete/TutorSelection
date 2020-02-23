import time
import base64
import hmac
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex

key = "selection"


# 加密内容需要长达16位字符，所以进行空格拼接
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text


# 加密秘钥需要长达16位字符，所以进行空格拼接
def pad_key(key):
    while len(key) % 16 != 0:
        key += ' '
    return key


# 加密密码
def encrypt_password(password):
    aes = AES.new(pad_key(key).encode(), AES.MODE_ECB)
    encrypted_text = aes.encrypt(pad(password).encode())
    encrypted_text_hex = b2a_hex(encrypted_text).decode("utf-8")
    return encrypted_text_hex


# 判断密码是否正确
def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password)


# 生成token
def generate_token(key, expire=3600):
    '''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 检验token是否过期
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
        # token certification success
    return True
