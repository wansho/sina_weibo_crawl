# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:25:47 2018

对现在的网页进行测试解析

@author: wansho
"""
from urllib.request import urlopen
from urllib.request import Request

from bs4 import BeautifulSoup


def downloadHtml(url, cookie):

    # 模拟了真实的浏览器，包括 cookie,user-agent等元素，最好是在进入了某一个电影的评论页面，再获取header
    headers = { 
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		 
		'Accept-Language':'zh-CN,zh;q=0.9',
		 'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':cookie,
        'Host':'weibo.cn',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'    
		}  

    req = Request(url=url, headers=headers)
    
    html = -1 # 如果返回 -1，说明爬取失败， 那么马上 进行数据的存储
    
    # 解决爬取失败问题
    try:
        html = urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(e)
        return html
    return html

def parse_main_content(html_str):
    
    # 解析每一条微博
    microblog_quene = []
    
    soup = BeautifulSoup(html_str)
    
    # 获取页面信息，看看还有多少页面没有爬取
    page_info = soup.find('div',attrs = {'class' : 'pass'})
    
    if page_info == None:
        print("---------------null-------------")
    else:
        print("---------not null-----------")
        
    print(page_info)
        
    return microblog_quene, nextpage

############################################################### 

'''
用beautifulsoap 修补一下网页
'''
def fix_html(html_str):
    # 修补html
    soup = BeautifulSoup(html_str,'html.parser', from_encoding="gb18030")
    fixed_html = soup.prettify()
    
    return fixed_html


if  __name__ == '__main__':

    first_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&advancedfilter=1&starttime=20180222&endtime=20180223&sort=time&page=77'
    cookie = 'WEIBOCN_WM=3333_2001; _T_WM=5ad11550fbf1922d3534220fe93e26c0; SCF=AnA5vjYoP5UxdBHxe5-hFYridMNAWw5uGpGR_ES8HicMWMEzTrLqLF4LtJQ3NTvEbM_lI0h3yqrTbowz_3H7Hd8.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh224JmmGS16QC9q88gApDH5JpX5K-hUgL.Foq71K2f1KepSKz2dJLoI79Nqg40IsYt; SUB=_2A253tIRXDeRhGeVI41oW9SbMyT2IHXVVViwfrDV6PUJbkdAKLVL1kW1NTBBvfj_JczYE_K1_wfAtEv_DsKiqcfOE; SUHB=0BL4btDxeWgkqF; SSOLoginState=1521546247'
    
    # 获取原网页
    html_source = downloadHtml(first_url,cookie)
    
    # 修补网页
    fixed_html = fix_html(html_source)
    
    microblogs =  []
    
    microblog_quene, nextpage = parse_main_content(fixed_html)