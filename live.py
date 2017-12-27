# -*- coding: utf-8 -*-
'''
各平台的规则
'''

import requests 
import json
import time
from db import Db


class Live:

    def __init__(self,live,url,pages):
        self.live = live
        self.url = url
        self.pages = pages
    
    def getApi(self,pageId):
        pageurl = self.url+str(pageId)

        if self.live == 'panda':
            pageurl += '&pagenum=120'

        if self.live == 'zhanqi':
            pageurl += '.json'
        
        response = requests.get( url = pageurl)
        result = response.text
        return json.loads(result)
    
    def insertData(self,datas):
        db = Db()
        for d in datas:
            db.insert(d)
    
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

    def __insertData(self,datas):
        db = Db()
        for d in datas:
            db.insert(d)

    def go(self,sleep=4):
        for x in range(self.pages):
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
            print('--------------insert 数据插入中 第'+str(x+1)+'次---------------')
            time.sleep(sleep)
            print('--------------间隔'+str(sleep)+'秒后再次请求---------------')

