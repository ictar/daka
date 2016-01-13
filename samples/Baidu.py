#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import re
import os,sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup
from time import time

class Baidu(Site):
	def __init__(self):
		#Site.__init__(self,sitename="Baidu")
		super(Baidu, self).__init__(sitename="Baidu")
		self.LOGIN_URL="https://passport.baidu.com/v2/api/?login"
		self.INDEX_URL = "http://www.baidu.com"
		self.TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
		
	def login(self,user="",psw=""):
		self._initial()
		self._getToken()
		bdHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Encoding":"gzip,deflate,sdch",
			"Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
			"Host":"passport.baidu.com",
			"Origin":"http://www.baidu.com",
			"Referer":"http://www.baidu.com/",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
		}
		bdData = {
			"staticpage":"https://www.baidu.com/cache/user/html/v3Jump.html",
			"token":self._token,
			"tpl":"mn",
			"username":user,
			"password":psw,
		}

		def respParserFunc(resp):
			resp = json.loads(self._opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
			return (1,u"登录成功~") if resp and resp["no"] == 0 else (0, u"登录失败~~~~(>_<)~~~~")
		
		self._login(method="POST",headers=bdHeaders, data=bdData, respParserFunc=respParserFunc)
		

	def _getToken(self):
		self._token = eval(self._opener.open(self.TOKEN_URL).read())['data']['token']

	def _initial(self):
		self._opener.open(self.INDEX_URL)

	#百度贴吧签到
	def _getMyTiebaURL(self):
		LIKETIEBA_URL = "http://tieba.baidu.com/f/like/mylike"
		page = self._opener.open(LIKETIEBA_URL).read().decode("gbk")
		soup = BeautifulSoup(page,"html.parser")
		trs = soup.find_all("tr")
		MAIN_URL = "http://tieba.baidu.com/"
		return [tr.contents[0].a["title"] + "::" + MAIN_URL + tr.contents[0].a["href"] for tr in trs[1:]]
	def getTbTbs(self, url):
		reg_getTbs = re.compile("PageData.tbs = \"(\w+)\"|\'tbs\': \"(\w+)|\'tbs\':\'(\w+)")
		return reg_getTbs.findall(self._opener.open(url).read().decode("UTF-8"))[0]
	def tiebaSignIn(self):
		likeUrls = self._getMyTiebaURL()
		#print likeUrls
		signHeaders = {
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
			"Host":"tieba.baidu.com",
			"Origin":"http://tieba.baidu.com",
			"Referer":"http://tieba.baidu.com",
		}
		signData = {
			"ie":"utf-8",
			"kw":"",
			"tbs":"",
		}
		SIGN_URL = "http://tieba.baidu.com/sign/add"
		for item in likeUrls:
			title, url = item.split("::")
			signData['kw'] = title.encode("utf-8")
			signData["tbs"] = self.getTbTbs(url)
			signHeaders["Referer"] = url
			self._logger.info(u"{0}吧开始签到".format(signData['kw'].decode("utf-8")))
			def respParserFunc(resp):
				resp = json.loads(resp.read().decode("utf-8"))
				if resp["no"] == 0:
					return (1,u"签到成功!!")
				if resp["no"] == 1101:
					return (1101,u"之前已经签到过了喔~")
				return (999,u"未知错误！\n {0} \n {1}".format(url,resp))
			
			self._daka(SIGN_URL, method="POST", headers=signHeaders, data=signData, respParserFunc=respParserFunc)

	# 百度知道签到
	def _getZhidaoToken(self,url):
		reg_gettk = re.compile("\"stoken\":\"(\w+)\"")
		return reg_gettk.findall(self._opener.open(url).read().decode("gbk"))[0:1]
	def zhidaoSignIn(self):
		signHeaders = {
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
			"Host":"zhidao.baidu.com",
			"Origin":"http://zhidao.baidu.com",
			"Referer":"http://zhidao.baidu.com",
		}
		signData = {
			"cm":100509,
			"utdata":"14,14,50,48,62,48,48,14,54,51,51,55,43,62,55,55,14488028744070",
			"stoken":self._getZhidaoToken("http://zhidao.baidu.com/")
		}
		SIGN_URL = "http://zhidao.baidu.com/submit/user"
		def respParserFunc(resp):
			resp = json.loads(resp.read().decode("utf-8"))
			return (resp["errorNo"],resp["errorMsg"])
		self._daka(SIGN_URL, method="POST", headers=signHeaders, data=signData, respParserFunc=respParserFunc)

	# 百度知道抽奖,untested
	def _getluckyToken(self, url):
		reg_getlkt = re.compile("'luckyToken', \'(\w+)\'")
		return reg_getlkt.findall(self._opener.open(url).read().decode("gbk"))[0]
	def zhidaolottery(self):
		LotteryHeaders = {
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
			"Host":"zhidao.baidu.com",
			"Referer":"http://zhidao.baidu.com/shop/lottery",
		}
		LotteryData = {
			"type":0,
			"token":self._getluckyToken("http://zhidao.baidu.com/shop/lottery"),
			"_":str(int(time()*1000)),
		}
		print LotteryData
		Lottery_URL = "http://zhidao.baidu.com/shop/submit/lottery"
		def respParserFunc(resp):
			resp = json.loads(resp.read().decode("gbk"))
			print resp
			return (resp["errno"], "{0}\n{1}".format(resp["errmsg"].encode("utf-8"),resp.get("data","").encode("utf-8")))
		self._daka(Lottery_URL, headers=LotteryHeaders, data=LotteryData, respParserFunc=respParserFunc)


def run():
	#read configuration file
	configFile = "user_config.ini"
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("baidu","username")
	pwd = cf.get("baidu","password")
	bd = Baidu()
	bd.login(username,pwd)
	bd.tiebaSignIn()
	bd.zhidaoSignIn()
	#bd.zhidaolottery()

if "__main__" == __name__:
	run()
