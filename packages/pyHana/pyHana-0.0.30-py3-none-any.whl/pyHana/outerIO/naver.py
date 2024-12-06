from ..common  import urlProc, code
from   bs4     import BeautifulSoup as bs
import numpy   as np
import pandas  as pd
import re

###################################################################################
#  GetFinInfo에서 url 호출 시 필요한 주식종목별 (1)암호파라미터 (2)id 값 구하는 함수
###################################################################################
def _GetParamInfo(shCode):
    urlTmp = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}"

    url = urlTmp.format(shCode)
    res = urlProc.requests_url_call(url)  

    sPos = res.text.find('function getAddInfoData01')
    sPos = res.text.find('encparam:', sPos)
    sPos = res.text.find("'",sPos)
    tPos = res.text.find("'",sPos+1)
    encparam = res.text[sPos+1:tPos]

    sPos = res.text.find('id:', tPos)
    sPos = res.text.find("'",sPos)
    tPos = res.text.find("'",sPos+1)
    id = res.text[sPos+1:tPos]
    
    return encparam, id

###################################################################################
#  각종 재무지표 구하는 함수
#  - 기업별 자산/부채 등 재무제표 항목, 매출/당기순이익 등 손익 항목, PER/PBR 등 
###################################################################################
def GetFinInfo(srchItem, rptGb='연간'):
    stockItem = code.StockItem(srchItem)
    if len(stockItem) == 1:
        shCode = stockItem.iloc[0]['종목코드']
    
    encparam, id = _GetParamInfo(shCode)
   
    gb = 'Q' if rptGb == '분기' else 'Y'
    urlTmp = "https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ={}&encparam={}&id={}"
    url = urlTmp.format(shCode, gb, encparam, id)
    headers = {"Referer":"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(shCode)}
    res = urlProc.requests_url_call(url, headers=headers)  
    soup = bs(res.text, "html.parser")

    resData = []
    
    if len(soup.select("table.gHead01")) ==2:
        data = soup.select("table.gHead01")[1]
        row = ['기준년월']
        for idx, th in enumerate(data.select("thead > tr")[1].select("th")):
            if idx < 5:
                row.append(th.text.strip()[:7])
            else:
                resData.append(row)
                break

        for tr in data.select("tbody > tr"):
            title = tr.select_one("th").text.strip()
            row = [title]

            for idx, td in enumerate(tr.select("td")):
                if idx <=4:
                    if td.text in [ u"\xa0", "N/A" ]:
                        row.append(0)
                    else:
                        if td.has_attr('title'):
                            x = td['title'].replace(",","").strip()
                        else:
                            x = td.text.replace(",","").strip()

                        if len(x) == 0:
                            row.append(0)
                        elif title in ['발행주식수(보통주)']:
                            row.append(int(float(x)))
                        else:
        #                     print(x)
                            row.append(float(x))
                else:
                    resData.append(row)
                    break     
    else:
        print('데이터 없음 : ', shCode)  

    return pd.DataFrame(np.transpose(resData).tolist()[1:], 
                columns = [ '기준년월', '매출액', '영업이익', '영업이익(발표기준)', '세전계속사업이익',  '당기순이익',  '당기순이익(지배)',
                        '당기순이익(비지배)', '자산총계', '부채총계', '자본총계', '자본총계(지배)', '자본총계(비지배)',
                        '자본금', '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 'CAPEX', 'FCF', '이자발생부채',
                        '영업이익률', '순이익률', 'ROE(%)', 'ROA(%)', '부채비율', '자본유보율', 'EPS(원)', 'PER(배)',
                        'BPS(원)', 'PBR(배)', '현금DPS(원)', '현금배당수익률', '현금배당성향(%)', '발행주식수(보통주)'] )
    
def getBizCategory():
    resData = []
    url = "https://finance.naver.com/sise/sise_group.naver?type=upjong"
    res = urlProc.requests_url_call(url,headers={"Referer":url})
    soup = bs(res.text, "html5lib")
        
    trs = soup.select_one("tbody").select("tr")

    for tr in trs:
        tds = tr.select("td")

        if len(tds) >= 6:
            line = []
            for idx, td in enumerate(tds[:6]):
                if idx == 0:
                    line.append( td.get_text().strip() )
                elif idx == 1:
                    line.append( float(td.get_text().strip().replace('%','')) )
                else:
                    line.append( int(td.get_text().strip()) )
                    
            line.append(tds[0].select_one('a[href]')['href'].replace('/sise/sise_group_detail.naver?type=upjong&no=',''))
            resData.append(line)   
            
    return pd.DataFrame(resData, columns=['업종명','등락률','전체','상승','보합','하락','linkNo'])       
    

def getBizDetail(bizList='', prtInd=False):       
    if type(bizList) == type(pd.DataFrame([])):
        bizList = bizList[['업종명','linkNo']].values.tolist()
    
    resData = []     
    url = "https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no={}"
        
    for i, [bizNm, linkNum] in enumerate(bizList):
                
        res = urlProc.requests_url_call(url.format(linkNum),headers={"Referer":"https://finance.naver.com/sise/sise_group.naver"})
        soup = bs(res.text, "html5lib")        

    #     time.sleep(0.1)
        trs = soup.select_one("[summary='업종별 시세 리스트']").select("tbody > tr")
        
        for tr in trs:
            tds = tr.select("td")
            
            if len(tds) >= 9:
                line = [bizNm, tds[0].select_one('a[href]')['href'].strip()[-6:], tds[0].select_one('a[href]').get_text()]
                
                for idx in range(1, 9):
                    # num = tds[idx].get_text().strip().replace('%','').replace(',','')
                    txt = tds[idx].get_text()
                    num = re.sub(r"[^0-9.+-]", "", txt)
                    if '하락' in txt or '하한가' in txt:
                        num = '-' + num 
                    line.append( float(num) if idx == 3 else int(num) )
                    
                resData.append(line + [linkNum])
                
        if prtInd:
            print('\r' + '업종별 종목 리스트 현행화({}/{}):'.format(i+1, len(bizList)), bizNm, ' '*50, end='')
            
    return pd.DataFrame(resData, columns=['업종명', '종목코드','종목명','현재가','전일대비','등락률','매수호가','매도호가','거래량','거래대금',
                                          '전일거래량', 'linkNo'])     
    
        
def getTheme():
    urlTmp = "https://finance.naver.com/sise/theme.naver?&page={}"
    pgNum = 1                
    resData = []

    while True:    
        url = urlTmp.format(pgNum) 
        res = urlProc.requests_url_call(url,headers={"Referer":url})
        soup = bs(res.text, "html5lib")
        
    #     time.sleep(0.1)
        trs = soup.select_one("tbody").select("tr")
        for tr in trs:
            tds = tr.select("td")
            
            if len(tds) >= 7:
                line = []
                for idx, td in enumerate(tds):
                    if idx in [1,2]:
                        line.append( float(td.get_text().strip().replace('%','')) )
                    elif idx in [3,4,5]:
                        line.append( int(td.get_text().strip()) )
                    else:
                        line.append( td.get_text().strip() )

                if len(line) == 7: line.append(None)
                line.append(tds[0].select_one('a[href]')['href'].replace('/sise/sise_group_detail.naver?type=theme&no=',''))
                resData.append(line)
        if  soup.select_one(".pgRR"):
            pgNum += 1
        else:
            break
            
    return pd.DataFrame(resData, columns=['테마명','등락률','최근3일평균등락률','상승','보합','하락','주도주1','주도주2','linkNo'])     

def getThemeDetail(thList='', prtInd=False):       
    if type(thList) == type(pd.DataFrame([])):
        thList = thList[['테마명','linkNo']].values.tolist()
            
    resData = []     
    url = "https://finance.naver.com/sise/sise_group_detail.naver?type=theme&no={}"
        
    for i, [themeNm, linkNum] in enumerate(thList):
        res = urlProc.requests_url_call(url.format(linkNum),headers={"Referer":"https://finance.naver.com/sise/theme.naver"})
        soup = bs(res.text, "html5lib")        

    #     time.sleep(0.1)
        trs = soup.select_one("[summary='업종별 시세 리스트']").select("tbody > tr")
        
        for tr in trs:
            tds = tr.select("td")
            
            if len(tds) >= 11:
                line = [themeNm, tds[0].select_one('a[href]')['href'].strip()[-6:], tds[0].select_one('a[href]').get_text()]
                
                for idx in range(2, 10):
                    # num = tds[idx].get_text().strip().replace('%','').replace(',','')
                    txt = tds[idx].get_text()
                    num = re.sub(r"[^0-9.+-]", "", txt)
                    if '하락' in txt or '하한가' in txt:
                        num = '-' + num 
                    line.append( float(num) if idx == 4 else int(num) )                    
                    
                line.append(tds[1].select_one('.info_txt').get_text())
                resData.append(line + [linkNum])
                
        if prtInd:
            print('\r' + '테마별 종목 리스트 현행화({}/{}):'.format(i+1, len(thList)), themeNm, ' '*50, end='')
            
    return pd.DataFrame(resData, columns=['테마명','종목코드','종목명','현재가','전일대비','등락률','매수호가','매도호가','거래량',
                                          '거래대금','전일거래량','비고','linkNo'])     