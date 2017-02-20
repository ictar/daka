#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.mafengwo.cn/
class Mafengwo(Site):
	def __init__(self):
		Site.__init__(self,sitename="Mafengwo")

	def login(self,user="",psw=""):
		login_url = "https://passport.mafengwo.cn/login-popup.html"
		data = {
			"passport": user,
			"password": psw,
		}
		btn = ("xpath", '//div[@class="login-buttons"]/button')

		self._login(login_url, data, btn)

	#签到
	def signIn(self):
		self._click("id", "head-btn-daka")

	def getHoney(self):
		''' 领取蜂蜜
		'''
		print "现在不能通过打卡领蜂蜜啦~~~~(>_<)~~~~"


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
	#mfw.getHoney()

if "__main__" == __name__:
	run()
