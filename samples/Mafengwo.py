#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser
from time import time

#http://www.mafengwo.cn/
class Mafengwo(Site):
	def __init__(self):
		Site.__init__(self,sitename="Mafengwo")
		self.LOGIN_URL = "https://passport.mafengwo.cn/login-popup.html"

	def login(self,user="",psw=""):
		self._logger.info("user is: %s" % user)
		mfwHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Encoding":"gzip, deflate",
			"Accept-Language":"zh-CN,zh;q=0.8",
			"Origin":"https://passport.mafengwo.cn",
			"Host":"passport.mafengwo.cn",
			"Referer":"https://passport.mafengwo.cn/login-popup.html",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
		}

		mfwData = {
			"passport":user,
			"password":psw,
			"code":"",
		}
		
		def respParserFunc(resp): 
			return (1, "Login Success!")  if 200 == resp.getcode() else (-1, "Wooooo, there must be something wrong~")
		code, msg = self._login(method="POST", headers=mfwHeaders, data=mfwData,respParserFunc=respParserFunc)
		if code == -1: self._login(method="POST", headers=mfwHeaders, data=mfwData,respParserFunc=respParserFunc)

	#签到
	def signIn(self):
		signHeaders = {
				"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
				#"Accept-Encoding":"gzip, deflate",
				"Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
				"Host":"www.mafengwo.cn",
				"Referer":"http://www.mafengwo.cn/",
			}
                #http://www.mafengwo.cn/ajax/ajax_japp.php?callback=jQuery18105755553864366139_1442836474475&app=daka&loaded_modules=%2Fjs%2FDropdown%2CInputListener%2CSuggestionXHR%2CDropList%2CSuggestion%2C%2Fjs%2FSiteSearch%2Cjq-upnum%2Cdialog%2FLayer%2Cdialog%2FDialogBase%2Cdialog%2FDialog%2CTopTip%2CSlider%2Cjq-mousewheel%2CScrollBar%2CCookie%2Cxdate%2Cjqui-core%2Cjqui-datepicker%2CDateRangePicker%2Cjq-tmpl%2CPagination%2CStorage%2Cjq-jgrowl&params=%7B%7D&_=1442836608590
		ts = int(time()*1000)
		SIGN_URL = "http://www.mafengwo.cn/ajax/ajax_japp.php?callback=jQuery18105755553864366139_%s&app=daka&loaded_modules=%%2Fjs%%2FDropdown%%2CInputListener%%2CSuggestionXHR%%2CDropList%%2CSuggestion%%2C%%2Fjs%%2FSiteSearch%%2Cjq-upnum%%2Cdialog%%2FLayer%%2Cdialog%%2FDialogBase%%2Cdialog%%2FDialog%%2CTopTip%%2CSlider%%2Cjq-mousewheel%%2CScrollBar%%2CCookie%%2Cxdate%%2Cjqui-core%%2Cjqui-datepicker%%2CDateRangePicker%%2Cjq-tmpl%%2CPagination%%2CStorage%%2Cjq-jgrowl&params=%%7B%%7D&_=%s" % (str(ts), str(ts+33))
		def respParserFunc(resp):
			resp = json.loads(resp.read().decode("utf-8")[41:-2])
			return (1, u"打卡成功~~") if resp["css"] else (-1, u"未知错误！\n %s" % resp)
		self._daka(SIGN_URL, headers=signHeaders, respParserFunc=respParserFunc)

	def getHoney(self):
		''' 领取蜂蜜
		'''
		honeyHeaders = {
				"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
				#"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
				"Host":"www.mafengwo.cn",
				"Referer":"http://www.mafengwo.cn/",
			}
		ts = int(time()*1000)
		HONEY_URL = "http://www.mafengwo.cn/ajax/ajax_daka.php?act=getHoney&callback=jQuery18108634763753507286_%s&_=%s" % (str(ts), str(ts+50))
		def respParserFunc(resp):
			content = resp.read().decode("utf-8")
			self._logger.info(content)
			resp = json.loads(content[41:-2])
			return (resp["ret"], resp["msg"])
		self._daka(HONEY_URL, headers=honeyHeaders, respParserFunc=respParserFunc)


def run():
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("mafengwo", "username")
	pwd = cf.get("mafengwo","password")
	mfw = Mafengwo()
	mfw.login(username,pwd)
	mfw.signIn()
	mfw.getHoney()

if "__main__" == __name__:
	run()
