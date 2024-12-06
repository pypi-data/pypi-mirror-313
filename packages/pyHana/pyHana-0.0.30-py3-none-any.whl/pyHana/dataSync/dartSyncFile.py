import pandas as pd
import pickle
import math
import gzip

# 결산기준일 변환 함수 SET_DT(2023,2) => 2023-06-30
SET_DT = lambda year, quarter : str(year)+'-'+"%02d"%(quarter * 3)+'-'+'%2d'%(31 if quarter in(1,4) else 30)

FILE_COLUMNS = {
            "02_손익계산서" :    {
                "1분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 1분기 3개월","당기 1분기 누적",
                                "전기 1분기 3개월","전기 1분기 누적","전기","전전기"],
                "반기보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 반기 3개월", "당기 반기 누적",
                                "전기 반기 3개월","전기 반기 누적","전기","전전기"],
                "3분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 3분기 3개월","당기 3분기 누적",
                                "전기 3분기 3개월","전기 3분기 누적","전기","전전기"],
                "사업보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기","전기","전전기"]
            },
            "02_손익계산서_연결" :    {
                "1분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 1분기 3개월","당기 1분기 누적",
                                "전기 1분기 3개월","전기 1분기 누적","전기","전전기"],
                "반기보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 반기 3개월", "당기 반기 누적",
                                "전기 반기 3개월","전기 반기 누적","전기","전전기"],
                "3분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 3분기 3개월","당기 3분기 누적",
                                "전기 3분기 3개월","전기 3분기 누적","전기","전전기"],
                "사업보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기","전기","전전기"]
            },    
            "03_포괄손익계산서" : {
                "1분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 1분기 3개월","당기 1분기 누적",
                                "전기 1분기 3개월","전기 1분기 누적","전기","전전기"],
                "반기보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 반기 3개월", "당기 반기 누적",
                                "전기 반기 3개월","전기 반기 누적","전기","전전기"],
                "3분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 3분기 3개월","당기 3분기 누적",
                                "전기 3분기 3개월","전기 3분기 누적","전기","전전기"],
                "사업보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기","전기","전전기"]

            },    
            "03_포괄손익계산서_연결" : {
                "1분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 1분기 3개월","당기 1분기 누적",
                                "전기 1분기 3개월","전기 1분기 누적","전기","전전기"],
                "반기보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 반기 3개월", "당기 반기 누적",
                                "전기 반기 3개월","전기 반기 누적","전기","전전기"],
                "3분기보고서" : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기 3분기 3개월","당기 3분기 누적",
                                "전기 3분기 3개월","전기 3분기 누적","전기","전전기"],
                "사업보고서"  : ["재무제표종류","종목코드","회사명","시장구분","업종","업종명","결산월","결산기준일","보고서종류","통화","항목코드","항목명","당기","전기","전전기"]

            }
        }

class DART:
    def __init__(self, file_path):
        """
        Args:
            (str) file_path : DART 일괄다운로드 파일 위치        
        """ 
        if file_path.endswith('/'):
            self.file_path = file_path
        else:
            self.file_path = file_path + '/'
        
        self.dartInfoDict = self._ReadFinalcialInfo()
        
    
    def _Pandas_ReadCsv_DartFile(self, year, quarter, reportKnd):
        """DART에서 제공하는 재무정보 일괄 다운로드 파일 읽기

        Args:
            (int) year               : 공시 년도
            (int) quarter            : 공시 분기 (1, 2, 3, 4)
            (str) reportKnd          : 재무정보 종류 ("02_손익계산서", "03_포괄손익계산서" )
        """        
                
        periodKnd = list(FILE_COLUMNS[reportKnd])[quarter-1] # quarter : 1(1분기보고서), 2(반기보고서), 3(3분기보고서), 4(사업보고서)
        fileNm = self.file_path + "%s_"%(year) + periodKnd + "_" + reportKnd + '.txt'
        print(fileNm, flush=True)
        
        try:    
            dfData = pd.read_csv(fileNm, sep='\t', engine='python', encoding='CP949', usecols=FILE_COLUMNS[reportKnd][periodKnd])
        except:
            dfData = pd.read_csv(fileNm, sep='\t', engine='python', encoding='utf-8', usecols=FILE_COLUMNS[reportKnd][periodKnd])
            
        return dfData

    def GetFinancialDataFromDartFile(self, year, quarter):
        """DART에서 제공하는 재무정보 일괄 다운로드 파일("02_손익계산서", "03_포괄손익계산서" ) 내용 중
           매출액, 영업이익, 당기순이익, 총포괄손익 정보 추출하여 DataFrame 형태로 반환
        
        Args:
            (int) year               : 공시 년도
            (int) quarter            : 공시 분기 (1, 2, 3, 4)
        반환항목:
            종목코드, 회사명, 매출액, 영업이익, 법인세전이익, 법인세, 당기순이익,
            총포괄손익, 총포괄(손익)_소유주(지분),'총포괄(손익)_비지배(지분)'
        """             
        if quarter == 1:        valueColumn = '당기 1분기 3개월'
        elif quarter == 2:      valueColumn = '당기 반기 3개월'
        elif quarter == 3:      valueColumn = '당기 3분기 3개월'
        elif quarter == 4:      valueColumn = '당기'

        dfSum = pd.DataFrame({})

        for reportKnd in ["03_포괄손익계산서_연결", "02_손익계산서_연결", "03_포괄손익계산서", "02_손익계산서"]:
            # (연결)손익계산서에 정보가 없는 경우를 대비해 (삼성전자 2019년 1,2분기 매출액 등)
            # 낮은 우선순위로 (일반)손익계산서 반영
            if reportKnd in ( "02_손익계산서", "03_포괄손익계산서" ):
                addPriority = 10
            else:
                addPriority = 0

            dfData = self._Pandas_ReadCsv_DartFile(year, quarter, reportKnd)

            # 데이터 클린징
            dfData = dfData.dropna(subset=[valueColumn], how='any', axis=0)
            dfData['종목코드'] = dfData['종목코드'].str.replace(']','').str.replace('[','')            
            dfData['항목명'] = dfData['항목명'].str.strip().str.replace('.','').str.replace(' ','').str.replace('I','')

            # 보고서별 항목명이 달라서 value로 통일
            dfData['value']  = dfData[valueColumn]

            # 각 항목별 데이터가 일관되게 작성되어 있지 않아 손익계산서와 포괄손익 계산서를 merge하여 구함
            # 우선순위 : 항목코드 정확하게 매칭(1순위), 검증결과 해당 항목으로 추정되는 항목명(2순위)            
            extCond = [ 
                 {"통합계정명" : "매출액",       "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_Revenue','ifrs_Revenue'] ] } 
                ,{"통합계정명" : "매출액",       "우선순위" : 2, "조건" : [ "항목명"  ,  ['매출', '영업수익', '매출액', '영업수익(매출액)','영업수익'] ] }
                ,{"통합계정명" : "영업이익",     "우선순위" : 1, "조건" : [ "항목명"  ,  ['영업이익'] ] }
                ,{"통합계정명" : "영업이익",     "우선순위" : 2, "조건" : [ "항목코드",  ['dart_OperatingIncomeLoss'] ] }
                ,{"통합계정명" : "당기순이익",   "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_ProfitLoss','ifrs_ProfitLoss'] ] }
                ,{"통합계정명" : "당기순이익",   "우선순위" : 2, "조건" : [ "항목명",    ['당기순이익', '연결당기순이익', '연결분기순이익', '연결분기순이익(손실)', '분기순손익', '분기순이익'] ] }
                ,{"통합계정명" : "당기순이익",   "우선순위" : 3, "조건" : [ "항목명end", '분기순이익(손실)' ] }  # endswith는 배열처리 
                ,{"통합계정명" : "법인세전이익", "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_ProfitLossBeforeTax','ifrs_ProfitLossBeforeTax'] ] } 
                ,{"통합계정명" : "법인세",       "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_IncomeTaxExpenseContinuingOperations','ifrs_IncomeTaxExpenseContinuingOperations'] ] }                                                                                        
                ,{"통합계정명" : "총포괄손익",   "우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_ComprehensiveIncome','ifrs_ComprehensiveIncome'] ] }
                ,{"통합계정명" : "총포괄손익",   "우선순위" : 2, "조건" : [ "항목명",    ['당기총포괄손익', '당기총포괄이익(손실)', '분기연결총포괄이익(손실)', '분기총포괄손익', '분기총포괄이익(손실)',
                                                                                        '연결포괄이익', '연결총포괄손익', '연결총포괄이익(손실)', '총포괄이익(손실)'] ] }
                ,{"통합계정명" : "총포괄_소유주","우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_ComprehensiveIncomeAttributableToOwnersOfParent','ifrs_ComprehensiveIncomeAttributableToOwnersOfParent'] ] }                                                                                         
                ,{"통합계정명" : "총포괄_소유주","우선순위" : 2, "조건" : [ "항목명",    ['지배지분총포괄이익'] ] }
                ,{"통합계정명" : "총포괄_비지배","우선순위" : 1, "조건" : [ "항목코드",  ['ifrs-full_ComprehensiveIncomeAttributableToNoncontrollingInterests','ifrs_ComprehensiveIncomeAttributableToNoncontrollingInterests'] ] }                                                                                         
                ,{"통합계정명" : "총포괄_비지배","우선순위" : 2, "조건" : [ "항목명",    ['비지배지분총포괄이익'] ] }        
            ]    
            for idx in range(0, len(extCond)): 
                if extCond[idx]["조건"][0] == "항목명end":
                    cond = ( dfData["항목명"].str.endswith(extCond[idx]["조건"][1]) )
                else:
                    cond = ( dfData[extCond[idx]["조건"][0]].isin(extCond[idx]["조건"][1]) )

                # 3월 결산 기준일 회사 제외 (사업보고서에 전년 4월 ~ 당해 3월 데이터 반영)
                cond = cond & ( dfData["결산기준일"] == SET_DT(year, quarter) )
                

                dfTemp = dfData[cond] [['종목코드','회사명', '결산기준일', 'value']]
                dfTemp['통합계정명'] = extCond[idx]["통합계정명"]
                dfTemp['우선순위']   = extCond[idx]["우선순위"] + addPriority
                                
                dfSum = pd.concat([dfSum, dfTemp])    

        dfSum['value'] = dfSum['value'].str.replace(',','').astype(dtype='int64')
        dfSum = dfSum.sort_values('우선순위').groupby(['종목코드','회사명','결산기준일','통합계정명']).first().reset_index()
        dfRes = pd.pivot_table(dfSum, values='value', index=['종목코드','회사명','결산기준일'], columns=['통합계정명'], aggfunc='sum'
                              ).reset_index()[['종목코드','회사명','결산기준일','매출액','영업이익','당기순이익','법인세전이익','법인세',
                                               '총포괄손익','총포괄_소유주','총포괄_비지배']]
        
        # dataframe을 dictionary로 변환, 저장 후 반환
        self._MergeIntoFinincialInfo(dfRes)


    def _MergeIntoFinincialInfo(self, data):
        """DART에서 제공하는 재무정보 일괄 다운로드 파일 읽어, 주요 정보 데이터 추출 후 (GetFinancialDataFromDartFile 모듈)
           기존 저장된 dictionary 데이터에 merge 수행
           최종 결과는 pickle에 저장하고, 
           Class변수 self.dartInfoDict에 저장

        Args:
            (dataframe) data : DART에서 제공하는 재무정보 일괄 다운로드 파일 읽어, 주요 정보 데이터 추출 후 dataframe 형태로 저장
        """                
            
        dartInfoDict = self.dartInfoDict

        for i in range(0, len(data)):
            shCode = data.iloc[i]["종목코드"]
            setDt = data.iloc[i]["결산기준일"]

            if not dartInfoDict.get(shCode):
                dartInfoDict[shCode] = {}
                dartInfoDict[shCode]['회사명'] = data.iloc[i]["회사명"]

            if not dartInfoDict[shCode].get("결산기준일"):
                dartInfoDict[shCode]["결산기준일"] = {}

            dartInfoDict[shCode]["결산기준일"][setDt] = {}

            # 1. 매출액
            if not math.isnan(data.iloc[i]['매출액']):
                dartInfoDict[shCode]["결산기준일"][setDt]["매출액"] = data.iloc[i]['매출액']
            # 2. 영업이익    
            if not math.isnan(data.iloc[i]['영업이익']):
                dartInfoDict[shCode]["결산기준일"][setDt]["영업이익"] = data.iloc[i]['영업이익']
            # 3. 당기순이익    
            if not math.isnan(data.iloc[i]['당기순이익']):
                dartInfoDict[shCode]["결산기준일"][setDt]["당기순이익"] = data.iloc[i]['당기순이익']
            # 당기순이익 제출하지 않은 경우 법인세전이익과 법인세로 계산   
            elif not math.isnan(data.iloc[i]['법인세전이익']):
                profitLoss = data.iloc[i]['법인세전이익']
                if not math.isnan(data.iloc[i]['법인세']):
                    profitLoss -= data.iloc[i]['법인세']
                dartInfoDict[shCode]["결산기준일"][setDt]["당기순이익"] = profitLoss
            # 4. 총포괄손익    
            if not math.isnan(data.iloc[i]['총포괄손익']):
                dartInfoDict[shCode]["결산기준일"][setDt]["총포괄손익"] = data.iloc[i]['총포괄손익']
            # 총포괄손익 제출하지 않은 경우 총포괄_소유주지분과 총포괄_비지배지분으로 계산   
            elif not math.isnan(data.iloc[i]['총포괄_소유주']):
                comprehensiveIncome = data.iloc[i]['총포괄_소유주']
                if not math.isnan(data.iloc[i]['총포괄_비지배']):
                    comprehensiveIncome += data.iloc[i]['총포괄_비지배']
                dartInfoDict[shCode]["결산기준일"][setDt]["총포괄손익"] = comprehensiveIncome    

        # 최종 결과 pickle 파일에 저장
        self._WriteFinalcialInfo(dartInfoDict)

        # 
        self.dartInfoDict = dartInfoDict

    def _ReadFinalcialInfo(self):
        # load            
        try:
            with gzip.open(self.file_path + 'dart_financial_info.pickle', 'rb') as f:
                data = pickle.load(f)
        except:
            print('pickle file load error >> ', self.file_path + 'dart_financial_info.pickle')
            data = {}
                
        return data

    def _WriteFinalcialInfo(self, data):
        # save
        # with gzip.open(self.file_path + 'dart_financial_info.pickle', 'wb') as f:
        with gzip.open(self.file_path + 'dart_financial_info.pickle', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def GetCompanyFinInfoDataFrame(self, shCode, unit="억"):

        df = pd.DataFrame([])
        for idx, acct in enumerate(['매출액','영업이익','당기순이익','총포괄손익']):
            data = self.GetCompanyAcctFinInfo(shCode, acct, unit="억")
            data = list(zip(*data))
            if idx ==0 :
                df['결산기준일'] = pd.DataFrame(data[0])

            df[acct] = pd.DataFrame(data[1])
        
        return df
           

    def GetCompanyAcctFinInfo(self, shCode, acct, unit="억"):
        acct_list = ['매출액','영업이익','당기순이익','총포괄손익']
        unit_list = {'천' : 1000, '만' : 10000, '백만' : 1000000, '천만' : 10000000, '억' : 100000000, '십억' : 1000000000, '조' : 1000000000000 }
        data = []
        
        if acct not in acct_list:
            print('유효하지 않은 계정과목 > ', acct)
            print('선택가능한 계정과목 > ', acct_list)
        elif not unit_list.get(unit):
            print('유효하지 않은 금액단위 > ', unit)
            print('선택가능한 금액단위 > ', unit_list.keys())        
        elif self.dartInfoDict.get(shCode):
            if self.dartInfoDict[shCode].get('결산기준일'):
                for ymd in sorted(self.dartInfoDict[shCode]['결산기준일'].keys()):
                    data.append([ymd, self.dartInfoDict[shCode]['결산기준일'][ymd][acct], unit])
                
        # 사업보고서(4분기)에는 1년 합계 데이터가 있어, 이전 3개 분기의 데이터 필요
        # 결산기준일 기준으로 정렬하여 추출한 결과값에 대해, 1분기부터 시작하는지, 중간에 누락된 분기는 없는지 확인하여
        # 누락 발견 시 오류메시지 출력하고 null값 반환
        if len(data) > 0:
            for i in range(0, len(data)):
                if i == 0:
                    year = int(data[i][0][0:4])
                    
                if  (year + int(i / 4)) != int(data[i][0][0:4]) or \
                    (i % 4) == 0 and data[i][0][5:10] != '03-31' or \
                    (i % 4) == 1 and data[i][0][5:10] != '06-30' or \
                    (i % 4) == 2 and data[i][0][5:10] != '09-30' or \
                    (i % 4) == 3 and data[i][0][5:10] != '12-31':
                        
                    print('누락된 분기보고서 오류 > ', i + 1, "번째 데이터")
                    print(data)
                    date = []
                    break
                    
                if (i % 4) == 3:   # 사업보고서(년 누적)인 경우 이전 3분기 값 차감 보정
                    data[i][1] = data[i][1] - data[i-1][1] - data[i-2][1] - data[i-3][1]  
                    
            for i in range(0, len(data)):
                data[i][1] = int(round(data[i][1] / unit_list[unit], 0))
        return data            