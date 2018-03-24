# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:57:51 2018

@author: wansho
"""
import datetime  
import time

def get_time(offset):

    today = datetime.date.today() 

    tomorrow = today + datetime.timedelta(offset)  
    need_time = tomorrow.strftime('%Y-%m-%d').replace('-','')

    return need_time

def get_now_time():
    today = datetime.date.today() 
    today_str = today.strftime('%Y-%m-%d') + '  ' + time.strftime("%H:%M:%S")  
    
    return today_str

if  __name__ == '__main__':

    print(get_time(-20))

    print(get_now_time())