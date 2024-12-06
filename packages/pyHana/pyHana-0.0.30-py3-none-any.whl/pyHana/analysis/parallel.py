import pandas    as pd
import datetime  as dt
from ..common    import code
from ..analysis  import backtest       as bt
from ..analysis  import stockEcoIndex  as se
from ..analysis  import func
import ray

@ray.remote
def index_backtest_parallel(shCode, indexNm, pType, frDt, toDt, addDays, max_retention_days, multiRetentionInd, maxItemNum,          
                       cashAmt, taxRatio, expenseRatio, dayMaxTradeNum, dfZeroCross, retType, idx, rLen):
    _, dfReport, _ = bt._index_backtest(shCode=shCode, indexNm=indexNm, pType=pType, frDt=frDt, toDt=toDt
                                    , addDays=addDays , max_retention_days = max_retention_days 
                                    , multiRetentionInd = multiRetentionInd, maxItemNum = maxItemNum          
                                    , cashAmt = cashAmt, taxRatio = taxRatio, expenseRatio = expenseRatio     
                                    , dayMaxTradeNum = dayMaxTradeNum     
                                    , dfZeroCross = dfZeroCross
                                    , retType = retType )    
    if (idx+1) % 1000 == 0:
        x = code.StockItem(shCode)['종목명']
        shName = x.values[0] if len(x) > 0 else None
        print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (idx+1), '/', rLen, shCode, shName)
    return dfReport

def _getIndexBacktestParallel(shCodeList, indexNm, pType, frDt, toDt, addDays, max_retention_days, multiRetentionInd, maxItemNum, cashAmt,
                            taxRatio, expenseRatio, dayMaxTradeNum, dfZeroCross, retType, rLen):
    
    dfRet = pd.DataFrame([])
    requests = []
    
    putZeroCross = ray.put(dfZeroCross)
    
    for idx, [shCode, shName, listDt ] in enumerate(shCodeList):
        sDt = max(frDt, listDt) # 코스피/코스닥 상장 이후 거래내역만 처리 (코넥스 -> 코스닥 등)
        dfReport = index_backtest_parallel.remote(shCode, indexNm, pType, sDt, toDt, addDays, max_retention_days, 
                                             multiRetentionInd, maxItemNum,          
                                             cashAmt, taxRatio, expenseRatio, dayMaxTradeNum, putZeroCross, retType, idx, rLen)      
            
        requests.append(dfReport)

    while len(requests):
        done, requests = ray.wait(requests) # 다된 작업은 done으로 넘긴다.
        dfRet = pd.concat([dfRet, ray.get(done[0])]) 
    
    ray.shutdown()
    
    return dfRet

@ray.remote
def _getGetStockIndexCorrRay(dfStocks, priceType, period, dfWeeks, indexNm, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd):
    return se._getGetStockIndexCorr(dfStocks, priceType, period, dfWeeks, indexNm, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd)

# 주식종목별 시장지표에 대한 상관계수 구하기 (병렬처리)
def _getGetStockIndexCorrParallel(dfStocks, priceType, period, dfWeeks, indexNmList, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd):
    ray.init(num_cpus=16)
    
    putStocks = ray.put(dfStocks)
    
    requests = []
    for indexNm in indexNmList:    
        retVal = _getGetStockIndexCorrRay.remote(putStocks, priceType, period, dfWeeks, indexNm, 
                                addDays, rptGb, sDate, eDate, extDt, prtInd)
        requests.append(retVal)    
    
    resData = []
    while len(requests):
        done, requests = ray.wait(requests) # 다된 작업은 done으로 넘긴다.
        resData += ray.get(done[0])
    
    ray.shutdown()    

    return resData    

# @ray.remote
# def GetCorrelation_parallel(shCode, shName, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, listDt, i, rlen):
#     if (i+1) % 1000 == 0:
#         print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, '/', rlen, shCode, shName)
#     return shCode, shName, se._getCorrVal(shCode, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate, listDt)

# def _getGetStockIndexCorrParallel(shCodes, priceType, period, dfWeeks, dfIndex, indexNm, rptGb, sDate, eDate):
#     putWeeks = ray.put(dfWeeks)
#     shCodeList = code.getShcodeList(shCodes)[['종목코드','종목명','상장일']].values.tolist()                   
#     requests = []; resData = []
#     rLen = len(shCodeList)
     
#     for i, [shCode, shName, listDt ] in enumerate(shCodeList):   
#         corrVal = GetCorrelation_parallel.remote(shCode, shName, priceType, period, putWeeks, dfIndex, indexNm, rptGb, 
#                                                  sDate, eDate, listDt, i, rLen)        
#         requests.append(corrVal)

#     while len(requests):
#         done, requests = ray.wait(requests) # 다된 작업은 done으로 넘긴다.
#         shCode, shName, corrVal = ray.get(done[0])
#         if len(corrVal) > 0:
#             resData.append([shCode, shName] + corrVal)        
    
#     ray.shutdown()    
    
#     return resData