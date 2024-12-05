"""
接口测试核心类
"""
import json
import os
import time
from urllib.parse import urlparse

import pytest
import allure
import jsonpath
from requests_toolbelt import MultipartEncoder
from tinet.LogUtil import log
from tinet.RequestUtil import HttpClient
from tinet.SignUtil import SignUtil
from tinet.YamlUtil import ReadYaml, PlaceholderYaml
from tinet.ApiConfig import config


class APIRequest:
    """
    接口测试核心类
    """

    # 初始化 接收文件 跟一个实体类
    def __init__(self, commonCase=None):
        """
        :param baseUrl: 请求地址
        :param AccessKeyId: AK
        :param AccessKeySecret: SK
        """
        self.commonCase = commonCase
        self.baseUrl = config.baseUrl
        self.AccessKeyId = config.accessKeyId
        self.AccessKeySecret = config.accessKeySecret
        self.globalBean = config
        self.assertFail = config().assertFail
        self.tenv = config.tEnv

    # 请求核心方法, 拿到文件后开始解析
    def doRequest(self, file, bean):
        # 请求的时候最终参数  先替换parameter中的占位符  再判断鉴权方式,如果是SIGN的POST就完整parameter否则GET就为空
        requestParameter = None
        dataSaveBean = bean
        yaml = ReadYaml(file).load_yaml()
        yamlId = yaml.get('id')
        yamlName = yaml.get('name')
        yamlKind = yaml.get('kind')
        yamlTestcase = yaml.get('testcases')
        # 先拿到所有testcase
        log.info(f"开始执行测试用例name: {yamlName}, id: {yamlId} , 测试用例: {yamlTestcase}")
        allure.attach(f"{yamlTestcase}", name=f"开始执行测试用例name: {yamlName}, id: {yamlId} ", attachment_type=allure.attachment_type.TEXT)
        # 添加公共session  判断是否有公共session
        clientSession = config.Session
        # 开始遍历testcase
        # allure.dynamic.title(yamlName)
        for testcase in yamlTestcase:
            with allure.step(testcase.get('name')):
                # 拿到用例如果是common的去common文件路径中拿测试用例
                if testcase.get('skip'):  # 判断是否跳过
                    log.info(f"用例: {json.dumps(testcase.get('name'), indent=4, ensure_ascii=False)}跳过")
                    continue
                sleeps = testcase.get('sleep')
                if sleeps:  # 判断是否需要等待
                    time.sleep(int(sleeps))
                    log.info(f"当前用例: {json.dumps(testcase.get('name'), indent=4, ensure_ascii=False)}执行前等待{sleeps}秒")
                if testcase.get('kind') and testcase.get('kind').lower() == 'common' and config.commonTestCasePath is not None:
                    log.info("读取common文件中的测试用例,匹配测试用例id: {}".format(testcase.get('id')))
                    allure.attach(f"读取common文件中的测试用例,匹配测试用例id: {testcase.get('id')}", name=f"读取common文件中的测试用例,匹配测试用例id: {testcase.get('id')}",
                                  attachment_type=allure.attachment_type.TEXT)
                    # 拿到common文件中的测试用例 然后重新赋值给testcase
                    testcase = self.getCommonTestCase(testcase, config.commonTestCasePath, testcase.get('id'))
                elif testcase.get('kind') and testcase.get('kind').lower() == 'common' and config.commonTestCasePath is None:
                    log.error(f"commonPath路径未配置,请检查配置文件")
                    raise Exception(f"commonPath路径未配置,请检查配置文件")
                # 执行当前用例 格式化为json 间隔4个空格
                log.info(f"执行当前用例name: {testcase.get('name')}, id: {testcase.get('id')}")
                allure.attach(f"{json.dumps(testcase, indent=4, ensure_ascii=False)}", name=f"执行当前用例name: {testcase.get('name')}, id: {testcase.get('id')}",
                              attachment_type=allure.attachment_type.TEXT)
                if self.tenv == 'gray':
                    testcase.get('headers')['t-env'] = 'gray'
                # 1. 先看看参数中是否有需要替换的参数
                if testcase.get('requestType') is None:
                    requestType = 'json'
                else:
                    requestType = testcase.get('requestType')
                repParameter = self.replaceParameterAttr(dataSaveBean, testcase.get('parameter'), requestType)
                repApi = self.replaceParameterAttr(dataSaveBean, testcase.get('api'))
                headers = self.replaceParameterAttr(dataSaveBean, testcase.get('headers'))
                # 2. 判断鉴权方式 authType 返回请求地址
                requestParameter, requestUrl = self.authType(testcase.get('authType'), repApi, testcase.get('method'), repParameter)
                # 3. 判断请求 requestType
                dataRequestParameter, jsonRequestParameter, paramsData, ModelData, requestType = self.requestType(requestType, requestParameter)
                # 4. 开始请求
                log.info(f"开始请求地址: {requestUrl} ")
                allure.attach(f"{requestUrl}", name=f"开始请求地址", attachment_type=allure.attachment_type.TEXT)
                log.info(f"开始请求方式: {testcase.get('method')}")
                allure.attach(f"{testcase.get('method')}", name=f"开始请求方式", attachment_type=allure.attachment_type.TEXT)
                if dataRequestParameter is not None:
                    log.info(f"开始请求参数dataRequestParameter: {dataRequestParameter}")
                    allure.attach(f"{dataRequestParameter}", name=f"开始请求参数dataRequestParameter", attachment_type=allure.attachment_type.TEXT)
                if jsonRequestParameter is not None:
                    log.info(f"开始请求参数jsonRequestParameter: {jsonRequestParameter}")
                    allure.attach(f"{jsonRequestParameter}", name=f"开始请求参数jsonRequestParameter", attachment_type=allure.attachment_type.TEXT)
                if paramsData is not None:
                    log.info(f"开始请求参数paramsData: {paramsData}")
                    allure.attach(f"{paramsData}", name=f"开始请求参数paramsDatar", attachment_type=allure.attachment_type.TEXT)
                if ModelData is not None:
                    log.info(f"开始请求参数ModelData: {ModelData}")
                    allure.attach(f"{ModelData}", name=f"开始请求参数ModelData", attachment_type=allure.attachment_type.TEXT)
                # form-data请求 需要处理一下header
                if dataRequestParameter is not None and requestType.lower() == 'form-data' or requestType.lower() == 'form-file':
                    headers['Content-Type'] = dataRequestParameter.content_type
                response = clientSession.request(method=testcase.get('method'), url=requestUrl, data=dataRequestParameter, json=jsonRequestParameter, params=paramsData, files= ModelData, headers=headers)
                try:  # 当返回不是 json 返回text
                    log.info(f"当前用例response: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
                    allure.attach(f"{json.dumps(response.json(), indent=4, ensure_ascii=False)}", name=f"当前用例response",
                                  attachment_type=allure.attachment_type.TEXT)
                except:
                    log.info(f"当前用例response: {json.dumps(response.text)}")
                    allure.attach(f"{json.dumps(response.text)}", name=f"当前用例response",
                                  attachment_type=allure.attachment_type.TEXT)
                # 5. 处理断言
                if testcase.get('assertFail'):
                    failtype = testcase.get('assertFail')
                else:
                    failtype = self.assertFail
                self.assertType(testcase.get('assert'), response, dataSaveBean, failtype)
                # 6. 处理response,根据data 来进行变量存取
                # try 里面的代码是为了处理response不是json格式的情况
                try:
                    self.addAttrSaveBean(dataSaveBean, self.globalBean, testcase.get('saveData'), response.json())
                except:
                    self.addAttrSaveBean(dataSaveBean, self.globalBean, testcase.get('saveData'), response.text)
        return clientSession

    # 处理断言方法  - eq: [ 'body.userId', 1 ]  通过testcase中的assert来判断断言方式  先取断言的方式 再取断言的内容跟值
    def assertType(self, assertType, response, bean, failType):
        log.info(f"开始处理断言: {assertType}")
        allure.attach(f"{assertType}", name=f"开始处理断言", attachment_type=allure.attachment_type.TEXT)
        # 判断assertType是否为空
        if assertType is None:
            log.info(f"断言为空,跳过断言")
            allure.attach(f"断言为空,跳过断言", name=f"断言为空,跳过断言", attachment_type=allure.attachment_type.TEXT)
            return None
        # 开始判断断言方式
        # [{'eq': ['body.userId', 1]}, {'eq': ['body.userId', 1]}] 循环判断
        for ass in assertType:
            key = list(ass.keys())[0]
            log.info(f"开始判断{key}断言: {ass.get(key)}")
            allure.attach(f"{ass.get(key)}", name=f"开始判断{key}断言", attachment_type=allure.attachment_type.TEXT)
            if 'status_code' in ass:
                # 断言 响应状态码 status_code
                # 取要断言的值
                if ass.get('status_code'):
                    log.info(f"断言status_code结束,{ass.get('status_code')}  ,response结果: {response.status_code}")
                    allure.attach(f"{ass.get('status_code')}  ,response结果: {response.status_code}", name=f"断言status_code结束", attachment_type=allure.attachment_type.TEXT)
                    self.assertChoose(str(response.status_code) == str(ass.get('status_code')), f"status_code断言失败: {ass.get('status_code')}  ,response结果: {response.status_code}", failType)
                    continue
            jsonpathResults = jsonpath.jsonpath(response.json(), ass.get(key)[0])
            if jsonpathResults is False:
                log.info(f'提取{ass.get(key)[0]}失败，请检查格式')
                allure.attach(f"提取{ass.get(key)[0]}失败，请检查格式", name=f"提取{ass.get(key)[0]}失败，请检查格式", attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(1 > 2, f"提取{ass.get(key)[0]}失败，断言失败, response结果: {json.dumps(response.text, indent=4, ensure_ascii=False)}", failType)
                continue
            if 'eq' in ass:
                # 相等判断 都转为str进行判断
                expectedResults = PlaceholderYaml(attrObj=bean, reString=ass.get('eq')[1]).replace().replaced_str
                # 判断 expectedResults 是否在 jsonpathResults list中  判断类型
                assResults = str(expectedResults) in [str(item) for item in jsonpathResults]
                log.info(f"断言eq结束: {jsonpathResults} 等于 {expectedResults}")
                allure.attach(f"{jsonpathResults} 等于 {expectedResults}", name=f"断言eq结束", attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(assResults is True, f"eq断言失败: {jsonpathResults} 不等于 {expectedResults}", failType)
            elif 'sge' in ass:
                # size greater than or equal
                expectedResults = PlaceholderYaml(attrObj=bean, reString=ass.get('sge')[1]).replace().replaced_str
                log.info(f"断言sge结束: {jsonpathResults} size >= {expectedResults}")
                allure.attach(f" {jsonpathResults} size >= {expectedResults}", name=f"断言sge结束",
                              attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(len(jsonpathResults) >= int(expectedResults), f"sge断言失败: {jsonpathResults} 小于 {expectedResults}", failType)
            elif 'ne' in ass:
                # not eq 断言
                return 'ne'
            elif 'nn' in ass:
                # not none
                # 判断json path 是否不为空 返回FALSE
                log.info(f"断言not none结束: {jsonpathResults}")
                allure.attach(f" {jsonpathResults} ", name=f"断言not none结束", attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(jsonpathResults is not None,
                                  f"not none断言失败: {ass.get('nn')[0]}  ,jsonpath结果: {jsonpathResults}", failType)
            elif 'none' in ass:
                # 判断json path 是否 返回FALSE
                log.info(f"断言none结束: {jsonpathResults}")
                allure.attach(f" {jsonpathResults} ", name=f"断言none结束", attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(jsonpathResults is True,
                                  f"none断言失败: {ass.get('none')[0]}  ,jsonpath结果: {jsonpathResults}", failType)
            elif 'in' in ass:
                # 判断预期值是否被返回值包含
                expectedResults = PlaceholderYaml(attrObj=bean, reString=ass.get('in')[1]).replace().replaced_str
                log.info(f"断言in结束: {expectedResults} 在 {jsonpathResults} 内")
                allure.attach(f" {expectedResults} 在 {jsonpathResults} 内", name=f"断言in结束",
                              attachment_type=allure.attachment_type.TEXT)
                self.assertChoose(str(expectedResults) in str(jsonpathResults), f"断言in失败: {expectedResults} 不在 {jsonpathResults} 内", failType)

    # 根据data从response中根据json还是其他方法来获取response中的值
    def addAttrSaveBean(self, bean, globalBean, data: list, response):
        # 先解析data 如果data为空则直接返回
        if data is None:
            return
        for d in data:
            log.info(f"获取要添加的属性表达式: data: {d}")
            allure.attach(f"{d}", name=f"获取要添加的属性表达式: data", attachment_type=allure.attachment_type.TEXT)
            # 判断 d 的key 是否为json 怎走jsonpath 解析
            if 'json' in d:
                log.info(f"开始解析json: {d.get('json')}")
                allure.attach(f"{d.get('json')}", name=f"开始解析json", attachment_type=allure.attachment_type.TEXT)
                # 解析json
                jsonPath = d.get('json')[1]
                # 获取jsonpath的值
                value = jsonpath.jsonpath(response, jsonPath)
                # 判断value是为False
                if value is False:
                    value = None
                log.info(f"解析完成jsonPath: {jsonPath} 的值: {value}")
                allure.attach(f"{jsonPath} 的值: {value}", name=f"解析完成jsonPath", attachment_type=allure.attachment_type.TEXT)
                # 给bean添加属性
                # 判断value是否为空 并且 value 不是false 并且value的长度是否为1 如果是则直接赋值 如果不是则赋值list
                # 如果value为空则不赋值 是多个则 赋值list
                saveBean = bean
                if d.get('json').__len__() == 3 and d.get('json')[2].lower() == 'global':
                    saveBean = globalBean
                else:
                    saveBean = bean
                if value is not None and len(value) > 1:
                    setattr(saveBean, d.get('json')[0], list(value))
                    log.info(f"添加属性完成: {d.get('json')[0]} = {list(value)}")
                    allure.attach(f"{d.get('json')[0]} = {list(value)}", name=f"添加属性完成", attachment_type=allure.attachment_type.TEXT)
                elif value is not None and len(value) == 1:
                    setattr(saveBean, d.get('json')[0], value[0])
                    log.info(f"添加属性完成: {d.get('json')[0]} = {value[0]}")
                    allure.attach(f"{d.get('json')[0]} = {value[0]}", name=f"添加属性完成", attachment_type=allure.attachment_type.TEXT)
                else:
                    log.error(f"添加属性失败: {d.get('json')[0]} = {value}")
                    allure.attach(f"{d.get('json')[0]} = {value}", name=f"添加属性失败", attachment_type=allure.attachment_type.TEXT)
            elif 'other' in d:
                log.info(f"开始解析other: {d.get('other')}")
                allure.attach(f"{d.get('other')}", name=f"开始解析other", attachment_type=allure.attachment_type.TEXT)

    # 拿到参数后先替换变量或者方法
    def replaceParameterAttr(self, bean, parameter, requestType='json'):
        # 先拿到所有的参数
        log.info(f"开始替换参数: {parameter}")
        allure.attach(f"{parameter}", name=f"开始替换参数", attachment_type=allure.attachment_type.TEXT)
        # 判断参数是否为空
        if parameter is None:
            return None
        # 开始调用方法替换
        if requestType.lower() == 'json-text':
            repParameter = PlaceholderYaml(yaml_str=parameter, attrObj=bean).replace().textLoad()
        else:
            repParameter = PlaceholderYaml(yaml_str=parameter, attrObj=bean).replace().jsonLoad()
        log.info(f"替换后的参数: {repParameter}")
        allure.attach(f"{repParameter}", name=f"替换后的参数", attachment_type=allure.attachment_type.TEXT)
        return repParameter

    # 判断请求方式 requestType
    def requestType(self, requestType, data):
        # 判断是否为空
        jsonRequestParameter = None
        dataRequestParameter = None
        paramsData = None
        ModelData = None
        if requestType is None:
            log.info(f"请求方式为空: {requestType} ,默认走json请求")
            allure.attach(f"{requestType}", name=f"请求方式为空,默认走json请求", attachment_type=allure.attachment_type.TEXT)
            jsonRequestParameter = data
        elif requestType.lower() == "json" or requestType.lower() == "json-text":
            # 进行json请求 JSON-TEXT: 入参含有str类型的字典使用
            log.info(f"请求方式为JSON: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为JSON", attachment_type=allure.attachment_type.TEXT)
            jsonRequestParameter = data
        elif requestType.lower() == "form-data":
            # 进行form请求, 该类型 不能传文件
            log.info(f"请求方式为FORM-DATA: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为FORM", attachment_type=allure.attachment_type.TEXT)
            dataRequestParameter = MultipartEncoder(fields=data)
        elif requestType.lower() == "form-model":
            # 进行form-model请求，该类型可以传文件，格式为 form-data
            log.info(f"请求方式为FORM-MODEL: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为FORM-Model", attachment_type=allure.attachment_type.TEXT)
            filename = data['filename']  # 获取文件字段
            log.info(type(data))
            log.info(data[filename])
            file_name = data[filename].split('\\')
            log.info(file_name[-1])
            data[filename] =  (file_name[-1], open(data[filename], 'rb'), 'application/octet-stream')
            for k,v in data.items():
                if type(v) == dict:
                    data[k] = (None, json.dumps(data[k]))
            log.info(data)
            ModelData = data
        elif requestType.lower() == "form-file":
            # 进行form-file请求，该类型可以传文件,格式为json
            log.info(f"请求方式为FORM-FILE: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为FORM-FILE", attachment_type=allure.attachment_type.TEXT)
            filename = data['filename']  # 获取文件字段
            data[filename] = (os.path.basename(data[filename]), open(data[filename], 'rb'), 'application/octet-stream')
            dataRequestParameter = MultipartEncoder(fields=data)
        elif requestType == "PARAMS":
            # 进行PARAMS请求
            log.info(f"请求方式为PARAMS: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为PARAMS", attachment_type=allure.attachment_type.TEXT)
            paramsData = data
        elif requestType == "DATA":
            # 进行DATA请求
            log.info(f"请求方式为DATA: {requestType}")
            allure.attach(f"{requestType}", name=f"请求方式为DATA", attachment_type=allure.attachment_type.TEXT)
            dataRequestParameter = data
        else:
            log.error("请求方式不支持")
            allure.attach(f"请求方式不支持", name=f"请求方式不支持", attachment_type=allure.attachment_type.TEXT)
        return dataRequestParameter, jsonRequestParameter, paramsData, ModelData, requestType

    # 判断鉴权方式 authType
    def authType(self, authType, url, method, parameter):
        # 判断baseurl 是否为None
        if self.baseUrl is None or self.isValidUrl(url):
            requestUrl = url
        else:
            requestUrl = self.baseUrl + url
        requestParameter = None
        if authType == "SIGN":
            # 进行签名
            requestUrl = SignUtil.signature(apiUrlPath=requestUrl, method=method, params=parameter, access_key_id=self.AccessKeyId, access_key_secret=self.AccessKeySecret)
            if method == "GET":
                requestParameter = None
            elif method == "POST":
                requestParameter = parameter
            allure.attach(f"{requestUrl}", name=f"SIGN鉴权请求", attachment_type=allure.attachment_type.TEXT)
            return requestParameter, requestUrl
        elif authType == "COOKIE" or authType is None:
            # 进行cookie
            requestParameter = parameter
            allure.attach(f"{requestUrl}", name=f"COOKIE鉴权请求", attachment_type=allure.attachment_type.TEXT)
            return requestParameter, requestUrl
        elif authType == "AUTH":
            # 进行auth
            pass
        else:
            log.error("鉴权方式不支持")
        return requestParameter, requestUrl

    # 根据common路径跟id 去重新赋值testcase
    def getCommonTestCase(self, testcase, commonFile, caseId):
        # 先判断 self.commonCase 是否为空,如果不为空则需要读取commonFile,否则读取用例类自定义commonfile
        if self.commonCase is None:
            # 读取commonFile
            commonFile = commonFile
        else:
            commonFile = os.path.join(commonFile.split('common')[0], f'common/{self.commonCase}')
        log.info(f"开始读取commonFile: {commonFile}")
        allure.attach(f"{commonFile}", name=f"开始读取commonFile", attachment_type=allure.attachment_type.TEXT)
        yaml = ReadYaml(commonFile).load_yaml()
        # 获取所有case
        commonCase = yaml.get('testcases')
        log.info(f"读取完成commonFile: {commonCase}")
        allure.attach(f"{commonCase}", name=f"读取完成commonFile", attachment_type=allure.attachment_type.TEXT)

        # 遍历commonCase ,如果id相同则返回case 如果遍历完没有找到则报错
        for case in commonCase:
            if case.get('id') == caseId:
                log.info(f"找到commonCase: {case}")
                allure.attach(f"{case}", name=f"找到commonCase", attachment_type=allure.attachment_type.TEXT)
                # 如果找到则返回case 将case的assert与testcase的assert进行合并
                case['assert'] = [item for item in (case.get('assert') or []) + (testcase.get('assert') or []) if
                                  item is not None]
                case['saveData'] = [item for item in (case.get('saveData') or []) + (testcase.get('saveData') or []) if
                                    item is not None]
                return case
        log.error(f"没有找到commonCase: {caseId}")
        allure.attach(f"{caseId}", name=f"没有找到commonCase", attachment_type=allure.attachment_type.TEXT)
        raise ValueError("Case with id {} not found".format(caseId))

    def assertChoose(self, ass, tips, type):
        """
        assertChoose 断言选择器
        :param ass:
        :param tips:
        :param type:
        :return:
        """
        if type == 'stop':
            assert ass, tips
        elif type == 'continue':
            pytest.assume(ass, tips)

    def isValidUrl(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
