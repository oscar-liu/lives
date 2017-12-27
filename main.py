# -*- coding: utf-8 -*-
'''
抓取各直播平台的主播相关信息
auth: litchi
date : 2017.12
'''
import yaml 
from live import Live

if __name__ == '__main__':
    f = open('config.yaml')
    config = yaml.load(f)

    #单线程
    for x in config:
        spiders = Live(x['name'],x['url'],x['pages'])
        spiders.go(2)

    # demo
    # spiders = Live('douyu','https://www.douyu.com/gapi/rkc/directory/0_0/',2)
    # spiders.go()

    
