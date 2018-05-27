# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:57:51 2018

@author: wansho
"""
import datetime  
import time
import platform
import re

'''
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''


def get_day_list(startday, endday):
    
    startday_year = int(startday[0:4])
    startday_month = int(startday[4:6])
    startday_day = int(startday[6:8])
    
    endday_year = int(endday[0:4])
    endday_month = int(endday[4:6])
    endday_day = int(endday[6:8])
    
    
    starttime = datetime.datetime(startday_year, startday_month, startday_day)
    endtime = datetime.datetime(endday_year, endday_month, endday_day)
    
    days = (endtime - starttime).days

    dayslist = []
    for i in range(days + 1):
        dayslist.append((starttime + datetime.timedelta(i)).strftime('%Y%m%d'))
    
    return dayslist
'''
获取当前年月日时分秒
'''
def get_now_time():
    today = datetime.date.today() 
    today_str = today.strftime('%Y-%m-%d') + '  ' + time.strftime("%H:%M:%S")  
    
    return today_str

'''
get the type of os
'''
def get_platform():
    os = 'Linux'
    my_platform = platform.platform()
    if my_platform.find('inux') != -1:
        return os
    elif my_platform.find('indow') != -1:
        os = 'Windows'
        return os

'''
if os is linux
    change '\\' in path into '/'
elif os is Windows
    change '/' in path into '\\'

default path : linux path
'''
def localize_path(path):
    os = get_platform()
    if os == 'Linux':# now os is Linux,default path is linux style: '/'
        return path
    else: # os is windows,need to change the '/' into '\\'
        re_str = '/'
        path = re.sub(re_str,'\\\\',path)
        return path
        
'''
def get_cookie_from_weibo(username, password):
    driver = webdriver.Chrome()
    driver.get('https://www.bilibili.com/ranking')
    assert "哔哩哔哩" in driver.title
    login_link = driver.find_element_by_link_text('登录')
    ActionChains(driver).move_to_element(login_link).click().perform()
    login_name = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginName"))
    )
    login_password = driver.find_element_by_id("loginPassword")
    login_name.send_keys(username)
    login_password.send_keys(password)
    login_button = driver.find_element_by_id("loginAction")
    login_button.click()
    cookie = driver.get_cookies()
    driver.close()
    return cookie
'''

if  __name__ == '__main__':
    startday = '20180501'
    endday = '20180520'
    print(get_day_list(startday, endday))
    pass
