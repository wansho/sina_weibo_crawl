# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 09:58:40 2017

@author: wansho
"""

# 电影类型
class microblog:
    
    neckname = ''
    index = ''
    content = ''
    time = ''
    location = ''
    sex = ''
    thumb_up_count = 0
    repost_count = 0
    comment_count = 0
    
    def set_neckname(self, neckname):
        self.neckname = neckname  
    def get_neckname(self):
        return self.neckname   
    
    def set_index(self, index):
        self.index = index
    def get_index(self):
        return self.index
    
    def set_time(self, time):
        self.time = time
    def get_time(self):
        return self.time
    
    def set_location(self, location):
        self.location = location
    def get_location(self):
        return self.location 
    
    def set_sex(self, sex):
        self.sex = sex
    def get_sex(self):
        return self.sex 
    
    def set_thumb_up_count(self, thumb_up_count):
        self.thumb_up_count = thumb_up_count
    def get_thumb_up_count(self):
        return self.thumb_up_count 
    
    def set_content(self, content):
        self.content = content
    def get_content(self):
        return self.content 
    
    def set_comment_count(self, comment_count):
        self.comment_count = comment_count
    def get_comment_count(self):
        return self.comment_count 
    
    def set_repost_count(self, repost_count):
        self.repost_count = repost_count
    def get_repost_count(self):
        return self.repost_count 