#!/usr/bin/python
#-*- coding:utf-8 -*-

import hashlib
import time,random
import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.zimuzu.tv/
class Zimuzu(Site):
	def __init__(self):
		Site.__init__(self,sitename="Zimuzu")
		self.LOGIN_URL = "http://www.zimuzu.tv/User/Login/ajaxLogin"

	def login(self,user="",psw=""):
		zmzHeaders = {
			"Accept":"*/*",
			"Accept-Language":"zh-CN,zh;q=0.8",
			"Host":"www.zimuzu.tv",
			"Referer":"http://www.zimuzu.tv/user/login",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
		}
		zmzData = {
			"account":user,
			"password":psw,
			"remember":1,
			"url_back":"http://www.zimuzu.tv/",
		}
		def respParserFunc(resp):
			resp = resp.read()
			try:
				if not resp: return (0, "Login Successfully~")
				resp = json.loads(resp.decode("utf-8"))
				return (resp.get("status",-1), resp.get("info",""))
			except Exception, e:
				return (-999, u"未知错误！\n %s" % "\n".join(resp))
		self._login(method="POST", headers=zmzHeaders, data=zmzData, respParserFunc=respParserFunc)
		

	#签到???
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"www.zimuzu.tv",
				"Referer":"http://www.zimuzu.tv/user/sign",
				}
		self._get("http://www.zimuzu.tv/user/sign", signHeaders,{})
		time.sleep(16)
		SIGN_URL = "http://www.zimuzu.tv/user/sign/dosign"
		def respParserFunc(resp):
			resp = resp.read()
			try:
				if not resp: return (0, "Login Successfully~")
				resp = json.loads(resp.decode("utf-8"))
				return (resp.get("status",-1), resp.get("info",""))
			except Exception, e:
				return (-999, u"未知错误！\n %s" % "\n".join(resp))
		self._daka(SIGN_URL, headers=signHeaders, respParserFunc=respParserFunc)

if __name__ == '__main__':
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("zimuzu","username")
	pwd = cf.get("zimuzu","password")
	zmz = Zimuzu()
	zmz.login(username,pwd)
	zmz.daka()
