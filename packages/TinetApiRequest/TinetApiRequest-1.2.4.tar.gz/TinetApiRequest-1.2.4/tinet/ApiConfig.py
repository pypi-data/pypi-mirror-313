from faker import Faker
import string, time
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import datetime
import pytz
import hashlib
import base64

from tinet.RequestUtil import HttpClient


class times:
    def __init__(self, dt=None, tz=pytz.timezone('Asia/Shanghai')):
        """
        初始化时间工具类

        :param dt: datetime对象，默认使用当前时间
        :param tz: 时区，默认使用本地时区
        """
        self.tz = tz
        self.dt = dt or datetime.datetime.now(self.tz)

    def to_datetime(self):
        """
        返回datetime对象

        :return: datetime对象
        """
        return self.dt

    def to_str(self, fmt='%Y-%m-%dT%H:%M:%SZ'):
        """
        将datetime对象转换为指定格式的字符串

        :param fmt: 时间格式，默认为'%Y-%m-%d %H:%M:%S'
        :return: 格式化后的时间字符串
        """
        return self.dt.strftime(fmt)


class ChineseDataGenerator:
    """
    生成中文数据的工具类
    """

    def __init__(self):
        self.fake = Faker(locale='zh_CN')

    def generate_name(self):
        """
        生成中文姓名，返回字符串。
        """
        return self.fake.name()

    def generate_address(self):
        """
        生成中文地址，返回字符串。
        """
        return self.fake.address()

    def generate_phone_number(self):
        """
        生成中文手机号，返回字符串。
        """
        return self.fake.phone_number()

    def generate_id_number(self):
        """
        生成中文身份证号码，返回字符串。
        """
        return self.fake.ssn()

    def random_number(self, digits=4):
        """
        生成一个4位随机整数并转换为字符串类型
        如果生成的整数不足4位，则在左侧用0进行填充
        """
        digits = int(digits)
        return "{:04d}".format(self.fake.random_number(digits=digits))

    def get_sk_password(self):
        """
        获取初始化的SK 加密后的密码
        :return:
        """
        return config.SKPassword

    @staticmethod
    def start_of_day():
        """
        获取当前时间开始时间戳：eg：2023-06-01 00:00:00
        """
        now = datetime.datetime.now()
        return datetime.datetime(now.year, now.month, now.day)

    @staticmethod
    def end_of_day():
        """
        获取当前时间开始时间戳：eg：2023-06-01 23:59:59
        """
        return ChineseDataGenerator.start_of_day() + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

    def start_of_day_s(self):
        """
        获取当前时间开始时间戳：eg：1685548800  秒级
        """
        return int(time.mktime(ChineseDataGenerator.start_of_day().timetuple()))

    def end_of_day_s(self):
        """
        获取当前时间结束时间戳：eg：1685635199 秒级
        """
        return int(time.mktime(ChineseDataGenerator.end_of_day().timetuple()))

    def random_externalId(self):
        """
        生成唯一性数据，crm用于 外部企业客户id
        """
        num = str(random.randint(1000, 9999))
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母
        chrs = random.sample(src_lowercase + src_uppercase, 3)
        for i in chrs:
            num += i
        return num

    def encryptPassword(self, plain_text='Aa112233'):
        """
        # 加密
        """
        password = config.accessKeySecret
        # 设置随机数生成器的种子
        secure_random = hashlib.sha1(password.encode()).digest()
        # 创建对称加密密钥生成器
        kgen = hashlib.sha1(secure_random).digest()[:16]
        # 创建密码器并初始化
        cipher = AES.new(kgen, AES.MODE_ECB)
        # 加密明文（使用PKCS7填充）
        padded_plain_text = pad(plain_text.encode(), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_plain_text)
        # 将加密结果转换为16进制字符串
        encrypted_text = base64.b16encode(encrypted_bytes).decode().lower()
        return encrypted_text

    def decrypt(self, encrypted_text, password):
        """
        # 解密
        """
        # 设置随机数生成器的种子
        secure_random = hashlib.sha1(password.encode()).digest()
        # 创建对称加密密钥生成器
        kgen = hashlib.sha1(secure_random).digest()[:16]
        # 创建密码器并初始化
        cipher = AES.new(kgen, AES.MODE_ECB)
        # 解密密文（parseHexStr2Byte方法为将16进制字符串转为二进制字节数组）
        encrypted_bytes = base64.b16decode(encrypted_text)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        decrypted_text = unpad(decrypted_bytes, AES.block_size).decode()
        return decrypted_text


class config:
    """
    配置文件
    """

    def __init__(self, baseUrl=None, AccessKeyId=None, AccessKeySecret=None, SKPassword=None, commonTestCasePath=None, methObj=None,
                 Session: HttpClient = HttpClient(), assertFail='stop', tEnv='base'):
        """
        初始化配置文件
        """
        self._baseUrl = baseUrl
        self._accessKeyId = AccessKeyId
        self._accessKeySecret = AccessKeySecret
        # SK加密 登录密码 后的 密码加密文本
        self._SKPassword = SKPassword
        self._commonTestCasePath = commonTestCasePath
        self._methObj = methObj
        self._assertFail = assertFail
        self._tEnv = tEnv
        # 构建全局session
        self._Session = Session

    @property
    def Session(self):
        return self._Session

    @Session.setter
    def Session(self, value):
        self._Session = value

    @property
    def methObj(self):
        return self._methObj

    @methObj.setter
    def methObj(self, value):
        self._methObj = value

    @property
    def SKPassword(self):
        return self._SKPassword

    @SKPassword.setter
    def SKPassword(self, value):
        self._SKPassword = value

    @property
    def commonTestCasePath(self):
        return self._commonTestCasePath

    @commonTestCasePath.setter
    def commonTestCasePath(self, value):
        self._commonTestCasePath = value

    @property
    def baseUrl(self):
        return self._baseUrl

    @baseUrl.setter
    def baseUrl(self, value):
        self._baseUrl = value

    @property
    def accessKeyId(self):
        return self._accessKeyId

    @accessKeyId.setter
    def accessKeyId(self, value):
        self._accessKeyId = value

    @property
    def accessKeySecret(self):
        return self._accessKeySecret

    @accessKeySecret.setter
    def accessKeySecret(self, value):
        self._accessKeySecret = value

    @property
    def assertFail(self):
        return self._assertFail

    @assertFail.setter
    def assertFail(self, value):
        self._assertFail = value

    @property
    def tEnv(self):
        return self._tEnv

    @tEnv.setter
    def tEnv(self, value):
        self._tEnv = value
