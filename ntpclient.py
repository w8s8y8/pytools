import os 
import time 
import ntplib 

c = ntplib.NTPClient() 
response = c.request('0.cn.pool.ntp.org') 

ts = response.tx_time 
_date = time.strftime('%Y-%m-%d',time.localtime(ts)) 
_time = time.strftime('%X',time.localtime(ts))
os.system('date {} && time {}'.format(_date,_time)) 