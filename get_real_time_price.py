#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import tushare,time
import datetime
#导入tushare库

send_ding_falg = False
first_write = True
notice_str = ''

stock_code_list = ['600109','601066','000547']
stock_old_price_map = {}


def get_notice_price():
    global send_ding_falg
    global first_write
    global notice_str
    
    notice_str = ''
    try:
        with open('price.txt', 'r') as f:
            data_res = f.read()
            data_list = data_res.split(';')
            for item in data_list:
                if item:
                    item_list = item.split(',')
                    stock_old_price_map[item_list[0]] = item_list[1]
    except:
        print('文件读取失败')
    
    for code in stock_code_list:
        data = tushare.get_realtime_quotes(code)
        open_price = float(data.loc[0]['open'])
        price = float(data.loc[0]['price'])
        a = price - open_price
        drift = float('%.2f' % a)
        percent = '{:.2%}'.format(drift/open_price)
        
        name = str(data.loc[0]['name'])
        price = str(data.loc[0]['price'])
        
        notice_str = notice_str + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t'+ name +' ： ' + ' ' + price + '\t' + str(drift) + '\t' + percent + '\n'
        
        old_price = stock_old_price_map.get(code)
        if open_price != price:
            send_ding_falg = True
        
        try:
            if first_write:
                with open('price.txt', 'w') as f:
                    f.truncate()
                    first_write = False
                    f.close()
            with open('price.txt', 'a') as f:
                write_res = f.write(code + ',' + price + ';')
        except IOError:
            print('文件写入失败')
            
    return notice_str


def dingTalk():
    global notice_str
    headers={
        'Content-Type': 'application/json'
            }
    data={
     'msgtype': 'markdown',
     'markdown': {
         'title':'通知',
         'text': '#### 今日通知：\n' + notice_str
         },
    'at': {
        'atMobiles': [
        ], 
        'isAtAll': 'false'
    }
  }
    json_data=json.dumps(data)
    r = requests.post(url='https://oapi.dingtalk.com/robot/send?access_token=fe293b25c86433258b3ce07c8cb32f29a' +
                      '318d33fd40f727caff4f273bff44b44',data=json_data,headers=headers)
    
    print(r.text)

if __name__ == '__main__':
    get_notice_price()
    global send_ding_falg
    if send_ding_falg:
        dingTalk()