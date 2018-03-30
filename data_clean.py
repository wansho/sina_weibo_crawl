# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:55:39 2018

@author: wansho
"""

import csv
import re

# 往csv中写入文件
def write_csv(path, datas):
    fw = open(path, 'a', newline='',  encoding='utf_8_sig')
    csv_writer = csv.writer(fw)
    
    for row in datas:
        csv_writer.writerow(row)
        
    fw.close()


def validate_data(readpath,writepath):
    
    fr = open(readpath, 'r', encoding='utf-8')

    csv_reader = csv.reader(fr)
    
    valid_datas = []
    
    # 用于去重
    repeat_detection_set = set()
    
    # 对不符合时间标准BLOG进行删除   注意这个正则表达式只能匹配今年的时间，而且不能匹配当天的数据
    # 删除重复数据
    re_time = r'[0-1][0-9]月[0-3][0-9]日 [0-9][0-9]:[0-9][0-9]'
    
    # 用于匹配换行符和多余的空格
    re_newline = r'(\n)+|( )+'
    
    all_data_count  = 0

    for row in csv_reader:
        
        all_data_count = all_data_count + 1
         
        name = row[0]
        time1 = row[3]
        
        content = row[4]
        # 将所有的换行和多余的空格删除
        content = re.sub(re_newline, '', content)
        
        if content.startswith(':'):
            content = content[1:]
        
        row[4] = content
        
        compare_source = name + time1
        
        if compare_source not in repeat_detection_set: # 不是重复的数据
            repeat_detection_set.add(compare_source)
            if re.match(re_time, time1): # 表示匹配，时间有效
                valid_datas.append(row)
                
            
    fr.close()
    
    print("总的数据量为：" + str(all_data_count))
    print("去重后数据量为：" + str(len(repeat_detection_set)))
    # 只要当年的数据，也就是2018年的数据
    print("去掉无效时间后，数据量为：" + str(len(valid_datas)))
    
    ## 将时间有效数据重新存储到另外一个文件中
    write_csv(writepath, valid_datas)
    
    repeat_detection_set.clear()
    valid_datas.clear()

def get_text(readpath,writepath):
    
    fr = open(readpath, 'r', encoding='utf_8_sig')
    
    fw = open(writepath, 'a', encoding='utf_8_sig')
    
    csv_reader = csv.reader(fr)
    
    for row in csv_reader:
        content = row[4]
        fw.write(content)
        fw.write('\n')
        
    fw.close()
    fr.close()
    

if __name__ == '__main__':

    path_read = "D:\\PythonProjects\\微博爬虫\\weibo_mobile_crawl\\weibo_mobile_crawl\\暂时爬取到的数据\\微博数据.csv"

    path_write_valid = "D:\\PythonProjects\\微博爬虫\\weibo_mobile_crawl\\weibo_mobile_crawl\\经过处理的数据\\微博数据_valid.csv"

    path_write_gettext = 'D:\\PythonProjects\\微博爬虫\\weibo_mobile_crawl\\weibo_mobile_crawl\\经过处理的数据\\微博内容文本.txt'

    validate_data(path_read,path_write_valid)
    get_text(path_write_valid,path_write_gettext)