from ..outerIO  import marketIndex as o_mi
from ..innerIO  import marketIndex as i_mi

# def syncBalticIndex(sDate, eDate):
#     df = o_mi.GetBalticIndex(sDate, eDate)

#     newData = df.values.tolist()
#     indexList = df.columns.tolist()[1:]    

#     for i in range(len(indexList)):
#         i_mi.SaveMarketIndex(indexList[i], [[data[0], data[i+1]] for data in newData])    


def syncMarketIndex(mIndexNm, sDate, eDate):
    
    if mIndexNm in ['BDI', 'BCI', 'BSI', 'BPI']:
        dfNew = o_mi.GetBalticIndex(sDate, eDate)  
        for mIndexNm in ['BDI', 'BCI', 'BSI', 'BPI']:
            i_mi.SaveMarketIndex(mIndexNm, dfNew[['일자',mIndexNm]])             
    else:
        dfNew = o_mi.GetNaverMarketIndex(mIndexNm, sDate, eDate)
        i_mi.SaveMarketIndex(mIndexNm, dfNew)              