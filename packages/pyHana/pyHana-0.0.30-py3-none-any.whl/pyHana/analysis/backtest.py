import pandas    as pd
import random, math
import datetime  as dt

from ..analysis   import backtest  as bt
from ..innerIO    import marketIndex as i_mi
from  ..innerIO   import stockInfo
from ..analysis   import findSignals as bs
from ..analysis   import func
from ..common     import code

# backtest 수행 : 성능 향상을 위해 dataframe 처리 최소화 버전
def backtest(dfData
           , maxItemNum = 1           # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) 
           , cashAmt = 100000000      # 초기 투자금
           , taxRatio = 0.2           # 거래세(%)
           , expenseRatio = 0.015     # 거래수수료(%) 
           , dayMaxTradeNum = 1       # 일 최대 매수 가능 종목수
           ):  
    invItemList = []  # 투자 진행 종목의 종료일자 - 다음 투자를 위해
    simulRes = []     # 투자 결과 리스트 저장

    # 처리속도 향상을 위해 dataframe -> list 변환 후 수행
    listTradeInfo = dfData[['종목코드','종목명','매수일자','매수가격','매도일자','매도가격']].values.tolist()    
    
    # # input 데이터의 종목수가 분산 투자 주식 수보다 적은 경우 보정처리 => 한 종목으로도 분산 투자 가능하도록 로직 삭제
    # maxItemNum = min(maxItemNum, len(dfData["종목코드"].unique()))
    
    listTradeDt = dfData["매수일자"].unique().tolist()
    listTradeDt.sort()
    
    while(len(listTradeDt) > 0):
        curDt = listTradeDt[0]

        # 투자일 경과 건 투자진행 종목 리스트에서 삭제
        i = 0
        while i < len(invItemList) and invItemList[i] < curDt:
            i += 1
        if i >= 0:
            invItemList = invItemList[i:]

        # maxItemNum 개의 종목에 투자금액 1/N 분배 (이미 투자진행중인 건은 잔존 현금의 투자금액 분배 시 제외)
        ##  cashAmt가 아니라 해당 일자까지 투자한 금액, 회수 못한 금액을 감안한 여유 자금 재계산 필요        
        sellAmtSum = 0
        sellExpenseSum = 0
        for i in range(len(simulRes)):
            # simulRes [종목코드(0),종목명(1),수량(2),매수일자(3),매수가격(4),매수금액(5),매수비용(6),
            #           매도일자(7),매도가격(8),매도금액(9),매도비용(10),손익(11),수익률(%)(12),평가금액(13)                                                  
            if simulRes[i][7] >= curDt:                  # '매도일자'
                sellAmtSum += simulRes[i][9]             # '매도금액'
                sellExpenseSum += simulRes[i][10]        # '매도비용'
        maxInvAmt = (cashAmt - sellAmtSum + sellExpenseSum) / ( maxItemNum - len(invItemList) )

        # 해당 일자에 대한 투자 대상종목 수 계산
        curInvItemNum =  min (maxItemNum - len(invItemList), dayMaxTradeNum )
        # dList = [x for x in listTradeInfo if x[2] == curDt]
        dList = [x for x in listTradeInfo if x[2] == curDt and maxInvAmt >= x[3]] # x[3] 주가. 1주이상 살 수 있는 종목만 list

        if len(dList) > curInvItemNum:
            random.shuffle(dList)
            dList = dList[:curInvItemNum]
        
        for x in dList:
            # 매입일자, 가격 구하기
            buyDt = x[2]
            buyPrice = x[3]
            # 매도일자, 가격 구하기
            sellDt = x[4]      
            sellPrice = x[5]

            #######################################################
            # 매수/매도 거래내역 만들기
            #######################################################
            
            # 주식수량
            buyCnt = int(maxInvAmt / buyPrice)

            # 매입계산
            buyAmt = buyCnt * buyPrice * (-1)
            buyExpense = int(buyAmt * expenseRatio / 100)

            # 매도계산
            sellAmt = buyCnt * sellPrice
            sellExpense = int(sellAmt * taxRatio / 100) * (-1) + int(sellAmt * expenseRatio / 100) * (-1)

            # 보유현금 계산
            deltaAmt = buyAmt + buyExpense + sellAmt + sellExpense
            cashAmt += deltaAmt

            # 거래수익률 계산
            earnRatio = deltaAmt / (buyAmt + buyExpense) * (-100)
             
            # 매도, 매수 결과
            simulRes.append([x[0], x[1], buyCnt, buyDt, buyPrice, buyAmt, buyExpense, 
                             sellDt, sellPrice, sellAmt, sellExpense, deltaAmt, earnRatio, cashAmt] )

            invItemList.append(sellDt)

        invItemList.sort()

        if len(invItemList) >= maxItemNum:
            # 보유 종목 갯수가 max인 경우, 보유종목의 최초 매도일자 이후로 이동
            i = 0
            while( i < len(listTradeDt) ):
                if listTradeDt[i] > invItemList[0]:
                    break
                i += 1

            listTradeDt = listTradeDt[i:]               
        else:
            # 추가 매수 가능한 경우, 다음 시그널 발생일로 이동
            listTradeDt = listTradeDt[1:]      
            
    return pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                           '매도일자','매도가격','매도금액','매도비용', '손익','수익률(%)','평가금액'])   

# backtest 수행 : 초기 버전
def backtest_df(dfData
           , maxItemNum = 1           # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) 
           , cashAmt = 100000000      # 초기 투자금
           , taxRatio = 0.2           # 거래세(%)
           , expenseRatio = 0.015     # 거래수수료(%) 
           , dayMaxTradeNum = 1       # 일 최대 매수 가능 종목수
           ):  

    invItemList = []  # 투자 진행 종목의 종료일자 - 다음 투자를 위해
    simulRes = []     # 투자 결과 리스트 저장

    # input 데이터의 종목수가 분산 투자 주식 수보다 적은 경우 보정처리
    maxItemNum = min(maxItemNum, len(dfData["종목코드"].unique()))
    
    dfItemCnt = dfData.groupby("매수일자").agg( 종목수=("종목코드", "count") ).reset_index()    

    while(len(dfItemCnt) > 0):
        curDt = dfItemCnt['매수일자'][0]

        # 투자일 경과 건 투자진행 종목 리스트에서 삭제
        i = 0
        while i < len(invItemList) and invItemList[i] < curDt:
            i += 1
        if i >= 0:
            invItemList = invItemList[i:]

        # maxItemNum 개의 종목에 투자금액 1/N 분배 (이미 투자진행중인 건은 잔존 현금의 투자금액 분배 시 제외)
        ##  cashAmt가 아니라 해당 일자까지 투자한 금액, 회수한 금액을 감안한 여유 자금 재계산 필요
        dfTemp = pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                                 '매도일자','매도가격','매도금액','매도비용','현금잔액','투자손익'])    
        dfTemp = dfTemp[dfTemp['매도일자'] >= curDt]

        maxInvAmt = (cashAmt - dfTemp['매도금액'].sum() + dfTemp['매도비용'].sum()) / ( maxItemNum - len(invItemList) )

        # 해당 일자에 대한 투자 대상종목 수 계산
        curInvItemNum =  min (maxItemNum - len(invItemList), dayMaxTradeNum )

    #     print('\n', cashAmt, maxInvAmt, curInvItemNum)

        dList = dfData[dfData['매수일자']==curDt][['종목코드','종목명','매수일자','매수가격',
                                                   '매도일자','매도가격']].values.tolist()
        if len(dList) > curInvItemNum:
            random.shuffle(dList)
            dList = dList[:curInvItemNum]

        for x in dList:
            # 매입일자, 가격 구하기
            buyDt = x[2]
            buyPrice = x[3]
            # 매도일자, 가격 구하기
            sellDt = x[4]      
            sellPrice = x[5]

            #######################################################
            # 매수/매도 거래내역 만들기
            #######################################################
            
            # 주식수량
            buyCnt = int(maxInvAmt / buyPrice)

            # 매입계산
            buyAmt = buyCnt * buyPrice * (-1)
            buyExpense = int(buyAmt * expenseRatio / 100)

            # 매도계산
            sellAmt = buyCnt * sellPrice
            sellExpense = int(sellAmt * taxRatio / 100) * (-1) + int(sellAmt * expenseRatio / 100) * (-1)

            # 보유현금 계산
            deltaAmt = buyAmt + buyExpense + sellAmt + sellExpense
            cashAmt += deltaAmt
    # 
            # 매도, 매수 결과
            simulRes.append([x[0], x[1], buyCnt, buyDt, buyPrice, buyAmt, buyExpense, sellDt, sellPrice, sellAmt, sellExpense, deltaAmt, cashAmt] )

            invItemList.append(sellDt)

        invItemList.sort()

        if len(invItemList) >= maxItemNum:
            # 보유 종목 갯수가 max인 경우, 보유종목의 최초 매도일자 이후로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['매수일자'] > invItemList[0]            ] [['매수일자','종목수']].reset_index()
        else:
            # 추가 매수 가능한 경우, 다음 시그널 발생일로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['매수일자'] > dfItemCnt['매수일자'].iloc[0] ] [['매수일자','종목수']].reset_index()

    return pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                           '매도일자','매도가격','매도금액','매도비용', '손익','평가금액'])   

def backtest_report(  dfStock = []     # backtest 대상 데이터(유효기간)
                    , dfRes   = []     # backtest 결과
                    , pType   = '종가' # 거래기준 가격(시가/종가 등)
                    , prtInd = True):  
    
    # # 주식보유상태인 경우 분석기간 종료일자 종가 기준으로 가치 산정, 없는 경우 거래기준 가격으로 산정
    if '종가' in dfStock.columns: 
        pLast = '종가'
    else:
        pLast = pType

    # # 투자수익률
    invEarnRatio = dfRes.iloc[len(dfRes)-1]['평가금액'] / ( dfRes.iloc[0]['평가금액'] - dfRes.iloc[0]['손익'] ) * 100 - 100

    # # 투자건당 평균 수익률
    # invAvgEarnRatio = sum([ (-1)*x[2]/(x[0]+x[1]) for x in dfRes[['매수금액','매수비용','손익']].values.tolist() ]) * 100 / len(dfRes)
    invAvgEarnRatio = dfRes['수익률(%)'].mean()
    
    frDt = dfStock.iloc[0]['일자']
    frPrice = dfStock.iloc[0][pType]
    toDt = dfStock.iloc[len(dfStock)-1]['일자']
    toPrice = dfStock.iloc[len(dfStock)-1][pLast]
        
    # # # 기본 수익률(분석기간)
    basicEarnRatio = ( ( toPrice * 0.99785 - frPrice * 0.00015 )
                     / frPrice ) * 100 - 100 
    
    # # # 결과 display
    if prtInd:
        print('투자수익률(backtest) : ', "%7.3f"%( invEarnRatio )+'%', end='   ')
        print('( 거래건수 :', len(dfRes), ', 건당 평균 수익률 :', "%.3f"%(invAvgEarnRatio)+'% )' ) 
        print('시장수익률(분석기간) : ', "%7.3f"%( basicEarnRatio )+'%', end='   ')
        print('( 시작일기준가 :', f"{frPrice:,}", '[' + frDt + ']',        
              ', 종료일기준가 :', f"{toPrice:,}", '[' + toDt + '] )') 

    val = []; colNm = []
    for x in ['종목코드', '종목명']:
        if x in dfStock.columns: 
            colNm.append(x)
            val.append(dfStock.iloc[0][x])

    return pd.DataFrame([val+[frDt, toDt, frPrice, toPrice, basicEarnRatio, invEarnRatio, len(dfRes), invAvgEarnRatio]]
               ,columns=colNm+['시작일자','종료일자','시작일기준가','종료일기준가','시장수익률','투자수익률','거래건수','거래당수익률'])


def get_earn_ratio(dfData):
    earn_ratio = 100
                   
    for i in range(len(dfData)):
        earn_ratio *= (dfData['매도가격'].iloc[i] / dfData['매수가격'].iloc[i])

    return (earn_ratio - 100)


def getMarketIndex(indexNm, daysForSignChange=1, indexGrowthSign='B'):
    # 일별 마켓지수 데이터 read (BDI지수, 달러환율, 금/원유 가격 등)
    dfIndex = i_mi.MarketIndex(indexNm)

    # (국내외)일별 마켓지수 데이터와 일별 주가 정보간 거래일자 불일치 건 매핑을 위해 
    # 일별 마켓지수 365일 데이터 생성 (누락된 일자는 전일자 기준으로 생성)
    dfIndex = func.makeFullDayData(dfIndex)

    # 일별 마켓지수 변동 값을 계산하여 diff 컬럼에 생성 (1)
    dfIndex = func.addDiffValue(dfIndex, indexNm)

    # 일별 마켓지수(예, BCI지수) 증감('diff')에 따른 Signal 생성 
    # 연속으로 (daysForSignChange)일 이상인 경우 매수/매도 시그널 생성
    #     indexGrowthSign : 지수가 오를 때 신호  (defualt : 'B')
    #                      - 'B'(매수) : 예) 운임지수, 인구 등 
    #                      - 'S'(매도) : 예) 인건비, 유가, 환율 등 
    #     daysForSignChange : 매수/매도 사인이 바뀌기 위해 필요한 연속 증가(감소) 일수 (default : 1)
    return bs.get_signal_by_zero_crossing(dfIndex, daysForSignChange=daysForSignChange, indexGrowthSign=indexGrowthSign) 


def index_backtest(shCode='', indexNm='', pType='종가', frDt='19960101', toDt='20991231'
                    , indexGrowthSign='B'       # 시장지수가 오를 때 매수(B)/매도(S) 신호 (defualt : 'B')
                    , daysForSignChange=1       # 매수/매도 사인 발생하기 위해 필요한 시장지수 연속 증가(감소) 일수 (default : 1)
                    , addDays=-1                # 선행일수 반영. 예) -1(1일전), 0(당일) 시장지수를 활용하여 매매(양수는 의미없음)
                    , max_retention_days = 9999 # S(매도) 사인이 발생하기 전이라도 (max_retention_days)일 이후 매도 처리
                    , multiRetentionInd = False # 매수(B) 이후 매도(S) 전 추가 매수(B) 발생 여부 (default : False)
                    , maxItemNum = 1            # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) (default : 1)
                                                # backtest 대상 종목수 이내 설정 가능(큰 경우 자동보정처리)
                    , cashAmt = 100000000       # 초기 투자금 (default : 1억)
                    , taxRatio = 0.2            # 거래세(%) (default : 0.2)
                    , expenseRatio = 0.015      # 거래수수료(%) (default : 0.015) 
                    , dayMaxTradeNum = 1        # 일 최대 매수 가능 종목수 (default : 1)      
                    , procTyp = '순차'          # 순차/병렬 처리             
                   ):
   
    shCodeList = code.getShcodeList(shCode)[['종목코드','종목명','상장일']].values.tolist()
    rLen = len(shCodeList)    
    if rLen > 1: 
        print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석시작 (' + indexNm + ')')  
    
    retType = 'SUM' if rLen > 1 else 'DET'
    
    dfZeroCross = getMarketIndex(indexNm, daysForSignChange=daysForSignChange, indexGrowthSign=indexGrowthSign)
    
    if procTyp == '병렬' and rLen >= 100:
        from  . import parallel
        dfRet = parallel._getIndexBacktestParallel(shCodeList, indexNm, pType, frDt, toDt, addDays, max_retention_days, 
                                                   multiRetentionInd, maxItemNum, cashAmt, taxRatio, expenseRatio, dayMaxTradeNum, 
                                                   dfZeroCross, retType, rLen)
    else:
        dfRes, dfReport, dfMerge, dfRet = _getIndexBacktestSingle(shCodeList, indexNm, pType, frDt, toDt, addDays, max_retention_days,
                                                                  multiRetentionInd, maxItemNum, cashAmt, taxRatio, expenseRatio, 
                                                                  dayMaxTradeNum, dfZeroCross, retType, rLen)

    if rLen > 1: 
        print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석종료 (' + indexNm + ')')  
        
    if  retType == 'SUM':
        return dfRet
    else:
        return dfRes, dfReport, dfMerge

def _getIndexBacktestSingle(shCodeList, indexNm, pType, frDt, toDt, addDays, max_retention_days, multiRetentionInd, maxItemNum, 
                            cashAmt, taxRatio, expenseRatio, dayMaxTradeNum, dfZeroCross, retType, rLen):
    dfRet = pd.DataFrame([])    
    for idx, [xCode, shName, listDt ] in enumerate(shCodeList):
        sDt = max(frDt, listDt) # 코스피/코스닥 상장 이후 거래내역만 처리 (코넥스 -> 코스닥 등)
        dfRes, dfReport, dfMerge = _index_backtest(shCode=xCode, indexNm=indexNm, pType=pType, frDt=sDt, toDt=toDt
                                        , addDays=addDays , max_retention_days = max_retention_days 
                                        , multiRetentionInd = multiRetentionInd, maxItemNum = maxItemNum          
                                        , cashAmt = cashAmt, taxRatio = taxRatio, expenseRatio = expenseRatio     
                                        , dayMaxTradeNum = dayMaxTradeNum     
                                        , dfZeroCross = dfZeroCross
                                        , retType = retType )        
            
        if  retType == 'SUM':
            dfRet = pd.concat([dfRet, dfReport])
            print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx+1, '/', rLen, xCode, shName, ' '*10, end='')
            
    return dfRes, dfReport, dfMerge, dfRet

def _index_backtest(shCode='', indexNm='', pType='종가', frDt='19960101', toDt='20991231'
                    , addDays=-1                # 선행일수 반영. 예) -1(1일전), 0(당일) 시장지수를 활용하여 매매(양수는 의미없음)
                    , max_retention_days = 9999 # S(매도) 사인이 발생하기 전이라도 (max_retention_days)일 이후 매도 처리
                    , multiRetentionInd = False # 매수(B) 이후 매도(S) 전 추가 매수(B) 발생 여부 (default : False)
                    , maxItemNum = 1            # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) (default : 1)
                                                # backtest 대상 종목수 이내 설정 가능(큰 경우 자동보정처리)
                    , cashAmt = 100000000       # 초기 투자금 (default : 1억)
                    , taxRatio = 0.2            # 거래세(%) (default : 0.2)
                    , expenseRatio = 0.015      # 거래수수료(%) (default : 0.015) 
                    , dayMaxTradeNum = 1        # 일 최대 매수 가능 종목수 (default : 1)      
                    , dfZeroCross = []
                    , retType = 'SUM'
                    ):
    
    prtInd = False if retType == 'SUM' else True
    
    dfStock = stockInfo.getValidTradeInfo(shCode, frDt, toDt)
    
    # 데이터병합(일별주가 + Signal) 및 선행일수 반영
    dfMerge = bs.mergeStockSignal(dfStock, dfZeroCross, addDays=addDays)
    # 일별 마켓지수 변동 값을 계산하여 diff 컬럼에 생성 (2). 병합으로 인해 누락된 이력에 대한 diff 보정 처리
    dfMerge = func.addDiffValue(dfMerge, indexNm)

    # backtest 수행을 위해 매수/매도 시그널 및 기준가격(종가 등) 확정
    #     max_retention_days : S(매도) 사인이 발생하기 전이라도 (max_retention_days)일 이후 매도 처리
    #     multiRetentionInd : 매수(B) 이후 매도(S) 전 추가 매수(B) 발생 여부 (default : False)
    dfSetSignal = bs.set_signal(dfMerge, pType = pType, max_retention_days = max_retention_days, multiRetentionInd = multiRetentionInd)

    # # backtest 수행 
    if len(dfSetSignal) > 0:
        dfRes = bt.backtest(dfSetSignal
                    , maxItemNum = maxItemNum          # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) (default : 1)
                                                    # backtest 대상 종목수 이내 설정 가능(큰 경우 자동보정처리)
                    , cashAmt = cashAmt                # 초기 투자금 (default : 1억)
                    , taxRatio = taxRatio              # 거래세(%) (default : 0.2)
                    , expenseRatio = expenseRatio      # 거래수수료(%) (default : 0.015) 
                    , dayMaxTradeNum = dayMaxTradeNum  # 일 최대 매수 가능 종목수 (default : 1)
                    )

        #  투자수익률 구하기
        dfReport = bt.backtest_report(dfStock = dfMerge # backtest 대상 데이터(유효기간) 
                                    , dfRes   = dfRes  # backtest 결과
                                    , pType   = pType
                                    , prtInd  = prtInd)      # 시가/종가    
    else:
        dfRes = pd.DataFrame([]) 
        dfReport = pd.DataFrame([]) 
    
    return dfRes, dfReport, dfMerge
    
    
# def backtest_infinite_purchase(dfStock, splitCnt = 40, invAmt = 100000000, settlePct=10, market='KOR'):
#     def priceLimit(Price):
#         def TickSize(Price):
#             if   Price  <   2000:       TickSize =    1
#             elif Price  <   5000:       TickSize =    5
#             elif Price  <  20000:       TickSize =   10
#             elif Price  <  50000:       TickSize =   50
#             elif Price  < 200000:       TickSize =  100
#             elif Price  < 500000:       TickSize =  500
#             else:                       TickSize = 1000

#             return TickSize
#         tick = TickSize(Price)

#         return math.ceil(Price/tick) * tick 
    
#     resList = []
#     poolAmt = invAmt               # 보유현금          
#     remainCnt = splitCnt * 2       # 남은 회차
#     tradeAmt = poolAmt / remainCnt # daily 매수금
#     buyCntTot = 0                  # 총매수개수
#     buyAmtTot = 0                  # 총매수금
#     avgBuyPrice = 0                # 평단가

#     for idx, [dt, hPrice, ePrice] in enumerate(dfStock[['일자','고가','종가']].values.tolist()):
#         if remainCnt == 0 or buyCntTot > 0 and (avgBuyPrice*(1 + settlePct/100)) <= hPrice:
#             if buyCntTot > 0 and (avgBuyPrice*(1 + settlePct/100)) <= hPrice:
#                 if market == 'KOR':
#                     sellPrice = priceLimit( avgBuyPrice*(1 + settlePct/100) )
#                 else:
#                     ## 미국은 소수점 달러 단위 거래
#                     sellPrice = avgBuyPrice*(1 + settlePct/100)
#             else:
#                 sellPrice = ePrice

#             poolAmt  += (sellPrice * buyCntTot)
#             buyCntTot = 0
#             buyAmtTot = 0        
#             remainCnt = splitCnt * 2
#             tradeAmt = poolAmt / remainCnt

#         # 첫 거래 시
#         if buyCntTot == 0 or remainCnt >= 2 and ePrice <= avgBuyPrice:
#             buyTryCnt = 2
#         else:
#             buyTryCnt = 1

#         if buyCntTot == 0:                   # 매수건수
#             buyCnt = int(tradeAmt / ePrice)
#         else:
#             buyCnt = int(tradeAmt / buyTryCnt / ePrice) * buyTryCnt

#         buyAmt = ePrice * buyCnt             # 매수금        
#         buyCntTot += buyCnt                  # 총매수개수
#         buyAmtTot += buyAmt                  # 총매수금

#         if buyCntTot > 0:
#             avgBuyPrice = buyAmtTot / buyCntTot 
#             remainCnt -= buyTryCnt        
#             poolAmt -= buyAmt
#         else:
#             avgBuyPrice = None

#         resList.append([dt, hPrice, ePrice, buyCnt, buyAmt, buyCntTot, buyAmtTot, avgBuyPrice, buyCntTot*ePrice,
#                         poolAmt, buyCntTot*ePrice + poolAmt, remainCnt/2  ])        
        
        
#     columns = ['일자','고가','종가','매수건수','매수금','총매수개수','총매수금','평균단가','주식평가금','보유현금','총자산','잔여회차']        
#     return  pd.DataFrame(resList, columns=columns)     


def loc_split_trading(dfStock, invAmt = 100000000, splitCnt=2, stocktPct=50, downPct = 0, upPct = 0):   
    resList = []
    buyCnt = 0                               # 분할구매 회차
    rebalAmt = int(invAmt * (1 - stocktPct/100))  # 리밸런싱금액 
    holdAmt = invAmt - rebalAmt        # 투자가능현금     
    holdStockCnt = 0                         # 보유주식수

    if len(dfStock) > 0:
        for idx, [dt, ePrice] in enumerate(dfStock[['일자', '종가']].values.tolist()):
            if idx == 0:
#                 stockTradeVol = math.trunc(holdAmt / splitCnt / ePrice) 
                stockTradeVol = 0
            elif ePriceLast == ePrice:
                stockTradeVol = 0
            elif ePriceLast * (1 + upPct/100) <= ePrice and buyCnt > 0:
                stockTradeVol = math.trunc(holdStockCnt / buyCnt) * -1
            elif ePriceLast * (1 + downPct/100) >= ePrice and buyCnt < splitCnt:
                stockTradeVol = math.trunc(holdAmt / (splitCnt-buyCnt) / ePrice) 
            else:
                stockTradeVol = 0                
                
            buyCnt += (1 if stockTradeVol > 0 else -1 if stockTradeVol < 0 else 0)

            holdStockCnt += stockTradeVol
            holdAmt = round(holdAmt - stockTradeVol * ePrice,6)

            ## 세금은 추후 반영
            if holdStockCnt == 0:
                invAmt = rebalAmt + holdAmt
                rebalAmt = int(invAmt * (1 - stocktPct/100))  # 리밸런싱금액 
                holdAmt = round(invAmt - rebalAmt, 6)         # 투자가능현금
            evalAmt = round(holdAmt + holdStockCnt * ePrice + rebalAmt, 6)
#             holdAmt = max(evalAmt * stocktPct/100 - holdStockCnt * ePrice, 0)
#             rebalAmt = evalAmt - holdAmt - holdStockCnt * ePrice
            
            chgPct = None if idx == 0 else ePrice/ePriceLast*100 - 100
        
            ePriceLast = ePrice

            resList.append([dt, ePrice, chgPct, stockTradeVol, holdStockCnt, holdAmt, rebalAmt, evalAmt, buyCnt])                
        
    columns = ['일자','종가', '변동률', '매매주식수', '보유주식수','매수가능현금','보유현금','총자산', '분할회차']        
    return  pd.DataFrame(resList, columns=columns)     


# def loc_infinite_purchase(dfStock, splitCnt = 40, invAmt = 100000000, settlePct=10, initPct=100, market='KOR'):
#     def priceLimit(Price):
#         def TickSize(Price):
#             if   Price  <   2000:       TickSize =    1
#             elif Price  <   5000:       TickSize =    5
#             elif Price  <  20000:       TickSize =   10
#             elif Price  <  50000:       TickSize =   50
#             elif Price  < 200000:       TickSize =  100
#             elif Price  < 500000:       TickSize =  500
#             else:                       TickSize = 1000

#             return TickSize
#         tick = TickSize(Price)

#         return math.ceil(Price/tick) * tick 
    
#     resList = []
#     poolAmt = invAmt               # 보유현금          
#     remainCnt = splitCnt * 2       # 남은 회차
#     buyCntTot = 0                  # 총매수개수
#     buyAmtTot = 0                  # 총매수금
#     avgBuyPrice = 0                # 평단가

#     for idx, [shCode, dt, hPrice, ePrice] in enumerate(dfStock[['종목코드','일자','고가','종가']].values.tolist()):
        
#         if remainCnt > 0:
#             tradeAmt = poolAmt / remainCnt       # daily 매수금    
#         else:            
#             tradeAmt = None
    
#         if buyCntTot > 0:
#             # 매수회차 소진 시 익일 종가로 initPct 비율 매도
#             if remainCnt == 0:
#                 buyCnt = 0                   # 매수건수
#                 buyPrice = 0                 # 매수가
                
#                 sellCnt = int(buyCntTot * initPct / 100)  # 매도건수
#                 sellPrice = ePrice           # 매도가
#                 buyAmtTot = buyAmtTot * (1 - initPct/100)   # 총매수금  
#                 remainCnt = math.ceil(splitCnt * 2 * initPct / 100)    # 잔여회차            
            
#             # 잔여 회차 내 매수(loc) 진행 + 매도(장중 익절가 도달 시 보유주식 익절)
#             else:                       
#                 if avgBuyPrice > ePrice:
#                     buyTryCnt = min(remainCnt, 2)
#                 else:
#                     buyTryCnt = 1
                
#                 if tradeAmt == None:
#                     print(shCode, dt, hPrice, ePrice, remainCnt, tradeAmt, buyTryCnt)
#                 buyCnt = int(tradeAmt / ePrice) * buyTryCnt                
                    
#                 buyPrice = ePrice
                    
#                 if (avgBuyPrice*(1 + settlePct/100)) <= hPrice:
#                     if market == 'KOR':
#                         sellPrice = priceLimit( avgBuyPrice*(1 + settlePct/100) )
#                     else:
#                         ## 미국은 소수점 달러 단위 거래
#                         sellPrice = math.ceil( avgBuyPrice*(1 + settlePct/100) *100) / 100
#                 else:
#                     sellPrice = 0
                
#                 if sellPrice > 0:
#                     sellCnt = buyCntTot
#                     remainCnt = splitCnt * 2       # 남은 회차
#                     buyAmtTot = 0        
#                 else:
#                     sellCnt = 0
                    
#                 if buyCnt > 0:
#                     remainCnt -= buyTryCnt
#         else:              
#             buyCnt = int(tradeAmt / ePrice) * 2
#             buyPrice = ePrice
#             sellCnt = 0
#             sellPrice = 0             
#             if buyCnt > 0:
#                 remainCnt -= 2
            
#         buyAmt  = buyCnt * buyPrice     # 매수금            
#         sellAmt = sellCnt *sellPrice    # 매도금       
#         buyCntTot += (buyCnt - sellCnt) # 보유개수
#         buyAmtTot += buyAmt             # 총매수금
#         poolAmt += (sellAmt - buyAmt)   # 보유현금                        

#         if buyCntTot > 0:
#             avgBuyPrice = buyAmtTot / buyCntTot 
#         else:
#             avgBuyPrice = None        

#         resList.append([dt, hPrice, ePrice, buyCnt, buyPrice, buyAmt, sellCnt, sellPrice, sellAmt, 
#                         buyCntTot, buyAmtTot, avgBuyPrice, buyCntTot*ePrice,
#                         poolAmt, buyCntTot*ePrice + poolAmt, remainCnt/2  ])        
        
        
#     columns = ['일자','고가','종가','매수건수','매수가', '매수금','매도건수', '매도가','매도금', '보유개수','총매수금','평균단가','주식평가금','보유현금','총자산','잔여회차'] 
#     return  pd.DataFrame(resList, columns=columns)     

def loc_infinite_purchase(dfStock, splitCnt = 40, invAmt = 100000000, settlePct=10, initPct=100, market='KOR'):    
    resList = []
    poolAmt = invAmt               # 보유현금          
    remainCnt = splitCnt * 2       # 남은 회차
    buyCntTot = 0                  # 총매수개수
    buyAmtTot = 0                  # 총매수금
    avgBuyPrice = 0                # 평단가    

    for idx, [shCode, dt, ePrice] in enumerate(dfStock[['종목코드','일자','종가']].values.tolist()):
            
        buyCnt = 0; buyPrice = 0; sellCnt = 0; sellPrice = 0; tradeAmt = 0; buyTryCnt = 0
        
        # 잔여 회차 내 매수(loc) 진행 
        if remainCnt > 0:
            tradeAmt = poolAmt / remainCnt       # daily 매수금    
            
            if avgBuyPrice > ePrice:
                buyTryCnt = min(remainCnt, 2)
            else:
                buyTryCnt = 1

            buyCnt = int(tradeAmt / ePrice) * buyTryCnt                                    
            buyPrice = ePrice       
                
        if buyCntTot > 0:
            # 매도(LOC 익절가 도달 시 보유주식 익절)
            if (avgBuyPrice*(1 + settlePct/100)) <= ePrice:
                sellPrice = ePrice
                sellCnt   = buyCntTot
                remainCnt = splitCnt * 2       # 남은 회차
                buyAmtTot = 0                    
            # 매수회차 소진 시 익일 종가로 initPct 비율 매도
            elif remainCnt == 0:
                remainCnt = int(splitCnt * 2 * initPct / 100)      # 잔여회차                
                sellCnt = int(buyCntTot * remainCnt/(splitCnt*2))  # 매도건수
                sellPrice = ePrice                                 # 매도가
                buyAmtTot = buyAmtTot * (1 - remainCnt/(splitCnt*2))     # 총매수금                     
                          
        else:              
            buyCnt = int(tradeAmt / ePrice) * 2
            buyPrice = ePrice         
            buyTryCnt = 2
            
        if buyCnt > 0:
            remainCnt -= buyTryCnt                  
        
            
        buyAmt  = buyCnt * buyPrice     # 매수금            
        sellAmt = sellCnt * sellPrice   # 매도금       
        buyCntTot += (buyCnt - sellCnt) # 보유개수
        buyAmtTot += buyAmt             # 총매수금
        poolAmt = round(poolAmt + sellAmt - buyAmt, 8)   # 보유현금                        

        if buyCntTot > 0:
            avgBuyPrice = buyAmtTot / buyCntTot 
        else:
            avgBuyPrice = 0        

        resList.append([dt, ePrice, buyCnt, buyPrice, buyAmt, sellCnt, sellPrice, sellAmt, 
                        buyCntTot, buyAmtTot, avgBuyPrice, buyCntTot*ePrice,
                        poolAmt, buyCntTot*ePrice + poolAmt, remainCnt/2  ])        
        
    columns = ['일자','종가','매수건수','매수가', '매수금','매도건수', '매도가','매도금', '보유개수','총매수금','평균단가','주식평가금','보유현금','총자산','잔여회차'] 
    return  pd.DataFrame(resList, columns=columns)     