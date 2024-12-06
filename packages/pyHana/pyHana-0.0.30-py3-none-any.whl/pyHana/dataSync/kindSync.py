# from   ..common   import conf, dataProc
from ..outerIO  import kind
from ..common   import conf, dataProc
from ..innerIO  import stockInfo  as sd
import pandas   as pd
import datetime 

def SyncStockItemInfoList():

    filePathNm = conf.companyInfoPath + "/주식종목(한국거래소).pkl"

    dfData = kind.GetStockItemInfoList()
    
    data = {}
    data['columns'] = dfData.columns.values.tolist()
    data['data'] = dfData.values.tolist()

    dataProc.WritePickleFile(filePathNm, data) 


def SyncShortSelling(sDate, eDate, shCode='', maxExtYears=2, truncInd='N', shCodeFr='000000', shCodeTo='zzzzzz'):
    ''' 
    - truncInd : Y(기존데이터 전체 tuncate) / N(기존 데이타 update) 
    - maxExtYears : 한국거래소에서 조회 가능한 최대기간 : 2년 (2024.04.14 기준). 초과 시 오류
    '''

    print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 작업 대상 정보 추출')    

    dfCmpList = kind.GetStockItemInfoList()
    
    if type(shCode) in (str, list) and len(shCode) >= 1:
        if type(shCode) == str:
            shCode = [shCode] 
        dfCmpList = pd.merge(dfCmpList, pd.DataFrame(shCode, columns=['종목코드']), on='종목코드')    
    else:
        dfCmpList = dfCmpList[(dfCmpList['종목코드']>=shCodeFr)&(dfCmpList['종목코드']<=shCodeTo)]
        
    dfCmpList = dfCmpList[['종목코드','표준코드','종목명']].values.tolist()
    dfCmpList.sort()        

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 데이터 저장 시작')   

    for idx, [shCode, isuCd, shName] in enumerate(dfCmpList):
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx+1, len(dfCmpList), shCode, shName, ' '*50, end='')

        frDt = sDate[0:6]+'01'
        while frDt <= eDate:
            
            toDt = min( (pd.to_datetime(str(int(frDt) + maxExtYears*10000), format='%Y%m%d')- datetime.timedelta(1)).strftime('%Y%m%d'), eDate)
            # print(frDt, toDt, sDate, eDate)
            
            newData = kind.GetShortSelling(shCode, max(frDt, sDate), toDt, shName=shName, isuCd=isuCd)
            sd._SaveShortSelling(shCode, newData, truncInd=truncInd)      

            frDt = str(int(frDt) + maxExtYears*10000)            
    
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ' 데이터 저장 완료')   
    
    
    

def SyncInvestorTradeVolume(sDate, eDate, shCode='', maxExtYears=2, truncInd='N', shCodeFr='000000', shCodeTo='zzzzzz'):
    ''' 
    - truncInd : Y(기존데이터 전체 tuncate) / N(기존 데이타 update) 
    - maxExtYears : 한국거래소에서 조회 가능한 최대기간 : 2년 (2024.04.14 기준). 초과 시 오류
    '''

    print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 작업 대상 정보 추출')    

    dfCmpList = kind.GetStockItemInfoList()
    
    if type(shCode) in (str, list) and len(shCode) >= 1:
        if type(shCode) == str:
            shCode = [shCode] 
        dfCmpList = pd.merge(dfCmpList, pd.DataFrame(shCode, columns=['종목코드']), on='종목코드')    
    else:
        dfCmpList = dfCmpList[(dfCmpList['종목코드']>=shCodeFr)&(dfCmpList['종목코드']<=shCodeTo)]      

    dfCmpList = dfCmpList[['종목코드','표준코드','종목명']].values.tolist()
    dfCmpList.sort()                  

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 데이터 저장 시작')   

    for idx, [shCode, isuCd, shName] in enumerate(dfCmpList):
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx+1, len(dfCmpList), shCode, shName, ' '*50, end='')

        frDt = sDate[0:6]+'01'
        while frDt <= eDate:
            toDt = min( (pd.to_datetime(str(int(frDt) + maxExtYears*10000), format='%Y%m%d')- datetime.timedelta(1)).strftime('%Y%m%d'), eDate)

            newData = kind.GetTradeVolumeByInvestor(shCode, max(frDt, sDate), toDt, shName=shName, isuCd=isuCd)
            sd._SaveInvestorTradeVolume(shCode, newData, truncInd=truncInd)      

            frDt = str(int(frDt) + maxExtYears*10000)            

    
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ' 데이터 저장 완료')   
    
    
def SyncDailyStockTradeInfo(sDate, eDate, **kwargs):
    ''' 
    **kwargs
    - truncInd : Y(기존데이터 전체 tuncate) / N(기존 데이타 update) 
    '''
    
    truncInd = kwargs.get('truncInd', 'N')
    maxExtYears = kwargs.get('maxExtYears', 2)
    sDate = max(sDate, '20140101')
    eDate = min(eDate, datetime.datetime.now().strftime('%Y%m%d'))

    if "sujung" in kwargs or "shCode" in kwargs :   
        dfCmpList = kind.GetStockItemInfoList()
        shCode = kwargs.get('shCode', '')
        if type(shCode) in (str, list) and len(shCode) >= 1:
            if type(shCode) == str:
                shCode = [shCode] 
            shCode = pd.DataFrame(shCode, columns=['종목코드'])
        dfCmpList = pd.merge(dfCmpList, shCode, on='종목코드')

        if kwargs.get('sujung', 'N') == 'Y': sujung = 'Y'
        else:                                sujung = 'N'          

        rLen = len(dfCmpList)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '현행화대상(' + str(rLen) + ')') 

        for idx in range(rLen):
            newData = pd.DataFrame([])
            
            shCode = dfCmpList.iloc[idx]['종목코드'] 
            isuCd = dfCmpList.iloc[idx]['표준코드']
            shName = dfCmpList.iloc[idx]['종목명']
            listDD = dfCmpList.iloc[idx]['상장일']                        
            
            sDt = max(sDate, listDD)
            if sDt <= eDate:
                frDt = sDt[0:6]+'01'
                while frDt <= eDate:
                    toDt = min( (pd.to_datetime(str(int(frDt) + maxExtYears*10000), format='%Y%m%d')- datetime.timedelta(1)).strftime('%Y%m%d'), eDate)
                    
                    newData = pd.concat([newData, kind.GetStockTradeInfo(shCode, max(frDt, sDt), min(toDt, eDate), isuCd, shName, sujung=sujung)])
                    
                    frDt = str(int(frDt) + maxExtYears*10000)      
                              
                sd._SaveStockTrade(shCode, newData, truncInd=truncInd)      

            print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '완료(' + str((idx+1)) + ')', shCode + '/' + shName, ' '*50, end='')  
        
    else:
        df = pd.DataFrame([])
        for x in pd.date_range(sDate, eDate):        
                
            if (x.weekday() in (5, 6) or   # 토요일/일요일
                datetime.datetime.strftime(x, '%m%d') in ('0101', '0301', '0505', '0606', '0815', '1003', '1225' ) or 
                datetime.datetime.strftime(x, '%m%d') == '1009' and datetime.datetime.strftime(x, '%Y') >= '2013' ):  # 법정공휴일
                pass
            else:
                cDate = datetime.datetime.strftime(x, '%Y%m%d')            
                df = pd.concat([df, kind.GetStockTradeInfo(cDate)])            
                
                print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '일자 :', cDate, end='')
            
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 작업대상 추출', ' '*50)   

        shCodeList = sorted(df['종목코드'].unique())
        for i, shCode in enumerate(shCodeList):
            # # 파일에 저장
            sd._SaveStockTrade(shCode, df[df['종목코드']==shCode], truncInd=truncInd)                      
            # sd._SaveStockTrade(shCode, df[df['종목코드']==shCode][['일자', '시가', '고가', '저가', '종가', '대비', '등락률', '거래량', 
            #                                                     '거래대금', '시가총액', '상장주식수']].values.tolist() )    

            print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 전체대상(' + str(len(shCodeList)) + '), 완료(' + str((i+1)) + '), 종목코드('  + shCode + ')', end='')            
    
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 일별 주가 현행화 완료')   

# def SynchDailyStockTradeInfo(sDate, eDate):

#     curDt = sDate
#     while curDt <= eDate:
#         x, columns = kind.GetStockTradeInfo(curDt)
#         df = pd.DataFrame(x, columns=columns)
#         df = df[df['시가']!='-']

#         if len(df) > 0:
#             print('')
#             for i in range(len(df)):
#                 # # 파일에 저장
#                 sd._SaveStockTrade('일별주가', df['종목코드'].iloc[i], [df[['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금']].iloc[i].tolist()])    

#                 print('\r' + curDt, (i+1), '/',  len(df), end='')
#             curDt = (datetime.datetime.strptime(curDt, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")     
#             print(' 완료')

# def SyncDividendInfo(sYear, eYear, marketType='', settlementMonth='', selYearCnt = 3, prtInd=False):
def SyncDividendInfo(sYear, eYear, mktId='', prtInd=False):
    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"

    yearCnt = 3
    for selYear in range(eYear, sYear-1, -yearCnt):
        if selYear < (sYear + yearCnt):
            yearCnt = selYear - sYear + 1
        
        print(selYear, yearCnt)            

        df = kind.GetDividendInfo(selYear, mktId=mktId, yearCnt=yearCnt, prtInd=prtInd)

        resData = df.values.tolist()
        columns = df.columns.tolist()[2:]

        # 기존 데이터 read
        currData = dataProc.ReadPickleFile(filePathNm)

        if not currData.get('data'):
            currData['data'] = {}   
        currData['columns'] = columns


        for idx in range(len(resData)):
            shCode = resData[idx][0]

            if not currData['data'].get(shCode):
                currData['data'][shCode] = {}
            if not currData['data'][shCode].get('info'):
                currData['data'][shCode]['info'] = []
            currData['data'][shCode]['종목명'] = resData[idx][1]

# ['종목코드', '종목명','사업년도','결산월','업종','업종별배당율','주식배당','액면가','기말주식수',
#                '주당배당금','배당성향','총배당금액','시가배당율']            
            currData['data'][shCode]['info'] = dataProc._MergeData(currData['data'][shCode]['info'] , [resData[idx][2:]])

        dataProc.WritePickleFile(filePathNm, currData) 


def SyncStockPriceIndex(indexNm, sDate, eDate, truncInd='N'):

    frDt = sDate[0:6]+'01'
    while frDt <= eDate:
        toDt = min( (pd.to_datetime(str(int(frDt)+20000), format='%Y%m%d')- datetime.timedelta(1)).strftime('%Y%m%d'), eDate)

        newData = kind.GetStockPriceIndex(indexNm, max(frDt, sDate), toDt)

        sd._SaveStockPriceIndex(indexNm, newData, truncInd=truncInd)        

        frDt = str(int(frDt)+20000)
