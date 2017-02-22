#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#i.sf-express.com
class SFexpress(Site):
	def __init__(self):
		Site.__init__(self,sitename="SFexpress")

	def _get_vcode(self):
		pass

	def login(self,user="",psw=""):
		login_url = "https://ssom.sf-express.com/cas/login?service=https://i.sf-express.com/service/cas/new/casLoginResult"
		data = {
			"username": user,
			"password": psw,
			"vcode": self._get_vcode()
		}
		btn = ("name", "submit")
		self._login(login_url, data, btn)

	#签到
	def daka(self):
		self._click("id", "checkin")


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
