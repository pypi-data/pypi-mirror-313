import re
import yaml
import json
from tinet.LogUtil import log
from tinet.ApiConfig import config


class PlaceholderYaml:
    """
    用于替换 yaml 文件中的占位符
    """

    def __init__(self, yaml_str=None, reString=None, attrObj=config, methObj=None, gloObj=config):
        if yaml_str:
            self.yaml_str = json.dumps(yaml_str)
        else:
            self.yaml_str = str(reString)

        self.attrObj = attrObj
        self.methObj = config.methObj if methObj is None else methObj
        self.gloObj = gloObj

    def replace(self):
        # 定义正则表达式模式
        # 用于匹配 ${attr} 和 #{method} 这样的占位符
        # $() #() 如果不匹配则报错
        pattern_attr = re.compile(r'\$\{(\w+)\}')
        pattern_method = re.compile(r'\#\{(.*?)\}')
        pattern_glo = re.compile(r'\$\$\{(\w+)\}')

        # 定义全局替换函数
        def replace_glo(match):
            # 获取占位符中的属性名
            attr_name = match.group(1)
            # 如果对象中有该属性，则返回该属性的值
            if hasattr(self.gloObj, attr_name):
                # 获取属性的值
                attr_value = getattr(self.gloObj, attr_name)
                # 如果属性的值是字符串，则返回该字符串
                if isinstance(attr_value, str):
                    return str(attr_value)
                # 如果属性的值是可调用对象，则返回方法名
                elif callable(attr_value):
                    return match.group(0)
                # 如果属性的值是字典，则返回该字典的字符串表示
                elif isinstance(attr_value, dict):
                    return str(attr_value)
                # 如果属性的值是列表，则返回该列表的字符串表示
                elif isinstance(attr_value, list):
                    return str(",".join(str(x) for x in attr_value))
                # 否则，返回属性的值（将其转换为字符串）
                else:
                    return str(attr_value)
            # 否则返回原字符串
            return match.group(0)

        # 定义替换函数
        def replace_attr(match):
            # 获取占位符中的属性名
            attr_name = match.group(1)
            # 如果对象中有该属性，则返回该属性的值
            if hasattr(self.attrObj, attr_name):
                # 获取属性的值
                attr_value = getattr(self.attrObj, attr_name)
                # 如果属性的值是字符串，则返回该字符串
                if isinstance(attr_value, str):
                    return str(attr_value)
                # 如果属性的值是可调用对象，则返回方法名
                elif callable(attr_value):
                    return match.group(0)
                # 如果属性的值是字典，则返回该字典的字符串表示
                elif isinstance(attr_value, dict):
                    return str(attr_value)
                # 如果属性的值是列表，则返回该列表的字符串表示
                elif isinstance(attr_value, list):
                    return str(",".join(str(x) for x in attr_value))
                # 否则，返回属性的值（将其转换为字符串）
                else:
                    return str(attr_value)
            # 否则返回原字符串
            return match.group(0)

        # 定义替换函数
        def replace_method(match):
            # 获取占位符中的方法名
            method_name = match.group(1)
            args = None
            if '(' in match.group(1):
                # 获取占位符中的方法名
                method_name = match.group(1).split('(')[0]
                # 获取参数列表
                args_str = match.group(1).split('(')[1][:-1]
                args = [arg.strip() for arg in args_str.split(',')]

            # 如果对象中有该方法，并且该方法是可调用的，则返回该方法的返回值
            if hasattr(self.methObj, method_name):
                # 获取方法
                method = getattr(self.methObj, method_name)
                # 如果方法是可调用对象，则调用该方法并返回其返回值的字符串表示
                if callable(method):
                    if args:
                        method_value = method(*args)
                    else:
                        method_value = method()
                    if isinstance(method_value, str):
                        return str(method_value)
                    else:
                        return str(method_value)
                # 否则，返回方法的字符串表示
                else:
                    return str(method)
            # 否则返回原字符串
            return match.group(0)

        # todo 判断是否有需要替换的 再进行替换
        log.info(f"开始替换str中的占位符: {self.yaml_str}")
        # 先进行全局替换
        replaced_str = pattern_glo.sub(replace_glo, self.yaml_str)
        # 替换占位符中的属性
        replaced_str = pattern_attr.sub(replace_attr, replaced_str)
        # 替换占位符中的方法
        replaced_str = pattern_method.sub(replace_method, replaced_str)
        self.replaced_str = replaced_str
        log.info("替换后的str内容为：{}".format(replaced_str))
        return self

    def jsonLoad(self):
        # 把replaced_str中的"[]"替换为[]  "{}"替换为{}   "'"替换为"/""  'None换为 null'
        replaced_str = self.replaced_str.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}').replace("'", "\"").replace('None','null')
        try:
            replaced_str = json.loads(replaced_str)
            log.info("替换后jsonLoad的str内容为：{}".format(replaced_str))
            return replaced_str
        except:
            log.info(f'*************替换失败-YAML,请检查格式{replaced_str}******************')

    def textLoad(self):
        return json.loads(self.replaced_str)


class ReadYaml:
    """
    用于读取 yaml 文件的工具类
    """

    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    def load_yaml(self):
        """
        读取 yaml 文件，并返回其中的数据。
        :return: dict
        """

        with open(self.yaml_file, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data if data is not None else {}  # 如果 data 为 None，则返回空字典

    def get(self, key, default=None):
        """
        获取 yaml 文件中的数据
        :param key: 数据的键
        :param default: 如果获取失败，则返回该默认值
        :return: dict
        """

        # 读取 yaml 文件
        data = self.load_yaml()
        # 获取数据
        return data.get(key, default) if data is not None else default

    def get_all(self):
        """
        获取 yaml 文件中的所有数据
        :return: dict
        """

        # 读取 yaml 文件
        data = self.load_yaml()
        # 如果 data 为 None，则返回空字典
        return data if data is not None else {}
