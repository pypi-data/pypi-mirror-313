import hmac
import hashlib
import base64
import urllib.parse
import json
from datetime import datetime
import time

import requests

from tinet.ApiConfig import times
from tinet.LogUtil import log



class SignUtil:
    @staticmethod
    def signature(apiUrlPath: str, method, params, access_key_id=None, access_key_secret=None):
        """
         签名算法的封装
        :param apiUrlPath:
        :param method:  RequestMethod.POST/GET
        :param params:  json参数
        :param access_key_id:
        :param access_key_secret:
        :return:
        """
        # 处理url 是否带http
        url = apiUrlPath
        # 处理AK  SK 为空则取环境变量
        access_key_secret = access_key_secret
        access_key_id = access_key_id
        # 获取当前时间戳和签名有效时间
        time1 = datetime.utcfromtimestamp(int(time.time()))
        timestamp = time1.strftime("%Y-%m-%dT%H:%M:%SZ")
        expires = 600
        # 将参数转换为字典，并添加 AccessKeyId、Timestamp 和 Expires 字段
        params_dict_fixed = dict()
        params_dict_fixed['AccessKeyId'] = access_key_id
        params_dict_fixed['Timestamp'] = timestamp
        params_dict_fixed['Expires'] = expires
        params_dict = params_dict_fixed.copy()
        if method.upper() == "GET":
            # 判断参数是否为空
            if params is not None and json.dumps(params).strip():
                params_dict.update(params)
        else:
            params_dict = params_dict
        # 对字典中的参数名进行字典排序
        sorted_params = sorted(params_dict.items(), key=lambda x: x[0])
        # 将参数名和参数值用 & 符号连接，并进行 URL 编码
        encoded_params = urllib.parse.urlencode([(k, v) for k, v in sorted_params])
        # 将请求方法、请求域名和编码后的参数字符串用 ? 符号连接
        # message = str(method) + '\n'+ urllib.parse.urlparse(url).hostname + '\n'+ encoded_params
        message = str(method) + urllib.parse.urlparse(url).hostname + urllib.parse.urlparse(url).path + "?" + encoded_params
        # log.info(f"{url}, 签名前地址: {message}")
        # 使用 AccessKeySecret 密钥对 message 进行哈希计算，并进行 base64 编码
        signature = base64.b64encode(hmac.new(
            access_key_secret.encode(), message.encode(), hashlib.sha1).digest()).decode()
        # 将 signature 进行 URL 编码，并添加到参数字典中
        # 将参数字典转换为字符串，并拼接成完整的请求地址
        if method == 'GET' or method == 'get':
            params_dict['Signature'] = signature
            url_with_signature = url + '?' + urllib.parse.urlencode(params_dict)
        elif method == 'POST' or method == 'post':
            params_dict_fixed['Signature'] = signature
            url_with_signature = url + '?' + urllib.parse.urlencode(params_dict_fixed)
        # log.info(f"{url}, 签名地址: {url_with_signature}")
        return url_with_signature