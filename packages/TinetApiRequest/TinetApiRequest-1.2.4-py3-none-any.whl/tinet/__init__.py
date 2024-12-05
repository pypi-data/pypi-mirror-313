from tinet.APIRequest import APIRequest
from tinet.ApiConfig import config, ChineseDataGenerator
from tinet.RequestUtil import HttpClient

apiConfig = config()
config.methObj = ChineseDataGenerator()
config.Session = HttpClient()
