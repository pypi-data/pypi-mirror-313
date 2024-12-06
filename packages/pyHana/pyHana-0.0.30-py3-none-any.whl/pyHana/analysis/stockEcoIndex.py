import pandas   as pd  
import datetime as dt

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
from  ..innerIO  import marketIndex    as mIndex
from  ..innerIO  import stockInfo
# from  ..innerIO  import stockInfo      as sd
from  ..common   import code  
from  ..analysis import findSignals    as bs
from  .          import func

def GetInterIndexCorrelation(indexNm1, indexNm2, sDate='20000101',  eDate='20991231', addDays=0, 
                             rptGb='기본', period='일'):
    """
    (input)
        indexNm1/2 : BDI 등 
        addDays    : indexNm1의 날짜 조정 일수 (예) 3 : indexNm1 일자 + 3일 = indexNm2 일자
        rptGb      : '기본' 원본 값으로 계산 / '증감' : 증감값으로 계산 / '전체' : 원본값 및 증감값으로 모두 계산
    (output)
        상관계수 return
    """
    
    columns=['인덱스1','인덱스2','분석대상건수']
    if rptGb in ['기본', '전체']:  columns += ['상관계수', 'p-value']
    if rptGb in ['증감', '전체']:  columns += ['증감값상관계수','증감값p-value','증감값유사도', '증감값비유사도']
    
    resData = []
            
    # 1년 365일 모든 일자에 대해 경제지수 데이터 생성 (없는 경우 전일 데이터 값으로 생성)
    # 선행일수 고려 증권거래일자와 매핑을 하기 위한 사전 작업
    dfIndex1 = mIndex.MarketIndex(indexNm1)
    dfIndex2 = mIndex.MarketIndex(indexNm2)
    if period=='일':
        dfIndex2 = func.makeFullDayData(dfIndex2)    
    if period=='주':
        dfWeeks = func.getISOWeeks(sDate=sDate, eDate=eDate, addDays=addDays)
    else:
        dfWeeks = []
        
    if period != '일':
        dfIndex1 = func.addPeriodGrp(dfIndex1, indexNm1, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=0)
    dfIndex2 = func.addPeriodGrp(dfIndex2, indexNm2, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=addDays)
    dfMerge = pd.merge(dfIndex1, dfIndex2)
                    
    # 병합한 데이터로 Correlation Value 계산 
    corrVal = func.CalcCorrRelation(dfMerge[indexNm1].values.tolist(), dfMerge[indexNm2].values.tolist(), rptGb=rptGb)

    if len(corrVal) > 0:
        resData.append([indexNm1, indexNm2] + corrVal)        

    retVal = pd.DataFrame(resData, columns=columns)
        
    return retVal

def _getGetStockIndexCorr(dfStocks, priceType, period, dfWeeks, indexNm, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd):
    resData = []
    #--------------------------------------------------------------------------------------------------------------------
    # 시장지표 처리하기               
    #--------------------------------------------------------------------------------------------------------------------
    dfIndex = mIndex.MarketIndex(indexNm)
    # 1년 365일 모든 일자에 대해 경제지수 생성하기 전, 지표의 평균 상승/하락 기간 구함
    avgPeriod, upPeriod, downPeriod = func.getAvgTurnAround(dfIndex[indexNm].values.tolist())
    # 1년 365일 모든 일자에 대해 경제지수 데이터 생성 (없는 경우 전일 데이터 값으로 생성)
    # 선행일수 고려 증권거래일자와 매핑을 하기 위한 사전 작업    
    if period=='일':
        dfIndex = func.makeFullDayData(dfIndex, eDate=extDt) 

    dfIndex = func.addPeriodGrp(dfIndex, indexNm, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=addDays)

    rLen = len(dfStocks.keys())
    for i, shCode in enumerate(dfStocks.keys()):
        shName = dfStocks[shCode]['종목명']
#         corrVal = _getCorrVal(dfStocks[shCode]['데이터'], priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate)
        
        # 주가정보와 지표정보를 선행 기준에 의해 병합
        dfStock = dfStocks[shCode]['데이터']
        if period != '일':
            dfStock = func.addPeriodGrp(dfStock, priceType, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=0)

        dfMerge = pd.merge(dfStock, dfIndex)

        if len(dfMerge) < 2:
            # print('분석 데이터 부족 :', shCode)
            corrVal = []
        else:
            # 병합한 데이터로 Correlation Value 계산 
            corrVal = func.CalcCorrRelation(dfMerge[priceType].values.tolist(), dfMerge[indexNm].values.tolist(), rptGb)            

        if len(corrVal) > 0:
            resData.append([indexNm, shCode, shName] + corrVal + [avgPeriod, upPeriod, downPeriod] )        

        if prtInd:
            print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), indexNm, i+1, '/', rLen, shCode, shName, ' '* 40, end='')    

    print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), indexNm, '완료', ' '* 100)    
    return  resData

# 주식종목별 시장지표에 대한 상관계수 구하기 (순차처리)
def _getGetStockIndexCorrSingle(dfStocks, priceType, period, dfWeeks, indexNmList, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd):
    resData = []
    for indexNm in indexNmList:
        res = _getGetStockIndexCorr(dfStocks, priceType, period, dfWeeks, indexNm, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd)
        resData += res

    return resData    

def GetStockIndexCorrelation(priceType='종가', indexNm='', shCodes=[], sDate='00000101',  eDate='99991231', 
                             addDays=0, rptGb='전체', period='일', extDt='',prtInd=True, procTyp = '순차'):    
    """
    (input)
        priceType : 시가/고가/저가/종가
        indexNm : BDI 등 
        shCodes : '000980' (특정종목), ['123456','005880'] (리스트). [ ] (데이터가 없으면 전 종목 분석)
        addDays : 주식거래 날짜 조정 일수 (예) 3 : 주식거래일자 + 3일 = indexNm2 일자
        rptGb   : '기본' 원본 값으로 계산 / '증감' : 증감값으로 계산 / '전체' : 원본값 및 증감값으로 모두 계산
        extDt   : 월요일 주가와 금요일 시장지표(BDI) 분석 시 시장지표 매핑하기 위해 사용
    (output)
        상관계수 return
    """
    if prtInd:
        print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석시작')
    
    dfStocks = stockInfo.MultiStocksTrade(shCodes, priceType, sDate, eDate, procTyp)
    print('\r'+ dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '주식정보 loading 완료')
    
    # (성능향상) 주차별 통계 생성하기 위해 일자를 년주차로 한번 변환 후 공통 사용
    if period=='주':
        dfWeeks = func.getISOWeeks(sDate=sDate, eDate=eDate, addDays=addDays)
    else:
        dfWeeks = []
    
    if type(indexNm) == str:
        indexNm = [indexNm]

    #--------------------------------------------------------------------------------------------------------------------
    # 종목리스트의 종목별 시장지표 상관계수 구하기               
    #--------------------------------------------------------------------------------------------------------------------        
    if procTyp == '병렬':
        from  . import parallel
        resData = parallel._getGetStockIndexCorrParallel(dfStocks, priceType, period, dfWeeks, indexNm, 
                                    addDays, rptGb, sDate, eDate, extDt, False)
    else:
        resData = _getGetStockIndexCorrSingle(dfStocks, priceType, period, dfWeeks, indexNm, 
                                    addDays, rptGb, sDate, eDate, extDt, prtInd) 
       
    #--------------------------------------------------------------------------------------------------------------------
    # 결과값 데이터 프레임으로 변환 후 반환하기              
    #--------------------------------------------------------------------------------------------------------------------        
    resData.sort(key = lambda x: x[3], reverse=True)
    
    columns=['시장지표', '종목코드','종목명','분석대상건수']
    if rptGb in ['기본', '전체']:  columns += ['상관계수', 'p-value']
    if rptGb in ['증감', '전체']:  columns += ['증감값상관계수','증감값p-value','증감값유사도', '증감값비유사도']
    columns += ['전체평균기간', '상승평균기간', '하락평균기간']
    retVal = pd.DataFrame(resData, columns=columns)
    
    if prtInd:
        print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석종료', ' '*40)
    
    return retVal

# def GetStockIndexCorrelation(priceType, indexNm, shCodes=[], sDate='00000101',  eDate='99991231', 
#                              addDays=0, rptGb='전체', period='일', extDt='',prtInd=True, procTyp = '순차'):    
#     """
#     (input)
#         priceType : 시가/고가/저가/종가
#         indexNm : BDI 등 
#         shCodes : '000980' (특정종목), ['123456','005880'] (리스트). [ ] (데이터가 없으면 전 종목 분석)
#         addDays : 주식거래 날짜 조정 일수 (예) 3 : 주식거래일자 + 3일 = indexNm2 일자
#         rptGb   : '기본' 원본 값으로 계산 / '증감' : 증감값으로 계산 / '전체' : 원본값 및 증감값으로 모두 계산
#         extDt   : 월요일 주가와 금요일 시장지표(BDI) 분석 시 시장지표 매핑하기 위해 사용
#     (output)
#         상관계수 return
#     """
#     if prtInd:
#         print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석시작', indexNm)
    
#     # (성능향상) 주차별 통계 생성하기 위해 일자를 년주차로 한번 변환 후 공통 사용
#     if period=='주':
#         dfWeeks = func.getISOWeeks(sDate=sDate, eDate=eDate, addDays=addDays)
#     else:
#         dfWeeks = []

#     #--------------------------------------------------------------------------------------------------------------------
#     # 시장지표 처리하기               
#     #--------------------------------------------------------------------------------------------------------------------
#     dfIndex = mIndex.MarketIndex(indexNm)
#     # 1년 365일 모든 일자에 대해 경제지수 생성하기 전, 지표의 평균 상승/하락 기간 구함
#     avgPeriod, upPeriod, downPeriod = func.getAvgTurnAround(dfIndex[indexNm].values.tolist())
#     # 1년 365일 모든 일자에 대해 경제지수 데이터 생성 (없는 경우 전일 데이터 값으로 생성)
#     # 선행일수 고려 증권거래일자와 매핑을 하기 위한 사전 작업    
#     if period=='일':
#         dfIndex = func.makeFullDayData(dfIndex, eDate=extDt) 
    
#     dfIndex = func.addPeriodGrp(dfIndex, indexNm, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=addDays)
    
#     #--------------------------------------------------------------------------------------------------------------------
#     # 종목리스트의 종목별 시장지표 상관계수 구하기               
#     #--------------------------------------------------------------------------------------------------------------------        
#     if procTyp == '병렬':
#         from  . import parallel
#         resData = parallel._getGetStockIndexCorrParallel(shCodes, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate)
#     else:
#         resData = _getGetStockIndexCorrSingle(shCodes, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, prtInd)
       
#     #--------------------------------------------------------------------------------------------------------------------
#     # 결과값 데이터 프레임으로 변환 후 반환하기              
#     #--------------------------------------------------------------------------------------------------------------------        
#     resData.sort(key = lambda x: x[3], reverse=True)
    
#     columns=['종목코드','종목명','분석대상건수']
#     if rptGb in ['기본', '전체']:  columns += ['상관계수', 'p-value']
#     if rptGb in ['증감', '전체']:  columns += ['증감값상관계수','증감값p-value','증감값유사도', '증감값비유사도']
    
#     retVal = pd.DataFrame(resData, columns=columns)
#     retVal['전체평균기간'] = avgPeriod
#     retVal['상승평균기간'] = upPeriod
#     retVal['하락평균기간'] = downPeriod    
#     if prtInd:
#         print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석종료', indexNm, ' '*40)
    
#     return retVal

# # 주식종목별 시장지표에 대한 상관계수 구하기 (순차처리)
# def _getGetStockIndexCorrSingle(shCodes, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, prtInd):
#     shCodeList = code.getShcodeList(shCodes)[['종목코드','종목명','상장일']].values.tolist()                   
#     resData = []   
#     for i, [shCode, shName, listDt ] in enumerate(shCodeList):
   
#         corrVal = _getCorrVal(shCode, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, listDt)
#         if len(corrVal) > 0:
#             resData.append([shCode, shName] + corrVal)        

#         if prtInd:
#             print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, '/', len(shCodeList), shCode, shName, ' '* 40, '\r', end='')
#     return resData


# def _getCorrVal(shCode, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, listDt):
#     sDt = max(sDate, listDt)        
#     dfStock = stockInfo.getValidTradeInfo(shCode, sDt, eDate)[['일자', priceType]]

#     # 주가정보와 지표정보를 선행 기준에 의해 병합
#     # dfMerge = dfStock.merge(dfIndex)[['일자', priceType, 'Signal일자', indexNm]]
#     if period != '일':
#         dfStock = func.addPeriodGrp(dfStock, priceType, dfWeeks=dfWeeks, period=period, sDate=sDt, eDate=eDate, addDays=0)
            
#     dfMerge = pd.merge(dfStock, dfIndex)
    
#     if len(dfMerge) < 2:
#         # print('분석 데이터 부족 :', shCode)
#         return []
#     else:
#         # 병합한 데이터로 Correlation Value 계산 
#         return func.CalcCorrRelation(dfMerge[priceType].values.tolist(), dfMerge[indexNm].values.tolist(), rptGb)         
        

    
