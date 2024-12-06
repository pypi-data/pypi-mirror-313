from ..outerIO  import naver       as o_naver
from ..innerIO  import companyInfo as i_company
import pandas as pd

   
def syncBizCategoryInfo(prtInd=False):
    # # 업종 리스트
    dfBizList = o_naver.getBizCategory()
    i_company._SaveBizCategory(dfBizList)
    print('업종 리스트 현행화 완료')
    
    # # 업종별 종목 리스트
    dfBizList = o_naver.getBizDetail(dfBizList[['업종명','linkNo']], prtInd=prtInd)
    i_company._SaveBizDetail(dfBizList)
    print('\r'+'업종별 종목 상세 현행화 완료',' '*50)    
    
   
def syncThemeInfo(prtInd=False):
    # # 테마 리스트
    dfThemeList = o_naver.getTheme()
    i_company._SaveTheme(dfThemeList)
    print('테마 리스트 현행화 완료')
    
    # # 테마별 종목 리스트
    dfThemeList = o_naver.getThemeDetail(dfThemeList[['테마명','linkNo']], prtInd=prtInd)
    i_company._SaveThemeDetail(dfThemeList)
    print('\r'+'테마별 종목 상세 현행화 완료',' '*50)        