import pickle
import os
import gzip

def ReadPickleFile(filePathNm, gzipInd=True):
    try:
        if gzipInd:
            with gzip.open(filePathNm, 'rb') as f:
                retVal = pickle.load(f)      
        else:
            with open(filePathNm, 'rb') as f:
                retVal = pickle.load(f)      
    except:
        retVal = {}
    
    return retVal

def WritePickleFile(filePathNm, currData, gzipInd=True):
    dirName = os.path.dirname(filePathNm)
    if not os.path.isdir(dirName):
        os.makedirs(dirName, exist_ok=True)

    if gzipInd:
        with gzip.open(filePathNm, 'wb') as f:
            pickle.dump(currData, f)       
    else:
        with open(filePathNm, 'wb') as f:
            pickle.dump(currData, f)           


def WriteTextFile(filePathNm, currData):    
    dirName = os.path.dirname(filePathNm)
    if not os.path.isdir(dirName):
        os.makedirs(dirName, exist_ok=True)

    f = open(filePathNm, 'w', encoding="utf8")
    f.write(currData)
    f.close()
    

def _MergeData(currData, newData, sortCols=1):
    # print('>>>>>>>>>>>> ', len(currData), len(newData))
    # sortCols 병합 시 중복 판단 기준 컬럼 수(앞에서부터)
    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 후 sort
    totList = [ x[0:sortCols] + [2] + x[sortCols:] for x in currData ] \
            + [ x[0:sortCols] + [1] + x[sortCols:] for x in newData ]
    
    # print(currData)
    # print(newData)
    # print(totList)
    
    totList.sort()
    # print(totList[0:5])

    # 중복데이터 제거 및 임시 우선순위 삭제
    noDupList = [ data[0:sortCols] + data[(sortCols+1):] 
                 for idx, data in enumerate(totList) if idx == 0 or data[0:sortCols] > totList[idx-1][0:sortCols] 
                ] 
    # print('>>>>>>>>>>>> ', len(currData), len(newData), len(totList), len(noDupList))

    return noDupList