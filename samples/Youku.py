#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
import json
import sys,os
sys.path.append('../')
from Site import Site
from ConfigParser import ConfigParser

#http://www.youku.cn/, unfinished
class Youku(Site):
	def __init__(self):
		super(Youku, self).__init__(sitename="Youku")
		self.LOGIN_URL = "https://login.youku.com/user/login_submit/"

	def login(self,user="",psw=""):
		self._getToken(user,psw)
		ykHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			#"Accept-Encoding":"gzip, deflate, sdch",
			"Accept-Language":"zh-CN,zh;q=0.8",
			"Host":"login.youku.com",
			"Referer":"http://login.youku.com/user/login_win?from=header",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
		}
		ykData = {
			"passport":user,
			"password":psw,
			"captcha":"",
			"remember":1,
			"callback":"logincallback"+str(int(time.time()*1000)),
			"from":"http%253A%252F%252Fwww.youku.com%252F%40%40%40%40header",
			"wintype":"pop",
		}
		def respParserFunc(resp):
			resp = eval(resp.read().decode("utf-8")[41:-2])
			return (1,"%s Login Success!"%user) if resp["code"] == 0 else (resp["code"].encode("utf-8"),resp["message"].encode("utf-8"))
		self._login(method="POST", headers=ykHeaders, data=ykData, respParserFunc=respParserFunc)

	#签到
	def signIn(self):
		signHeaders = {
				"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
				"Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"actives.youku.com",
                "Referer":"http://actives.youku.com/task/signv2/index",
              }
		SIGN_URL = "http://actives.youku.com/task/signv2/qiandao?pl=web"
		def respParserFunc(resp):
			resp = json.loads(resp.read().encode("utf-8"))
			return (resp["errno"], resp["errmsg"])
		self._daka(SIGN_URL, headers=signHeaders, respParserFunc=respParserFunc)

if __name__ == '__main__':
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("youku","username")
	pwd = cf.get("youku","password")
	yk = Youku()
	yk.login(username,pwd)
	yk.signIn()
