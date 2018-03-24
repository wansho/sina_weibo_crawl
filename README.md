[TOC]
## Introduction
最近需要新浪微博的数据做研究，苦于找不到满意的数据，新浪微博的API对数据的获取有限制，也找不到合适的爬虫代码，遂自己实现了一个爬取新浪微博的爬虫。

爬取的数据是  `新浪微博搜索某一个话题`，得到的微博数据，下面是爬取到的有关苹果手机的微博示例：
![数据Demo](http://ox1llsxib.bkt.clouddn.com/%E6%95%B0%E6%8D%AEDemo.JPG-origin)



之前也爬取过 [豆瓣电影短评](http://wansho.cn/2017/12/21/blog_source/Coding/%E7%88%AC%E5%8F%96%E8%B1%86%E7%93%A3%E7%94%B5%E5%BD%B1%E7%9F%AD%E8%AF%84/)，但是好久没有再练手了，发现遗忘了很多知识点，加上新浪微博对爬虫的嗅觉异常灵敏，导致中间遇到了非常多的坑，不过好在大多数的问题，都已经解决了。所以今天索性总结一下，如果以后再写爬虫，可以拿来参考。

另外，我不是写爬虫的专家，对python的语法也不是很熟悉，也没有用scrapy这种爬虫工具（感觉用不到，因为爬虫的思想还是很简单的），所以写出来的爬虫应该比不上专业的水准，最后我会共享该程序的源码。

- - -

本文涉及的主要知识点有如下几个，其顺序大概是我写爬虫的步骤：

1. 选择合适的爬取源

2. 分析生成要爬取网站的`url`

3. 根据url下载目标网页（利用`cookie`模拟登陆）

4. 用`Beautifulsoap`和`正则表达式(re)`解析网页中需要的内容

5. 将数据存储到csv文件中

另外，这五个主要步骤中遇到了很多`坑`，特别是第一个步骤和第三个步骤，我会在这些步骤中都提到。


* * *

## Programming

#### 选择合适的爬取源

由于之前爬取豆瓣电影评论的时候，我直接爬取了PC浏览器端的网页，而且在利用cookie进行模拟登陆后爬取的非常顺利，所以我觉得微博也应该这么爬取，所以我注册了一个微博的账号，通过浏览器端拿到了cookie，觉得万事大吉了。根本没有考虑到新浪微博和豆瓣的差异。

结果，利用cookie确实可以顺利爬到相关网页的数据，但是，当我看到服务器返回的HTML代码，我惊呆了，汉字全是unicode码，于是我查找了[python3 如何 进行转码](http://blog.csdn.net/yexiaohhjk/article/details/68066843)[文献1]，了解到python3的转码函数：
```
#  python 的str类型，通过encode() 可以转码为指定的bytes类型
encode()
#  python 的bytes类型，通过decode() 可以转换成为指定的str类型
decode()
```
通过使用 `html = urlopen(req).read()`方法，我们能够获取到请求的网页数据，但是返回的是`bytes`类型，所以我们需要 `html = urlopen(req).read().decode('utf-8')`转成`str`类型。

但是即使如此，返回的HTML字符串，里面的汉字仍然是Unicode编码（\u开头，加上四个16进制的字符）：
![Unicode编码举例](http://ox1llsxib.bkt.clouddn.com/unicode%E7%BC%96%E7%A0%81%E4%B8%BE%E4%BE%8B.JPG-origin)

所以我们还要继续编解码，将里面的unicode字符转成中文，具体代码如下：
```
encode("utf-8").decode('unicode_escape')
```

如此得到的网页源码，中文才会正常显示。

但是问题又来了，微博返回的HTML源码太复杂了，我仔细分析后，才发现微博源码是HTML下又嵌套了一个HTML。
如图，我要爬取的内容就在嵌套的那个HTML下，而且里面的特殊字符都是用转义字符进行了转义，这样的网页在即使下载下来了，也要花大量的精力写规则进行解析。
![原网页](http://ox1llsxib.bkt.clouddn.com/%E6%BA%90%E7%BD%91%E9%A1%B5%E7%9A%84%E8%A7%A3%E6%9E%90%E9%9A%BE%E5%BA%A6.JPG-origin)

当我解决了转义字符后，我又发现了一个更难的问题：有的微博内容太多，被折叠了，需要进行`动态加载`。。。。。

几经波折，我最终找到了一个简单的方法：
[所有社交网站爬虫，优先选择爬移动版](https://www.zhihu.com/question/29666539 )[文献2]

最终，我选择了爬取移动版的网页：`https://weibo.cn/` ,移动版的源码，看起来，真的是清清爽爽！
![移动版源码](http://ox1llsxib.bkt.clouddn.com/%E7%A7%BB%E5%8A%A8%E7%89%88%E6%BA%90%E7%A0%81%E7%A4%BA%E4%BE%8B.JPG-origin)

这些问题折磨了我一整天，最终得到了一个惨痛的教训：

**写爬虫要优先爬取移动版网页！**

**写爬虫要优先爬取移动版网页！**

**写爬虫要优先爬取移动版网页！**

如果要写爬取PC 浏览器端的爬虫，可以参考这篇BLOG：[【python网络编程】新浪爬虫：关键词搜索爬取微博数据](http://blog.csdn.net/jiange_zh/article/details/47361555) [文献4]

* * *

#### 分析生成要爬取网站的`url`

确定了要爬取的网页后，接下来的事情就非常轻松了。

首先是构造url，无非是分析一下想要爬取的网页的url的结构，然后就可以构造自己想要爬取的信息的url即可。

例如，我想要爬取微博搜索下有关苹果手机的微博，那么我到 [微博搜索](https://weibo.cn/search/) 下，利用高级搜索搜索苹果手机3月3日到3月18日的微博，点击一下刷新，地址栏就能显示详细的url，然后把url拿来分析一下：
```
https://weibo.cn/search/?advancedfilter=1&keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&starttime=20180303&endtime=20180317&sort=time&smblog=%E6%90%9C%E7%B4%A2&rand=1948&p=r
```
`https://weibo.cn/search/?advancedfilter=1`   是高级搜索的前缀
`&`   是连接符
`keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA`    是搜索的关键字，后面跟的是 "苹果手机" 的url中文编码
`starttime=20180303&endtime=20180317`    是起止时间
`sort=time`    是按照时间顺序搜索
`smblog=%E6%90%9C%E7%B4%A2`     是固定的字符，后面跟的是  “搜索”  的url中文编码
`rand=1948&p=r`   这两项我没有搞清楚，rand经常会变化，但是不影响搜索结果，p = r 是一个固定值

如此，我们的url就可以构造如来了。

当我们爬取完第一页的内容，我发现第二页往后的url需要重新构造，其url如下：
```
https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&advancedfilter=1&starttime=20180303&endtime=20180317&sort=time&page=2
```
其中大部分内容都和第一个的url一样， 注意 ` page ` 的值就是要爬取的页面。

这里有一个点要注意，构造url时，如果搜索关键词时中文的，需要进行url转码，**url链接的字符只能来自ASCII表**。具体代码如下：
```
from urllib.parse import quote

keyword = "苹果手机"
url_keyword = 'keyword=' + quote(keyword)
```

* * *
#### 下载目标网页

url构造出来后，那么就可以下载目标网页了。

如果只是测试玩玩，那么只需要 `urlopen(url).read().decode('utf-8')`就可以获取目标网页的html源码字符串。

但是这么做是肯定会被服务器端的反爬虫检测出来的。我们需要模拟浏览器进行访问，也就是设置 `header`:

```
headers = {
 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'Accept-Language':'zh-CN,zh;q=0.9',
 'Cache-Control':'max-age=0',
 'Connection':'keep-alive',
 'Cookie':'WEIBOCN_WM=3333_2001; ALF=1523686076; SCF=AnA5vjYoP5UxdBHxe5-hFYridMNAWw5uGpGR_ES8HicM__1dKu5Fo_2k1Z1gI8INK4H-wP4i9XlQqFtnZFqb_1Y.; SUB=_2A253rmOdDeRhGeBO4lMU-S3Nzj6IHXVVUQ3VrDV6PUJbktAKLXjFkW1NRYuzLZXesXLlghQGPXJ5JlZVP9wWWeMD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh224JmmGS16QC9q88gApDH5JpX5K-hUgL.Foq71K2f1KepSKz2dJLoI79Nqg40IsYt; SUHB=0M2VZj_NSAVG7w; SSOLoginState=1521095629; _T_WM=5ad11550fbf1922d3534220fe93e26c0',
 'Host':'weibo.cn',
 'Upgrade-Insecure-Requests':'1',
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
} 
```

header的获取步骤如下：
1. 用chrome浏览器打开 https://weibo.cn/search/ 网页
2. 鼠标右击页面空白处选择 `检查`
3. 选中最上层的`Network`
4. 按 `F5` 刷新网页
5. 选中`Name` 栏第一个，然后找到右边栏中的 `Request Headers`，里面就是我们要的内容，也是浏览器发给新浪微博服务器的请求
![获取header](http://ox1llsxib.bkt.clouddn.com/%E7%88%AC%E8%99%AB_1.JPG-origin)

这里有一个坑很多人不知道，就是我们在模拟header时，`Accept-Encoding:gzip, deflate, br`这一项不能加进去，否则服务器返回的数据是经过压缩处理的，我们在转码的时候会报类似于：
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1：invalid start byte`的错误，浏览器能够自动解压，程序却不能自动解压gzip，需要额外进行设置才行。

我被这个bug卡了好久，直到看了这个BLOG：[编解码报错](http://blog.csdn.net/Hudeyu777/article/details/76023441 )[参考3]

另外，在下载源网页这个阶段，可能会出现被服务器禁止访问的情况，也就是被服务器的反爬虫机制识别了出来，这时候程序通常会报一个`forbidden` 的异常并停滞运行，为了保护我们之前爬到的数据，我们要对请求服务器的这段代码进行异常处理。

```
    html = -1 # 如果返回 -1，说明爬取失败， 那么马上 进行数据的存储
    # 解决爬取失败问题
    try:
        html = urlopen(req).read().decode('utf-8')
    except Exception:
        return html
    return html
```

* * *
#### 解析目标网页
网页的解析，我使用的工具是` beautifulsoap `。

首先修补一下网页，使的HTML源码呈现出层次，这样又便于我们对源码进行分析，找到里面的规律。
```
def fix_html(html_str):
    # 修补html
    soup = BeautifulSoup(html_str,'html.parser', from_encoding="gb18030")
    fixed_html = soup.prettify()
    return fixed_html
```

这里我就不对源码进行分析了，而是把beautifulsoap中常用的方法总结一下，免得以后用到的时候，再去网上查找。以以下的HTML代码解析为例。

```
<div class="c" id="M_G7xSB64Vy">
   <div>
    <a class="nk" href="https://weibo.cn/u/5462588938">
     风中的承诺VV
    </a>
    <span class="ctt">
     :更不用说那些代言了国产手机却日常使用
     <span class="kt">
      苹果手机
     </span>
     的明星们了！//【小米员工用iPhone 雷军：国内通病，华为员工也用】 小米员工用iPhone 雷军：国内通病，华为员工也用
    </span>
    <a href="https://weibo.cn/attitude/G7xSB64Vy/add?uid=6091593152&amp;rl=1&amp;st=49c9cf">
     赞[0]
    </a>
    <a href="https://weibo.cn/repost/G7xSB64Vy?uid=5462588938&amp;rl=1">
     转发[0]
    </a>
    <a class="cc" href="https://weibo.cn/comment/G7xSB64Vy?uid=5462588938&amp;rl=1#cmtfrm">
     评论[0]
    </a>
    <a href="https://weibo.cn/fav/addFav/G7xSB64Vy?rl=1&amp;st=49c9cf">
     收藏
    </a>
    <!-- -->
    <span class="ct">
     03月15日 23:58 来自
     <a href="https://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2F3g.sina.com.cn">
      手机新浪网
     </a>
    </span>
   </div>
  </div>
```
这是一条微博的HTML源码，我们可以看到一条微博就是一个`class = "c" 的division`。

> 例一：
获取包含 class 为 c ，并且存在id属性的 div ， 也就是获取源码中所有的微博division

```
# 对于存在 id属性，我们可以用正则表达式匹配任何值
microblog_soups = soup.find_all('div', attrs = {'class' : 'c'}, id = re.compile('.*'))
```

> 例二：
获取昵称，class = "nk"

```
# 注意是 get_text(),而不是 gettext()
nickname = microblog_soup.find('a',attrs = {'class' : 'nk'}).get_text().strip()
```

> 例三：
获取用户主页，class = "nk"

```
index = microblog_soup.find('a',attrs = {'class' : 'nk'}).get('href').strip()
```


> 例四：
获取点赞数

```
# 获取点赞数 例如：0
re_str = u'https://weibo.cn/attitude.*' # 正则表达式，用来匹配href的值
thumb_up = microblog_soup.find('a', href = re.compile(re_str)).get_text().strip()
thumb_up_count = int(re.findall(re_num,thumb_up[2:])[0])
```

> 例五：
获取微博内容

```
content = microblog_soup.find('span',attrs = {'class' : 'ctt'}).get_text().strip()
```

这里有一个很好的Demo：[python 之 BeautifulSoup标签查找与信息提取](https://www.cnblogs.com/my1e3/p/6657926.html?utm_source=itdadao&utm_medium=referral)[参考5]


* * *

#### 数据的存储
目前接触到的比较方便的存储方式，就是存储成csv文件。
代码如下：
```
# 新建一个cvs文件
def init_csv(path,attrs):
    csvfile = open(path, 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(attrs)
    csvfile.close()
    return

# 写入cvs文件
def write_csv(path,items):
    csvfile = open(path, 'a', newline='', encoding='utf-8')
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

path = "C:\\Users\\wansho\\Desktop\\微博数据.csv"
attrs = ['昵称','性别','所在地','时间','内容','点赞数','转发数','评论数','主页']
my_io.init_csv(path,attrs)
my_io.write_csv(path,microblogs)

```
* * *

## Source code
[Github](https://github.com/wansho/)  https://github.com/wansho/sina_weibo_crawl


* * *

## Next
现在写成的爬虫还是有缺陷的，虽然采用了cookie模拟登陆，但是在爬取的过程中还是能够被微博反爬虫机制发现，目前问题还没有解决。

* * *
## Reference
1. `python转码` http://blog.csdn.net/yexiaohhjk/article/details/68066843
2. `优先选择爬移动版`  https://www.zhihu.com/question/29666539 
3. `编解码报错` http://blog.csdn.net/Hudeyu777/article/details/76023441
4. `【python网络编程】新浪爬虫：关键词搜索爬取微博数据`  http://blog.csdn.net/jiange_zh/article/details/47361555
5. `python 之 BeautifulSoup标签查找与信息提取`   https://www.cnblogs.com/my1e3/p/6657926.html?utm_source=itdadao&utm_medium=referral

* * *
## Tools
1. 在线正则表达式 http://tool.oschina.net/regex/
2. Unicode编码转换器 http://tool.chinaz.com/Tools/Unicode.aspx
3. url转码 http://tool.oschina.net/encode?type=4