# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 19:11:39 2018

@author: wansho
"""

import csv


'''
根据path地址将字符串写入文件中
'''
def write_html(html_str, path):
    writer = open(path, 'w',  encoding='utf-8')
    writer.write(html_str)
    writer.close()
    



# 新建一个cvs文件
def init_csv(path,attrs):
    csvfile = open(path, 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(attrs)
    csvfile.close()
    return

# 写入cvs文件
def write_csv(path,items):
    csvfile = open(path, 'a', newline='',  encoding='utf-8')
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