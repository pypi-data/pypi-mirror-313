import logging
import time

"""
日志工具类:
    定义日志输出
"""


class LogConfig:

    @staticmethod
    def logger_set():
        # 第一步：创建一个日志收集器
        log = logging.getLogger()

        # 第二步：设置收集器收集的等级
        log.setLevel(logging.INFO)

        # 第三步：设置输出渠道以及输出渠道的等级
        curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        # fh = logging.FileHandler(f"./log/{curTime}.log", encoding="utf8")
        # fh.setLevel(logging.INFO)
        # log.addHandler(fh)
        # fh.setFormatter(form)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        log.addHandler(sh)
        # 创建一个输出格式对象
        formats = '%(thread)d: %(asctime)s -- [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        form = logging.Formatter(formats)
        # 将输出格式添加到输出渠道

        sh.setFormatter(form)

        return log


log = LogConfig.logger_set()
