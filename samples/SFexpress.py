#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#i.sf-express.com
class SFexpress(Site):
	def __init__(self):
		Site.__init__(self,sitename="SFexpress")
		self.LOGIN_URL = "https://i.sf-express.com/sso/login"

	def login(self,user="",psw=""):
		execution, lt, eventId = self._getLoginInfo()
		if execution and lt and eventId:
			sfHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				#"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"Host":"i.sf-express.com",
				"Referer":"https://i.sf-express.com/new/cn/sc/user/login.html",
				"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
			}
			sfData = {
				"loginView":"json",
				"service":"https://i.sf-express.com/service/new/ticket/loginResult",
				"username":user,
				"password":psw,
				"lt":lt,#LT-2869409-Jipndam5LkfTQrjqx0oJdSW7boNrMD,
				"execution":execution,#"e1s1",
				"_eventId":eventId,#"submit",
				"checkVerifyCode":1,
				"loginSource":"",
				"userLoginType":0,
				"verifyCode":"",
			}
			def respParserFunc(resp):
				if 200 == resp.getcode():
					result = json.loads(resp.read())
					if result.get("hasErr"):
						return (result["hasErr"], result["err"])
					else:
						return (1,"%s Login Success!"%user)
				else:
					return (1,"%s Login Success!"%user)
			self._login(headers=sfHeaders, data=sfData, respParserFunc=respParserFunc)
		else:
			self._logger.error("cannot get value of execution, lt or eventId")
	# get execution, lt, _eventId for login
	def _getLoginInfo(self):
		sfHeaders = {
				"Accept":"*/*",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"Host":"i.sf-express.com",
				"Referer":"https://i.sf-express.com/new/cn/sc/user/login.html",
				"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
			}
		sfData = {
			"loginView":"json",
			"service":"https://i.sf-express.com/service/new/ticket/loginResult"
		}
		url = "https://i.sf-express.com/sso/login"
		resp = self._get(url, headers=sfHeaders, data=sfData)
		resp = json.loads(resp.read().strip())
		if resp["hasErr"] == 0:
			self._logger.info("Get Info for user succeed~~")
			return (resp["execution"], resp["lt"], resp["_eventId"])
		else:
			self._logger.error("Wooooo, there must be something wrong~\n code = %s \n message = %s \n" % (resp["hasErr"].encode("utf-8"), resp["err"].encode("utf-8")))
			return ("", "", "")
		

	#签到
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"i.sf-express.com",
				"Referer":"https://i.sf-express.com/new/cn/sc/i-index.html",
				}
		SIGN_URL = "https://i.sf-express.com/service/new/member/checkin"
		def respParserFunc(resp):
			resp = resp.read()
			if "errorcode" in resp:
				self._logger.error("checkin error: %s" % resp)
				return (-1, "daka failed")
			else:
				self._logger.info("checkin successfully: %s" % resp)
				return (0, resp)
		self._daka(SIGN_URL, method="POST", headers=signHeaders, respParserFunc=respParserFunc)


def run():
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("sfexpress","username")
	pwd = cf.get("sfexpress","password")
	sf = SFexpress()
	sf.login(username,pwd)
	sf.daka()

if __name__ == '__main__':
	run()
