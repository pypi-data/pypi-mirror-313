import argparse
from colorama import init

# 解决Window环境中打印颜色问题
init(autoreset=True)


def encrypt()->None:
    ''' 
    加密工具的命令行入口
    Command line entry for encryption tools
    '''
    
    parser = argparse.ArgumentParser(description='asterisk-security加密工具')
    parser.add_argument('-key', metavar='K', type=str,  \
        help='加密密钥，长度不能超过22个字符，否则，进行左右11个字符截取，格式：[a-zA-Z0-9]+，不得包含特殊字符 encrypt key, length should not exceed 22 characters, otherwise, left and right 11 characters will be intercepted, format: [a-zA-Z0-9]+, no special characters allowed')
    parser.add_argument('-txt', metavar='T', type=str,  \
        help='需要加密的字符串 string to be encrypted')
    
    key = parser.parse_args().key if parser.parse_args() else ''
    txt = parser.parse_args().txt if parser.parse_args() else ''
    if not key:
        print('\033[31m加密密钥不能为空。\033[0m')
        return
    if not txt:
        print('\033[31m需要加密的字符串不能为空。\033[0m')
        return
    from asterisksecurity.encryption import AsteriskEncrypt
    a = AsteriskEncrypt(key)
    print(f'加密结果：{a.encrypt(txt)}')

def decrypt()->None:
    ''' 
    解密工具的命令行入口
    Command line entry for decryption tools
    '''
    
    parser = argparse.ArgumentParser(description='asterisk-security解密工具')
    parser.add_argument('-key', metavar='K', type=str,  \
        help='解密密钥，长度不能超过22个字符，否则，进行左右11个字符截取，格式：[a-zA-Z0-9]+，不得包含特殊字符 decrypt key, length should not exceed 22 characters, otherwise, left and right 11 characters will be intercepted, format: [a-zA-Z0-9]+, no special characters allowed')
    parser.add_argument('-txt', metavar='T', type=str,  \
        help='需要解密的字符串 string to be decrypted')
    
    key = parser.parse_args().key if parser.parse_args() else ''
    txt = parser.parse_args().txt if parser.parse_args() else ''
    if not key:
        print('\033[31m解密密钥不能为空。\033[0m')
        return
    if not txt:
        print('\033[31m需要解密的字符串不能为空。\033[0m')
        return
    from asterisksecurity.encryption import AsteriskEncrypt
    a = AsteriskEncrypt(key)
    try:
        print(f'解密结果：{a.decrypt(txt)}')
    except Exception as e:
        print(f'\033[31m解密失败：{e}\033[0m')