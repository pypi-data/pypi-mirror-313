from .           import conf, dataProc
from ..outerIO   import kind
import pandas    as pd

# 증권사에서 조회한 데이터를 파일로 저장하여, 데이터 분석 시 사용 (분석 수행 시 증권사 IF 최소화)
# 화면별 저장할 컬럼 정의
saveColumns = {
    "일별주가" : ['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금'],
    "t3518"    : ['일자', '종가'],
}


def _GetCmpnyName(shCode):    
    df = dataProc.ReadPickleFile( conf.stockInfoPath + "/stockitem_list.pkl" )    

    return df[df['종목코드']==shCode]

# 미국 ETF종목 기본 정보 return
def EtfListUSA(shCode='', shName=''):   
    filePathNm = conf.companyInfoPath + "/주식종목(미국ETF).pkl"
    currData = dataProc.ReadPickleFile(filePathNm)
    df = pd.DataFrame(currData.get('data', []), columns=currData['columns'])
    
    if len(shCode) > 0:       
        if type(shCode) == type(pd.DataFrame([])):
            dfX = shCode[['종목코드']] 
        else:
            if type(shCode) == str:
                dfX = [shCode]
            elif type(shCode) == list:
                dfX = shCode 
            dfX = pd.DataFrame(dfX, columns=['종목코드'])  
        df = pd.merge(dfX, df)         
    if len(shName) > 0:
        df = df.query("종목명.str.contains(@shName)")
    return  df

# 주식종목 기본 정보 return
def StockItemList():
    filePathNm = conf.companyInfoPath + "/주식종목(한국거래소).pkl"
    currData = dataProc.ReadPickleFile(filePathNm)      
    return  pd.DataFrame(currData.get('data', []), columns=currData['columns'])

def StockItem(srchItem):
    df = StockItemList()

    dfRes = df[df['종목명']==srchItem] 
    if len(dfRes) == 0:
        dfRes = df[df['종목코드']==srchItem]
    if len(dfRes) == 0:
        x = kind.GetStockItemInfoList()[['종목코드','종목명','표준코드']]
        dfRes = x[x['종목코드']==srchItem]
        if len(dfRes) == 0:
            dfRes = x[x['종목명']==srchItem]
            if len(dfRes) == 0:
                dfRes = x[x['표준코드']==srchItem]
    
    return dfRes  

def StockItemLike(title=''):   
    """
    종목명 return
    """
    df = StockItemList()

    return df[df['종목명'].str.contains(title)]

# 반복 실행을 위한 리스트 타입 종목코드 반환
def getShcodeList(shCode):
    stockInfo = StockItemList().query("시장구분 != 'KONEX'")
    if len(shCode) > 0:
        if type(shCode) == type(pd.DataFrame([])):
            dfX = shCode[['종목코드']] 
        else:
            if type(shCode) == str:
                dfX = [shCode]
            elif type(shCode) == list:
                dfX = shCode
            dfX = pd.DataFrame(dfX, columns=['종목코드'])
        stockInfo = pd.merge(dfX, stockInfo)
    
    return stockInfo