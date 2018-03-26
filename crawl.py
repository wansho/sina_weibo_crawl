# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:04:20 2018

爬取 https://weibo.cn/  中指定话题的微博，采用了微博的高级搜索

@author: wansho
"""

from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote

from bs4 import BeautifulSoup

import my_io
import re

import microblog

# 用于延时
import time

# 用于生成延时随机数
import random

import sys

import tools


############################################################### 

'''
设置要爬取的url

mobile高级搜索设置

返回要爬取的url
'''
def set_url(keyword, start_time, end_time):
    
    ori = 'https://weibo.cn/search/?advancedfilter=1'

    keyword = 'keyword=' + quote(keyword)  # 必须是英文或者中文转码，也就是说必须是ASCII
    
    sort = 'sort=time'
    
    smblog = '搜索'
    url_smblog = 'smblog=' +  quote(smblog)  
    
    #rand 会变，每换一个话题，都要在浏览器中重新获取rand值
    rand = 'rand=2151'
    others = 'p=r&' + rand + '&p=r'
    
    connector = '&'
 
    url = ori +  connector + keyword + connector + start_time \
        + connector + end_time + connector + sort \
        + connector + url_smblog + connector + others
        
    
    return url

############################################################### 
    
############################################################### 

'''
设置要爬取的下一页的url

返回要爬取的url

还没测试
'''
def set_next_url(keyword, start_time, end_time, page_number):
    
    ori = "https://weibo.cn/search/mblog?hideSearchFrame="
    keyword = 'keyword=' + quote(keyword)  # 必须是英文或者中文转码，也就是说必须是ASCII
    advanced_setting = 'advancedfilter=1'
    
    sort = 'sort=time'
    
    page = 'page=' + str(page_number)  
    connector = '&'
 
    url = ori +  connector + keyword + connector + advanced_setting \
        + connector + start_time + connector + end_time \
        + connector + sort + connector + page
        
    return url

############################################################### 


'''
下载给定url的网页

返回值：网页的 字符串 形式
如果返回 -1，说明爬取失败， 那么马上 进行数据的存储

'''
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

############################################################### 

'''
用beautifulsoap 修补一下网页
'''
def fix_html(html_str):
    # 修补html
    soup = BeautifulSoup(html_str,'html.parser', from_encoding="gb18030")
    fixed_html = soup.prettify()
    
    return fixed_html

############################################################### 
    
'''
对网页内容进行解析，得到
1、昵称
2、主页地址
3、所在地区（详细地址）
4、点赞数，转发数，评论数
5、发微博的时间
6、微博内容
7、地址
8、性别

获取还有多少页没有爬的信息

返回爬取完一个页面后得到的 微博集合(microblog_quene) + 下页信息

下页信息，如果 == -1，那么说明到了最后一页，如果没到，则返回下页页码，继续爬取
    如果 == -2 ，那么在爬取性别和地址的时候爬取失败，要及时存储数据，退出程序
    如果 == -3，那么说明网页爬取的有问题，需要重新爬取
'''
def parse_main_content(html_str):
    
    # 解析每一条微博
    microblog_quene = []
    
    soup = BeautifulSoup(html_str)
    
    allpage = 'default'
    
    # 获取包含 class 为 c ，存在id属性的 div  很重要
    microblog_soups = soup.find_all('div', attrs = {'class' : 'c'}, id = re.compile('.*'))
    
    # 获取页面信息，看看还有多少页面没有爬取,这里可能会出问题，导致page_info为none，
    # 问题可能出在：爬取到的信息出错，需要重新爬一遍
    page_info = soup.find('div',attrs = {'class' : 'pa'})
    
    if page_info == None: # 页面爬取失败，重新爬取
        nextpage = -3
        info = '爬取到的信息有错误，需要重新爬取该页面'
        log(info)
        return microblog_quene, nextpage, allpage
    else:
        page_info = page_info.get_text().strip()
    
    nextpage = -1

    if page_info.find('下页') == -1: # 没有找到下页，说明到了最后一页
        return microblog_quene, nextpage, allpage
    else:
        re_str = r'[1-9][0-9]*/[1-9][0-9]*页'  ## 匹配的结果  1/100页
        ss = re.findall(re_str, page_info)[0]
        
        # 获取下一页
        nextpage = int(ss[0 : ss.find('/')]) + 1
        allpage = int(ss[ss.find('/') + 1 : ss.find('页')])
 
    # 对每一条blog进行遍历爬取
    for microblog_soup in microblog_soups:
        
        # 获取昵称
        nickname = microblog_soup.find('a',attrs = {'class' : 'nk'})
        # 进行判空处理，防止程序异常退出
        if nickname == None: # 页面爬取失败，重新爬取
            nextpage = -3
            info = '爬取到的信息有错误，需要重新爬取该页面'
            log(info)
            return microblog_quene, nextpage, allpage
        else:
            nickname = nickname.get_text().strip()
        
        # print('nickname : ' + nickname + '\n')
        
        # 获取用户主页  https://weibo.cn/a813689091
        index = microblog_soup.find('a',attrs = {'class' : 'nk'}).get('href')
        # 进行判空处理，防止程序异常退出
        if index == None: # 页面爬取失败，重新爬取
            nextpage = -3
            info = '爬取到的信息有错误，需要重新爬取该页面'
            log(info)
            return microblog_quene, nextpage, allpage
        else:
            index = index.strip()
        # print('index : ' + index + '\n')
        
        # 地址和性别
        sex,location = parse_user(index,cookie)
        
        # 爬取用户主页的时候遇到问题
        if sex == -1 or sex == -2:
            try_times = 3
            while try_times > 0:
                try_times = try_times - 1
                if sex == -2: # 解析网页的时候失败，说明返回的网页有问题，要重新爬取
                    time_delay = random.randint(10,20)
                else :
                    time_delay = 60 * 6 # 爬取网页失败，6分钟后进行第二次尝试
                time.sleep(time_delay)
                sex,location = parse_user(index,cookie) # 第二次尝试
                if sex != -1 and sex != -2:
                    break
            if try_times == 0: ## 尝试三次后仍然不成功
                nextpage = -2 # 尝试仍然不成功，返回 -2，表示爬取用户主页三次后失败
                return microblog_quene, nextpage, allpage
            
        # 获取用户内容,内容中间有很多空格，需要删减
        # content需要分 是转发的，还是原创的
        divs = microblog_soup.find_all('div')
        ss = ''
        flag = 0 # 表示不是转发的 2 表示是转发的  双重保险，只有出现了 ‘转发理由’ 和 ‘转发了’，才能证明这条微博是转发的
        aim_div = divs[0]
        for div in divs:
            ss = div.get_text().strip()
            if ss.find('转发理由:') != -1 or ss.find('转发了') != -1:
                if ss.find('转发理由:') != -1: # 确认是转发的微博后定位到内容div
                    aim_div = div
                flag = flag + 1
            
        if flag == 2: # 表示这条微博是转发的
            ss = aim_div.get_text().strip()
            content = ss[ss.find('转发理由') + 5 : ss.find('赞[0]')]
        else: # 这条微博是原创的微博
            content = microblog_soup.find('span',attrs = {'class' : 'ctt'}).get_text().strip()
        
        # print('content:' + content + '\n')

        # 获取时间   03月15日 23:26
        time1 = microblog_soup.find('span',attrs = {'class' : 'ct'}).get_text().strip()
        time1 = time1[:12]
        # print('time:' + time + '\n')
        
        ## 用来匹配评论数、转发数等数字
        re_num = '[0-9]*'
        
        # 获取点赞数  例如：0
        re_str = u'https://weibo.cn/attitude.*' # 正则表达式，用来匹配href的值
        thumb_up = microblog_soup.find('a', href = re.compile(re_str)).get_text().strip()
        thumb_up_count = int(re.findall(re_num,thumb_up[2:])[0])
        # print('thumb_up_count:' + str(thumb_up_count) + '\n')
    

        # 获取转发数  例如：0
        re_str = u'https://weibo.cn/repost.*'  # 正则表达式，用来匹配href的值
        repost = microblog_soup.find('a', href = re.compile(re_str)).get_text().strip()
        repost_count = int(re.findall(re_num,repost[3:])[0])
        # print('repost_count:' + str(repost_count) + '\n')

        # 获取评论数  例如：0
        re_str = u'https://weibo.cn/comment.*' # 正则表达式，用来匹配href的值
        # 如果用户转发了别人的微博，那么这里评论会有两个，第一个是原文评论，第二个才是用户的评论
        comment = microblog_soup.find_all('a', attrs = {'class' : 'cc'}, href = re.compile(re_str))
        commentlen = len(comment)
        if commentlen == 1: # 不是转发
            comment = comment[0].get_text().strip()
        else:
            comment = comment[1].get_text().strip()
        
        comment_count = int(re.findall(re_num,comment[3:])[0])
        
        # print('comment_count:' + str(comment_count ) + '\n')
         
        # print('============================================================')
 
        # new 一个微博的类,装入上面爬取到的信息
        microblog_item = microblog.microblog()
        
        microblog_item.set_neckname(nickname)
        microblog_item.set_index(index)
        microblog_item.set_location(location)
        microblog_item.set_comment_count(comment_count)
        microblog_item.set_sex(sex)
        microblog_item.set_repost_count(repost_count)
        microblog_item.set_thumb_up_count(thumb_up_count)
        microblog_item.set_time(time1)  # 这里忘记改了。。。
        microblog_item.set_content(content)
        
        microblog_quene.append(microblog_item)
        
    return microblog_quene, nextpage, allpage

############################################################### 
        
'''
根据用户主页的url，爬取用户的相关信息，例如性别、所在地等信息
还可以爬取更多信息，例如学历，是否为大V
返回性别和位置

如果返回 -1 -1,则表示爬取失败，重新爬取
如果返回 -2 -2，则表示爬取的内容有错误，需要重新爬取

'''
def parse_user(url,cookie):
    
    sex = -2
    location = -2
    
    # 获取原网页
    html_source = downloadHtml(url,cookie)
    
    # 爬取失败
    if html_source == -1:
        return html_source, html_source
        
    # 修补网页
    fixed_html = fix_html(html_source)
    
    soup = BeautifulSoup(fixed_html)
    
    user_soup = soup.find('div',attrs = {'class' : 'u'})
    
    # 判断是否爬取的内容有错误
    if user_soup == None:
        return sex,location 
    
    # 性别和地址所在的字符串
    sex_location = user_soup.find('span',attrs = {'class' : 'ctt'})
    
    # 判断是否爬取的内容有错误
    if sex_location == None:
        return sex,location 
        
    sex_location = sex_location.get_text().strip()
        
    
    # 写正则表达式取出性别和地址
    re_str = r'男/.{0,6}|女/.{0,8}'
    sex_location = re.findall(re_str,sex_location)[0]
    sex = sex_location[:1]
    location = sex_location[2:]

    #print(sex)
    #print(location)
    #print("-----------------------------------")
    
    return sex,location

###############################################################

'''
在系统运行中打log
'''
def log(ss):
    path = "C:\\Users\\wansho\\Desktop\\微博爬虫\\logs.txt"
    my_io.log(ss,path)
    print(ss)


###############################################################
'''
向csv文件中写入数据,超过50条就存储

如果config == 1,全部存储
否则超过50条就存储
'''
def write_data(microblogs,path,config):
    
    if config == 1:
        my_io.write_csv(path,microblogs)
        microblogs.clear()
        info = '写入剩余数据成功'
        log(info)
    else:
        if len(microblogs) > 50:
            my_io.write_csv(path,microblogs)
            microblogs.clear()
            info = '写入50条数据成功'
            log(info)
    
    return microblogs

###############################################################
'''
爬取网页失败，进行第二次尝试
'''
def next_try_downloadhtml(url, cookie):
    
    time_delay = 60 * 6 # 6分钟后进行第二次尝试
    time.sleep(time_delay)
    
    # 获取原网页
    html_source = downloadHtml(url,cookie)
    
    
    return html_source

###############################################################
'''
爬取网页失败，在退出前进行断点存储

后来仔细考虑后发现，断点可以不加，因为在log中会有显示在哪里断的
'''
def save_break_point(path,info):
    
    writer = open(path, 'a',  encoding='utf-8')
    time_str = tools.get_now_time()
    writer.write('\n----------' + time_str + '----------\n')
    writer.write(info + '\n')
    writer.flush()
    writer.close()

###############################################################

'''
# 按照日期进行爬取
startday 是从今天往前算开始爬取的天数
days 是从当前往前算截止的天数
startday - days 就是要爬取的天数
'''
def crawl_as_days(startday,days):
    path = "C:\\Users\\wansho\\Desktop\\微博爬虫\\微博数据.csv"
    
    break_point_path = 'C:\\Users\\wansho\\Desktop\\微博爬虫\\breakpoint.txt'
    
    ## 如果是断点续爬，那么就不用在这里初始化
    # attrs = ['昵称','性别','所在地','时间','内容','点赞数','转发数','评论数','主页']
    # my_io.init_csv(path,attrs)
    
    keyword = "苹果手机"
    
    cookie = 'WEIBOCN_WM=3333_2001; _T_WM=5ad11550fbf1922d3534220fe93e26c0; SCF=AnA5vjYoP5UxdBHxe5-hFYridMNAWw5uGpGR_ES8HicMWMEzTrLqLF4LtJQ3NTvEbM_lI0h3yqrTbowz_3H7Hd8.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh224JmmGS16QC9q88gApDH5JpX5K-hUgL.Foq71K2f1KepSKz2dJLoI79Nqg40IsYt; SUB=_2A253tIRXDeRhGeVI41oW9SbMyT2IHXVVViwfrDV6PUJbkdAKLVL1kW1NTBBvfj_JczYE_K1_wfAtEv_DsKiqcfOE; SUHB=0BL4btDxeWgkqF; SSOLoginState=1521546247'
    
    # startday = 16 # 往前爬取一个月的微博内容
    while startday > days:
        
        # 一天一天的爬取
        start_time = 'starttime=' + tools.get_time(0 - startday - 1)
        end_time = 'endtime=' + tools.get_time(0 - startday - 1) # 经过测试，如果是爬取一天内的内容，那么startday 和 endday应该一样
        startday = startday - 1
        
        first_url = set_url(keyword, start_time, end_time)
        
        # 爬取第一个页面
        # 打印出url，方便分析
        info = "首页url: \n" + first_url
        log(info)
        
        # 获取原网页
        html_source = downloadHtml(first_url,cookie)
        
        # 爬取失败
        if html_source == -1:
            info = "-------------首页爬取失败，正在尝试第二次爬取-------------"
            log(info)
            try_times = 3  # 尝试爬取三次
            while try_times > 0:
                try_times = try_times - 1
                html_source = next_try_downloadhtml(first_url,cookie)
                if html_source == -1:
                    continue
                else: # 第二次爬取尝试成功
                    info = "-------------尝试再次爬取成功-------------"
                    log(info)
                    break
            
            if try_times == 0: # 爬取失败了
                info = '尝试三次后爬取失败，下面存储断点'
                saved_url = first_url
                save_break_point(break_point_path,saved_url)
                sys.exit()
            
        
        # 修补网页
        fixed_html = fix_html(html_source)
        
        microblogs =  []
        
        microblog_quene, nextpage,allpage = parse_main_content(fixed_html)
        
        # 合并爬取到的BLOG
        microblogs = microblogs + microblog_quene
        
         # 满50条就存储
        write_data(microblogs,path,2)
        
        old_nextpage = 1
        
        error_count = 1 # 如果爬取的页面一直有问题，说明可能下一页不是正常的页面，所以我们要及时跳出来
        
            
        ##############################################################
        # 开始爬取 第 n 页  n >= 2
        while nextpage != -1:
            # 由于第一个页面没有明确的下一页的url，所以还是在浏览器中测试，然后，找到下一页的规律
            # 下面的链接，nextpage是重点，其他和之前的没啥区别
            
            next_url = set_next_url(keyword, start_time, end_time, nextpage)
            
            info = '\n\n------------第 ' + str(nextpage) +  ' 页'  +  ' // 总页数: ' + str(allpage) +'-------------- \n\n'
            log(info)
            info = 'next_url ： \n' + next_url + '\n\n'
            log(info)
        
            html_source = downloadHtml(next_url,cookie)
            
            # 爬取失败
            if html_source == -1:
                info = "-------------爬取失败 顺序页爬取失败-------------"
                log(info)
                try_times = 3  # 尝试爬取三次
                while try_times > 0:
                    try_times = try_times - 1
                    html_source = next_try_downloadhtml(next_url,cookie)
                    if html_source == -1:
                        continue
                    else: # 第二次爬取尝试成功
                        info = "-------------尝试再次爬取成功-------------"
                        log(info)
                        break
                
                if try_times == 0: # 爬取失败了
                    info = '尝试三次后爬取失败，下面存储断点'
                    saved_url = first_url
                    save_break_point(break_point_path,saved_url)
                    sys.exit()
    
            
            fixed_html = fix_html(html_source)
            microblog_quene, nextpage, allpage = parse_main_content(fixed_html)
            
            if nextpage == -2: # 爬取失败,在爬取个人主页三次后的时候失败
                info = "-------------爬取用户主页三次后失败-------------"
                log(info)
                # sys.exit()
                break
            
            if nextpage == -3: # 爬取的网页哟问题，需要重新爬取
                error_count = error_count + 1 
                if error_count == 6: # 尝试六次后，依旧有问题，说明可能爬到了不是想要的页面
                    error_count = 0
                    break
                else:
                    nextpage = old_nextpage
                    continue
            
            if nextpage == -1: # 一天的内容已经爬取完成
                break
            
            microblogs = microblogs + microblog_quene
            
            # 如果nextpage有效，就存储nextpage，用来防止nextpage无效时
            old_nextpage = nextpage
            
            # 满50条就存储
            write_data(microblogs,path,2)
            
            # 延时，防止被反爬虫，这个时间需要不断测试，达到一个平衡点
            sleep_time = random.randint(10,20)
            time.sleep(sleep_time)
            
        # 爬完一天的数据，进行一次存储
        write_data(microblogs,path,1)
        
    
if __name__ == "__main__":
    crawl_as_days(17,0)
    
    crawl_as_days(51, 25)
