#!/usr/bin/python
#-*- coding:utf-8 -*-

import random
import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser

#bulo.hujiang.com
class Hujiang(Site):
	def __init__(self, **kws):
		Site.__init__(self, sitename="Hujiang")

	def login(self,user="",psw=""):
		login_url = "http://bulo.hjenglish.com/"
		data = {
			"username": user,
			"password": psw
		}
		btn = ("xpath", '//*[@id="hp-login-normal"]/button')
		click_login = ("xpath", '//div[@class="reg_log"]/a[@class="log_now"]')

		self._login(login_url, data, btn, click_login)

	#签到
	def daka(self):
		SIGN_URL = "http://bulo.hujiang.com/app/api/ajax_take_card.ashx?%.17f"%random.random()
		self._daka(SIGN_URL)
		print self._browser.find_by_xpath("//body").first.text


def run():
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	cf = ConfigParser()
	cf.read(configFile)
	username = cf.get("hujiang","username")
	pwd = cf.get("hujiang","password")
	hj = Hujiang()
	hj.login(username,pwd)
	hj.daka()

if __name__ == '__main__':
	run()
