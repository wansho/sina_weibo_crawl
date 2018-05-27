# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 19:11:39 2018

@author: wansho
"""

import csv
import tools
import json


'''
根据path地址将字符串写入文件中
'''
def write_html(html_str, path):
    writer = open(path, 'w',  encoding='utf-8')
    writer.write(html_str)
    writer.close()
    
def load_ips(path):
    reader = open(path, 'r')
    
    ips = []
    
    while True:
        ip = reader.readline()
        if not ip:
            break
        ips.append(ip.strip())

    reader.close()
    
    return ips

# 新建一个cvs文件
def init_csv(path,attrs):
    csvfile = open(path, 'a', newline='', encoding='utf_8_sig')
    writer = csv.writer(csvfile)
    writer.writerow(attrs)
    csvfile.close()
    return

# 往csv中写入文件
def write_csv2(path, datas):
    fw = open(path, 'w', newline='',  encoding='utf_8_sig')
    csv_writer = csv.writer(fw)
    
    for row in datas:
        csv_writer.writerow(row)
        
    fw.close()
    
# 读取csv文件,以列表的形式返回
def read_csv(path):
    fr = open(path, 'r', encoding='utf-8')
    
    listt = []

    csv_reader = csv.reader(fr)
    for row in csv_reader:
        listt.append(row)
        
    return listt

# 在程序中打log，并将log写在
# 返回1 则没有问题，返回 -1，则写入log的时候发生异常
def log(info,path):
    
    writer = -1
    
    try:
        writer = open(path, 'a',  encoding='utf-8')
        
        time_str = tools.get_now_time()
        writer.write('\n----------' + time_str + '----------\n')
        writer.write(info + '\n')
        writer.flush()
        writer.close()
        return 1
    except Exception as e:
        
        if writer != -1:
            writer.close()
        
        return -1
        print (e)

# 写入cvs文件
def write_csv(path,items):
    csvfile = open(path, 'a', newline='',  encoding='utf_8_sig')
    writer = csv.writer(csvfile)
    
    row = []
    for item in items:
        neckname = item.get_neckname()
        sex = item.get_sex()
        location = item.get_location()
        time = item.get_time()
        content = item.get_content()
        get_thumb_up_count = item.get_thumb_up_count()
        repost_count = item.get_repost_count()
        comment_count = item.get_comment_count()
        index = item.get_index()

        row.append(neckname)
        row.append(sex)
        row.append(location)
        row.append(time)
        row.append(content)
        row.append(get_thumb_up_count)
        row.append(repost_count)
        row.append(comment_count)
        row.append(index)
        
        writer.writerow(row)
        row.clear()

    
    csvfile.close()
    return

# 测试文件读写异常
def demo():
    
    writer = -1
    
    path = 'D:\\考研\\专业课辅导资料\\17级辅导资料\\专业课历年真题试卷\\10年以前真题PDF版\\2002年操作系统和答案.pdf'
    
    try:
        writer = open(path, 'a',  encoding='utf-8')
        writer.write('\n--------------------\n')
        writer.flush()
        writer.close()
        
    except Exception as e:
        print("文件写入异常")

if  __name__ == '__main__':

    # log("demo","C:\\Users\\wansho\\Desktop\\log.txt"
    
    json_path = tools.localize_path('D:\\读研\\新浪微博数据集\\weibo.json')
    read_json(json_path)
    