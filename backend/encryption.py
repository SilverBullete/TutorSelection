import time
import jwt

from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex

from TutorSelection.settings import PASSWORD_KEY, TOKEN_KEY



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
    aes = AES.new(pad_key(PASSWORD_KEY).encode(), AES.MODE_ECB)
    encrypted_text = aes.encrypt(pad(password).encode())
    encrypted_text_hex = b2a_hex(encrypted_text).decode("utf-8")
    return encrypted_text_hex


# 判断密码是否正确
def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password)



"""payload 中一些固定参数名称的意义, 同时可以在payload中自定义参数"""
# iss  【issuer】发布者的url地址
# sub 【subject】该JWT所面向的用户，用于处理特定应用，不是常用的字段
# aud 【audience】接受者的url地址
# exp 【expiration】 该jwt销毁的时间；unix时间戳
# nbf  【not before】 该jwt的使用时间不能早于该时间；unix时间戳
# iat   【issued at】 该jwt的发布时间；unix 时间戳
# jti    【JWT ID】 该jwt的唯一ID编号

# headers
headers = {
    'alg': "HS256",  # 声明所使用的算法
}

"""headers 中一些固定参数名称的意义"""
# jku: 发送JWK的地址；最好用HTTPS来传输
# jwk: 就是之前说的JWK
# kid: jwk的ID编号
# x5u: 指向一组X509公共证书的URL
# x5c: X509证书链
# x5t：X509证书的SHA-1指纹
# x5t#S256: X509证书的SHA-256指纹
# typ: 在原本未加密的JWT的基础上增加了 JOSE 和 JOSE+ JSON。JOSE序列化后文会说及。适用于JOSE标头的对象与此JWT混合的情况。
# crit: 字符串数组，包含声明的名称，用作实现定义的扩展，必须由 this->JWT的解析器处理。不常见。


# 生成token
def generate_token(id, user_type):
    token_dict = {
        'iat': time.time(),
        'exp': time.time() + 86400,
        'id': id,
        'type': user_type
    }
    jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                           TOKEN_KEY,  # 进行加密签名的密钥
                           headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                           ).decode('ascii')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
    return jwt_token


# 检验token是否过期
def certify_token(token):
    data = None
    try:
        data = jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])
    except Exception as e:
        # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
        return {"message": str(e)}
    return data
