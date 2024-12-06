import win32com.client
import pythoncom
import pandas as pd
import time
import datetime as dt
import sys, os

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
from   ..common  import conf

# 압축
COMP_Y_TRCODE = ['t8410','t8411','t8412','t8413','t8414','t8415','t8416','t8417','t8418','t8419']
# COMP_Y_TRCODE = []

# 개발가이드에 t8413, t8410의 nextkey가 OutBlock(cts_date)로 정의되어 있으나, 데이터 값이 정상적으로 반환되지 않아서,
# 실제로는 OutBlock1(cts_date) 사용
nextKeys = {
            "t1305": { "InBlock": ["t1305InBlock",  "date"],      "OutBlock": ["t1305OutBlock", "date"     ]  },
            "t1486": { "InBlock": ["t1486InBlock",  "cts_time"],  "OutBlock": ["t1486OutBlock", "cts_time" ]  },
            "t1444": { "InBlock": ["t1444InBlock",  "idx"],       "OutBlock": ["t1444OutBlock", "idx"      ]  },
            "t1516": { "InBlock": ["t1516InBlock",  "shcode"],    "OutBlock": ["t1516OutBlock", "shcode"   ], "Sort": "ASC"  },
            "t3518": { "InBlock": ["t3518InBlock",  "cts_date"],  "OutBlock": ["t3518OutBlock", "cts_date" ]  },
            "t8410": { "InBlock": ["t8410InBlock",  "cts_date"],  "OutBlock": ["t8410OutBlock1", "date"    ], "Sort": "ASC"  },
            "t8413": { "InBlock": ["t8413InBlock",  "cts_date"],  "OutBlock": ["t8413OutBlock1", "date"    ], "Sort": "ASC"  }
            }
# 기간 검색 조건이 InBlock에 없는 경우 stopKey에 등록하여 처리
# 
stopKeys = {
            "t3518": { "Block": "t3518OutBlock1",  "column": "date", 'posision':"LAST" },
            }

def funcname():
    return sys._getframe(1).f_code.co_name + "()"
def callername():
    return sys._getframe(2).f_code.co_name + "()"

def GetDataColumn(trCode):
    
    field_list  = {}
    field_list[trCode] = {}
    field_list[trCode]['input'] = {}
    field_list[trCode]['output'] = {}

    # with open("C:/eBest/xingAPI/Res/" + trCode + '.res', 'r') as f:
    # with open(conf.xingAPIRes + '/' + trCode + '.res', 'r') as f:
    #     text = f.readlines()
    try:    
        with open(conf.xingAPIRes + '/' + trCode + '.res', 'r', encoding='CP949') as f:
            text = f.readlines()
    except:
        with open(conf.xingAPIRes + '/' + trCode + '.res', 'r', encoding='utf-8') as f:
            text = f.readlines()


    fr_list = []
    to_list = []
    for idx, line in enumerate(text):
        if line.strip() == 'begin':
            fr_list.append(idx)
        if line.strip() == 'end':
            to_list.append(idx)
            
    for i in range(len(fr_list)):
        block_header = text[fr_list[i] - 1].strip().replace(';','').split(',')
        blockNm = block_header[0]
        inOutKnd = block_header[2]
        
        field_list[trCode][inOutKnd][blockNm] = {}
        if len(block_header) == 4 and block_header[3] == 'occurs':
            field_list[trCode][inOutKnd][blockNm]['OCCURS'] = 'Y'
        else:
            field_list[trCode][inOutKnd][blockNm]['OCCURS'] = 'N'

        korColList = []
        engColList = []

        for j in range(fr_list[i] + 1, to_list[i]):
            x = text[j].strip().replace(' ','').split(',')

            korColList.append(x[0])
            engColList.append(x[1])

        field_list[trCode][inOutKnd][blockNm]['kor'] = korColList
        field_list[trCode][inOutKnd][blockNm]['eng'] = engColList            
        
    return field_list
        
class XAEventHandler:
    login_state = 0
    query_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print(msg, code, flush=True)
            XAEventHandler.login_state = 1
        else:
            print("로그인 실패", code, msg, flush=True)

    def OnReceiveData(self, code):
        XAEventHandler.query_state = 1    

    # def OnDisconnect(self):
    #     print("Session Disconnect....", flush=True)
    #     XAEventHandler.login_state = 0


class Ebest:
    def __init__(self, login=False, debug=False):

        self.debug = debug
        self.instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XAEventHandler)
    
        if login:
            self.CommConnect()

            self.next_keys = nextKeys
            # with open('next_keys.json') as f:
            #     self.next_keys = json.load(f)
        # with open('field_list.pkl', 'rb') as f:
        #     self.field_list = pickle.load(f)       
                   

    def CommConnect(self):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
      
        id = conf.ebestId
        passwd = conf.ebestPwd
        cert_passwd = conf.certPwd

        self.instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
        self.instXASession.Login(id, passwd, cert_passwd, 0, 0)

        while XAEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()

        num_account = self.instXASession.GetAccountListCount()
        for i in range(num_account):
            account = self.instXASession.GetAccountList(i)
            print(account)

    def CommDisConnect(self):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())

        self.instXASession.DisconnectServer()
        XAEventHandler.login_state = 0

    def _GetDataFrameKor(self, instXAQuery, blockNm):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
        # print(instXAQuery[blockNm]['kor'])
        return pd.DataFrame(instXAQuery[blockNm]['data'], columns=instXAQuery[blockNm]['kor'])


    def GetBlockData(self, *args, **kwargs):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
        
        trCode = args[0]        
        inBlockNm = args[1] 
        field_list = args[2] 
      
        XAEventHandler.query_state = 0     
        instXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAEventHandler)
        # instXAQuery.ResFileName = "C:\\eBEST\\xingAPI\\Res\\" + trCode + ".res"
        instXAQuery.ResFileName = conf.xingAPIRes + "/" + trCode + ".res"
        
        for key, value in kwargs.items():
            if key not in ( 'SLEEPTIME' ):    # 내부 처리 용도로만 사용
                instXAQuery.SetFieldData(inBlockNm, key, 0, value)      

        if trCode in COMP_Y_TRCODE:
            instXAQuery.SetFieldData(inBlockNm, "comp_yn", 0, "Y")

        # 초당 전송 가능 횟수에 따른 sleep
        trCountPerSec = instXAQuery.GetTRCountPerSec(trCode)
        if self.debug: print(dt.datetime.now(), ' > ',  '초당건수 : ', trCountPerSec)

        # 10분에 200건 제한을 위해 대량 호출 시 SLEEPTIME 사용
        sleepTime = kwargs.get('SLEEPTIME', 0)
        if sleepTime > 0:
            time.sleep(sleepTime)
        else: 
            if trCountPerSec > 0:
                time.sleep(1 / trCountPerSec)     
        
        # 10분당 전송 횟수 초과하지 않도록 대기
        # trCountLimit = instXAQuery.GetTRCountLimit(trCode)
        # sleep_cnt = 0
        # while trCountLimit > 0 and (instXAQuery.GetTRCountRequest(trCode) * 10) >= trCountLimit:
        #     if sleep_cnt >= 10:
        #         raise UserWarning("기간별 호출제한 대기 > 제한건수(", trCountLimit, '), 호출건수(', instXAQuery.GetTRCountRequest(trCode), ')')

        #     time.sleep(60)
        #     sleep_cnt += 1            
        #     print('\r', dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '(TR)', trCode, '(Sleep)', sleep_cnt, 
        #           '제한건수', trCountLimit, '호출건수', instXAQuery.GetTRCountRequest(trCode),
        #           '\r', end='', flush=True)
            

        instXAQuery.Request(True)    
        
        while XAEventHandler.query_state == 0:
            pythoncom.PumpWaitingMessages()

        ###  test test
        for trBlockNm in list(field_list[trCode]['output'].keys()):
            if trCode in COMP_Y_TRCODE and field_list[trCode]['output'][trBlockNm]['OCCURS'] == 'Y':
                nDecompSize = instXAQuery.Decompress(trBlockNm)
                if nDecompSize <= 0:
                    print('Invalid Block Info ', trCode, trBlockNm)

        return instXAQuery
    
    def GetTrData(self, *args, **kwargs):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())

        trCode = args[0]        
        field_list = GetDataColumn(trCode)
        inBlockNm = list(field_list[trCode]['input'].keys())[0]
        
        instXAQuery = self.GetBlockData(trCode, inBlockNm, field_list, **kwargs)

        return self.GetFieldData(trCode, [instXAQuery], field_list)
    

    def GetTrDataOccurs(self, *args, **kwargs):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())

        instXAQueryArray = []
        trCode = args[0]
        field_list = GetDataColumn(trCode)
       
        inBlockNm  = self.next_keys[trCode]['InBlock'][0]
        inFieldNm  = self.next_keys[trCode]['InBlock'][1]
        OutBlockNm = self.next_keys[trCode]['OutBlock'][0]
        OutFieldNm = self.next_keys[trCode]['OutBlock'][1]
 
        ## Max Multi Block Cnt (default 100)
        maxCnt     = kwargs.get('MaxCallCnt', 100)
        getCnt     = 0

        occursBlockNm = [i for i in field_list[trCode]['output'].keys() if field_list[trCode]['output'][i]['OCCURS'] in ('Y')][0]

        srchCond = {}        
        searchRange = kwargs.get('SEARCHRANGE', []) # INBLOCK에 기간 검색조건이 없는 경우 별도 처리

        for key, value in kwargs.items():
            if key not in ('MaxCallCnt', 'SEARCHRANGE'):
                srchCond[key] = value

        if trCode in COMP_Y_TRCODE:
            srchCond['cts_date'] = srchCond['edate']
        elif  trCode in ('t3518'):               
            # INBLOCK에 기간 검색조건이 없는 경우 별도 처리
            srchCond['cts_date'] = (dt.datetime.strptime(searchRange[1], "%Y%m%d") + dt.timedelta(days=1)).strftime("%Y%m%d") 

        instXAQuery = self.GetBlockData(trCode, inBlockNm, field_list, **srchCond)
        # print('xxx >' , instXAQuery.GetBlockCount(occursBlockNm))
        while getCnt < maxCnt and \
            ( 
              trCode not in COMP_Y_TRCODE and instXAQuery.GetBlockCount(occursBlockNm) > 0 or
              trCode     in COMP_Y_TRCODE and int(instXAQuery.GetFieldData(trCode+"OutBlock", "rec_count", 0)) > 0
            ):

            retValueFirst = instXAQuery.GetFieldData(OutBlockNm, OutFieldNm, 0)
            
            if trCode in ('t8410', 't8413') and \
               ( retValueFirst < srchCond['sdate'] or retValueFirst > srchCond['cts_date'] ):
            #    ( retValueFirst < kwargs['sdate'] or retValueFirst > kwargs['edate'] ):
                break 

            # 결과값으로 return할 array에 저장
            instXAQueryArray.append(instXAQuery)      

            getCnt += 1

            nextValue = retValueFirst
            
            if trCode in ('t8410', 't8413'):
                nextValue = (dt.datetime.strptime(nextValue, "%Y%m%d") - dt.timedelta(days=1)).strftime("%Y%m%d")     
                if nextValue < kwargs['sdate'] or nextValue > kwargs['edate']:
                    break 
                else:
                    srchCond['edate'] = nextValue
                    srchCond['cts_date'] = nextValue

            # INBLOCK에 기간 검색조건이 없는 경우 별도 로직으로 처리
            if trCode in ('t3518'):
                if stopKeys[trCode]['posision'] == 'FIRST':
                    idx = 0
                else:
                    idx = instXAQuery.GetBlockCount(occursBlockNm) - 1

                # print('------------------------------------------------------')
                # print(stopKeys[trCode]['Block'], stopKeys[trCode]['column'], idx)
                # print(instXAQuery.GetFieldData(stopKeys[trCode]['Block'], stopKeys[trCode]['column'], idx))
                # print(searchRange[0] , searchRange[1])

                curVal = instXAQuery.GetFieldData(stopKeys[trCode]['Block'], stopKeys[trCode]['column'], idx)
                if curVal < searchRange[0] or searchRange[1] < curVal:
                    break

            if getCnt < maxCnt:
                srchCond[inFieldNm] = nextValue
                
                instXAQuery = self.GetBlockData(trCode, inBlockNm, field_list, **srchCond)
 
        return self.GetFieldData(trCode, instXAQueryArray, field_list)

    def GetFieldData(self, trCode, instDataArray, field_list):
        if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())

        returnData = {}

        ## Block내 data순서와 Block간의 SORT가 방식이 다른 경우 전처리
        if len(self.next_keys.get(trCode,'')) > 0 and \
           self.next_keys[trCode].get('Sort', '') == 'ASC':
            temp = []
            for i in range(len(instDataArray), 0, -1):
                temp.append(instDataArray[i-1])
            instDataArray = temp

        ## OutBlock, OutBlock1 등 모든 Block에 대해 필드별 데이터 추출 후 결과 return
        for trBlockNm in list(field_list[trCode]['output'].keys()):
            returnData[trBlockNm] = {}
            returnData[trBlockNm]['kor'] = field_list[trCode]['output'][trBlockNm]['kor']
            returnData[trBlockNm]['eng'] = field_list[trCode]['output'][trBlockNm]['eng']
            returnData[trBlockNm]['data'] = []

            for instData in instDataArray:
                for i in range(instData.GetBlockCount(trBlockNm)):
                    fieldData = []
                    
                    for j in range(len(returnData[trBlockNm]['eng'])):
                        fieldData.append(instData.GetFieldData(trBlockNm, returnData[trBlockNm]['eng'][j], i))

                    returnData[trBlockNm]['data'].append(fieldData)

        return returnData    

    # def GetListData(self, instXAQuery, blockNm):
    #     if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
    #     return instXAQuery[blockNm]['data']

    # def _GetDataFrameKor(self, instXAQuery, blockNm):
    #     if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
    #     return pd.DataFrame(instXAQuery[blockNm]['data'], columns=instXAQuery[blockNm]['kor'])

    # def GetDataFrameEng(self, instXAQuery, blockNm):
    #     if self.debug: print(dt.datetime.now(), ' > ',  callername(), ' > ', funcname())
    #     return pd.DataFrame(instXAQuery[blockNm]['data'], columns=instXAQuery[blockNm]['eng'])
    
    def GetStockItemList(self, gubun):
        """
        gubun : '0'(전체) 1'(코스피) '2'(코스닥)             
        """
        dfStock = pd.DataFrame([])  

        if gubun in ('1','0'):
            instXAQuery = self.GetTrData('t9945', gubun = '1')
            dfStock = pd.concat([dfStock, self._GetDataFrameKor(instXAQuery, 't9945OutBlock')], ignore_index=True)

        if gubun in ('2','0'):
            instXAQuery = self.GetTrData('t9945', gubun = '2')
            dfStock = pd.concat([dfStock, self._GetDataFrameKor(instXAQuery, 't9945OutBlock')], ignore_index=True)

        dfStock.rename(columns={'단축코드':'종목코드'}, inplace=True)

        return  dfStock


if __name__ == "__main__":
    pass    