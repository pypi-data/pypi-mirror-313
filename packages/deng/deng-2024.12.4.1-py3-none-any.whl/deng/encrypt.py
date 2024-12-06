import jwt
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as oaep_cipher

from .file import check_path_is_exits


def to_encode(connect: str) -> str:
    return str(
        base64.b64encode(bytes(connect, encoding="utf8")),
        encoding="utf8",
    )


def to_decode(connect: str) -> str:
    return str(base64.b64decode(bytes(connect, encoding="utf8")), encoding="utf8")


def sum_md5(param_str: str) -> str:
    """计算字符串MD5值"""
    if isinstance(param_str, int):
        param_str = str(param_str)
    _hash = hashlib.md5()
    _hash.update(param_str.encode("UTF-8"))
    return _hash.hexdigest()


def md5sum(*, _file_path: str = None, _string: str = None):
    """计算文件md5值"""
    if _file_path:
        check_path_is_exits(_file_path, path_type="file")
        with open(_file_path, "rb") as _file:
            # 每次读取8192个字节，防止文件过大导致内存溢出
            md5 = hashlib.md5()
            while True:
                chunk = _file.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
            return md5.hexdigest()

    if _string:
        m = hashlib.md5()
        m.update(_string.encode())
        return m.hexdigest()

    raise ValueError("参数_file_path与_string必须二选一，不能都为空")


def md5_file(target):
    """计算文件md5值"""
    return md5sum(_file_path=target)


def md5_str(target):
    """计算字符串md5值"""
    return md5sum(_string=target)


def jwt_decode(
    jwt_token: str,
    verify_signature: bool = False,
    verify_exp: bool = False,
    verify_nbf: bool = False,
    verify_iat: bool = False,
    verify_aud: bool = False,
    verify_iss: bool = False,
    **kwargs,
) -> dict:
    """解析 JWT Token"""
    return jwt.decode(
        jwt_token,
        algorithms=["HS256"],
        options={
            "verify_iss": verify_iss,
            "verify_aud": verify_aud,
            "verify_iat": verify_iat,
            "verify_nbf": verify_nbf,
            "verify_exp": verify_exp,
            "verify_signature": verify_signature,
            **kwargs,
        },
    )


class MyCrypto(object):
    """RSA加密算法特性：
    1. 公钥加密，私钥解密；
    2. 公钥相同，明文相同，但每次加密后得到的密文不同；
    """

    @classmethod
    def encrypt(cls, data, xsrf_token=None, old_secret=None) -> str:
        """加密"""
        if xsrf_token:
            key = cls.sha256(xsrf_token)
        else:
            key = old_secret
        if len(key) >= 32:
            key = key[:32]
        else:
            key = cls.__add_to_32(key)
        cipher1 = AES.new(key=key.encode("utf-8"), mode=AES.MODE_ECB)
        ct = cipher1.encrypt(pad(data.encode("utf-8"), 16))
        encrypt_data = base64.b64encode(ct)
        return encrypt_data.decode("utf-8")

    @classmethod
    def decrypt(cls, data, xsrf_token=None, old_secret=None) -> str:
        """解密"""
        if xsrf_token:
            key = cls.sha256(xsrf_token)
        else:
            key = old_secret
        if len(key) >= 32:
            key = key[:32]
        else:
            key = cls.__add_to_32(key)
        ct = base64.b64decode(data)
        cipher2 = AES.new(key=key.encode("utf-8"), mode=AES.MODE_ECB)
        pt = unpad(cipher2.decrypt(ct), 16)
        return pt.decode("utf-8")

    @classmethod
    def __add_to_32(cls, text):
        while len(text) % 32 != 0:
            text += "\0"
        return text

    @classmethod
    def sha256(cls, data):
        """sha256加密"""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def aes_cbc_encrypt(key, content, iv):
        """AES CBC加密"""
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        # 处理明文
        content_padding = pad(content.encode("utf-8"), 16, style="pkcs7")
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding)
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding="utf-8")
        return result

    @staticmethod
    def aes_cbc_decrypt(key, content, iv):
        """AES CBC解密"""
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        content = base64.b64decode(content)
        text = cipher.decrypt(content)
        return unpad(text, 16, style="pkcs7").decode("utf-8")

    @staticmethod
    def rsa_encrypt(key, data):
        """RSA非对称加密，用于通过用户名与密码创建新用户时"""
        pub_key = f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"
        pub_key = RSA.importKey(str(pub_key))
        cipher = oaep_cipher.new(pub_key, hashAlgo=SHA256)
        rsa_text = base64.b64encode(cipher.encrypt(data.encode("utf-8")))
        return rsa_text.decode("utf-8")

    @staticmethod
    def rsa_decrypt(key, data):
        """RSA非对称解密，用于通过用户名与密码创建新用户时"""
        pri_key = (
            "-----BEGIN RSA PRIVATE KEY-----\n"
            + key
            + "\n"
            + "-----END RSA PRIVATE KEY-----"
        )
        pri_key = RSA.import_key(pri_key)
        cipher = oaep_cipher.new(pri_key, hashAlgo=SHA256)
        rsa_text = cipher.decrypt(base64.b64decode(data))
        return rsa_text.decode("utf-8")
