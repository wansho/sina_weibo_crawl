# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:47:00 2018

看看微博里有多少种表情

@author: wansho
"""

import re
import os
import my_io
import tools
import matplotlib.pyplot as plt  

'''
获取到微博中的各种表情

path : 微博内容纯文本

return :所有表情的字典，键：表情 值：出现的次数

'''
def get_moodface(path):
    fr = open(path, 'r', encoding = 'utf-8')
    
    mood_re = '\[[\u4e00-\u9fa5a-zA-z0-9]{1,5}\]'
    
    mood_dict = {}
    
    for line in fr.readlines():
        
        mood_list = re.findall(mood_re, line)
        for mood in mood_list:
            if mood in mood_dict.keys():
                count = mood_dict.get(mood) + 1
                mood_dict.update({mood : count})
            else:
                mood_dict.update({mood : 1})
    
    fr.close()
    return mood_dict

'''
对字典按照values进行排序，冒泡排序
降序排序，返回两个数组，分别对应key和value
'''  
def dict_sort(dictt):

    mood_list = []
    mood_count = []
    
    for key in mood_dict.keys():
        mood_list.append(key)
        mood_count.append(mood_dict.get(key))
    
    # 开始排序
    j = len(mood_list) -1
    while j > 0:
        i = 0
        while i < j:
            if mood_count[i] < mood_count[i + 1]:
                tmp = mood_count[i]
                tmp1 = mood_list[i]
                mood_count[i] = mood_count[i + 1]
                mood_list[i] = mood_list[i + 1]
                mood_count[i + 1] = tmp
                mood_list[i + 1] = tmp1
                
            i = i + 1
            
        j = j - 1
    
    return mood_list,mood_count

'''
将listt中的数据按照时间进行归类
统计每一天的微博数
listt 是 一个列表，里面存储了从源文件中读取到的每条微博的具体信息
返回两个数组，第一个数组存储日期，第二个数组存储 当天发的微博，例如：
1月1日|1月2日|1月3日|   |   |   |
      |      |
'''
def day_classify(listt):
    
    dayslist = []
    contentslist = []
    
    day = -1
    contentlist = []
    for i in range(len(listt)):
        
        row = listt[i]
        time1 = row[3]
        daytime = time1[:11]
        
        if daytime not in dayslist:# 新的一天
            contentlist = []
            contentlist.append(row)
            contentslist.append(contentlist)
            dayslist.append(daytime)
            day = day + 1
        else: # 还是当前天
            contentlist = contentslist[day]
            contentlist.append(row)
            contentslist[day] = contentlist
    
    return dayslist,contentslist

'''
listt is all weibos in one day

return: the count of weibo created in one hour 

'''
def hour_classifier(listt): 
    
    # 24 hours
    hour_count = [0] * 24
    
    for i in range(len(listt)):
        row = listt[i]
        time1 = row[3]
        hour = time1[12:14]
        
        if hour.startswith('0'):
            hour = hour[1:]
        
        hour = int(hour)
        hour_count[hour] = hour_count[hour] + 1
        
    return hour_count

if __name__ == '__main__':
    
    path = os.path.abspath('.')
    # windows 
    
    mood_dict = get_moodface(path + tools.localize_path('/经过处理的数据/苹果手机2017内容文本.txt'))
    
    mood_list, mood_count = dict_sort(mood_dict)
        
    mood_path = path + tools.localize_path('/经过处理的数据/表情排序.txt')
    fw = open(mood_path, 'w', encoding = 'utf_8_sig')
    for mood,count in zip(mood_list,mood_count):
        fw.write(mood + '  ' + str(count) + '\n')
        
    fw.close()
    
    readpath = path + tools.localize_path('/经过处理的数据/苹果手机2017_valid_sorted.csv')

    contents = my_io.read_csv(readpath)
    
    dayslist,contentslist = day_classify(contents)
    
    '''
    # print the count of weibo in each day
    for daylist, contentlist in zip(dayslist,contentslist):
        print(daylist,len(contentlist))
       
    # print the count of weibo in 24 hours(a day)
    for i in range(7):
        hour_count = hour_classifier(contentslist[i])
        print(dayslist[i])
        print(hour_count)
        x = range(0,len(hour_count))
        
        plt.plot(x,hour_count )

        plt.legend()
        plt.show() 
    '''
    
   
    
