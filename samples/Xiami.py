#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
import json
import re
import urllib2
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.xiami.com/
class Xiami(Site):
	def __init__(self):
		Site.__init__(self,sitename="Xiami")
		self.LOGIN_URL = r"https://login.xiami.com/web/login"

	def login(self,user="",psw=""):
		xmHeaders = {
			"Accept":"*/*",
			#"Accept-Encoding":"gzip, deflate",
			"Accept-Language":"zh-CN,zh;q=0.8",
			#"Host":"login.xiami.com",
			"Referer":self.LOGIN_URL,
			#"Origin":"https://login.xiami.com",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
		}
		xmData = {	
			"email":user,
			"password":"123",#psw,
			"remember":1,
			"LoginButton":"%E7%99%BB%E5%BD%95",
		}
		def respParserFunc(resp):
			resp = resp.read().decode("utf-8")
			return (0,"login successfully~") if -1 != resp.find(u"我的虾米") \
					else (-1, resp)
		self._login(method="POST", headers=xmHeaders, data=xmData, respParserFunc=respParserFunc)

	#签到
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"www.xiami.com",
				"Referer":"http://www.xiami.com/",
				}
		SIGN_URL = "http://www.xiami.com/task/signin"
		def respParserFunc(resp):
			resp = resp.read()
			print resp
			return (0,"unknown")
		self._daka(SIGN_URL, method="POST", headers=signHeaders, respParserFunc=respParserFunc)

if __name__ == '__main__':
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("xiami","username")
	pwd = cf.get("xiami","password")
	xm = Xiami()
	xm.login(username,pwd)
	xm.daka()
