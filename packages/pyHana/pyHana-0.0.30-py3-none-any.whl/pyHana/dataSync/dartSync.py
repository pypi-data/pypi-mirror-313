from ..outerIO  import dart
from ..common   import conf, dataProc, code
from ..outerIO  import ebest    as eb
import pandas as pd
import datetime

def SyncCmpnyList(prtInd=False):

    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"

    dfData = dart.GetCmpnyList(prtInd=prtInd)

    dataProc.WritePickleFile(filePathNm, dfData) 

def SyncCmpnyAcntInfo(year, quarter, selectToc = 0, currentPageSize = 100, prtInd=False):        
    errMsg = ''
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '작업시작 :', ('연결' if selectToc == 0 else '') + '재무제표',
          '(' + str(year) + '년 ' + str(quarter) + '분기)')
    
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    
    # stockItemList = dart.GetCmpnyList(prtInd=prtInd)

    filePathNm = conf.companyInfoPath + "/재무정보(금감원).pkl"

    # selectToc : 0 (연결재무제표), 5(재무제표)    
    df = dart.GetCmpnyAcntInfo(year, quarter, selectToc=selectToc, currentPageSize=currentPageSize, prtInd=prtInd)

    resData = df.values.tolist()
    columns = df.columns.tolist()

    # print(resData)

    # 기존 데이터 read
    currData = dataProc.ReadPickleFile(filePathNm)

    if not currData.get('data'):
        currData['data'] = {}   

    # columns
    # '종목명', '결산월', 
    # '기준년도', '기준월', '기준분기', '보고서종류'
    # '유동자산','비유동자산','자산총계','유동부채','비유동부채','부채총계','자본금','이익잉여금','자본총계',
    # '매출액','영업이익','세전이익','당기순이익'

    currData['columns'] = columns[2:] + ['매출액_분기','영업이익_분기','세전이익_분기','당기순이익_분기']

    rLen = len(resData)
    for idx in range(rLen):        
        title = resData[idx][0]
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx+1, '/', rLen, title, ' '*50, end='')
        
        if len(stockItemList[stockItemList['회사명']==title]) > 0:
            shCode = stockItemList[stockItemList['회사명']==title]['종목코드'].values[0]
        else:
            x = code.StockItem(title)['종목코드'].values.tolist()
            shCode = x[0] if len(x) > 0 else ''

        if len(shCode) > 0:
            if not currData['data'].get(shCode):
                currData['data'][shCode] = {}
            if not currData['data'][shCode].get('info'):
                currData['data'][shCode]['info'] = []
            currData['data'][shCode]['종목명'] = title
            currData['data'][shCode]['결산월'] = resData[idx][1]
                
            tmpData = dataProc._MergeData(currData['data'][shCode]['info'], [resData[idx][2:] + [0,0,0,0]], sortCols=2)
            # columns
            # '기준년도', '기준월', '기준분기', '보고서종류'
            # '유동자산','비유동자산','자산총계','유동부채','비유동부채','부채총계','자본금','이익잉여금','자본총계',
            # '매출액','영업이익','세전이익','당기순이익'
            # '매출액_분기','영업이익_분기','세전이익_분기','당기순이익_분기'
                
            for i in range(len(tmpData)):
                # 매출액(13번째)
                
                    
                for x in [13,14,15,16]:  # 위치 13번째: 매출액, 14:당기순이익, 15:영업이익, 16:세전이익
                    if  tmpData[i][3] == '1분기' and type(tmpData[i][x]) == int:
                        tmpData[i][x+4] = tmpData[i][x]
                 
                    elif i > 0 and tmpData[i][3] != '1분기' and \
                        ( tmpData[i-1][0] == ( tmpData[i][0] - (1 if tmpData[i][2] == 1 else 0) ) ) and \
                        ( type(tmpData[i-1][x]) == int ) and ( type(tmpData[i][x]) == int ) and \
                        ( tmpData[i-1][3] == '1분기' and tmpData[i][3] == '반기'  or \
                          tmpData[i-1][3] == '반기'  and tmpData[i][3] == '3분기' or \
                          tmpData[i-1][3] == '3분기' and tmpData[i][3] == '사업' ):
                        
                        tmpData[i][x+4] = tmpData[i][x] - tmpData[i-1][x]

                    # if (i == 0 and tmpData[i][2] != '1분기'):
                    #     continue
                    # elif tmpData[i][2] == '1분기':
                    #     if type(tmpData[i][x]) == int:
                    #         tmpData[i][x+4] = tmpData[i][x]
                    # else:
                    #     if type(tmpData[i][x]) == int and type(tmpData[i-1][x]) == int :
                    #         tmpData[i][x+4] = tmpData[i][x] - tmpData[i-1][x]

            currData['data'][shCode]['info'] = tmpData            
        else:
            if errMsg != '':
                errMsg += '\n'
            errMsg += '회사정보 누락 : ' + title

    dataProc.WritePickleFile(filePathNm, currData)
    
    filePathNm = conf.basePath + "/작업결과/재무정보(금감원)_오류_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".txt"           
    dataProc.WriteTextFile(filePathNm, errMsg)
    
    print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '작업종료 :', ('연결' if selectToc == 0 else '') + '재무제표',
        '(' + str(year) + '년 ' + str(quarter) + '분기)')


def SaveCashFlowFromDartFile(year, quarter, file_path):
    """DART에서 제공하는 재무정보 일괄 다운로드 파일("04_현금흐름표") 내용 중
       영업현금흐름 정보 추출하여 DataFrame 형태로 반환

    반환항목:
        종목코드, 회사명, 매출액, 영업활동현금흐름
    """          

    SET_DT = lambda year, quarter : str(year)+'-'+"%02d"%(quarter * 3)+'-'+'%2d'%(31 if quarter in(1,4) else 30)

    FILE_COLUMNS = {
                "04_현금흐름표_연결" : {
                    "1분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드",
                                    "항목명","당기 1분기","전기 1분기","전기","전전기"],
                    "반기보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드",
                                    "항목명","당기 반기","전기 반기","전기","전전기"],
                    "3분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드",
                                    "항목명","당기 3분기","전기 3분기","전기","전전기"],
                    "사업보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드",
                                    "항목명","당기","전기","전전기"]
                }            
            }

    filePathNm = conf.companyInfoPath + "/현금흐름표(금감원).pkl"

    def _Pandas_ReadCsv_DartFile(year, quarter, reportKnd, file_path):
        """DART에서 제공하는 재무정보 일괄 다운로드 파일 읽기
        """            
        periodKnd = list(FILE_COLUMNS[reportKnd])[quarter-1] # quarter : 1(1분기보고서), 2(반기보고서), 3(3분기보고서), 4(사업보고서)
        fileNm = file_path + '/' + "%s_"%(year) + periodKnd + "_" + reportKnd + '.txt'
        print(fileNm, flush=True)

        try:    
            dfData = pd.read_csv(fileNm, sep='\t', engine='python', encoding='CP949', usecols=FILE_COLUMNS[reportKnd][periodKnd])
        except:
            dfData = pd.read_csv(fileNm, sep='\t', engine='python', encoding='utf-8', usecols=FILE_COLUMNS[reportKnd][periodKnd])

        return dfData  

    def _MergeIntoFinincialInfo(df):
        """DART에서 제공하는 재무정보 일괄 다운로드 파일 읽어, 주요 정보 데이터 추출 후 (GetCashFlowFromDartFile 모듈)
        기존 저장된 데이터에 merge 수행
        """         
        resData = df.values.tolist()
        columns = df.columns.tolist()[3:]

        # 기존 데이터 read        

        currData = dataProc.ReadPickleFile(filePathNm)        

        if not currData.get('data'):
            currData['data'] = {}   
        currData['columns'] = columns + ['영업현금_분기','투자현금_분기','재무현금_분기']

        for idx in range(len(resData)):
            shCode = resData[idx][0]

            if not currData['data'].get(shCode):
                currData['data'][shCode] = {}
            if not currData['data'][shCode].get('info'):
                currData['data'][shCode]['info'] = []
            currData['data'][shCode]['종목명'] = resData[idx][1]
            currData['data'][shCode]['결산월'] = resData[idx][2]

    #         currData['data'][shCode]['info'] = dataProc._MergeData(currData['data'][shCode]['info'] , [resData[idx][2:]])
            tmpData = dataProc._MergeData(currData['data'][shCode]['info'] , [resData[idx][3:] + [0,0,0]], sortCols=2)
            
            # columns
            # '기준년도', '기준분기', '결산기준일', '보고서종류'
            # '영업활동현금흐름','투자활동현금흐름','재무활동현금흐름'
            # '영업현금_분기','투자현금_분기','재무현금_분기'

            for i in range(len(tmpData)):
                for x in [4, 5, 6]:  # '영업활동현금흐름','투자활동현금흐름','재무활동현금흐름'
                        
                    if  tmpData[i][3] == '1분기' and type(tmpData[i][x]) == float:
                        tmpData[i][x+3] = tmpData[i][x]
                        
                    elif i > 0 and tmpData[i][3] != '1분기' and \
                        ( tmpData[i-1][0] == ( tmpData[i][0] - (1 if tmpData[i][2] == 1 else 0) ) ) and \
                        ( type(tmpData[i-1][x]) == float ) and ( type(tmpData[i][x]) == float ) and \
                        ( tmpData[i-1][3] == '1분기' and tmpData[i][3] == '반기'  or \
                        tmpData[i-1][3] == '반기'  and tmpData[i][3] == '3분기' or \
                        tmpData[i-1][3] == '3분기' and tmpData[i][3] == '사업' ):

                        tmpData[i][x+3] = tmpData[i][x] - tmpData[i-1][x]
                        
            currData['data'][shCode]['info'] = tmpData         
            
        dataProc.WritePickleFile(filePathNm, currData)    

    if quarter == 1:        valueColumn = '당기 1분기'
    elif quarter == 2:      valueColumn = '당기 반기'
    elif quarter == 3:      valueColumn = '당기 3분기'
    elif quarter == 4:      valueColumn = '당기'

    dfSum = pd.DataFrame({})

    for reportKnd in ["04_현금흐름표_연결"]:
        # (연결)현금흐름표에 정보가 없는 경우를 대비해 (삼성전자 2019년 1,2분기 매출액 등)
        # 낮은 우선순위로 (일반)현금흐름표 반영 (현재 미사용)
        addPriority = 10 if reportKnd in ( "04_현금흐름표" ) else 0

        dfData = _Pandas_ReadCsv_DartFile(year, quarter, reportKnd, file_path)

        # 데이터 클린징
        dfData = dfData.dropna(subset=[valueColumn], how='any', axis=0)
        dfData['종목코드'] = dfData['종목코드'].str.replace(']','').str.replace('[','')            
        dfData['항목명'] = dfData['항목명'].str.strip().str.replace('.','').str.replace(' ','').str.replace('I','')
        dfData['기준년도'] = year        
        dfData['기준분기'] = dfData['결산기준일'].apply(lambda x: 1 if x <= str(year)+'-03-31' else 2 if x <= str(year)+'-06-30' else 3 if x <= str(year)+'-09-30' else 4)
        
        dfData['보고서종류'] = dfData['보고서종류'].str.replace('보고서','')
       
        # 보고서별 항목명이 달라서 value로 통일
        dfData['value']  = dfData[valueColumn]

        # 각 항목별 데이터가 일관되게 작성되어 있지 않아 손익계산서와 포괄손익 계산서를 merge하여 구함
        # 우선순위 : 항목코드 정확하게 매칭(1순위), 검증결과 해당 항목으로 추정되는 항목명(2순위)            
        extCond = [ 
             {"통합계정명" : "영업활동현금흐름",       "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_CashFlowsFromUsedInOperatingActivities'] ] } 
            ,{"통합계정명" : "영업활동현금흐름",       "우선순위" : 2, "조건" : [ "항목명"  ,  ['영업활동현금흐름','영업활동으로인한현금흐름'] ] }
            ,{"통합계정명" : "영업활동현금흐름",       "우선순위" : 3, "조건" : [ "항목명"  ,  ['영업활동순현금흐름'] ] }                
            ,{"통합계정명" : "투자활동현금흐름",       "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_CashFlowsFromUsedInInvestingActivities'] ] } 
            ,{"통합계정명" : "투자활동현금흐름",       "우선순위" : 2, "조건" : [ "항목명"  ,  ['투자활동현금흐름','투자활동으로인한현금흐름'] ] }
            ,{"통합계정명" : "재무활동현금흐름",       "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_CashFlowsFromUsedInFinancingActivities'] ] } 
            ,{"통합계정명" : "재무활동현금흐름",       "우선순위" : 2, "조건" : [ "항목명"  ,  ['재무활동현금흐름','재무활동으로인한현금흐름'] ] }                
        ]    
        for idx in range(0, len(extCond)): 
            if extCond[idx]["조건"][0] == "항목명end":
                cond = ( dfData["항목명"].str.endswith(extCond[idx]["조건"][1]) )
            else:
                cond = ( dfData[extCond[idx]["조건"][0]].isin(extCond[idx]["조건"][1]) )

            # 3월 결산 기준일 회사 제외 (사업보고서에 전년 4월 ~ 당해 3월 데이터 반영)
#             cond = cond & ( dfData["결산기준일"] == SET_DT(year, quarter) )

            dfTemp = dfData[cond] [['종목코드','회사명', '결산월', '기준년도', '기준분기', '결산기준일', '보고서종류', 'value']]
            dfTemp['통합계정명'] = extCond[idx]["통합계정명"]
            dfTemp['우선순위']   = extCond[idx]["우선순위"] + addPriority                

            dfSum = pd.concat([dfSum, dfTemp])     
            
    dfSum['value'] = dfSum['value'].str.replace(',','').astype(dtype='int64')
    dfSum = dfSum.sort_values('우선순위').groupby(['종목코드','회사명','결산월', '기준년도', '기준분기', '결산기준일', '보고서종류','통합계정명']).first().reset_index()
    dfRes = pd.pivot_table(dfSum, values='value', index=['종목코드','회사명','결산월', '기준년도', '기준분기', '결산기준일', '보고서종류'], columns=['통합계정명'], aggfunc='sum'
                          ).reset_index()[['종목코드','회사명','결산월', '기준년도', '기준분기', '결산기준일', '보고서종류','영업활동현금흐름','투자활동현금흐름','재무활동현금흐름']]

    _MergeIntoFinincialInfo(dfRes)   