# asterisk-security

## 介绍

这个小项目最初是几年前写Django的项目，想在后端写个cookie的加密功能，后来就自己动手写了一个可以加密的函数。主要是个人工作的积累而已。随着后续开发的需求，将不断将更多的个人经验总结道这个开源项目。

项目交流与缺陷提交[这里](https://gitee.com/zhangxin_1/asterisk-security)

注意：

* 发行版本的版本号不一定连续，中间的版本号都是开发中的版本号，不正式发布。
* 版本号为A.B.C.mmdd.hhmm的格式，只须关注A.B.C即可，mmdd.hhmm为build时间戳

## 软件架构

```markdown
/
|-- asterisksecurity/
|   |-- encryption.py
|   |   |-- AsteriskEncrypt
|   |
|   |-- error.py
|   |   |-- InvalidEncriptionKey
```

## 安装教程

1. `pip install asterisk-security`

## 使用说明

### 安装后在python代码中引入，实例化后调用

1. 需要以key来实例化`AsteriskEncrypt`类
2. `encrypt`方法可以将传参字符串进行加密并返回字符串
3. `decrypt`方法将已加密的字符串进行解密

例子：

```python
from asterisksecurity.encryption import AsteriskEncrypt

def test_encrypt():
    key = 'X7UJi2VdqcQlc3thv2dDPEn5y3yv3eTk35yyAhlKeAY1'
    a = AsteriskEncrypt(key)
    s = '你好世界！Hello World!'
    s_enc = a.encrypt(s)
    print(s_enc)

    a_dec = a.decrypt(s_enc)
    print(a_dec)

if __name__ == '__main__':
    test_encrypt()

```

### 直接使用命令行

* 使用asencrypt命令

```command-line
usage: asencrypt [-h] [-key K] [-txt T]

asterisk-security加密工具

options:
  -h, --help  show this help message and exit
  -key K      加密密钥，长度不能超过22个字符，否则，进行左右11个字符截取，格式：[a-zA-Z0-9]+，不得包含特殊字符 encrypt key, length should not exceed 22 characters, otherwise, left and
              right 11 characters will be intercepted, format: [a-zA-Z0-9]+, no special characters allowed
  -txt T      需要加密的字符串 string to be encrypted```markdown


```

* 使用asdecrypt命令
  
```command-line
usage: asdecrypt [-h] [-key K] [-txt T]

asterisk-security解密工具

options:
  -h, --help  show this help message and exit
  -key K      解密密钥，长度不能超过22个字符，否则，进行左右11个字符截取，格式：[a-zA-Z0-9]+，不得包含特殊字符 decrypt key, length should not exceed 22 characters, otherwise, left and
              right 11 characters will be intercepted, format: [a-zA-Z0-9]+, no special characters allowed
  -txt T      需要解密的字符串 string to be decrypted
```

## 错误说明

1. key字符串如果不符合格式要求，会抛出error
2. 其他在解密过程中有任何error都不做处理。

## 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
