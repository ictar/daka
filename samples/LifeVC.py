#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.lifevc.com/
class LifeVC(Site):
	def __init__(self):
		Site.__init__(self,sitename="LifeVC")
		self.LOGIN_URL = "https://account.lifevc.com/account/login"

	def login(self,user="",psw=""):
		self._logger.info("user is: %s" % user)
		lvcHeaders = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Origin":"https://account.lifevc.com",
                "Host":"account.lifevc.com",
                "Referer":"https://account.lifevc.com/Account/login?rt=%2fUserCenter",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }

		lvcData = {
			"acct":user,
			"pwd":psw,
			"validation":"",
		}
		
		def respParserFunc(resp): 
			resp = json.loads(resp.read().decode("utf-8"))
			return (resp.get("Status"), resp.get("Message"))
		code, msg = self._login(method="POST", headers=lvcHeaders, data=lvcData,respParserFunc=respParserFunc)

	#签到
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip, deflate",
				"Accept-Language":"zh-CN,zh;q=0.8",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"account.lifevc.com",
                "Referer":"https://account.lifevc.com/UserCenter",
              }
		SIGN_URL = "https://account.lifevc.com/usercenter/doSignIn"
		def respParserFunc(resp):
			resp = json.loads(resp.read().decode("utf-8"))
			return (resp.get("Status"), resp.get("Message"))
		self._daka(SIGN_URL, method="POST", headers=signHeaders, respParserFunc=respParserFunc)

if "__main__" == __name__:
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("lifevc", "username")
	pwd = cf.get("lifevc","password")
	lvc = LifeVC()
	lvc.login(username,pwd)
	lvc.daka()
