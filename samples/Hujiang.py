#!/usr/bin/python
#-*- coding:utf-8 -*-

import hashlib
import time,random
import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#bulo.hujiang.com
class Hujiang(Site):
	def __init__(self):
		Site.__init__(self,sitename="Hujiang")
		self.loginurl="http://pass.hujiang.com/quick/synclogin.aspx"
		self.INDEX_URL = "http://bulo.hujiang.com/"
		self._callback = "jQuery18307142652559559792_1442495521490"
		self.LOGIN_URL = "http://pass.hujiang.com/quick/synclogin.aspx"
		self.TOKEN_URL = "http://pass.hujiang.com/quick/account/?callback=%s&account=%s&password=%s&code=&act=loginverify&source=bulo_anon&_=%s"

	def login(self,user="",psw=""):
		self._getToken(user,psw)
		hjHeaders = {
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate, sdch",
			"Accept-Language":"zh-CN,zh;q=0.8",
			"Host":"pass.hujiang.com",
			"Referer":"http://bulo.hujiang.com/anon/?source=nbulo&returnurl=http%3a%2f%2fbulo.hujiang.com%2fhome%2f",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
		}
		hjData = {
			"token":self._token,
			"remeberdays":14,
			"callback":self._callback,
			"_":str(int(time.time()*1000)),
		}
		def respParserFunc(resp):
			#print resp.read().decode("utf-8")[41:-2]
			resp = eval(resp.read().decode("utf-8")[41:-2])
			return (1,"%s Login Success!"%user) if resp["code"] == 0 else (resp["code"].encode("utf-8"),resp["message"].encode("utf-8"))
		self._login(headers=hjHeaders, data=hjData, respParserFunc=respParserFunc)
		
	def _md5(self,pwd):
		m = hashlib.md5()
		m.update(pwd)
		return m.hexdigest()
	def _getToken(self,user,psw):
		hjHeaders = {
				"Accept":"*/*",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"Host":"pass.hujiang.com",
				"Referer":"http://bulo.hujiang.com/anon/?source=nbulo&returnurl=http%3a%2f%2fbulo.hujiang.com%2fhome%2f",
				"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
			}
		url = self.TOKEN_URL%(self._callback,user,self._md5(psw),str(int(time.time()*1000)))
		def respParserFunc(resp):
			true, false, null = 'true', 'false', ''
			resp = eval(resp.read().replace(self._callback,""))
			if resp["code"] == 0:
				self._logger.info("Get Token for user %s succeed~~" % user)
			else:
				self._logger.info("Wooooo, there must be something wrong~\n code = %s \n message = %s \n" % (resp["code"].encode("utf-8"), resp["message"].encode("utf-8")))
			return (resp["code"], resp["data"]["ssotoken"])
		code, self._token = self._process(url, headers=hjHeaders, respParserFunc=respParserFunc)

	#签到
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"bulo.hujiang.com",
				"Referer":"http://bulo.hujiang.com/home/",
				}
		SIGN_URL = "http://bulo.hujiang.com/app/api/ajax_take_card.ashx?%.17f"%random.random()
		def respParserFunc(resp):
			resp = resp.read()
			try:
				if int(resp[0]) > 0:
					return (0, u"打卡成功，获得%s沪元，共打卡%s天~~" % (resp[0],resp[1]))
				if int(resp[0]) == 0:
					return (1, u"已经打过卡了喔~~")
				if int(resp[0]) == -1:
					return (-1, u"用户未激活")
			except Exception, e:
				return (-999, u"未知错误！\n %s" % resp)
		self._daka(SIGN_URL, headers=signHeaders, respParserFunc=respParserFunc)

if __name__ == '__main__':
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("hujiang","username")
	pwd = cf.get("hujiang","password")
	hj = Hujiang()
	hj.login(username,pwd)
	hj.daka()
