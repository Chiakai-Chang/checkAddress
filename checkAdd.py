# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:19:07 2020

@author: chiakai
"""

def checkAdd(Address):
    '''
    借用內政部國土測繪中心「國土測繪圖資服務雲」之電子地圖，查詢任意地址之完整行政區(至村里鄰)及經緯度。
    
    Parameters
    ----------
    Address : str
        請輸入要查詢的地址

    Returns
    -------
    Address : str
        回覆完整行政區之地址
        
    lnglat : list
        回覆經緯度list
    '''
    #不要print警告
    import sys, warnings
    if not sys.warnoptions:
        warnings.simplefilter("ignore") 
    
    origin = f'{Address}'    
    #將地址中的段處理成中文
    #中文數字轉換阿拉伯數字包
    import cn2an, re
    
    duan = re.findall('\d+段', Address)
    for s in duan:
        newS = cn2an.transform(s, "an2cn")
        Address = Address.replace(s,newS)
    #print(f'>>改段結果：{Address}')
      
    #把樓跟室切割出來
    try:
        floor = re.findall('\d+樓', Address)[0]
        Address = Address.replace(floor,'')
    except :
        floor = ''
    try:
        room = re.findall('\d+室', Address)[0]
        Address = Address.replace(room,'')
    except :
        room = ''
        
    #將中文轉換成網址看得懂的格式
    import urllib.parse
    addrQ = urllib.parse.quote(Address)
    #print(f'>>改字結果：{addrQ}')
    
    #透過內政部國兔測繪中心國土測繪圖資服務雲，查詢地點的座標與正確地點名稱
    from requests_html import HTMLSession
    
    s = HTMLSession()
    
    #開始查詢
    url = 'https://api.nlsc.gov.tw/MapSearch/QuerySearch'
    
    header = {
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "zip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "216",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "api.nlsc.gov.tw",
        "Origin": "https://maps.nlsc.gov.tw",
        "Referer": "https://maps.nlsc.gov.tw/T09/mapshow.action",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
        }
    
    data = {
            "word": addrQ,
            "feedback": "XML",
            }
    
    r = s.post(url=url, headers=header, data=data,verify=False)
    if r.status_code == 200:
        print('>>查詢成功')
    
    realAddress = f"{r.html.find('CONTENT')[0].text}{floor}{room}"
    #先將結果中的全形數字轉回一般數字
    big = ['０','１','２','３','４','５','６','７','８','９']
    small = [x for x in range(10)]
    numdict = dict(zip(big, small))
    for n in big:
        realAddress = realAddress.replace(n, f'{numdict[n]}')
    print(f'>>原始地址為：{origin}')
    print(f'>>完整地址為：{realAddress}')
    
    lnglat = f"{r.html.find('LOCATION')[0].text}".split(',')
    print(f'>>經緯度為：{lnglat}')
    
    return realAddress, lnglat

if __name__ == '__main__':
    Address = '新北市三重區重新路2段46之8號3樓'
    result = checkAdd(Address)