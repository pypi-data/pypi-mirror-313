# import os, sys
import pandas as pd
# import re
import datetime as dt
# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
from   ..common import conf, dataProc
from   ..common import code

def EtfTradeInfoUSA(shCode):        
    x = code.EtfListUSA(shCode=shCode)[['종목코드','종목명']]
    shName = x.values[0][1] if len(x) == 1 else ''
          
    filePathNm = conf.stockInfoPath + "/일별주가USA/" + shCode + ".pkl"        
    currData = dataProc.ReadPickleFile(filePathNm)      
    columns = currData.get('columns', []) 
    retVal = currData.get(shCode, [])

    if len(retVal) > 0:
        retVal = pd.DataFrame(retVal, columns=columns) 
        retVal['종목명'] = shName
        columns.remove('종목코드')
        retVal = retVal[['종목코드','종목명']+columns]

    return retVal        


def _SaveShortSelling(shCode, newData, truncInd='N'):     
    columns=['일자', '공매도거래량', '공매도거래량업틱', '공매도거래량업틱예외', '전체거래량', '공매도거래량비중', '공매도거래대금',
             '공매도거래대금업틱', '공매도거래대금업틱예외', '전체거래대금', '공매도거래대금비중','공매도잔고수량', '상장주식수',
             '공매도잔고금액', '시가총액', '공매도잔고비중']
    
    if type(newData) == type(pd.DataFrame([])):
        newData = newData[columns].values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    filePathNm = conf.stockInfoPath + "/공매도/" + shCode + ".pkl"            
    
    # 기존 데이터 Read
    if truncInd == 'Y':  ## 과거 저장 데이터 truncate, 신규 데이터만 저장
        currData = {}
    else:
        currData = dataProc.ReadPickleFile(filePathNm)    

    if not currData.get('columns'):
        currData['columns'] = columns
        
    if not currData.get(shCode):
        currData[shCode] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData[shCode] = dataProc._MergeData(currData[shCode], newData) 

    dataProc.WritePickleFile(filePathNm, currData) 


def ShortSelling(srchItem):    
    columns=['일자', '공매도거래량', '공매도거래량업틱', '공매도거래량업틱예외', '전체거래량', '공매도거래량비중', '공매도거래대금',
             '공매도거래대금업틱', '공매도거래대금업틱예외', '전체거래대금', '공매도거래대금비중','공매도잔고수량', '상장주식수',
             '공매도잔고금액', '시가총액', '공매도잔고비중']
    
    x = code.StockItem(srchItem)[['종목코드','종목명']].values.tolist()
    [shCode, shName] = x[0] if len(x) == 1 else ['','']             
    
    filePathNm = conf.stockInfoPath + "/공매도/" + shCode + ".pkl"            

    currData = dataProc.ReadPickleFile(filePathNm)
        
    retVal = currData.get(shCode, [])

    retVal = pd.DataFrame(retVal, columns=columns)

    return retVal


def _SaveInvestorTradeVolume(shCode, newData, truncInd='N'):     
    columns=['일자', '금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금', '기타법인',
             '개인', '외국인', '기타외국인', '외국인보유수량', '외국인지분율', '외국인한도수량',
             '외국인한도소진율', '전체주식수']

    if type(newData) == type(pd.DataFrame([])):
        newData = newData[columns].values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    filePathNm = conf.stockInfoPath + "/투자자별거래/" + shCode + ".pkl"            
    
    # 기존 데이터 Read
    if truncInd == 'Y':  ## 과거 저장 데이터 truncate, 신규 데이터만 저장
        currData = {}
    else:
        currData = dataProc.ReadPickleFile(filePathNm)    

    if not currData.get('columns'):
        currData['columns'] = columns
        
    if not currData.get(shCode):
        currData[shCode] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData[shCode] = dataProc._MergeData(currData[shCode], newData) 

    dataProc.WritePickleFile(filePathNm, currData) 


def InvestorTradeVolume(srchItem):    
    columns=['일자', '금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금', '기타법인',
             '개인', '외국인', '기타외국인', '외국인보유수량', '외국인지분율', '외국인한도수량',
             '외국인한도소진율', '전체주식수']
    
    x = code.StockItem(srchItem)[['종목코드','종목명']].values.tolist()
    [shCode, shName] = x[0] if len(x) == 1 else ['','']                   
    
    filePathNm = conf.stockInfoPath + "/투자자별거래/" + shCode + ".pkl"            

    currData = dataProc.ReadPickleFile(filePathNm)
        
    retVal = currData.get(shCode, [])

    retVal = pd.DataFrame(retVal, columns=columns)

    return retVal


def _SaveStockTrade(shCode, newData, truncInd='N'):            
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터를 파일로 저장 
# 종목코드 + 거래일자 형태의 데이터만 저장
# 기존 + 신규 데이터 병합하여 저장.
# 중복 row가 있는 경우 기존 데이터는 제외 처리    
                
    # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일 

    if type(newData) == type(pd.DataFrame([])):
        newData = newData[['일자', '시가', '고가', '저가', '종가', '대비', '등락률', '거래량', '거래대금', '시가총액', 
                           '상장주식수']].values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    filePathNm = conf.stockInfoPath + "/일별주가/" + shCode + ".pkl"            
    
    # 기존 데이터 Read
    if truncInd == 'Y':  ## 과거 저장 데이터 truncate, 신규 데이터만 저장
        currData = {}
    else:
        currData = dataProc.ReadPickleFile(filePathNm)    

    if not currData.get('columns'):
        currData['columns'] = ['일자', '시가', '고가', '저가', '종가', '대비', '등락률', '거래량', '거래대금', '시가총액', '상장주식수']
        
    if not currData.get(shCode):
        currData[shCode] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData[shCode] = dataProc._MergeData(currData[shCode], newData) 

    dataProc.WritePickleFile(filePathNm, currData) 


def StockTrade(shCode):    
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터 저장한 파일에서 데이터 추출 

    x = code.StockItem(shCode)[['종목코드','종목명']]
    shCode = x.values[0][0] if len(x) == 1 else ''
    shName = x.values[0][1] if len(x) == 1 else ''    
    
    filePathNm = conf.stockInfoPath + "/일별주가/" + shCode + ".pkl"            

    currData = dataProc.ReadPickleFile(filePathNm)
        
    retVal = currData.get(shCode, [])
    if len(retVal) > 0:
        columns=['일자', '시가', '고가', '저가', '종가', '대비', '등락률', '거래량', '거래대금', '시가총액', '상장주식수']
        retVal = pd.DataFrame(retVal, columns=columns)
        retVal['종목코드'] = shCode
        retVal['종목명'] = shName
        
        retVal = retVal[['종목코드','종목명']+columns]

    # retVal = retVal.astype({'시가':'int64','고가':'int64','저가':'int64',
    #                         '종가':'int64','거래량':'int64','거래대금':'int64'}).reset_index(drop=True)
    
    # retVal = retVal[retVal['거래량'] > 0]

    return retVal


def getValidTradeInfo(shCode, sDt, tDt):
    # columns = ['종목코드', '종목명']+code.saveColumns["일별주가"]
    columns = ['종목코드', '종목명', '일자', '시가', '고가', '저가', '종가', '대비', '등락률', '거래량', '거래대금', '시가총액', '상장주식수'] 

    df = StockTrade(shCode) 
    if len(df) > 0:         
        df = df.query("@sDt <= 일자 and 일자 <= @tDt and 시가 > 0 and 고가 > 0 and 저가 > 0 and 종가 > 0 and 거래량 > 0").reset_index()

    # if len(df) > 0:
    #     df['종목코드'] = shCode  
    #     x = code.StockItem(shCode)['종목명']
    #     df['종목명'] = x.values[0] if len(x) > 0 else None
                
    #     df = df[columns]
    # else:
    #     df = pd.DataFrame([], columns = columns)      
    
    return df    

def _GetStocksTradeSingle(shCodes, priceType, sDate, eDate):
    dfRes = {}
    rLen = len(shCodes)
    for i, [shCode, shName, listDt ] in enumerate(shCodes):       
        sDt = max(sDate, listDt)       
        dfRes[shCode] = {}
        dfRes[shCode]['종목명'] = shName
        dfRes[shCode]['데이터'] = getValidTradeInfo(shCode, sDt, eDate)[['일자', priceType]]
        print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, '/', rLen, shCode, shName, ' '*40, end='')
    
    return dfRes

def MultiStocksTrade(shCodes, priceType, sDate, eDate, procTyp):
    shCodeList = code.getShcodeList(shCodes)[['종목코드','종목명','상장일']].sort_values('종목코드').values.tolist()
    if procTyp == '병렬':
        from  . import parallel
        dfRes = parallel._GetStocksTradeParallel(shCodeList, priceType, sDate, eDate)
    else:
        dfRes = _GetStocksTradeSingle(shCodeList, priceType, sDate, eDate)
    
    return dfRes
##  미사용
def ReadStockItemInfoDetail(shCode=''):   
    """
    종목 상세정보 return
    """    
    
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    retVal = []
    if shCode == '':
        for key, _ in currData['data'].items():
            if currData['data'][key].get('info'):
                retVal.append(currData['data'][key]['info'])        
    else:
        if currData['data'].get(shCode):
            retVal = [currData['data'][shCode].get('info','')]

    # retVal = pd.DataFrame(retVal, columns=currData.get('columns',''))
                # dfStock = dfStock.astype({'시가총액':'int64', '현재가':'int64', 'PER':'float64','EPS':'int64','PBR':'float64',
                #                         'ROA':'float64','ROE':'float64','EBITDA':'float64','EVEBITDA':'float64',
                #                         '액면가':'float64','SPS':'float64','CPS':'float64','BPS':'float64','T.PER':'float64',
                #                         'T.EPS':'float64','PEG':'float64','T.PEG':'float64',
                #                         '주식수':'int64','자본금':'int64','배당금':'int64','배당수익율':'float64','외국인':'float64' })    

    if len(retVal) > 0:
        retVal = pd.DataFrame(retVal, columns=currData.get('columns',''))
    return retVal

def ReadEbestMarketIndexInfo(symbol):       
    filePathNm = conf.marketIndexPath + "/이베스트증권/" + symbol + ".pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    return currData    

def SaveEbestMarketIndexInfo(trcode, symbol, hname, nation, kind, newData):            
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터를 파일로 저장 
# 해외지수 + 기준일자 형태의 데이터만 저장
# 기존 + 신규 데이터 병합하여 저장.
# 중복 row가 있는 경우 기존 데이터는 제외 처리    
                
    # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일 
    if type(newData) == type(pd.DataFrame([])):
        newData = newData.values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    # 기존 데이터 Read
    filePathNm = conf.marketIndexPath + "/이베스트증권/" + symbol + ".pkl"
    currData = dataProc.ReadPickleFile(filePathNm)                 
    if not currData.get('columns'):
        currData['columns'] = code.saveColumns[trcode]

    currData['시장지표']   = hname
    currData['국가']     = nation
    currData['종목종류'] = kind

        
    if not currData.get('data'):
        currData['data'] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData['data'] = dataProc._MergeData(currData['data'], newData) 
        
    dataProc.WritePickleFile(filePathNm, currData) 


def StockPriceIndex(indexNm):   
    """
    주가 지수 return
    """        
    filePathNm = conf.stockInfoPath + "/주가지수/" + indexNm + ".pkl"
    currData = dataProc.ReadPickleFile(filePathNm)      

    return  pd.DataFrame(currData.get(indexNm, []), columns=currData['columns'])



def _SaveStockPriceIndex(indexNm, newData, truncInd='N'):                        
    # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일 
    columns=['일자', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '상장시가총액']

    if type(newData) == type(pd.DataFrame([])):
        newData = newData[columns].values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    filePathNm = conf.stockInfoPath + "/주가지수/" + indexNm + ".pkl"         
   
    # 기존 데이터 Read
    if truncInd == 'Y':  ## 과거 저장 데이터 truncate, 신규 데이터만 저장
        currData = {}
    else:
        currData = dataProc.ReadPickleFile(filePathNm)   
        
    if not currData.get('columns'):
        currData['columns'] = columns
        
    if not currData.get(indexNm):
        currData[indexNm] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData[indexNm] = dataProc._MergeData(currData[indexNm], newData) 

    dataProc.WritePickleFile(filePathNm, currData) 