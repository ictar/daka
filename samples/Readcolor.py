#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser
import base64
import rsa
import binascii

#http://readcolor.com/
class Readcolor(Site):
	def __init__(self):
		Site.__init__(self,sitename="Readcolor")
		self.LOGIN_URL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
	
	def login(self,user="",psw=""):
		self._wblogin(user,psw)
		headers = {
			"Host": "api.weibo.com",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Origin": "https://api.weibo.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
			"Content-Type": "application/x-www-form-urlencoded",
			"Referer": "https://api.weibo.com/oauth2/authorize?client_id=786182754&redirect_uri=http%3A%2F%2Freadcolor.com%2Foauth%2Ffinish&response_type=code&display=default"
		}
		postData = {
			"action":"login",
			"display":"default",
			"withOfficalFlag":0,
			"quick_auth":"null",
			"withOfficalAccount":"",
			"scope":"",
			"ticket":self.ticket,
			"isLoginSina":"",
			"response_type":"code",
			"regCallback":"https://api.weibo.com/2/oauth2/authorize?client_id=786182754&response_type=code&display=default&redirect_uri=http://readcolor.com/oauth/finish&from=&with_cookie=",
			"redirect_uri":"http://readcolor.com/oauth/finish",
			"client_id":"786182754",#网站固定值
			"appkey62":"1gpWpQ",#网站固定值
			"state":"",
			"verifyToken":"null",
			"from":"",
			"switchLogin":"0",
			"userId":"",
			"passwd":"",
		}
		authURL = "https://api.weibo.com/oauth2/authorize"
		def respParserFunc(resp):
			#print resp.read()
			return (resp.getcode(),"\n".join(resp.info().headers))
		code, self.location = self._process(
									url=authURL, 
									#headers=headers, 
									method="POST",
									data=postData,
									respParserFunc=respParserFunc)
		print code, self.location
		self._logger.info(u"返回码是：{0}, Location为：{1}".format(code, self.location))
	
	def _wblogin(self,user="",psw=""):
		servertime, nonce, pubkey, rsakv = self._getLoginInfo()
		postData = {
			'entry': 'openapi',
			'gateway': '1',
			'from': '',
			'savestate': '0',
			'userticket': '1',
			"pagerefer": "http://readcolor.com/",
			"ct":1800, #网站固定值
			"s":1,
			"vsnf": "1",
			"vsnval":"",
			"door":"",
			"appkey":"1gpWpQ", #网站固定值
			"su": self._getSu(user),
			"service": "miniblog",
			"servertime": servertime,
			"nonce": nonce,
			"pwencode": "rsa2",
			"rsakv": rsakv,
			"sp": self._getSp(psw, servertime, nonce, pubkey),
			"sr": "1440*900",
			"encoding": "UTF-8",
			"cdult":2,
			"prelt": "38",
			"domain":"weibo.com",
			"returntype": "TEXT",
		}
		def respParserFunc(resp):
			resp = json.loads(resp.read())
			return (resp.get("retcode"),resp.get("ticket"))
		code, self.ticket = self._login(method="POST", data=postData, respParserFunc=respParserFunc)
	
	def _getLoginInfo(self):
		preLoginURL = r'http://login.sina.com.cn/sso/prelogin.php'
		preLoginData = {
			"entry":"weibo",
			"callback":"sinaSSOController.preloginCallBack",
			"su":"",
			"rsakt":"mod",
			"client":"ssologin.js(v1.4.18)",
		}
		resp = self._get(url=preLoginURL, data=preLoginData).read()
		data = json.loads(resp[35:-1])
		servertime = data["servertime"]
		nonce = data["nonce"]
		pubkey = data["pubkey"]
		rsakv = data["rsakv"]
		return servertime, nonce, pubkey, rsakv

	def _getSu(self, username):
		"""加密用户名，su为POST中的用户名字段"""
		su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
		return su

	def _getSp(self, password, servertime, nonce, pubkey):
		"""加密密码，sp为POST中的用户名字段"""
		pubkey = int(pubkey, 16)
		key = rsa.PublicKey(pubkey, 65537)
		# 以下拼接明文从js加密文件中得到
		message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
		message = message.encode('utf-8')
		sp = rsa.encrypt(message, key)
		# 把二进制数据的每个字节转换成相应的2位十六进制表示形式。
		sp = binascii.b2a_hex(sp)
		return sp

	#签到
	def daka(self):
		signHeaders = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				#"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"readcolor.com",
				}
		SIGN_URL = "http://readcolor.com/users/sign"
		def respParserFunc(resp):
			resp = json.loads(resp.read())
			return (1,u"打卡成功！") if resp["succeed"] else (0, "{}".format(resp))
		self._daka(SIGN_URL, headers=signHeaders, respParserFunc=respParserFunc)

if __name__ == '__main__':
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("readcolor","username")
	pwd = cf.get("readcolor","password")
	rc = Readcolor()
	rc.login(username,pwd)
	rc.daka()
