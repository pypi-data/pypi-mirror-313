import pandas    as pd
import datetime  as  dt
# from   ..innerIO import stockInfo  as sd
# from   ..common  import code

def MACD(df, window_fast, window_slow, window_signal, colNm='종가'):
    macd = pd.DataFrame()
    macd['일자'] = df['일자']
    macd['ema_fast'] = df[colNm].ewm(span=window_fast).mean()
    macd['ema_slow'] = df[colNm].ewm(span=window_slow).mean()
    macd['macd'] = macd['ema_fast'] - macd['ema_slow']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    
    return macd


# 전일자 대비 마켓지수(예, BCI지수) 등의 증감값('diff')이
# 연속으로 (daysForSignChange)일 이상인 경우 매수/매도 시그널 생성
def get_signal_by_zero_crossing(dfData, indexGrowthSign='B', daysForSignChange=1):    
    """
    indexGrowthSign : 지수가 오를 때 신호  
                     - B(매수) : 예) 운임지수, 인구 등
                     - S(매도) : 예) 인건비, 유가, 환율 등 
    daysForSignChange : 매수/매도 사인이 바뀌기 위해 필요한 연속 증가(감소) 일수
    """
    plusConsecutiveCnt = 0
    minusConsecutiveCnt = 0    

    sig_list = []

    for diff in dfData['diff'].values:
        if diff > 0:
            plusConsecutiveCnt  += 1
            minusConsecutiveCnt  = 0    
        elif diff < 0:
            plusConsecutiveCnt   = 0
            minusConsecutiveCnt += 1                
        
        if plusConsecutiveCnt >= daysForSignChange:
            sig_list.append(indexGrowthSign)
        elif minusConsecutiveCnt >= daysForSignChange:
            sig_list.append('S' if indexGrowthSign=='B' else 'B')
        else:
            sig_list.append(None)
 
    dfData['Signal'] = sig_list
    
    return dfData

# 데이터 병합 (일별주가 + 매수/매도 Signal) 및 선행일수 반영 
def mergeStockSignal(dfStock, dfSign, addDays=0):
    """       
    addDays : (addDays)일 전 signal 참조해서 거래하도록 데이터 매핑 (default : 0)
    """    
    idxStock = 0
    idxSignal = 0    
    mergeData = []
    dfSignal = dfSign.copy()
    
    if addDays > 0:
        print("addDays는 0 또는 음수값만 선택 가능!!!")
        return
    
    # 선행일자 적용
    advance = -addDays
    if advance != 0:        
        applyDt = dfSignal['일자'].tolist()[advance:]
        curDt = applyDt[len(applyDt) - 1]
        for i in range(advance):
            applyDt.append( (dt.datetime.strptime(curDt, "%Y%m%d") + dt.timedelta(days=i+1)).strftime("%Y%m%d") )
        dfSignal.rename(columns={"일자":"Signal일자"},inplace=True)
        dfSignal['일자'] = applyDt        
    
    # 일별 주가와 일별 경제 지수 merge 
    dfRes = pd.merge(dfStock, dfSignal)
    
    # 첫번째 Signal만 남기고 나머지 Signal 삭제 
    sigList = []
    lastSignal = ''
    buyCnt = 0
    
    for sign in dfRes['Signal']:
        if lastSignal != sign and ( buyCnt > 0 or sign == 'B'):
            sigList.append(sign)
            lastSignal = sign
            buyCnt += 1
        else:
            sigList.append('')
    dfRes['Signal'] = sigList
    
    return dfRes

# 당일 거래 vs 이동평균의 시가/종가, 거래량/거래대금을 비교하여 매수 시그널 생성
# 실거래시는 장종료 1시간전 수치로 판단
def get_signal_by_trade_volume(df, pType='종가', volType='거래량'
                             , maDays=1000          # 이동평균 산정기간
                             , frVolRatio = 2       # 이동평균 거래량(대금) 대비 기준일 거래량(대금)의 최소 배수
                             , toVolRatio = 999999  # 이동평균 거래량(대금) 대비 기준일 거래량(대금)의 최대 배수                             
                             , frPriceRatio  = 0.9  # 이동평균 종가(시가) 대비 기준일 종가(시가)의 최소 배수
                             , toPriceRatio  = 1):   # 이동평균 종가(시가) 대비 기준일 종가(시가)의 최대 배수

    def getBuySignal(row):
        signal = None
        
        if  ( (row['이동평균'+pType] * frPriceRatio) <= row[pType] <= (row['이동평균'+pType] * toPriceRatio) ):
            if ( (row['이동평균'+volType] * frVolRatio) <= row[volType] <= (row['이동평균'+volType] * toVolRatio) ):
                signal = 'B'
               
        return signal   

    df = df[['종목코드','종목명','일자','시가','고가','저가','종가',volType]].reset_index(drop=True)

    #-------------------------------------------------------------------------------------------
    # 3) 일별 데이터에 각각에 대해, 이전 ( maDays )개 데이터에 대한 (평균)거래대금, (평균)종가 구하기        
    #-------------------------------------------------------------------------------------------    
    df['이동평균'+pType] = df[pType].rolling(window=maDays, closed='right').mean()
    df['이동평균'+volType] = df[volType].rolling(window=maDays, closed='right').mean()        

    # NaN 데이터 제거
    df = df.dropna()
    
    if len(df) > 0:
        #---------------------------------------------------------------------------------------
        # 4) 거래대금(배수) 구간대별 매수 Signal 찾기
        #---------------------------------------------------------------------------------------        
        df['Signal'] = df.apply(lambda x: getBuySignal(x), axis=1 )
    
    return df

# backtest 수행을 위해 매수/매도 시그널 및 기준가격(종가 등) 확정
def set_signal(dfData
               , pType = '종가'              # '시가' or '종가'  
               , max_retention_days = 99999  #  S(매도) 사인이 발생하기 전이라도 최대보유일 이후 매도 처리
               , multiRetentionInd = False): #  매수(B) 이후 매도(S) 전 추가 매수(B) 발생 여부  
                                             #  예) 거래량 기반 분산 투자 시, 특정종목 매도 전까지 동일 종목 추가 매수 허용 여부
    
#     보완대상 
#             cutoffRatio = 0, # 손절 수익률 (-100 <= x <0)
#             profitRatio = 0, # 익절 수익률 (0 < x)   
    
    buy_idx = 0
    sell_idx = 0
    TRADE_CNT = len(dfData)
    last_sell_dt = '00000000'

    dfBacktestList = []
    dfBuyList = []
    dfSellList = []
    
    for idx, data in enumerate(dfData[['Signal','일자',pType]].values.tolist()):
        if data[0]=='B':
            dfBuyList.append([idx] + data[1:])
        elif data[0]=='S':
            dfSellList.append([idx] + data[1:])
    
    while( buy_idx < len(dfBuyList) ):
        buy_dt = dfBuyList[buy_idx][1]
        
        # 주식 기보유 상태에서 재구매(multiRetentionInd==true) 여부 처리 로직 적용
        if (multiRetentionInd == False) and (buy_dt <= last_sell_dt):                 
            buy_idx += 1
            continue   

        trade_idx_buy = dfBuyList[buy_idx][0]
        buy_price = dfBuyList[buy_idx][2]        
        
        # 매수일자 이후에 발생한 'S' signal 찾기
        while( (sell_idx < len(dfSellList)) and dfSellList[sell_idx][1] <= buy_dt ):      
            sell_idx += 1

        if sell_idx < len(dfSellList):  # 매수일자 이후에 S' signal 있는 경우
            trade_idx_sell = min(dfSellList[sell_idx][0], trade_idx_buy + max_retention_days) # 최대보유일 로직처리        
            sell_price = dfData[pType].iloc[trade_idx_sell]       
        else:  # 매수일자 이후에 S' signal 없는 경우
            if (trade_idx_buy + max_retention_days) <= (TRADE_CNT-1): # 최대보유일 한도에 의해 매도 처리 
                trade_idx_sell = trade_idx_buy + max_retention_days                
                sell_price = dfData[pType].iloc[trade_idx_sell]       
            else: 
                trade_idx_sell = TRADE_CNT-1
                # 매수 이후 계속 보유중인 경우 마지막 거래일 종가로 투자가치 평가
                if '종가' in dfData.columns: 
                    sell_price = dfData['종가'].iloc[trade_idx_sell]
                else:
                    sell_price = dfData[pType].iloc[trade_idx_sell]

        sell_dt = dfData['일자'].iloc[trade_idx_sell]

        dfBacktestList.append([dfData['종목코드'].iloc[0], dfData['종목명'].iloc[0], 
                               trade_idx_buy, buy_dt, buy_price, 
                               trade_idx_sell, sell_dt, sell_price, 
                               (sell_price*0.99785)/(buy_price*1.00015 )*100-100
#                                (sell_price)/(buy_price)*100-100
                              ])
        last_sell_dt = sell_dt
                
        buy_idx += 1

    return pd.DataFrame(dfBacktestList, columns=['종목코드','종목명','매수Idx','매수일자','매수가격','매도Idx','매도일자','매도가격','수익률(%)'])

# backtest 수행을 위해 매수/매도 시그널 및 기준가격(종가 등) 확정
def set_signal_20230921(dfData
               , pType = '종가'              # '시가' or '종가'  
               , max_retention_days = 99999  #  S(매도) 사인이 발생하기 전이라도 최대보유일 이후 매도 처리
               , multiRetentionInd = False): #  매수(B) 이후 매도(S) 전 추가 매수(B) 발생 여부  
    
#     보완대상 
#             cutoffRatio = 0, # 손절 수익률 (-100 <= x <0)
#             profitRatio = 0, # 익절 수익률 (0 < x)   
    
    trade_idx = 0
    buy_idx = 0
    sell_idx = 0
    TRADE_CNT = len(dfData)
    last_sell_dt = '00000000'

    dfBacktestList = []
    dfTradeList = dfData[['일자',pType,'종목코드','종목명']].sort_values('일자').values.tolist()
    dfBuyList  = dfData[dfData['Signal']=='B'][['일자','Signal']].sort_values('일자').values.tolist()
    dfSellList = dfData[dfData['Signal']=='S'][['일자','Signal']].sort_values('일자').values.tolist()
    
    while( buy_idx < len(dfBuyList) ):
        buy_dt = dfBuyList[buy_idx][0]
        buy_idx += 1
        
        # 주식 기보유 상태에서 재구매(multiRetentionInd==true) 여부 처리 로직 적용
        if (multiRetentionInd == False) and (buy_dt <= last_sell_dt):                 
            continue   

        while( (trade_idx < TRADE_CNT) and (dfTradeList[trade_idx][0] < buy_dt) ):
            trade_idx += 1

        if trade_idx >= (TRADE_CNT - 1):  # 마지막 거래일에 B 시그널 버림
            break
        elif dfTradeList[trade_idx][0] > buy_dt:
            print('(set_signal check!!) 일자 : ', dfTradeList[trade_idx][0], ' vs 시그널적용일자 : ', buy_dt)
        else:
            buy_price = dfTradeList[trade_idx][1]
            trade_idx_buy = trade_idx
            sell_dt = None

            while( (sell_idx < len(dfSellList)) and sell_dt == None ):      
                if buy_dt < dfSellList[sell_idx][0]:
                    sell_dt = dfSellList[sell_idx][0]
                else:
                    sell_idx += 1

            if sell_dt == None:
                sell_dt = dfTradeList[TRADE_CNT - 1][0]

            # 주식 최대 보유기간(max_retention_days) 로직 적용
            for i in range(trade_idx + 1, min(trade_idx + 1 + max_retention_days, TRADE_CNT)):
                if sell_dt == dfTradeList[i][0]:
                    break
            
            sell_dt = dfTradeList[i][0]
            sell_price = dfTradeList[i][1]
            trade_idx_sell = i

            dfBacktestList.append([dfTradeList[i][2], dfTradeList[i][3], 
                                   trade_idx_buy, buy_dt, buy_price, 
                                   trade_idx_sell, sell_dt, sell_price, 
                                   sell_price/buy_price*100-100])
            last_sell_dt = sell_dt

    return pd.DataFrame(dfBacktestList, columns=['종목코드','종목명','매수Idx','매수일자','매수가격','매도Idx','매도일자','매도가격','수익률(%)'])


# 미사용 버전
def set_signal_for_backtest(dfTrade, dfSignal, pType = '종가', max_retention_days = 99999, multiRetentionInd = False):
    trade_idx = 0
    buy_idx = 0
    sell_idx = 0
    TRADE_CNT = len(dfTrade)
    last_sell_dt = '00000000'

    dfBacktestList = []
    dfBuyList  = dfSignal[dfSignal['Signal']=='B'][['일자','Signal']].sort_values('일자').values.tolist()
    dfSellList = dfSignal[dfSignal['Signal']=='S'][['일자','Signal']].sort_values('일자').values.tolist()

    
    while( buy_idx < len(dfBuyList) ):
        buy_dt = dfBuyList[buy_idx][0]
        buy_idx += 1
        
        # 주식 기보유 상태에서 재구매(multiRetentionInd==true) 여부 처리 로직 적용
        if (multiRetentionInd == False) and (buy_dt <= last_sell_dt):                 
            continue   

        while( (trade_idx < TRADE_CNT) and (dfTrade['일자'].iloc[trade_idx] < buy_dt) ):
            trade_idx += 1

        if trade_idx >= (TRADE_CNT - 1):  # 마지막 거래일에 B 시그널 버림
            break
        elif dfTrade['일자'].iloc[trade_idx] > buy_dt:
            print('(check!!) 일자 : ', dfTrade['일자'].iloc[trade_idx], ' vs 시그널적용일자 : ', buy_dt)
        else:
            buy_price = dfTrade[pType].iloc[trade_idx]
            trade_idx_buy = trade_idx
            sell_dt = None

            while( (sell_idx < len(dfSellList)) and sell_dt == None ):      
                if buy_dt < dfSellList[sell_idx][0]:
                    sell_dt = dfSellList[sell_idx][0]
                else:
                    sell_idx += 1

            if sell_dt == None:
                sell_dt = dfTrade['일자'].iloc[TRADE_CNT - 1]

            # 주식 최대 보유기간(max_retention_days) 로직 적용
            for i in range(trade_idx + 1, min(trade_idx + 1 + max_retention_days, TRADE_CNT)):
                if sell_dt == dfTrade['일자'].iloc[i]:
                    break
            
            sell_dt = dfTrade['일자'].iloc[i]
            sell_price = dfTrade[pType].iloc[i]
            trade_idx_sell = i

            dfBacktestList.append([trade_idx_buy, buy_dt, buy_price, trade_idx_sell, sell_dt, sell_price, sell_price/buy_price*100-100])
            last_sell_dt = sell_dt

    return pd.DataFrame(dfBacktestList, columns=['매수Idx','매수일자','매수가격','매도Idx','매도일자','매도가격','수익률(%)'])