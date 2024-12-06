from ..common  import urlProc, code
from   bs4     import BeautifulSoup as bs
import numpy   as np
import pandas  as pd

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