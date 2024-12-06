from ..outerIO  import yahoo
from ..common   import conf, dataProc, code
import pandas   as pd
import datetime 


def SyncEtfListUSA():

    filePathNm = conf.companyInfoPath + "/주식종목(미국ETF).pkl"

    dfData = yahoo.GetEtfListUSA()
    
    data = {}
    data['columns'] = dfData.columns.values.tolist()
    data['data'] = dfData.values.tolist()

    dataProc.WritePickleFile(filePathNm, data) 


def _MergeUSAData(currData, newData, sortCols=1):
    # print('>>>>>>>>>>>> ', len(currData), len(newData))
    # sortCols 병합 시 중복 판단 기준 컬럼 수(앞에서부터)
    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 후 sort
    totList = [ x[0:sortCols] + [2] + x[sortCols:] for x in currData ] \
            + [ x[0:sortCols] + [1] + x[sortCols:] for x in newData ]   
    
    totList.sort()
    # print(totList[0:5])

    # 중복데이터 제거 및 임시 우선순위 삭제
    noDupList = [ data[0:sortCols] + data[(sortCols+1):] 
                 for idx, data in enumerate(totList) if idx == 0 or data[0:sortCols] > totList[idx-1][0:sortCols] 
                ] 
    # print('>>>>>>>>>>>> ', len(currData), len(newData), len(totList), len(noDupList))

    return noDupList


def SyncEtfTradeInfoUSA(shCode='', sDate='20140101', eDate='99991231', truncInd='N'):
    ''' 
    **kwargs
    - truncInd : Y(기존데이터 전체 tuncate) / N(기존 데이타 update) 
    '''

    eDate = min(eDate, datetime.datetime.now().strftime('%Y%m%d'))

    dfCmpList = code.EtfListUSA()
    if type(shCode) in (str, list) and len(shCode) >= 1:
        if type(shCode) == str:
            shCode = [shCode] 
        shCode = pd.DataFrame(shCode, columns=['종목코드'])
    dfCmpList = pd.merge(dfCmpList, shCode, on='종목코드')

    rLen = len(dfCmpList)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '현행화대상(' + str(rLen) + ')') 

    for idx, [shCode, shName] in enumerate(dfCmpList[['종목코드','종목명']].values.tolist()):
        filePathNm = conf.stockInfoPath + "/일별주가USA/" + shCode + ".pkl"                    
        # 기존 데이터 Read
        if truncInd == 'Y':  ## 과거 저장 데이터 truncate, 신규 데이터만 저장
            currData = {}
        else:
            currData = dataProc.ReadPickleFile(filePathNm)    
            
        if not currData.get('columns'):
            currData['columns'] = ['종목코드','일자','시가','고가','저가','종가','거래량','배당금']
            
        if not currData.get(shCode):
            currData[shCode] = []        
        
        # 신규 데이터 read
        if len(currData[shCode]) == 0:
            frDt = sDate; toDt = eDate
        else:
            frDt = min(currData[shCode][-1][1], sDate)
            toDt = max(currData[shCode][0][1],  eDate)

        # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일         
        newData = yahoo.GetEtfTradeInfoUSA(shCode=shCode, frDt = frDt, toDt = toDt).values.tolist()
                
        # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
        currData[shCode] = dataProc._MergeData(currData[shCode], newData, sortCols=2) 

        dataProc.WritePickleFile(filePathNm, currData)        

        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '완료(' + str((idx+1)) + ')',
              shName + ' (' + shCode + ')', ' '*50, end='')  
        
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 일별 미국 ETN 거래정보 저장 완료')   




