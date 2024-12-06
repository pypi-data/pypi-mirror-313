from   bs4      import BeautifulSoup as bs
import time  
import re
import pandas   as pd
from ..common   import urlProc, code
import json    

# Url에서 특정 조회조건의 값을 추출
# GetUrlAttrValue = lambda url, key: [x for x in url.split('&') if x[0:len(key)] == key][0].split('=')[1]

# common_headers = {"X-Forwarded-For": "127.0.0.1"}
common_headers = {"X-Forwarded-For": "127.0.0.1",
                  "Host":"data.krx.co.kr",
                  "Origin":"http://data.krx.co.kr",
                  "Referer":"http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101",
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                  "X-Requested-With":"XMLHttpRequest"
                 }
# 403 Forbidden 해결방안
# https://www.hahwul.com/2021/10/08/bypass-403/
# X-Custom-IP-Authorization: 127.0.0.1
# X-Forwarded: 127.0.0.1
# X-Forwarded-For: 127.0.0.1
# X-Forwarded-Host: localhost
# X-Forwarded-By: 127.0.0.1
# X-Forwarded-Port: 80
# X-Forward-For: 127.0.0.1
# X-Remote-IP: 127.0.0.1
# X-Originating-IP: 127.0.0.1
# X-Remote-Addr: 127.0.0.1
# X-Client-IP: 127.0.0.1
# X-Real-IP: 127.0.0.1
# X-True-IP: 127.0.0.1
# Redirect: http://localhost
# Referer: http://localhost
# Host: localhost

def GetStockItemInfoList():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    params = 'bld=dbms/MDC/STAT/standard/MDCSTAT01901&locale=ko_KR&mktId=ALL&share=1&csvxls_isNo=false'
    res = urlProc.requests_url_call(url, headers=common_headers, params=params)    
    dList = json.loads(res.text)['OutBlock_1']
    dfCmpList = pd.DataFrame.from_dict(dList).rename(columns={
                "ISU_CD":"표준코드", "ISU_SRT_CD":"종목코드", "ISU_NM":"한글종목명", "ISU_ABBRV":"종목명", "ISU_ENG_NM":"영문종목명",
                "LIST_DD":"상장일", "MKT_TP_NM":"시장구분", "SECUGRP_NM":"증권구분", "SECT_TP_NM":"소속부", "KIND_STKCERT_TP_NM":"주식종류",
                "PARVAL":"액면가", "LIST_SHRS":"상장주식수"})    
    dfCmpList['상장일'] = dfCmpList['상장일'].apply(lambda x: x.replace('/',''))
    return dfCmpList

# def GetDividendInfo(selYear, currentPageSize = 100, marketType='', settlementMonth='', yearCnt = 3, prtInd=False):
    # currentPageSize(페이지당 조회건수) : 15 / 30 / 50 / 100
    # marketType(시장구분) : 전체 '', 유가증권 '1', 코스닥 '2' 코넥스 '6' 
    # settlementMonth(결산월) : 전체 '', 1월~12월 : '01'~'12'
    # selYearCnt(최근 몇년간 조회) : 1 / 2 / 3 
    # selYear : 기준년도 (해당 년도를 기준으로 최근 이전 {selYearCnt} 년간 자료 조회)
    
    # url    = "https://kind.krx.co.kr/disclosureinfo/dividendinfo.do"
    # params = "method=searchDividendInfoSub&forward=dividendinfo_sub"
    # params += "&searchCodeType=&searchCorpName=&repIsuSrtCd=&chkOrgData=&searchCorpNameTmp="
    # params += "&currentPageSize={}&marketType={}&settlementMonth={}".format(currentPageSize, marketType, settlementMonth)
    # params += "&selYear={}&selYearCnt={}&pageIndex={}"        
def GetDividendInfo(selYear, mktId='', yearCnt = 3, prtInd=False):    
    # mktId(시장구분) : 전체 '', 유가증권 '1', 코스닥 '2' 코넥스 '6' 
    # yearCnt(최근 몇년간 조회) : 1 / 2 / 3 
    # selYear : 기준년도 (해당 년도를 기준으로 최근 이전 {selYearCnt} 년간 자료 조회)
    
    mktId = 'STK' if mktId == '1' else 'KSQ' if mktId == '2' else 'KNX' if mktId == '6'  else 'ALL'

    columns = [['종목코드','종목명','사업년도','결산월','업종','업종별배당율','주식배당','액면가','기말주식수',
            '주당배당금','배당성향','총배당금액','시가배당율'],
            ["ISU_CD","ISU_NM","BZ_YY","ACNTCLS_MM","IDX_IND_NM","DIV_YD","PERSHR_DIV_CMSTK_SHRS","PARVAL","LIST_SHRS",
                "CMSTK_DPS","DIV_INCLIN","DIV_TOTAMT","MKTPRC_CMSTK_DIV_RT"]]
    
    url     = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    params  = 'bld=dbms/MDC/STAT/issue/MDCSTAT20901&locale=ko_KR&mktId={}&'
    params += 'tboxisuCd_finder_comnm0_1=%EC%A0%84%EC%B2%B4&isuCd=ALL'
    params += '&isuCd2=ALL&codeNmisuCd_finder_comnm0_1=&param1isuCd_finder_comnm0_1=&acntclsMm='
    params += '&basYy={}&indTpCd={}&share=1&money=1&csvxls_isNo=true'
    
    params = params.format(mktId, selYear, yearCnt)
    res = urlProc.requests_url_call(url, headers=common_headers, params=params, prtInd=prtInd)
    dList = json.loads(res.text)['output']

    dfDividend = pd.DataFrame.from_dict(dList)[columns[1]]
    dfDividend.columns = columns[0]
    dfDividend['업종별배당율'] = dfDividend['업종별배당율'].replace(",","").replace("-","0").astype('float')
    dfDividend['주식배당']     = dfDividend['주식배당' ].replace(",","").replace("-","0").astype('float')
    dfDividend['액면가']       = dfDividend['액면가'   ].apply(lambda x: round(float(x.replace("무액면","0").replace(",","").replace("-","0")),0)).astype('int64')
    dfDividend['기말주식수']   = dfDividend['기말주식수'].apply(lambda x: x.replace(",","").replace("-","0")).astype('int64')
    dfDividend['주당배당금']   = dfDividend['주당배당금'].apply(lambda x: x.replace(",","").replace("-","0")).astype('float')
    dfDividend['배당성향']     = dfDividend['배당성향'  ].apply(lambda x: x.replace(",","").replace("-","0")).astype('float')
    dfDividend['총배당금액']   = dfDividend['총배당금액'].apply(lambda x: round(float(x.replace("무액면","0").replace(",","").replace("-","0")),0)).astype('int64')
    dfDividend['시가배당율']   = dfDividend['시가배당율'].apply(lambda x: x.replace(",","").replace("-","0")).astype('float')
    
    return dfDividend


def GetStockPriceIndex(mIndexNm, sDate, eDate, prtInd=False):

    urlDict = {
        '코스피'    : {  'indIdx'  : '1',  'indIdx2' : '001' },
        '코스피100' : {  'indIdx'  : '1',  'indIdx2' : '034' },
        '코스피200' : {  'indIdx'  : '1',  'indIdx2' : '028' },
        '코스닥'    : {  'indIdx'  : '2',  'indIdx2' : '001' },        
    }    

    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    params = 'bld=dbms/MDC/STAT/standard/MDCSTAT00301&locale=ko_KR&tboxindIdx_finder_equidx0_0={}&indIdx={}&indIdx2={}&codeNmindIdx_finder_equidx0_0={}'
    params += '&param1indIdx_finder_equidx0_0=&strtDd={}&endDd={}&share=1&money=1&csvxls_isNo=false'
    
    headers = common_headers
    headers["Referer"] = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010103"
    
    res = urlProc.requests_url_call(url, params = params.format(mIndexNm, urlDict[mIndexNm]['indIdx'], urlDict[mIndexNm]['indIdx2'], mIndexNm, sDate, eDate), 
                                    headers=headers, prtInd=prtInd)      
    dList = json.loads(res.text)['output']

    rData = []
    errCnt = 0

    for data in dList:
        if data['MKTCAP'] != '-':
            rData.append([ data['TRD_DD'].replace('/',''), 
                          float(data['CLSPRC_IDX'].replace(",","").replace("-","0")), 
                          float(data['PRV_DD_CMPR'].replace(",","").replace("-","0")), 
                          float(data['UPDN_RATE'].replace(",","").replace("-","0")), 
                          float(data['OPNPRC_IDX'].replace(",","").replace("-","0")), 
                          float(data['HGPRC_IDX'].replace(",","").replace("-","0")), 
                          float(data['LWPRC_IDX'].replace(",","").replace("-","0")), 
                          int(data['ACC_TRDVOL'].replace(",","").replace("-","0")), 
                          int(data['ACC_TRDVAL'].replace(",","").replace("-","0")), 
                          int(data['MKTCAP'].replace(",","").replace("-","0")), 
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
        
    return pd.DataFrame( rData, columns=['일자', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '상장시가총액'] )


def GetStockTradeInfo(*args, **kwargs):
    rData = []
    errCnt = 0

    ## 전체 주식 특정일자로 조회
    if len(args) == 1 and len(args[0]) == 8 and args[0].isnumeric():
        srchDt = args[0]

        url    = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        params = "bld=dbms/MDC/STAT/standard/MDCSTAT01501&locale=ko_KR&mktId=ALL&share=1&money=1&csvxls_isNo=false&trdDd={}"
            
        params = params.format(srchDt)
        res = urlProc.requests_url_call(url, headers=common_headers, params=params)    
        dList = json.loads(res.text)['OutBlock_1']

        for data in dList:
            if data['TDD_OPNPRC'] != '-':
                rData.append([ data['ISU_SRT_CD'], data['ISU_ABBRV'], srchDt, 
                            int(data['TDD_OPNPRC'].replace(",","")), 
                            int(data['TDD_HGPRC'].replace(",","")), 
                            int(data['TDD_LWPRC'].replace(",","")), 
                            int(data['TDD_CLSPRC'].replace(",","")), 
                            int(data['CMPPREVDD_PRC'].replace(",","")), 
                            float(data['FLUC_RT'].replace(",","")),                        
                            int(data['ACC_TRDVOL'].replace(",","")), 
                            int(data['ACC_TRDVAL'].replace(",","")),
                            int(data['MKTCAP'].replace(",","")),
                            int(data['LIST_SHRS'].replace(",",""))
                            ])
            else:
                errCnt += 1
        
        if errCnt > 0:
            print("\n", srchDt, "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
            
        return pd.DataFrame( rData, columns=['종목코드', '종목명', '일자', '시가', '고가', '저가', '종가', '대비', '등락률',
                                            '거래량', '거래대금', '시가총액', '상장주식수'] )
    ## 특정 종목 기간 조회
    elif len(args) in (3,5):
        frDt = args[1]
        toDt = args[2]
        
        if len(args) == 5:
            shCode = args[0]
            isuCd = args[3]
            shName = args[4]
        else:
            x = code.StockItem(args[0])[['종목코드','종목명','표준코드']].values.tolist()
            [shCode, shName, isuCd] = x[0] if len(x) == 1 else ['','','']
            
            # url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT01901&locale=ko_KR&mktId=ALL&share=1&csvxls_isNo=false'
            # res = urlProc.requests_url_call(url)    
            # dList = json.loads(res.text)['OutBlock_1']
            # for data in dList:
            #     if data['ISU_SRT_CD'] == shCode:
            #         isuCd = data['ISU_CD']
            #         shName = data['ISU_ABBRV']
            #         break         
                
                
        url    = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        params = 'bld=dbms/MDC/STAT/standard/MDCSTAT01701&locale=ko_KR&'
        params += 'tboxisuCd_finder_stkisu0_15={}&isuCd={}&isuCd2=&codeNmisuCd_finder_stkisu0_15={}'
        params += '&param1isuCd_finder_stkisu0_15=ALL&strtDd='
        params += '{}&endDd={}&share=1&money=1&csvxls_isNo=false'
        if kwargs.get('sujung', 'N') == 'Y':
            params += '&adjStkPrc_check=Y&adjStkPrc=2'
        else:
            params += '&adjStkPrc=1'

        params = params.format(shCode, isuCd, shName, frDt, toDt)
        res = urlProc.requests_url_call(url, headers=common_headers, params=params)    
        dList = json.loads(res.text)['output']

        for data in dList:
            if data['TDD_OPNPRC'] != '-':
                rData.append([ shCode, shName, data['TRD_DD'].replace('/',''), 
                            int(data['TDD_OPNPRC'].replace(",","")), 
                            int(data['TDD_HGPRC'].replace(",","")), 
                            int(data['TDD_LWPRC'].replace(",","")), 
                            int(data['TDD_CLSPRC'].replace(",","")), 
                            int(data['CMPPREVDD_PRC'].replace(",","")), 
                            float(data['FLUC_RT'].replace(",","")),                        
                            int(data['ACC_TRDVOL'].replace(",","")), 
                            int(data['ACC_TRDVAL'].replace(",","")),
                            int(data['MKTCAP'].replace(",","")),
                            int(data['LIST_SHRS'].replace(",",""))
                            ])
            else:
                errCnt += 1

        if errCnt > 0:
            print("\n", srchDt, "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)

        return pd.DataFrame( rData, columns=['종목코드', '종목명', '일자', '시가', '고가', '저가', '종가', '대비', '등락률',
                                            '거래량', '거래대금', '시가총액', '상장주식수'] )    
    else:
        print('유효한 검색조건 1 : ', "GetStockTradeInfo(일자)" )
        print('유효한 검색조건 2 : ', "GetStockTradeInfo(종목코드, 시작일자, 종료일자, sujung='Y/N' )" )
        print('유효한 검색조건 3 : ', "GetStockTradeInfo(종목코드, 시작일자, 종료일자, 표준코드, 종목명, sujung='Y/N' )" )




def GetTradeVolumeByInvestor(shCode, sDate, eDate, shName='', isuCd=''):
    if shName == '' or isuCd == '':       
        x = code.StockItem(shCode)[['종목코드','종목명','표준코드']].values.tolist()
        [shCode, shName, isuCd] = x[0] if len(x) == 1 else ['','','']        
        
    # 투자자별 거래량
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?"
    params =  'bld=dbms/MDC/STAT/standard/MDCSTAT02303&locale=ko_KR&inqTpCd=2&trdVolVal=1&askBid=3&'
    params += 'tboxisuCd_finder_stkisu0_2={}%2F{}&isuCd={}&isuCd2={}&codeNmisuCd_finder_stkisu0_2={}&'
    params += 'param1isuCd_finder_stkisu0_2=ALL&strtDd={}&endDd={}&detailView=1&share=1&csvxls_isNo=false'
    
    res = urlProc.requests_url_call(url, headers=common_headers, params=params.format(shCode, shName, isuCd, isuCd, shName, sDate, eDate) )
    # print(url.format(shCode, shName, isuCd, isuCd, shName, sDate, eDate) )
    # print(res.text)
    dList = json.loads(res.text)['output']

    rData = []
    errCnt = 0

    for data in dList:
        if data['TRD_DD'] != '-':
            rData.append([ data['TRD_DD'].replace('/',''), 
                          int(data['TRDVAL1'].replace(",","")), 
                          int(data['TRDVAL2'].replace(",","")),  
                          int(data['TRDVAL3'].replace(",","")),  
                          int(data['TRDVAL4'].replace(",","")),  
                          int(data['TRDVAL5'].replace(",","")),  
                          int(data['TRDVAL6'].replace(",","")), 
                          int(data['TRDVAL7'].replace(",","")),  
                          int(data['TRDVAL8'].replace(",","")),  
                          int(data['TRDVAL9'].replace(",","")),  
                          int(data['TRDVAL10'].replace(",","")),  
                          int(data['TRDVAL11'].replace(",",""))
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
    
    dfInvestor = pd.DataFrame(rData, columns=['일자', '금융투자', '보험', '투신', '사모', '은행', '기타금융',
                                              '연기금', '기타법인', '개인', '외국인', '기타외국인'] )
    
    # 외국인 보유량
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?"
    params =  'bld=dbms/MDC/STAT/standard/MDCSTAT03702&locale=ko_KR&searchType=2&mktId=ALL&trdDd={}&'
    params += 'tboxisuCd_finder_stkisu0_11={}/{}&isuCd={}&isuCd2={}&codeNmisuCd_finder_stkisu0_11={}&'
    params += 'param1isuCd_finder_stkisu0_11=ALL&strtDd={}&endDd={}&share=1&csvxls_isNo=false'
    
    res = urlProc.requests_url_call(url, headers=common_headers, params=params.format(eDate,  shCode, shName, isuCd, isuCd, shName, sDate, eDate))
    dList = json.loads(res.text)['output']

    rData = []
    errCnt = 0 
    
    for data in dList:
        if data['TRD_DD'] != '-':
            rData.append([ data['TRD_DD'].replace('/',''),                           
                          int(data['FORN_HD_QTY'].replace(",","")),  
                          float(data['FORN_SHR_RT'].replace(",","")),  
                          int(data['FORN_ORD_LMT_QTY'].replace(",","")),  
                          float(data['FORN_LMT_EXHST_RT'].replace(",","")),                            
                          int(data['LIST_SHRS'].replace(",",""))
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
    
    dfForn = pd.DataFrame( rData, columns=['일자', '외국인보유수량', '외국인지분율', '외국인한도수량',
                                       '외국인한도소진율', '전체주식수'] )
       
    return pd.merge(dfInvestor, dfForn).astype({'외국인보유수량':'int64',
                                       '외국인한도수량':'int64', '전체주식수':'int64'})
    
    
def GetShortSelling(shCode, sDate, eDate, shName='', isuCd=''):
    if shName == '' or isuCd == '':
        x = code.StockItem(shCode)[['종목코드','종목명','표준코드']].values.tolist()
        [shCode, shName, isuCd] = x[0] if len(x) == 1 else ['','','']               
        
    # 공매도 거래량
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?"
    params =  'bld=dbms/MDC/STAT/srt/MDCSTAT30102&locale=ko_KR&searchType=2&mktId=STK&secugrpId=STMFRTSCIFDRFS&'
    params += 'secugrpId=SRSW&secugrpId=BC&inqCond=STMFRTSCIFDRFSSRSWBC&trdDd={}&'
    params += 'tboxisuCd_finder_srtisu1_4={}/{}&isuCd={}&isuCd2={}&codeNmisuCd_finder_srtisu1_4={}&'
    params += 'param1isuCd_finder_srtisu1_4=&strtDd={}&endDd={}&share=1&money=1&csvxls_isNo=false'

    res = urlProc.requests_url_call(url, headers=common_headers, params=params.format(eDate, shCode, shName, isuCd, shCode, shName, sDate, eDate) )
    dList = json.loads(res.text)['OutBlock_1']

    rData = []
    errCnt = 0

    for data in dList:
        if data['TRD_DD'] != '-':
            rData.append([ data['TRD_DD'].replace('/',''), 
                          int(data['CVSRTSELL_TRDVOL'].replace(",","")), 
                          int(data['UPTICKRULE_APPL_TRDVOL'].replace(",","")),  
                          int(data['UPTICKRULE_EXCPT_TRDVOL'].replace(",","")),  
                          int(data['ACC_TRDVOL'].replace(",","")),  
                          float(data['TRDVOL_WT'].replace(",","")),  
                          int(data['CVSRTSELL_TRDVAL'].replace(",","")), 
                          int(data['UPTICKRULE_APPL_TRDVAL'].replace(",","")),  
                          int(data['UPTICKRULE_EXCPT_TRDVAL'].replace(",","")),  
                          int(data['ACC_TRDVAL'].replace(",","")),  
                          float(data['TRDVAL_WT'].replace(",","")) 
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
    
    dfInvestor = pd.DataFrame(rData, columns=['일자', '공매도거래량', '공매도거래량업틱', '공매도거래량업틱예외',
                                              '전체거래량', '공매도거래량비중', 
                                              '공매도거래대금', '공매도거래대금업틱', '공매도거래대금업틱예외',
                                              '전체거래대금', '공매도거래대금비중'] )
    
    # 공매도 잔고
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?"
    params  = 'bld=dbms/MDC/STAT/srt/MDCSTAT30502&locale=ko_KR&searchType=2&mktTpCd=1&trdDd={}&'
    params += 'tboxisuCd_finder_srtisu0_5={}/{}&isuCd={}&isuCd2={}&codeNmisuCd_finder_srtisu0_5={}&'
    params += 'param1isuCd_finder_srtisu0_5=&strtDd={}&endDd={}&share=1&money=1&csvxls_isNo=false'
    
    res = urlProc.requests_url_call(url, headers=common_headers, params=params.format(eDate,  shCode, shName, isuCd, shCode, shName, sDate, eDate) )
    dList = json.loads(res.text)['OutBlock_1']

    rData = []
    errCnt = 0 

    for data in dList:
        if data['RPT_DUTY_OCCR_DD'] != '-':
            rData.append([ data['RPT_DUTY_OCCR_DD'].replace('/',''),                           
                          int(data['BAL_QTY'].replace(",","")),  
                          int(data['LIST_SHRS'].replace(",","")),  
                          int(data['BAL_AMT'].replace(",","")),                              
                          int(data['MKTCAP'].replace(",","")),
                          float(data['BAL_RTO'].replace(",",""))
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
    
    dfForn = pd.DataFrame( rData, columns=['일자', '공매도잔고수량', '상장주식수', '공매도잔고금액',
                                       '시가총액', '공매도잔고비중'] )
       
    return pd.merge(dfInvestor, dfForn).astype({'공매도잔고수량':'int64',
             '상장주식수':'int64', '공매도잔고금액':'int64', '시가총액':'int64'})
    

def CompareStockPrice(frDt, toDt):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    params = "bld=dbms/MDC/STAT/standard/MDCSTAT01602&locale=ko_KR&mktId=ALL&strtDd={}&endDd={}&adjStkPrc_check=Y&adjStkPrc=2&share=1&money=1&csvxls_isNo=false"
    params = params.format(frDt, toDt)
    res = urlProc.requests_url_call(url, headers=common_headers, params=params)    
    dList = json.loads(res.text)['OutBlock_1']

    rData = []
    errCnt = 0

    for data in dList:
        if data['TDD_CLSPRC'] != '-':
            rData.append([ data['ISU_SRT_CD'], data['ISU_ABBRV'],
                        int(data['BAS_PRC'].replace(",","")), int(data['TDD_CLSPRC'].replace(",","")), 
                        int(data['CMPPREVDD_PRC'].replace(",","")), float(data['FLUC_RT'].replace(",","")), 
                        int(data['ACC_TRDVOL'].replace(",","")), 
                        int(data['ACC_TRDVAL'].replace(",",""))
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
        
    return pd.DataFrame( rData, columns=['종목코드', '종목명', '시작일기준가', '종료일종가', '대비', '등락률', '거래량', '거래대금'] )


# def GetFinancialIncator(*args):


# .replace("-","0")) 로직 삭제


#     rData = []
#     errCnt = 0
#     dList = []

#     ## 전체 주식 특정일자로 조회
#     if len(args) == 1 and len(args[0]) == 8 and args[0].isnumeric():
#         srchDt = args[0]    
#         url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
#         params='bld=dbms/MDC/STAT/standard/MDCSTAT03501&locale=ko_KR&searchType=1&mktId=ALL&trdDd={}&param1isuCd_finder_stkisu0_12=ALL&csvxls_isNo=false'
#         res = urlProc.requests_url_call(url, params = params.format(srchDt) )      
#         dList = json.loads(res.text)['output']

#         for data in dList:
#             if data['ISU_SRT_CD'] != '-':
#                 rData.append([ data['ISU_SRT_CD'], 
#                             data['ISU_ABBRV'].strip(),
#                             srchDt,
#                             data['TDD_CLSPRC'].replace(",",""), 
#                             int(data['EPS'].replace(",","").replace("-","0")), 
#                             float(data['PER'].replace(",","").replace("-","0")), 
#                             int(data['FWD_EPS'].replace(",","").replace("-","0")), 
#                             float(data['FWD_PER'].replace(",","").replace("-","0")), 
#                             int(data['BPS'].replace(",","").replace("-","0")), 
#                             float(data['PBR'].replace(",","").replace("-","0")), 
#                             int(data['DPS'].replace(",","").replace("-","0")), 
#                             float(data['DVD_YLD'].replace(",","").replace("-","0")), 
#     #                           str(int(int(data['ACC_TRDVAL'].replace(",",""))/1000000)) 
#                             ])
#             else:
#                 errCnt += 1
        
#         if errCnt > 0:
#             print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
            
#         return pd.DataFrame( rData, columns=['종목코드', '종목명', '일자', '종가', 'EPS', 'PER', '선행EPS', '선행PER', 'BPS', 'PBR', '주당배당금', '배당수익률'] )

#     ## 특정 종목 기간 조회
#     elif len(args) == 3:
#         x = code.GetStockItem(args[0])
#         if len(x) == 1:
#             frDt = args[1]
#             toDt = args[2]
#             shCode = x['종목코드'].values[0]
#             shName = x['종목명'].values[0]
#             stdCode = x['표준코드'].values[0]

#             url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
#             params = 'bld=dbms/MDC/STAT/standard/MDCSTAT03502&locale=ko_KR&searchType=2&mktId=ALL&trdDd={}&tboxisuCd_finder_stkisu0_12={}/{}'
#             params += '&isuCd={}&isuCd2={}&codeNmisuCd_finder_stkisu0_12={}&param1isuCd_finder_stkisu0_12=ALL&strtDd={}&endDd={}&csvxls_isNo=false'
#             res = urlProc.requests_url_call(url, params = params.format(toDt, shCode, shName, stdCode, stdCode, shName, frDt, toDt) )      
#             dList = json.loads(res.text)['output']

#             for data in dList:
#                 if data['TDD_CLSPRC'] != '-':
#                     rData.append([  shCode, 
#                                     shName,
#                                     data['TRD_DD'],                                           # 일자 
#                                     data['TDD_CLSPRC'].replace(",",""),                       # 종가
#                                     int(data['EPS'].replace(",","").replace("-","0")),        # EPS
#                                     float(data['PER'].replace(",","").replace("-","0")),      # PER
#                                     int(data['FWD_EPS'].replace(",","").replace("-","0")),    # 선행EPS
#                                     float(data['FWD_PER'].replace(",","").replace("-","0")),  # 선행PER
#                                     int(data['BPS'].replace(",","").replace("-","0")),        # BPS
#                                     float(data['PBR'].replace(",","").replace("-","0")),      # PBR
#                                     int(data['DPS'].replace(",","").replace("-","0")),        # 주당배당금
#                                     float(data['DVD_YLD'].replace(",","").replace("-","0")),  # 배당수익률
#                                 ])
#                 else:
#                     errCnt += 1
            
#             if errCnt > 0:
#                 print("\n", "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
                
#             return pd.DataFrame( rData, columns=['종목코드', '종목명', '일자', '종가', 'EPS', 'PER', '선행EPS', '선행PER', 'BPS', 'PBR', '주당배당금', '배당수익률'] )
          
#     else:
#         print('유효한 검색조건 1 : ', "GetStockTradeInfo(일자)" )
#         print('유효한 검색조건 2 : ', "GetStockTradeInfo(종목코드, 시작일자, 종료일자)" ) 
#         print('유효한 검색조건 3 : ', "GetStockTradeInfo(종목명, 시작일자, 종료일자)" ) 


        
# def GetFinancialInfo(year, fiscalgubun, currentPageSize = 100):
#     columns = ['종목코드','종목명','유동자산','고정자산','자산총계','유동부채','고정부채','부채총계','자본금',
#                '자본잉여금','이익잉여금','자본총계','매출액','영업이익','세전이익','당기순이익']
    
#     resData = []

#     urlTmp = "https://kind.krx.co.kr/compfinance/financialinfo.do?method=searchFinancialInfoWithRange&forward=list"
#     urlTmp += "&finsearchtype=finstat&titleofaccnt=A010%7CA040%7CA080%7CA090%7CA100%7CA110%7CA120%7CA130%7CA140%7CA160%7CA170%7CA180%7CA190%7CA200"
#                                                 # A010|A040|A080|A090|A100|A110|A120|A130|A140|A160|A170|A180|A190|A200
#     # urlTmp += "&orderMode=A080&orderStat=D"  # 자산총계 역순 정렬 (생략)    
#     urlTmp += "&fromDate=&toDate="
#     urlTmp += "&A010=checkbox&a010_from=&a010_to=" # 유동자산
#     urlTmp += "&A040=checkbox&a040_from=&a040_to=" # 고정자산
#     urlTmp += "&A080=checkbox&a080_from=&a080_to=" # 자산총계
#     urlTmp += "&A090=checkbox&a090_from=&a090_to=" # 유동부채
#     urlTmp += "&A100=checkbox&a100_from=&a100_to=" # 고정부채
#     urlTmp += "&A110=checkbox&a110_from=&a110_to=" # 부채총계
#     urlTmp += "&A120=checkbox&a120_from=&a120_to=" # 자본금
#     urlTmp += "&A130=checkbox&a130_from=&a130_to=" # 자본잉여금
#     urlTmp += "&A140=checkbox&a140_from=&a140_to=" # 이익잉여금
#     urlTmp += "&A160=checkbox&a160_from=&a160_to=" # 자본총계
#     urlTmp += "&A170=checkbox&a170_from=&a170_to=" # 매출액
#     urlTmp += "&A180=checkbox&a180_from=&a180_to=" # 영업이익
#     urlTmp += "&A190=checkbox&a190_from=&a190_to=" # 세전이익
#     urlTmp += "&A200=checkbox&a200_from=&a200_to=" # 당기순이익
#     urlTmp += "&acntgType=I&isfirst=false&marketType=all&industry="
#     urlTmp += "&currentPageSize={}&fiscalyear={}&fiscalgubun={}".format(currentPageSize, year, fiscalgubun)
#     urlTmp += "&pageIndex={}"


#     pgNum = 1
#     while True:                
#         # res = req.get(url)
#         url = urlTmp.format(pgNum)
#         res = urlProc.requests_url_call(url)

#         soup = bs(res.text, "html.parser")

#         trs = soup.tbody.select("tr")
#         for tr in trs:    
#             tds = tr.select("td")

#             for idx, td in enumerate(tds):
#                 if idx == 1:
#                     shcode = td.select_one("a#companysum").get("onclick").split("'")[1]
#                     if len(shcode) == 5:
#                         shcode += '0'
#                     title = td.select_one("a#companysum").get("title")
                    
#                     trVal = [shcode, title]
                    
#                 elif idx > 1:        
                    
#                     val = re.sub(r"[^0-9]", "", td.text.strip())
                    
#                     if len(val) > 0:
#                         val = int(val)
#                     else:
#                         val = 0
                                
#                     trVal.append(val)

#             resData.append(trVal)

#         x=soup.select_one("section.paging-group div.info strong")
#         curNum = int(x.text)
#         totNum = int(x.next_sibling.split("/")[1].split("\xa0")[0])
        
#         if curNum >= totNum:
#             break

#         pgNum += 1

#         time.sleep(0.1)
    
#     return resData, columns