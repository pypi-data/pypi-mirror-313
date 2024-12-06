from ..common     import conf, dataProc, code, urlProc
from ..outerIO    import naver
from ..outerIO    import kind
import datetime
from   bs4      import BeautifulSoup as bs

def SyncCmpnyFinInfoNaver(srchItem='', shCodeFr='000000', shCodeTo='zzzzzz'):
    columns = ['종류', '종목코드', '종목명', '기준년월', '매출액', '영업이익', '영업이익발표기준', '세전계속사업이익', '당기순이익', 
               '당기순이익지배', '당기순이익비지배', '자산총계', '부채총계', '자본총계', '자본총계지배', '자본총계비지배', '자본금', 
               '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 'CAPEX', 'FCF', '이자발생부채','영업이익률', '순이익률',
               'ROE', 'ROA', '부채비율', '자본유보율', 'EPS', 'PER', 'BPS', 'PBR', '현금DPS', '현금배당수익률', '현금배당성향', '보통주식수']    

    print(str(datetime.datetime.now()), '> 작업시작')
    
    ## 처리대상 종목 정보 가져오기
    if len(srchItem) > 0:
        dfCmpList = [code.StockItem(srchItem)[['종목코드','종목명']].values.tolist()[0]]
    else:         
        df = kind.GetStockItemInfoList()
        df = df[df['주식종류']=='보통주']
        df = df[(df['종목코드']>=shCodeFr)&(df['종목코드']<=shCodeTo)]
        dfCmpList = df[['종목코드','종목명']].values.tolist()
        dfCmpList.sort()
    
    ## 종목별 재무정보 읽어오기
    listData = []
    urlTmp = "https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"

    for idx, [shCode, shName] in enumerate(dfCmpList):
        print('\r'+str(datetime.datetime.now()), '>', idx+1, '/', len(dfCmpList), shCode, shName, end="")

        url = urlTmp.format(shCode)
        res = urlProc.requests_url_call(url)    
        soup = bs(res.text, "html.parser")

        listData += [['연간', shCode, shName] + x for x in naver.GetFinInfo(shCode, '연간').values.tolist()] # 연결_연간
        listData += [['분기', shCode, shName] + x for x in naver.GetFinInfo(shCode, '분기').values.tolist()] # 연결_분기    
        
    # 재무정보(네이버) update
    filePathNm = conf.companyInfoPath + "/재무정보(네이버).pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    currData['columns'] = columns

    frPos=0; toPos=0; listLen = len(listData)
    while toPos <= listLen:
        if toPos >= listLen or listData[frPos][0] != listData[toPos][0] \
                            or listData[frPos][1] != listData[toPos][1]:
            
            resData = listData[frPos : toPos]
            rptGb = resData[0][0]
            shCode = resData[0][1]
            shName = resData[0][2]

            if not currData.get(rptGb):
                currData[rptGb] = {}   
            if not currData[rptGb].get(shCode):
                currData[rptGb][shCode] = {}
            currData[rptGb][shCode]['종목명'] = shName

            if not currData[rptGb][shCode].get('info'):
                currData[rptGb][shCode]['info'] = []

            tmpData = dataProc._MergeData(currData[rptGb][shCode]['info'], 
                                          [x[3:] for x in resData], sortCols=1)
            tmpData = [x for x in tmpData if len(x[0]) >= 6]
            currData[rptGb][shCode]['info'] = tmpData                   

            frPos = toPos

        toPos += 1

    dataProc.WritePickleFile(filePathNm, currData)  