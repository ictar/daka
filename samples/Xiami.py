#!/usr/bin/python
#-*- coding:utf-8 -*-

import splinter
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.xiami.com/
class Xiami(Site):
	def __init__(self):
		Site.__init__(self,sitename="Xiami")

	def login(self,user="",psw=""):
		login_url = r"https://login.xiami.com/member/login"
		data = {
			"account": user,
			"pw": psw,
		}
		btn = ("id", "submit")
		click_login = ("id", "J_LoginSwitch")

		self._login(login_url, data, btn, click_login)

	#签到
	def daka(self):
		try:
			self._click("xpath", "//b[@class='icon tosign']")
		except splinter.exceptions.ElementDoesNotExist as e:
			pass

def run():
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("xiami","username")
	pwd = cf.get("xiami","password")
	xm = Xiami()
	xm.login(username,pwd)
	xm.daka()
	
if __name__ == '__main__':
	run()
