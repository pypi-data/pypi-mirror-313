from pyDes import des, CBC, PAD_PKCS5
import hashlib
import base64,re

class AsteriskEncrypt():
    '''
    加密类提供了加密和解密的方法
    The encryption class provides encryption and decryption methods.
    在初始化类时需要提供加密和解密的密钥
    The encryption and decryption keys need to be provided when the class is initialized.
    密钥为字符串，不能为“-_”，初始化方法会自动进行密钥处理
    The key is a string and cannot be "-_". The initialization method will automatically process the key.
    加密方法使用了哈希+DES的算法。
    The encryption method uses a hash+DES algorithm.
    构造函数需要输入key字符串，该字符串可以自定义，但是不能包含“-_”字符。
    The constructor needs to input the key string, which can be customized, but cannot contain "-_" characters.
    可以加密包含中文的字符串。
    Strings containing Chinese characters can be encrypted.
    '''

    def __init__(self, key:str):
        '''
        加密用的key字符串，一般为字母和数字数字
        The key string used for encryption is generally a combination of letters and numbers.
        Args:
            key(str): a-z,A-Z,0-9
        '''

        # key的字符串长度不能超过22个字符，否则，进行左右11个字符截取
        if not self.__valid_key(key):
            from asterisksecurity.error import InvalidEncriptionKey
            raise InvalidEncriptionKey()
        # key字符串范围为a-z,A-Z,0-9，以正则表达式进行验证
        if re.match(r'^[a-zA-Z0-9]+$', key) is None:
            from asterisksecurity.error import InvalidEncriptionKey
            raise InvalidEncriptionKey('The key string can only contain a-z, A-Z, 0-9.')
        
        k_b = len(key)
        if k_b > 22:
            key = key[:-2]
        if k_b == 22:
            key = key+'=='
        elif k_b > 11:
            key = key[:11] + key[-11:] + '=='
        else:
            key = key + (22-k_b) * '0' + '=='
        
        self.key_f = base64.b64decode(key)[:8]
        self.key_b = base64.b64decode(key)[8:]

    def __valid_key(self, key:str) -> bool:
        """
        使用正则表达式验证key的格式
        Validate the key format using regular expression.
        Args:
            key(str): The key to be validated. 待验证的key
        Returns:
            bool: True if the key format is valid, False otherwise. 如果key格式有效，则返回True，否则返回False
        """
        import re
        if key.endswith('=='):
            key = key[:-2]
        pattern = r'^[a-zA-Z0-9]+$'
        if re.match(pattern, key):
            return True
        return False

    def encrypt(self, s:str)->str:
        """
        加密字符串的方法
        The method of encrypting strings.
        Args：
            s(str):需要加密的字符串 string to be encrypted
        Return:
            str:加密后的字符串 encrypted string
        """
        
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        m_body = m.digest()
        data = str(m_body) + str(s.encode('utf-8'))
        KEY = self.key_f
        IV = self.key_b
        k_des = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
        des_data = k_des.encrypt(data)
        _final = base64.b64encode(des_data)
        return bytes.decode(_final)

    def decrypt(self, s:str)->str:
        """
        encrypt对应的解密方法
        The decryption method corresponding to encrypt.
        Args：
            s(str):加密后的字符串 encrypted string
        Returns:
            str: 解密后的字符串 decrypted string
        """
    
        decode_b64 = base64.b64decode(bytes(s, encoding='utf8'))
        KEY = self.key_f
        IV = self.key_b
        k_des = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
        decode_des = k_des.decrypt(decode_b64)
        i = decode_des.find(b"'",2) + 1
        return bytes(bytes.decode(decode_des[i:]).replace("b'", "").strip("'"),'utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')

    @classmethod    
    def generate_key(cls)->str:
        """
        生成一个随机的key
        Generate a random key.
        Returns:
            str: 生成的key generated key
        """
        import random
        import string
        return ''.join(random.sample(string.ascii_letters+string.digits, 22)) + '=='
        