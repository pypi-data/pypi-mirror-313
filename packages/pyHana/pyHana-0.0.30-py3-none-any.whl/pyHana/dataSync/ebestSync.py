import datetime as dt
import time
import pandas   as pd

import datetime as dt
import sys, os
# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
from   ..common   import conf, dataProc
from   ..outerIO  import ebest      as eb
from   ..innerIO  import stockInfo  as sd

def SynchStockItemList():
    ebest = eb.Ebest(login=True, debug=False)

    df = ebest.GetStockItemList('0')
    
    filePathNm = conf.stockInfoPath + "/stockitem_list.pkl"
    dataProc.WritePickleFile(filePathNm, df)        
   

##  미사용
def SynchStockItemInfo(in_shCode='', gubun='0', updateInfoType='0', frProcCnt=1, toProcCnt=99999, lastUpdateDt='99991231', sleepTime=3): 
    """ 
    shCode : 종목코드가 있는 경우 특정종목만 수행. gubun 값은 무시
    gubun : '0'(전체) '1'(코스피) '2'(코스닥) 
    updateInfoType : '0'(전체 : 종목리스트 + 기업정보) '1'(종목 리스트 only)

    frProcCnt / toProcCnt : 속도 이슈 (10분당 200건만 조회가능)로 중간에 작업 중단 현상 발생. 작업 분할 시 사용
    allRedoInd : True(항상 모든 데이터 현행화 대상) / False (재작업 시 당일 기 수행분 제외)

    우량주 등 일시 주식은 정보 없음
    """
    toDay = dt.datetime.now().strftime('%Y%m%d')

    columns = ['종목코드','기업코드','한글기업명','시가총액','현재가','PER','EPS','PBR','ROA','ROE','EBITDA','EVEBITDA','액면가','SPS','CPS','BPS','T.PER','T.EPS','PEG','T.PEG',
               '주식수','자본금','배당금','배당수익율','외국인','시장구분','시장구분명','업종구분명','그룹명',
               '위험고지구분1_정리매매','위험고지구분2_투자위험','위험고지구분3_단기과열','기업코드','결산년월','결산구분','최근분기년도'] 

    #-------------------------------------------------------------------------------------
    # 증권 시스템 로그인
    #-------------------------------------------------------------------------------------
    ebest = eb.Ebest(login=True, debug=False)

    #-------------------------------------------------------------------------------------
    # 기존 저장된 정보 Read
    #-------------------------------------------------------------------------------------    
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    #-------------------------------------------------------------------------------------
    # 현행화 대상 종목 리스트 만들기
    #-------------------------------------------------------------------------------------
    dfTemp = ebest.GetStockItemList(gubun)[['종목코드','종목명']]
    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '전체 종목수 >> ', len(dfTemp))

    if type(in_shCode) == list:
        in_shCode = '|'.join(in_shCode)        
    if len(in_shCode) > 0:
        dfTemp = dfTemp[dfTemp['종목코드'].str.contains(in_shCode)]    
    shcodeList = dfTemp.values.tolist()    

    # 재작업시 기 현행화 된 데이터는 작업 대상에서 제외
    workingList = []
    for item in shcodeList:
        shCode = item[0]

        # 재작업시 기 현행화 된 데이터는 작업 대상에서 제외
        if currData.get('data') and currData['data'].get(shCode) and currData['data'][shCode].get('updateDt')\
            and currData['data'][shCode]['updateDt'] >= lastUpdateDt:  
            pass
        else:
            workingList.append(item)
    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '변경대상(기완료제외) >> ', len(workingList))

    if frProcCnt > 1 or toProcCnt < len(workingList):
        workingList = workingList[max(0,frProcCnt-1) : min(len(workingList),toProcCnt)]

    workCntFinal = len(workingList)
    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'update대상건수 >> ', workCntFinal)

    #-------------------------------------------------------------------------------------
    # Dictionary 구조 선처리
    #-------------------------------------------------------------------------------------
    currData['columns'] = columns  ## 컬럼정보는 항상 최종본 현행화 (별다른 의미 없음)
    if not currData.get('data'):        
        currData['data'] = {}    
    
    #-------------------------------------------------------------------------------------
    # 현행화 대상 처리
    #-------------------------------------------------------------------------------------    
    for i, item in enumerate(workingList):
        procInd = False
        shCode = item[0]

        if not currData['data'].get(shCode):
            currData['data'][shCode] = {}   
            
        currData['data'][shCode]['updateDt'] = toDay
        currData['data'][shCode]['hName'] = item[1]                

        # 기업정보는 10분당 200회만 수행 가능. updateInfoType:'0'(default값)인 경우만 수행할 수 있도록 작업 세분화
        if updateInfoType == '0':
            while procInd == False:
                try:    
                    instXAQuery = ebest.GetTrData('t3320', gicode=shCode+'A', SLEEPTIME=sleepTime)
                    # return pd.DataFrame(instXAQuery[blockNm]['data'], columns=instXAQuery[blockNm]['kor'])|
                    dfStock1 = ebest._GetDataFrameKor(instXAQuery, 't3320OutBlock')
                    dfStock1['종목코드'] = shCode
                    dfStock1['기업코드'] = 'A' + shCode
                    dfStock2 = ebest._GetDataFrameKor(instXAQuery, 't3320OutBlock1')                

                    procInd = True

                except:
                    print("오류발생 : SynchStockItemInfo")

            dfStock = pd.merge(dfStock1, dfStock2, on='기업코드')
            if len(dfStock) > 0:
                dfStock['한글기업명'] = dfStock['한글기업명'].apply(lambda x: x.strip())
                dfStock['그룹명'] = dfStock['그룹명'].apply(lambda x: x.strip())

                # dfStock.rename(columns={'shcode':'종목코드','hname':'종목명'}, inplace=True)

                currData['data'][shCode]['info'] = dfStock[columns].head(1).values.tolist()[0]
            else:
                print('SynchStockItemInfo: data not found ', shCode, item[1])

        print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'proc_cnt >> ', i+1, '\r', end='')    
        if (i + 1) % 100 == 0 or (i + 1) == workCntFinal:
            print('')    
            
    # # 파일에 저장
    dataProc.WritePickleFile(filePathNm, currData)    
    
    ebest.CommDisConnect()
    del ebest    


def SynchDailyStockTradeInfo(sDate, eDate, shCode='', gubun='0', periodKnd='', sleepTime = 3):
# shCode : 종목코드가 있는 경우 gubun 값은 무시
# gubun : '0'(전체) 1'(코스피) '2'(코스닥)
# periodKnd : 'ALL' (sDate 이전 데이터도 동기화) -> 최근에 상장된 주식들도 매번 작업 수행
#             '' (저장된 데이터가 있는 경우 저장된 데이터 이후부터 eDate까지 동기화)

    ebest = eb.Ebest(login=True, debug=False)
    
    if len(shCode) > 0:
        shcodeList = [shCode]
    else:
        gubun = ['1','2'] if gubun == '0' else [gubun]
        shcodeList = []
        for x in gubun:
            instXAQuery = ebest.GetTrData('t9945', gubun = x)
            dfStock = ebest._GetDataFrameKor(instXAQuery, 't9945OutBlock')
            shcodeList += dfStock['단축코드'].values.tolist()
        
    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'total cnt >> ', len(shcodeList))

    getList = []
    for i, shcode in enumerate(shcodeList):        

        df = sd.ReadStockTrade(shcode) #, 't8410')

        if type(df) != list:
            df = df.values.tolist()

        if len(df) > 0:
            if periodKnd == 'ALL' and sDate < df[0][0]:
                getList.append([shcode, sDate, df[0][0]])
            if df[len(df)-1][0] < eDate:
                getList.append([shcode, df[len(df)-1][0], eDate]) 
        else:
            getList.append([shcode, sDate, eDate]) 

        if (i+1)%10 == 0:
            print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'proc cnt >> ', i+1,'\r', end='')  

    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '작업대상 cnt >> ', len(getList), ' '*40)          
    
    for i, x in enumerate(getList):
        procInd = False
        shcode = x[0]

        while procInd == False:
            try:    
                instXAQuery = ebest.GetTrDataOccurs('t8410', shcode=shcode, gubun='2', qrycnt=2000, sdate=x[1], edate=x[2], sujung='Y', SLEEPTIME=sleepTime)
                dfStock = ebest._GetDataFrameKor(instXAQuery, 't8410OutBlock1')

                procInd = True

            except UserWarning as UW: 
                print(UW)

                ebest.CommDisConnect()
                time.sleep(2)
                del ebest
                ebest = eb.Ebest(login=True, debug=False)

            except:
                print("오류발생")

        # # 파일에 저장
        sd._SaveStockTrade(shcode, dfStock[['날짜','시가', '고가', '저가', '종가', '거래량', '거래대금']])    

        if (i + 1) % 5 == 0:
            print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'proc_cnt >> ', i+1)    
            
    ebest.CommDisConnect()
    time.sleep(2)
    del ebest    


def  SynchEbestMarketIndexInfo(sDate, eDate, symbol='', periodKnd='', maxProcCnt=9999, sleepTime=3):
    """
    periodKnd : 'ALL' (sDate 이전 데이터도 동기화) -> 최근에 상장된 주식들도 매번 작업 수행
                '' (저장된 데이터가 있는 경우 저장된 데이터 이후부터 eDate까지 동기화)

    입력 파일 정보
    - 이베스트 HTS 4009(해외지수차트) 화면에서 지수코드 찾기(돋보기) 버튼 누른 후
      해외종목 안내 팝업 화면에서 전 종목 TAB 선택 후 데이터 그리드에서 마우스 우측 클릭하여 
      엑셀로 보낸 후 파일명 "oversea_index_list.csv"로 utf-8로 저장. 쉼표로 구분
       [코드,한글명,영문명,국가,exid,kind,real_flag] 컬럼으로 저장

    """
    

    if len(symbol) > 0:
        symbols = list(symbol)
    else:
        try:
            dfIndexList = pd.read_csv(conf.fileInfoPath + "/이베스트증권/overseas_index_list.csv", sep=',', engine='python', encoding='euc-kr').dropna()
        except:
            dfIndexList = pd.read_csv(conf.fileInfoPath + "/이베스트증권/overseas_index_list.csv", sep=',', engine='python', encoding='utf-8').dropna()

        dfIndexList['코드'] = dfIndexList['코드'].apply(lambda x: x.strip())
        dfIndexList['한글명'] = dfIndexList['한글명'].apply(lambda x: x.strip())
        dfIndexList['국가'] = dfIndexList['국가'].apply(lambda x: x.strip())

        symbols = [row for row in dfIndexList.values.tolist() if symbol in row[0]]

    # 기존 저장된 정보 Read
    getList = []
    for i, row in enumerate(symbols):     
        symbol = row[0]
        currData = sd.ReadEbestMarketIndexInfo(symbol)

        if not currData.get('data'):
            currData['data'] = []

        df = currData['data']
        if len(df) > 0:
            if periodKnd == 'ALL' and sDate < df[0][0]:
                getList.append([row, sDate, df[0][0]])
            if df[len(df)-1][0] < eDate:
                getList.append([row, df[len(df)-1][0], eDate]) 
        else:
            getList.append([row, sDate, eDate]) 

        if (i+1)%10 == 0:
            print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'proc cnt >> ', i+1,'\r', end='')  

    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '작업대상 cnt >> ', len(getList), ' '*40)          
    
    ebest = eb.Ebest(login=True, debug=False)

    for i, listVal in enumerate(getList):
        # procInd = False

        symbol = listVal[0][0]
        hname = listVal[0][1]
        nation = listVal[0][3]
        kind = listVal[0][5] # 종목종류
        sDate = listVal[1]
        eDate = listVal[2]

        # dfStock = pd.DataFrame([])

        # while procInd == False:
        #     try:    
        instXAQuery = ebest.GetTrDataOccurs('t3518', kind=kind, symbol=symbol, cnt=500, jgbn='0', 
                                            SLEEPTIME=sleepTime, SEARCHRANGE=[sDate, eDate])
        dfStock = ebest._GetDataFrameKor(instXAQuery, 't3518OutBlock1')

            #     procInd = True

            # except:
            #     print("오류발생 : SynchEbestMarketIndexInfo")

            # break

        # # 파일에 저장
        sd.SaveEbestMarketIndexInfo('t3518', symbol, hname, nation, kind, dfStock[['일자','현재가']])    

        if (i + 1) % 5 == 0:
            print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'proc_cnt >> ', i+1)    
        if (i + 1) >= maxProcCnt:
            break
            
    ebest.CommDisConnect()
    del ebest    