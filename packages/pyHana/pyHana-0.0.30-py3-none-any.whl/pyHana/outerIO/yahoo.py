from ..common  import urlProc
from   bs4     import BeautifulSoup as bs
import pandas  as pd
import re
import datetime


#치환 문자열 
replacements = {
    'Jan':'01',    'Feb':'02',    'Mar':'03',    'Apr':'04',    'May':'05',    'Jun':'06',
    'Jul':'07',    'Aug':'08',    'Sep':'09',    'Oct':'10',    'Nov':'11',    'Dec':'12'
}

def mreplace(text, replacements):
    regex = re.compile("|".join(map(re.escape, replacements.keys())), re.IGNORECASE)

    def rmatch(match):
        return replacements[match.group(0)]

    return regex.sub(rmatch, text)

## 미국 ETF 종목 일별 주가 정보 가져오기
def GetEtfTradeInfoUSA(shCode='', frDt = '20100101', toDt = '99991231'):        
    frSec = (datetime.datetime.strptime(frDt, '%Y%m%d') - datetime.datetime.strptime('19700101', '%Y%m%d')).days *86400
    toSec = (datetime.datetime.strptime(toDt, '%Y%m%d') - datetime.datetime.strptime('19700101', '%Y%m%d')).days *86400
    frSec, toSec

    urlTmp = "https://finance.yahoo.com/quote/{}/history/?period1={}&period2={}"
    url = urlTmp.format(shCode, frSec, toSec)

    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "accept-encoding":"gzip, deflate, br, zstd",
               "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
               }
    res = urlProc.requests_url_call(url, headers=headers, method='GET')           
    soup = bs(res.text, "html.parser")
    
    resData = []
    divData = []
    if len(soup.select("section.container > h1")) == 1:
        shName = soup.select_one("section.container > h1").text
    else:
        shName = ''

    if len(soup.select("table > tbody")) == 1:
        trs = soup.select("table > tbody > tr")

        for tr in trs:
            tds = tr.select("td")

            x = tds[0].text.strip().replace(",","").split()
            trDt = x[2] + mreplace(x[0], replacements) + "%02d"%( int(x[1]) )

            ## 액면분할 등 주식수 변동 시 display
            if tr.text.strip().find('Splits',0) >= 0:
                print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), shName, tds[1].text.strip(), '('+trDt+')')
            ## 배당금 추출
            elif len(tds) == 2 and tds[1].text.strip().find('Dividend',0) >= 0:
                divData.append([trDt, float(tds[1].text.replace("Dividend",'').strip().replace(",",""))])                
            ## 주식거래정보 추출
            else:
                line = [shCode]
                for idx, td in enumerate(tds):
                    if idx == 0:
                        x = td.text.strip().replace(",","").split()
                        line.append(trDt)          
                    elif idx <=5:
                        line.append(float(td.text.strip().replace(",","")))
                    else:
                        line.append(int(td.text.strip().replace(",","").replace("-","0")))
                resData.append(line)    

    # 주식거래 + 배당금 merge
    dfTrade = pd.DataFrame(resData, columns=['종목코드','일자','시가','고가','저가','종가','조정가','거래량'])
    dfDividend = pd.DataFrame(divData, columns=['일자','배당금'])
    dfMerge = pd.merge(dfTrade, dfDividend, how='left').sort_values('일자').reset_index(inplace=False).fillna(0)

    return dfMerge[['종목코드','일자','시가','고가','저가','종가','거래량','배당금']]       


## 미국 ETF 종목정보 가져오기
def GetEtfListUSA():
    print(datetime.datetime.now(), '미국 ETF 종목정보 가져오기 Start')
    
    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "accept-encoding":"gzip, deflate, br, zstd",
               "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
               }
    urlTmp = "https://finance.yahoo.com/markets/etfs/most-active/?start={}&count={}"

    resData = []
    frCnt = 0
    pgCnt = 100

    while 1:        
        url = urlTmp.format(frCnt, pgCnt)
        print('\r' + str(datetime.datetime.now()), url, end='')
        
        res = urlProc.requests_url_call(url, headers=headers, method='GET')           
        soup = bs(res.text, "html.parser")

        if len(soup.select("table > tbody")) == 1 and len(soup.select("table > tbody > tr")) > 1:
            trs = soup.select("table > tbody > tr")

            for tr in trs:
                # x = tr.select("td")[0].select("div > span")
                x = tr.select("td")
                resData.append([x[0].text.strip(), x[1].text.strip()])
        else:
            break

        frCnt += pgCnt

    print('\r' + str(datetime.datetime.now()), '미국 ETF 종목정보 가져오기 End : ', len(resData), '개 종목', ' '*50)
    return pd.DataFrame(sorted(resData), columns=['종목코드','종목명'])       