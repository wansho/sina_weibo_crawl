# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:55:39 2018

把时间不符合规范的18年的数据清洗掉
将微博内容中所有换行和空格去掉
删除掉重复爬取过的微博

@author: wansho
"""

import csv
import re

import os

import my_io
import tools

'''
将时间有问题的数据、重复的数据、很短的数据、还有链接，都删除掉
'''
def validate_data(readpath,writepath,year):
    
    fr = open(readpath, 'r', encoding='utf-8')

    csv_reader = csv.reader(fr)
    
    valid_datas = []
    
    # 用于去重
    repeat_detection_set = set()
    
    # 对不符合时间标准BLOG进行删除   注意这个正则表达式只能匹配今年的时间，而且不能匹配当天的数据
    # 删除重复数据
    if year == 'nowyear':
        re_time = r'[0-1][0-9]月[0-3][0-9]日 [0-9][0-9]:[0-9][0-9]'
    else:
        re_time = r'2017-[0-9]{1,2}-[0-9]{1,2} [0-9][0-9]:[0-9][0-9]'
    
    # 用于匹配换行符和多余的空格
    re_newline = r'(\n)+|( )+'
    
    all_data_count  = 0

    for row in csv_reader:
        
        all_data_count = all_data_count + 1
         
        name = row[0]
        time1 = row[3]
        
        content = row[4]
        
        # 将内容中所有的换行和多余的空格都换成一个空格
        content = re.sub(re_newline, ' ', content)
        
        # 在爬取数据的时候，微博的内容可能多包含了一个 ： ，所以我们要去掉：
        if content.startswith(':'):
            content = content[1:]
            
        # 过滤content中的 @
        re_aite = '\s@[^\s]{1,10}'
        if content.find('@') != -1:
            content = re.sub(re_aite,' ',content)
          
        # 过滤content中的url
        re_url = '(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
        if len(re.findall(re_url,content)) != 0:
            content = re.sub(re_url,' ',content) 
            
        # 下面过滤掉短数据
        re_space = '( )+'
        content_no_space = re.sub(re_space,'',content)
        content_len = len(content_no_space)
        if content_len < 5:
            continue

        row[4] = content
        
        compare_source = name + time1
        
        # 去重,去掉无效时间
        if compare_source not in repeat_detection_set: 
            repeat_detection_set.add(compare_source)       
            
            # 看时间是否有效
            if re.match(re_time, time1) : # 表示匹配，时间有效
                # 此处要判断年限，因为18年和17年的时间格式不同，要统一调整成
                # 2017年09月09日 10:19分 的格式
                if year == 'nowyear': # 当年的时间
                    time1 = '2018年' + time1
                    
                else: #'oldyear'
                   time1 = time1[0:4] + '年' + time1[5:7] + '月' + \
                           time1[8:10] + '日 ' + time1[-8:-3]
                   
                row[3] = time1
                
                valid_datas.append(row)

            
    fr.close()
    
    print("总的数据量为：" + str(all_data_count))
    print("有效数据量为：" + str(len(valid_datas)))
    
    ## 将时间有效数据重新存储到另外一个文件中
    my_io.write_csv2(writepath, valid_datas)
    
    repeat_detection_set.clear()
    valid_datas.clear()

'''
将数据集中的微博内容提取到一个单独的TXT文件中
'''
def get_text(readpath,writepath):
    
    fr = open(readpath, 'r', encoding='utf_8_sig')
    
    fw = open(writepath, 'w', encoding='utf_8_sig')
    
    csv_reader = csv.reader(fr)
    
    for row in csv_reader:
        content = row[4]
        fw.write(content)
        fw.write('\n')
        
    fw.close()
    fr.close()
    

if __name__ == '__main__':
    
    abs_path = os.path.abspath('.')
    
    name = '中兴'

    path_read = abs_path + tools.localize_path("/暂时爬取到的数据/2018数据/" + name +  "2018.csv")

    path_write_valid = abs_path + tools.localize_path("/经过处理的数据/2018数据/" + name + "2018_valid.csv")

    path_write_gettext = abs_path + tools.localize_path('/经过处理的数据/2018数据/' + name + '2018内容文本.txt')
    
    # 因为当年和往年的数据 在时间的格式上有很大的差别，所以要统一格式, nowyear lastyear
    year = 'nowyear' 
    
    validate_data(path_read,path_write_valid, year)
    
    get_text(path_write_valid,path_write_gettext)