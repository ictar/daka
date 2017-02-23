#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,os
sys.path.append('../')
from Site import Site
from ConfigParser import ConfigParser

#http://www.youku.cn/, unfinished
class Youku(Site):
	def __init__(self):
		super(Youku, self).__init__(sitename="Youku")

	def login(self,user="",psw=""):
		login_url = "http://www.youku.com/"
		click_login = ("id", "qheader_login")
		data = {
			"YT-ytaccount": user,
			"YT-ytpassword": psw,
		}
		btn = ("id", "YT-nloginSubmit")

		self._login(login_url, data, btn, click_login)

	#签到
	def signIn(self):
		self._click("xpath", "//div[@class='task-info']/a")

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
