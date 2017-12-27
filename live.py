# -*- coding: utf-8 -*-
'''
各平台的规则
'''

import requests 
import json
import time
from db import Db


class Live:

    def __init__(self,live,url):
        self.live = live
        self.url = url
        self.pages = 1

    # 请求接口
    def getApi(self,pageId):
        pageurl = self.url+str(pageId)

        if self.live == 'panda':
            pageurl += '&pagenum=120'

        if self.live == 'zhanqi':
            pageurl += '.json'
        
        response = requests.get( url = pageurl)
        result = response.text
        return json.loads(result)

    #获取总页码，决定请求次数
    def getPageCount(self,datas):
        if self.live == 'douyu':
            self.pages = datas['data']['pgcnt']
        elif self.live == 'huya':
            self.pages = datas['data']['totalPage']
        elif self.live == 'panda':
            self.pages = int(datas['data']['total']/120)
        elif self.live == 'zhanqi':
            self.pages = int(datas['data']['cnt']/20)
        return self.pages

    """------------------数据格式化----------------------"""

    #斗鱼
    def douyu(self,datas):
        _lists = datas['data']['rl']
        _result = []
        for rs in _lists:
            tmp = { 
                'rid'       : rs['rid'],
                'category'  : rs['c2name'], 
                'number'    : rs['ol'],
                'name'      : rs['nn'],
                'uid'       : rs['uid'],
                'source'    : '斗鱼',
                'url'       : rs['url']
            }
            _result.append(tmp)
        return _result

    #虎牙
    def huya(self,datas):
        _lists = datas['data']['datas']
        _result = []
        for rs in _lists:
            tmp = { 
                'rid'       : rs['gid'],
                'category'  : rs['gameFullName'], 
                'number'    : rs['totalCount'],
                'name'      : rs['nick'],
                'uid'       : rs['uid'],
                'source'    : '虎牙',
                'url'       : '/'+rs['privateHost']
            }
            _result.append(tmp)
        return _result
    
    #熊猫
    def panda(self,datas):
        _lists = datas['data']['items']
        _result = []
        for rs in _lists:
            tmp = { 
                'rid'       : rs['id'],
                'category'  : rs['classification']['cname'], 
                'number'    : rs['person_num'],
                'name'      : rs['userinfo']['nickName'],
                'uid'       : rs['userinfo']['rid'],
                'source'    : '熊猫',
                'url'       : '/'+str(rs['id'])
            }
            _result.append(tmp)
        return _result
    
    #战旗
    def zhanqi(self,datas):
        _lists = datas['data']['rooms']
        _result = []
        for rs in _lists:
            tmp = { 
                'rid'       : rs['id'],
                'category'  : rs['newGameName'], 
                'number'    : rs['online'],
                'name'      : rs['nickname'],
                'uid'       : rs['uid'],
                'source'    : '战旗',
                'url'       : rs['url']
            }
            _result.append(tmp)
        return _result

    #数据入库
    def __insertData(self,datas):
        db = Db()
        for d in datas:
            db.insert(d)

    """
    执行
    请求一次接口，获取总页码
    根据总页，遍历请求接口数据
    """
    def go(self,sleep=2):
        response = self.getApi(1)
        pages = self.getPageCount(response)
        print('获取平台总页码数，请等待5秒钟' )
        time.sleep(5)
        print(self.live + '分页数数：' + str(pages)+"，开始执行数据遍历请求")
        for x in range(pages):
            datas = self.getApi( str(x+1) )
            if self.live == 'douyu':
                datas = self.douyu(datas)
            elif self.live == 'huya':
                datas = self.huya(datas)
            elif self.live == 'panda':
                datas = self.panda(datas)
            elif self.live == 'zhanqi':
                datas = self.zhanqi(datas)
            # print(datas)
            self.__insertData(datas)
            print('-------'+self.live+'-------insert 数据插入中 第'+str(x+1)+'次---------------')
            time.sleep(sleep)
            print('--------------间隔'+str(sleep)+'秒后再次请求---------------')

