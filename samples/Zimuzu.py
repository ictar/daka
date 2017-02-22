#!/usr/bin/python
#-*- coding:utf-8 -*-
"""
zimuzu.tv
网站已停止签到,改为累计登录网站时间,每天使用浏览器或APP访问网站即可自动获得一个登录累计
"""
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#http://www.zimuzu.tv/
class Zimuzu(Site):
	def __init__(self):
		Site.__init__(self, sitename="Zimuzu")

	def login(self,user="",psw=""):
		login_url = "http://www.zmz2017.com/user/login"
		data = {
			"email": user,
			"password": psw
		}
		btn = ("id", 'login')
		self._login(login_url, data, btn)


def run():
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("zimuzu","username")
	pwd = cf.get("zimuzu","password")
	zmz = Zimuzu()
	zmz.login(username,pwd)

if __name__ == '__main__':
	run()
