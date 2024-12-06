import re
import datetime
import pandas as pd
from   ..common               import code
from   ..innerIO              import stockInfo
from   dateutil.relativedelta import relativedelta

colShortSell = ['공매도거래량', '공매도거래량업틱', '공매도거래량업틱예외', '전체거래량', 
                '공매도거래량비중', '공매도거래대금', '공매도거래대금업틱', '공매도거래대금업틱예외',
                '전체거래대금', '공매도거래대금비중']
colInvestor =  ['금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금', '기타법인', '개인',
                '외국인', '기타외국인', '외국인보유수량', '외국인지분율', '외국인한도수량', 
                '외국인한도소진율', '전체주식수']
colTradeInfo = ['시가', '고가', '저가', '종가', '대비', '등락률', '거래량', '거래대금', '시가총액', 
                '상장주식수']

colFinInfo = ['종류', '종목코드', '종목명', '기준년월', '매출액', '영업이익', '영업이익발표기준', 
                '세전계속사업이익', '당기순이익', '당기순이익지배',
                '당기순이익비지배', '자산총계', '부채총계', '자본총계', '자본총계지배', '자본총계비지배',
                '자본금', '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 'CAPEX', 'FCF', '이자발생부채',
                '영업이익률', '순이익률', 'ROE', 'ROA', '부채비율', '자본유보율', 'EPS', 'PER',
                'BPS', 'PBR', '현금DPS', '현금배당수익률', '현금배당성향', '보통주식수']   
    
def inquireFinInfo(cond, dfY, dfQ):
 
    condCols = [
                [colNM, colNM[:colNM.find('_')], colNM[(colNM.find('_')+1):], ''] if colNM.count('_') == 1  else
                [colNM, colNM[:colNM.find('_')], colNM[(colNM.find('_')+1):colNM.rfind('_')], colNM[colNM.rfind('_')+1:]]            
                for colNM in [x for x in re.sub(r'[()<>=|&+-/*]', ' ', cond.strip()).split(' ') 
                              if (x not in ('', 'and', 'or', '기준년도', '분기')) and not x.isdigit() ] ]

    for idx, col in enumerate(condCols):
        if (col[1] not in colFinInfo) or (not col[2].isdigit()) or\
           not (len(col[3])==0 or len(col[3])==2 and col[3][0].isdigit() and col[3][1] == 'Q'): 
            raise Exception('유효하지 않은 컬럼명 : ' + col[0])
        else:
            dfTmp = dfY[ dfY['기준년월'].apply(lambda x: True if x[0:4] == col[2] else False) ][[
                        '종목코드', '종목명',col[1]]]  if len(col[3]) == 0 else\
                    dfQ[ dfQ['기준년월']== (col[2] + '/' + "%02d"%(int(col[3][0])*3)) ] [[
                        '종목코드','종목명',col[1]]]
            
            if len(dfTmp) == 0:
                raise Exception('데이터 없음 : ' + col[0])
            else:
                dfTmp.rename(columns={col[1]:col[0]},inplace=True)

            if idx == 0: dfNew = dfTmp
            else:        dfNew = dfNew.merge(dfTmp)

    return dfNew[dfNew.eval(cond)]

def _getPeriod(basDt, periodKnd, idx1, idx2):  
    if periodKnd == 'W':
        day = datetime.date(int(basDt[:4]), int(basDt[4:6]), int(basDt[6:]))
        wDay = day.weekday()
        frDt = day - datetime.timedelta(days = wDay)
        frDt = frDt - datetime.timedelta(days = max(idx1, idx2) * 7)

        toDt = day - datetime.timedelta(days = (min(idx1, idx2) * 7 + wDay - 6) )
    elif periodKnd == 'M':
        day = datetime.date(int(basDt[:4]), int(basDt[4:6]), 1)
        frDt = day - relativedelta(months = max(idx1, idx2))
        toDt = day - relativedelta(months = (min(idx1, idx2) -1)) - datetime.timedelta(days = 1)
    else:
        raise Exception('getPeriod > invalid periodKnd : ' + periodKnd)  

    return frDt.strftime("%Y%m%d"), toDt.strftime("%Y%m%d")        

def _getDailyData(shCode, col, basDt, dfData):
    colNmNew = col[0]
    colNm    = col[1]

    dfNew = []
    valTyp = ''

    if len(col) == 2:
        dfNew = dfData[dfData['일자']==basDt]
    elif len(col) == 3:
        if col[2].isdigit() and len(col[2]) == 8:
            dfNew = dfData[dfData['일자']==col[2]]
        elif col[2][0] == 'D' and col[2][1:].isdigit():                
            idx = dfData.index[dfData['일자']==basDt]                
            if len(idx) > 0 and (idx - int(col[2][1:])) >= 0:
                dfNew = dfData.loc[idx - int(col[2][1:])]
        else:
            raise Exception('조회 조건 오류 :' + shCode + ' ' + basDt + ' ' + colNmNew)
    elif len(col) == 4:
        if col[2][0] in ('W','M') and col[2][1:].isdigit() and col[3] in ('최대','최소','평균'):    
            frDt, toDt = _getPeriod(basDt, col[2][0], int(col[2][1:]), int(col[2][1:]))
            dfNew = dfData[(dfData['일자']>=frDt)&(dfData['일자']<=toDt)]
            valTyp = col[3]
        else:
            raise Exception('조회 조건 오류 :' + shCode + ' ' + basDt + ' ' + colNmNew)        
    elif len(col) == 5:
        if col[2][0] in ('D','W','M') and col[2][1:].isdigit() and col[2][0] == col[3][0] and \
           col[3][0] in ('D','W','M') and col[3][1:].isdigit() and col[4] in ('최대','최소','평균'):
            valTyp = col[4] 
            if col[2][0] in ('W','M'):
                frDt, toDt = _getPeriod(basDt, col[2][0], int(col[2][1:]), int(col[3][1:]))
                dfNew = dfData[(dfData['일자']>=frDt)&(dfData['일자']<=toDt)]
            else:
                idx = dfData.index[dfData['일자']==basDt]                
                minDelta = min( int(col[2][1:]) , int(col[3][1:])) 
                maxDelta = max( int(col[2][1:]) , int(col[3][1:])) 

                if len(idx) > 0 and (idx - maxDelta) >= 0:
                    dfNew = dfData.loc[idx.values[0] - maxDelta : idx.values[0] - minDelta] 
        else:
            raise Exception('조회 조건 오류 :' + shCode + ' ' + basDt + ' ' + colNmNew)    
    else:
        raise Exception('조회 조건 오류 :' + shCode + ' ' + basDt + ' ' + colNmNew)    

    if len(dfNew) == 1:
        val = dfNew[colNm].values[0]
    elif len(dfNew) > 1:
        val = dfNew[colNm].max() if valTyp == '최대' else dfNew[colNm].min() if valTyp == '최소' \
                                                     else dfNew[colNm].mean()
    else:
#         print('데이터 없음 >>', '(종목코드)', shCode, '(컬럼)', colNmNew)
        val = None

    return val


def inquireDailyData(cond, shCodes, basDt):   
    resData = []
    
    ## 조건문 파싱하여 조회에 필요한 컬럼 추출
    condCols = [ [col] + col.split('_')            
                 for col in sorted(list(set([x for x in re.sub(r'[()<>=|&+-/*]', ' ', cond.strip()).split(' ') 
                                     if (x not in ('', 'and', 'or')) and not x.isdigit() ] )) )
               ]
    ## 컬럼별 저장된 테이블(추출함수) 찾기 
    condCols = [ [ 'Short' if col[1] in colShortSell else 'Invest' if col[1] in colInvestor \
                  else 'Trade' if col[1] in colTradeInfo else '' , col ]                   
                 for col in condCols
               ]    
    for x in condCols:
        if len(x[0]) == 0:
            raise Exception('조회 조건 오류 :' + shCode + ' ' + x[1][0])      
            
    ## 조회에 필요한 테이블(추출함수) 중복 제거
    dataUnique = list(set( [ x[0] for x in condCols ] ))
     
    if len(shCodes) == 0:
        shCodes = code.StockItemList()['종목코드'].values.tolist()
    elif type(shCodes) == str:
        shCodes = [shCodes]
    elif type(shCodes) == type(pd.DataFrame([])):
        shCodes = shCodes['종목코드'].values.tolist()
        
    for idx, shCode in enumerate(shCodes):
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), shCode, idx+1, '/', len(shCodes), ' '*50, end='')
        for x in dataUnique:
            if x == 'Short':
                dfShort = stockInfo.ShortSelling(shCode)
            elif x == 'Invest':
                dfInvest = stockInfo.InvestorTradeVolume(shCode)                
            elif x == 'Trade':
                dfTrade = stockInfo.StockTrade(shCode)

        data = []
        for idx, [tbl, col] in enumerate(condCols):   
            val = _getDailyData(shCode, col, basDt,
                               dfShort if tbl == 'Short' else dfInvest if tbl == 'Invest' else dfTrade if tbl == 'Trade' else None)        
            if val != None:
                data.append(val)

        if len(data) == len(condCols):
            resData.append([shCode] + data)
        
    dfNew = pd.DataFrame(resData, columns = ['종목코드'] + [x[1][0] for x in condCols])
    return dfNew[dfNew.eval(cond)]   

def prtInvestResult(df, frDt, toDt):
    x = df['수익률'].agg(['size', 'mean', 'max', 'min']).tolist()
    cnt = "%10d"%int(x[0])
    cnt = ' '*(6-len(cnt) if len(cnt) <= 6 else 0) + cnt
    earnAvg = "%8.2f"%round(x[1],2)+' %'
    earnAvg = ' '*(10-len(earnAvg) if len(earnAvg) <= 10 else 0) + earnAvg
    earnMax = "%8.2f"%round(x[2],2)+' %'
    earnMax = ' '*(10-len(earnMax) if len(earnAvg) <= 10 else 0) + earnMax
    earnMin = "%8.2f"%round(x[3],2)+' %'
    earnMin = ' '*(10-len(earnMin) if len(earnMin) <= 10 else 0) + earnMin    

    print(' [ 종목 수익률 ]')
    print('┌────┬─────┬────┬─────┐')
    print('│ 종목수 │' + cnt + '│최대수익│' + earnMax + '│')
    print('├────┼─────┼────┼─────┤') 
    print('│평균수익│' + earnAvg + '│최소수익│' + earnMin + '│')
    print('└────┴─────┴────┴─────┘')       

    for idx, idxNm in enumerate(['코스피','코스닥']):
        x = stockInfo.StockPriceIndex(idxNm)
        frDt = x[x['일자']>=frDt]['일자'].values[0]
        toDt = x[x['일자']<=toDt]['일자'].values[-1]
        frIdx = x[x['일자']>=frDt]['종가'].values[0]
        toIdx = x[x['일자']<=toDt]['종가'].values[-1]
        
        earn = "%8.2f"%round(toIdx/frIdx*100-100,2)+' %'
        earn = ' '*(10-len(earn) if len(earn) <= 10 else 0) + earn
        frIdx = "%8.2f"%round(frIdx,2) 
        frIdx = ' '*(6-len(frIdx) if len(frIdx) <= 6 else 0) + frIdx
        toIdx = "%8.2f"%round(toIdx,2) 
        toIdx = ' '*(6-len(toIdx) if len(toIdx) <= 6 else 0) + toIdx
   
        if idx == 0:
            print(' [ 주요 지수 ]')
            print('┌────┬─────┐┌────┬────┬────┬────┐') 
            print('│ 지수명 │기간수익률││  일자  │  지수  │  일자  │  지수  │')
            print('├────┼─────┤├────┼────┼────┼────┤')
            
        print('│ ' + idxNm + ' │' + earn + '││' + frDt + '│' + frIdx, end='')
        print('│' + toDt + '│' + toIdx + '│')    
        
        if idx == 1:    
            print('└────┴─────┘└────┴────┴────┴────┘')    
        else:
            print('├────┼─────┤├────┼────┼────┼────┤')      