# Miku 


## 项目说明
由于抓取的目标网址在普通情况下不可访问，所以代码需要部署在海外的vps上，
推荐[vultr](https://www.vultr.com/?ref=7788287)，每月最低仅需$3.5


- crawl.py
  
  爬虫代码，抓取几个海外的代理网站

- prove.py 

  验证代码，每隔一段时间验证数据库里的代理是否还存活

- app.py

  Tornado框架搭建的api服务

- run.py
  
  启动文件
  



## 下载安装

- 下载源码


    git clone https://github.com/ngauerh/Miku.git


- 安装依赖


    cd Miku
    pip install -r requirements.txt
    
    
- 配置settings.py
    
    
    DB是数据库配置，使用MySQL数据库
    
    SERVER_PORT 是api服务使用的端口
    
    API_USERNAME，API_PASSWD是使用api时需携带的参数
    

- 启动
    
    
    python3 run.py
    
    
## 使用
启动过十秒后就可以从数据库里看到抓取的代理IP


| api | method | description | arg |
| :------: | :------: | :------: | :------: |
| / | GET | Hello, Welcome to Miku | None |
| /get_all | GET | 获取所有代理 | None |
| /get | GET | 随机获取一个代理 | None |
| /overseas | GET | 随机获取一个海外代理 | None |
| /delete | GET | 删除代理 | proxy=ip |



<pre>
import requests

# 获取代理
def get_proxy():
    res = requests.get("http://127.0.0.1:SERVER_PORT/get", param={'usr':API_USERNAME,'password':API_PASSWD})
    return res.text

# 删除代理
def del_proxy():
    res = requests.get("http://127.0.0.1:SERVER_PORT/delete?proxy={}".format(ip), param={'usr':API_USERNAME,'password':API_PASSWD})
    
</pre>

    
