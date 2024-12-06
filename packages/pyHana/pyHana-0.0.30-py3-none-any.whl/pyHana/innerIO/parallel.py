import ray
import datetime as dt
from . import stockInfo

@ray.remote
def _GetStocksTradeRay(shCode, shName, priceType, sDate, eDate, i, rLen):
    if (i+1)%500 == 0:
        print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, '/', rLen, shCode, shName)
    return shCode, shName, stockInfo.getValidTradeInfo(shCode, sDate, eDate)[['일자', priceType]]

def _GetStocksTradeParallel(shCodes, priceType, sDate, eDate):
    ray.init()
    
    requests = []
    rLen = len(shCodes)
    for i, [shCode, shName, listDt ] in enumerate(shCodes):    
        retVal = _GetStocksTradeRay.remote(shCode, shName, priceType, max(sDate, listDt), eDate, i, rLen)
        requests.append(retVal)

    dfRes = {}
    while len(requests):
        done, requests = ray.wait(requests) # 다된 작업은 done으로 넘긴다.
        shCode, shName, dfGet = ray.get(done[0])
        if len(dfGet) > 0:
            dfRes[shCode] = {}
            dfRes[shCode]['종목명'] = shName
            dfRes[shCode]['데이터'] = dfGet
    
    ray.shutdown()    
    
    return dfRes    