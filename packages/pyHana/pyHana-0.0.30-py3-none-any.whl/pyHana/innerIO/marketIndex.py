import gzip, pickle
import pandas as pd

# import re

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '.'))
from ..common import conf, dataProc

# 실행환경이 주피터노트북인지 체크
# JupyterInd = True if sys.argv[0].endswith('ipykernel_launcher.py') else False

# econIndexFileNm  = conf.marketIndexPath + "/economic_index_info.pkl"

# def SaveMarketIndex(indexNm, newMarketIndex):    
#     currMarketIndex = dataProc.ReadPickleFile(econIndexFileNm)
        
#     # 내부적 연산 시 list형으로 통일 후 수행    
#     if type(newMarketIndex) == type(pd.DataFrame([])):
#         newMarketIndex = newMarketIndex.values.tolist()
#     elif type(newMarketIndex) != list:
#         raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')
    
#     if not currMarketIndex.get(indexNm):
#         currMarketIndex[indexNm] = {}
#         currMarketIndex[indexNm]['columns'] = ['일자', indexNm]
#         currMarketIndex[indexNm]['data']    = [] 
    
#     # 경제지수 input data 정렬 및 중복 제거 (크롤링 시 중복 발생하는 케이스 )
#     # 날짜 형식도 8자리 숫자로 통일
#     newMarketIndex = [ [data[0].replace('-','').replace('/','')] + data[1:] for data in newMarketIndex ]        
#     # currList = currMarketIndex[indexNm]['data']
#     # totList = currList + newMarketIndex
#     # totList.sort()

#     # noDupList = [ [data[0].replace('-','').replace('/',''), data[1] ]
#     #               for idx, data in enumerate(totList) if idx == 0 or data[0] > totList[idx-1][0] ]    
    
#     # currMarketIndex[indexNm]['data'] = noDupList


#     currMarketIndex[indexNm]['data']  = dataProc._MergeData(currMarketIndex[indexNm]['data'] , newMarketIndex) 

        
#     with gzip.open(econIndexFileNm, 'wb') as f:
#         pickle.dump(currMarketIndex, f)              


# def ReadMarketIndex_old(indexNm, objTyp='DataFrame'):    
#     currMarketIndex = dataProc.ReadPickleFile(econIndexFileNm)
        
#     retVal = currMarketIndex.get(indexNm, {})
    
#     if objTyp == 'list':
#         pass
#     else:
#         retVal = pd.DataFrame(retVal['data'], columns=retVal['columns'])

#     return retVal


import gzip, pickle
import pandas as pd

from pyHana.common import conf, dataProc

def SaveMarketIndex(indexNm, newMarketIndex):    
    econIndexFileNm  = conf.marketIndexPath + "/" + indexNm + ".pkl"
    currMarketIndex = dataProc.ReadPickleFile(econIndexFileNm)

    if len(currMarketIndex) > 0:
        if type(currMarketIndex) == type(pd.DataFrame([])):
            currMarketIndex = currMarketIndex.values.tolist()
        elif type(currMarketIndex) != list:
            raise Exception('SaveMarketIndex >> current file type 오류')                
    else:
        currMarketIndex = []
        
    # 내부적 연산 시 list형으로 통일 후 수행    
    if type(newMarketIndex) == type(pd.DataFrame([])):
        newMarketIndex = newMarketIndex.values.tolist()
    elif type(newMarketIndex) != list:
        raise Exception('SaveMarketIndex >> newMarketIndex type 오류 : list형 또는 DataFrame 형태만 처리 가능')
      
    # 경제지수 input data 정렬 및 중복 제거 (크롤링 시 중복 발생하는 케이스 )
    # 날짜 형식도 8자리 숫자로 통일
    newMarketIndex = [ [data[0].replace('-','').replace('/','')] + data[1:] for data in newMarketIndex ] 
    
    currMarketIndex = dataProc._MergeData(currMarketIndex, newMarketIndex)
        
    with gzip.open(econIndexFileNm, 'wb') as f:
        pickle.dump(currMarketIndex, f)              


def MarketIndex(indexNm, objTyp='DataFrame'):    
    econIndexFileNm  = conf.marketIndexPath + "/" + indexNm + ".pkl"
    retVal = dataProc.ReadPickleFile(econIndexFileNm)

    if objTyp == 'DataFrame':
        retVal = pd.DataFrame(retVal, columns = ['일자',indexNm] )

    return retVal


def UpdateMarketIndex(indexNm, date, val):    
    econIndexFileNm  = conf.marketIndexPath + "/" + indexNm + ".pkl"
    currMarketIndex = dataProc.ReadPickleFile(econIndexFileNm)
        
    newMarketIndex = [[date, val]]
      
    # 경제지수 input data 정렬 및 중복 제거 (크롤링 시 중복 발생하는 케이스 )
    # 날짜 형식도 8자리 숫자로 통일
    newMarketIndex = [ [data[0].replace('-','').replace('/','')] + data[1:] for data in newMarketIndex ] 
    
    currMarketIndex = dataProc._MergeData(currMarketIndex, newMarketIndex)
        
    with gzip.open(econIndexFileNm, 'wb') as f:
        pickle.dump(currMarketIndex, f)      