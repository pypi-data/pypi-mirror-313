import os
import configparser

# 설정파일 읽기
configPath = os.environ['PyhanaConfigPath']
config = configparser.ConfigParser()    
config.read(configPath+'/config.ini', encoding='utf-8') 

# print(configPath+'/config.ini')

ebestId  = config['ebest']['id']
ebestPwd = config['ebest']['pwd']
certPwd  = config['ebest']['certpwd']
xingAPIRes = config['ebest']['xingAPIRes']

basePath        = config['path']['base']
fileInfoPath    = config['path']['fileInfo']
marketIndexPath = config['path']['marketIndex']
stockInfoPath   = config['path']['stockInfo']
companyInfoPath = config['path']['companyInfo']
dataAnalPath    = config['path']['dataAnal']