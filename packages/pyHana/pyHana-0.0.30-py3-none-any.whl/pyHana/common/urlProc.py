import requests
import time
import datetime

def requests_url_call(urlStr, headers='', params='', method='', prtInd = False):
    errInd = 'N'
    
    if prtInd: 
        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), urlStr, params, end='')

    while(1):
        try:                       
            if len(headers) == 0:      
                resp = requests.get(urlStr, timeout=(5, 60)) # connect timeout 5초, read timeout 30로 각각 설정    
            # 2024.08.12 GET 방식 header 추가
            elif method == 'GET' and len(headers) > 0:
                resp = requests.get(urlStr, timeout=(5, 60), headers=headers)   
                
            # 2023.10.24 post 방식 추가
            elif len(headers) > 0 and len(params) > 0 :
                resp = requests.post(urlStr, timeout=(5, 60), headers=headers, params=params)   
            elif len(headers) > 0:
                resp = requests.post(urlStr, timeout=(5, 60), headers=headers)   
            elif len(params) > 0 :
                resp = requests.post(urlStr, timeout=(5, 60), params=params)   

            if errInd == 'Y':
                print('>> Requests retry success : ', flush=True)    
                
            return resp
        
        except Exception as e:
            print("\n", type(e), ':',  e, flush=True)
            errInd = 'Y'
            time.sleep(1)
    if prtInd: 
        print(' '*400, '\r', end='')         
           
    return resp