import pandas    as pd
import datetime  as  dt
from   scipy    import stats

XNOR = lambda x,y: 1 if (x>0 and y>0) or (x<0 and y<0) else 0
XOR  = lambda x,y: 1 if (x>0 and y<0) or (x<0 and y>0) else 0

ADDDAYS = lambda x,y: dt.datetime.strftime(dt.datetime.strptime(x, '%Y%m%d') + dt.timedelta(days = y), '%Y%m%d') 


# # 선행 일자 반영을 위해 분석대상기간 전후로 조정일수만큼 추가 조회를 하기 위한 날짜 조정
# def getAdjustDt(sDate, eDate, period='일', addDays=0):    
#     if addDays != 0:
#         frAdj = 0; toAdj = 0
#         if addDays < 0:
#             frAdj = -1 + addDays
#         elif addDays > 0:
#             toAdj = 1 + addDays
#         if period=='일':        
#             sDate = dt.datetime.strptime(sDate, '%Y%m%d') + dt.timedelta(weeks = frAdj)
#             eDate = dt.datetime.strptime(eDate, '%Y%m%d') + dt.timedelta(weeks = toAdj)
        
#     return [sDate, eDate]

def getISOWeeks(sDate='20000101', eDate='20991231', addDays=0):
    sDate = max(sDate, '20000101')
    eDate = min(eDate, dt.datetime.strftime(dt.datetime.now(), '%Y%m%d'))

    # 속도향상을 위해 일자별 해당년도 n주차를 먼저 구한 후 분석대상 데이터와 조인
    #   - ISO 기준 약 3,000건에 대해 기준년, 주차 계산 시 0.1초 소요
    #   - 미리 계산해서 join하는데 0.01초 소요 
    frAdj = 0; toAdj = 0
    if addDays < 0:
        frAdj = -1 + addDays
    elif addDays > 0:
        toAdj = 1 + addDays
        
    frDt = dt.datetime.strptime(sDate, '%Y%m%d') + dt.timedelta(weeks = frAdj)
    toDt = dt.datetime.strptime(eDate, '%Y%m%d') + dt.timedelta(weeks = toAdj)

    listWeeks = [[dt.datetime.strftime(x, '%Y%m%d'), dt.datetime.strftime(x, '%G%V') ] for x in pd.date_range(frDt, toDt)]
    return pd.DataFrame(listWeeks,columns=['일자','년주차'])


def addPeriodGrp(df, colNm, dfWeeks=[], period='주', sDate='20000101', eDate='20991231', addDays=0): 
    grpBtColNm = '년주차' if period == '주' else '년월' if period == '월' else '분기' if period == '분기' else '년도'  if period == '년' else '일자' 
    
    if period != '일':
        if period == '주':
            if len(dfWeeks) == 0:
                dfWeeks = getISOWeeks(sDate, eDate, addDays)
            df = df.merge(dfWeeks)
        elif period == '월':
            df['년월'] = df['일자'].apply(lambda x: x[:6])
        elif period == '분기':
            df['분기'] = df['일자'].apply(lambda x: x[:4] + '1Q' if x[4:6] <= '03' else '2Q' if x[4:6] <= '06' else '3Q' if x[4:6] <= '09' else '4Q')
        elif period == '년':
            df['년도'] = df['일자'].apply(lambda x: x[:4])
            
        df = df.groupby(grpBtColNm).agg({colNm:"mean"}).reset_index()
        
    if addDays != 0: 
        df[colNm + grpBtColNm] = df[grpBtColNm]  
        df[grpBtColNm] = df[grpBtColNm].shift(addDays) 
        df = df.dropna()[[grpBtColNm,colNm + grpBtColNm,colNm]]
    
    return df

# 일/주/월/분기/년 평균 데이터를 구하고 선행 기준에 의해 병합
# 상관계수 값 구한 후 반환
# def mergeAdvance(df1, colNm1, df2, colNm2, sDate='20000101', eDate='20991231', addDays=0, period='일', dfWeeks=[]):
#     sDate = max(sDate, '20000101')
#     eDate = min(eDate, dt.datetime.strftime(dt.datetime.now(), '%Y%m%d'))        

#     if df1['일자'].iloc[0] < sDate or eDate < df1['일자'].iloc[len(df1)-1]:
#         df1 = df1.query("'"+sDate+"' <= 일자 and 일자 <= '"+eDate+"'")
    
#     if period == '일':
#         df2[colNm2+'일자'] = df2['일자']    
#         df2['일자'] = df2.apply(lambda x: ADDDAYS(x['일자'], -addDays), axis=1)        
#         dfMerge = df1.merge(df2)[['일자', colNm1, colNm2+'일자', colNm2]]
#     else:
#         df1 = addPeriodGrp(df1, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=addDays)
#         df2 = addPeriodGrp(df2, dfWeeks=dfWeeks, period=period, sDate=sDate, eDate=eDate, addDays=addDays)
        
#         grpBtColNm = '년주차' if period == '주' else '년월' if period == '월' else '분기' if period == '분기' else '년도' 
#         df1 = df1.groupby(grpBtColNm).agg({colNm1:"mean"}).reset_index()
#         df2 = df2.groupby(grpBtColNm).agg({colNm2:"mean"}).reset_index()
        
#         df2[colNm2+grpBtColNm] = df2[grpBtColNm]
#         df2[grpBtColNm] = df2[grpBtColNm].shift(addDays)    
        
#         dfMerge = pd.merge(df1, df2)[[grpBtColNm,colNm1,colNm2+grpBtColNm,colNm2]]        
        
#     return dfMerge.dropna()            


# (국내외)일별 마켓지수 데이터와 일별 주가 정보간 거래일자 불일치 건 매핑을 위해 
# 일별 마켓지수 365일 데이터 생성 (누락된 일자는 전일자 기준으로 생성)
def makeFullDayData(df, eDate=''):
    column_list = [col_nm for col_nm in df.columns if col_nm != '일자']
    dfList = df[['일자']+column_list].values.tolist()
    sDate = dfList[0][0]
    if len(eDate) == 0:
        eDate = dfList[len(dfList)-1][0]

    # 변수 초기화
    resData = []
    dfIdx = 0

    for x in pd.date_range(sDate, eDate):        
        cDate = dt.datetime.strftime( x, '%Y%m%d')

        if cDate == dfList[dfIdx][0]:
            lastVal = dfList[dfIdx][1:]
            # dfIdx += 1
            if dfIdx < len(dfList) - 1:
                dfIdx += 1            

        resData.append([cDate] + lastVal)

    return pd.DataFrame(resData, columns = ['일자']+column_list)


def CalcCorrRelation(vList1, vList2, rptGb='기본'):
    vList1 = [float(x) if (type(x) == str and '.' in x) else (int(x) if (type(x) == str)  else x) for x in vList1]
    vList2 = [float(x) if (type(x) == str and '.' in x) else (int(x) if (type(x) == str)  else x) for x in vList2]
    recCnt = len(vList1)   
    
    if recCnt >= 5:    
        resData = [recCnt]
        if rptGb in ['기본', '전체']:
            corVal = stats.pearsonr(vList1, vList2)         
            resData += [corVal[0], corVal[1]] 
            
        if rptGb in ['증감', '전체']:
            deltaList1 = [vList1[i] - vList1[i-1] for i in range(1, recCnt)]
            deltaList2 = [vList2[i] - vList2[i-1] for i in range(1, recCnt)]

            corVal = stats.pearsonr(deltaList1, deltaList2) 

            resData += [corVal[0], corVal[1],
                        sum([XNOR(deltaList1[i],deltaList2[i]) for i in range(recCnt-1)])/(recCnt-1),
                        sum([XOR(deltaList1[i],deltaList2[i]) for i in range(recCnt-1)])/(recCnt-1)
                        ]
    else:
        resData = []
    
    return resData

def _MakeSignal(df, colNm, indexGrowthSign='B', consecutiveCntForSignChange=1):
    
    """
    indexGrowthSign : 지수가 오를 때 신호  
      - B(매수) : 예) 운임지수, 인구 등
      - S(매도) : 예) 인건비, 유가, 환율 등 
    consecutiveCntForSignChange : 매수/매도 사인이 바뀌기 위해 필요한 연속 증가(감소) 일수
    """
    
    # 변수 초기화
    resData = []

    signal = 'S'
    plusConsecutiveCnt = 0
    minusConsecutiveCnt = 0
    
    for idx, curVal in enumerate(df['colNm'].values.tolist()):          
        if idx > 0:

            if lastVal < curVal:
                plusConsecutiveCnt  += 1
                minusConsecutiveCnt  = 0
            elif lastVal > curVal:
                plusConsecutiveCnt   = 0
                minusConsecutiveCnt += 1                
            
            # 특정 일수 이상 index 수치가 연속 증가 시 SELL -> BUY
            if   indexGrowthSign == 'B' and signal == 'S' and plusConsecutiveCnt  >= consecutiveCntForSignChange :
                signal = 'B'
            # 특정 일수 이상 index 수치가 연속 감소 시 BUY -> SELL
            elif indexGrowthSign == 'B' and signal == 'B' and minusConsecutiveCnt >= consecutiveCntForSignChange :
                signal = 'S'
            # 특정 일수 이상 index 수치가 연속 증가 시 BUY -> SELL
            elif indexGrowthSign == 'S' and signal == 'B' and plusConsecutiveCnt  >= consecutiveCntForSignChange :
                signal = 'S'
            # 특정 일수 이상 index 수치가 연속 감소 시 SELL -> BUY
            elif indexGrowthSign == 'S' and signal == 'S' and minusConsecutiveCnt >= consecutiveCntForSignChange :
                signal = 'B'                             
            
            # if   indexGrowthSign == 'B' and lastVal < curVal and signal == 'S' :
            #     signal = 'B'
            # elif indexGrowthSign == 'B' and lastVal > curVal and signal == 'B' :
            #     signal = 'S'
            # elif indexGrowthSign == 'S' and lastVal < curVal and signal == 'B' :
            #     signal = 'S'
            # elif indexGrowthSign == 'S' and lastVal > curVal and signal == 'S' :
            #     signal = 'B'                    
            
        lastVal = curVal
        
        if idx > 0 and (plusConsecutiveCnt == consecutiveCntForSignChange or minusConsecutiveCnt == consecutiveCntForSignChange):
            resData.append(signal)
        else:
            resData.append('')
    
    return resData

# 전일자 대비 지정컬럼(예, BCI지수)의 증감값 계산하여 'diff' 컬럼에 생성
def addDiffValue(df, colNm):
    resData = []

    for idx, curVal in enumerate(df[colNm]):        
        if idx == 0:
            diff = 0
        else:
            diff = curVal - lastVal
        
        resData.append(diff)
            
        lastVal = curVal

    df['diff'] = resData   

    return df

def getAvgTurnAround(values=[]):
    upSignCnt = 0
    upDatCnt = 0
    downSignCnt = 0
    downDataCnt = 0
    sign = '0'
    
    for i in range(len(values)-1):
        if sign == '+':
            if values[i] <= values[i+1]:
                upDatCnt += 1
            else:
                sign = '-'
                downSignCnt += 1
                downDataCnt += 1                     
        elif sign == '-':
            if values[i] >= values[i+1]:
                downDataCnt += 1
            else:
                sign = '+'
                upSignCnt += 1
                upDatCnt += 1            
        elif sign == '0':
            if values[i] < values[i+1]:
                sign = '+'
                upSignCnt += 1
                upDatCnt += 1
            elif values[i] > values[i+1]:
                sign = '-'
                downSignCnt += 1
                downDataCnt += 1         
                
    #  avgPeriod, upPeriod, downPeriod              
    return (upDatCnt + downDataCnt)/(upSignCnt + downSignCnt), upDatCnt/upSignCnt, downDataCnt/downSignCnt

def get_avg_updown_period(dfStock):   
    upList = []
    downList = []
    
    columns=['상승일수','상승기간수','하락일수','하락기간수','평균상승일수','평균하락일수','평균변동일수','최대상승일수','최대하락일수']
    if '종목코드' in dfStock.columns:
        columns = ['종목코드'] + columns    
    
    for idx, [dt, ePrice] in enumerate(dfStock[['일자', '종가']].values.tolist()):
        if idx == 0:
            lstSign = 'None'            
        else:
            if ePriceLast != ePrice:
                if ePriceLast < ePrice:
                    if lstSign != 'UP':
                        accumDays = 1
                        lstSign = 'UP'
                    else:
                        accumDays += 1                    
                elif ePriceLast > ePrice:
                    if lstSign != 'DOWN':
                        accumDays = -1
                        lstSign = 'DOWN'
                    else:
                        accumDays -= 1
                
                if accumDays > 0:
                    upList.append(accumDays)
                else:
                    downList.append(accumDays)
                
        ePriceLast = ePrice
   
    upDays = len(upList)                # 상승한 일수
    upPeriodCnt = upList.count(1)       # 상승기간 수
    downDays = len(downList)            # 하락한 일수
    downPeriodCnt = downList.count(-1)  # 하락기간 수            
        
    if upDays > 0 or downDays > 0:
        resList = [ upDays, upPeriodCnt, downDays, downPeriodCnt,
                    upDays/upPeriodCnt if upPeriodCnt > 0 else None, 
                    downDays/downPeriodCnt if downPeriodCnt > 0 else None,
                    (upDays+downDays) / (upPeriodCnt+downPeriodCnt),
                    max(upList), abs(min(downList))
                  ]
        
        if '종목코드' in dfStock.columns:
            resList = [ dfStock[['종목코드']].values.tolist()[0] + resList ]
    else:
        resList = []        
        
    return pd.DataFrame(resList, columns=columns)