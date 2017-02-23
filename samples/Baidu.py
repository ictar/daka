#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Site import Site
from ConfigParser import ConfigParser
import time

class Baidu(Site):
	def __init__(self):
		super(Baidu, self).__init__(sitename="Baidu")
		
	def login(self,user="",psw=""):
		login_url = "https://tieba.baidu.com/index.html"
		click_login = ("xpath", "//li[@class='u_login']/div/a")
		data = {
			"userName": user,
			"password": psw,
		}
		btn = ("xpath", '//*[@id="TANGRAM__PSP_8__submit"]')
		self._login(login_url, data, btn, click_login)
		self._visit("http://tieba.baidu.com/f/user/json_userinfo")
		time.sleep(3)
		print self._browser.find_by_xpath("//body").first.text
		

	#百度贴吧签到
	def tiebaSignIn(self):
		tieba_url = "https://tieba.baidu.com/index.html"
		self._visit(tieba_url)
		time.sleep(3)
		self._click("xpath", '//div[@id="onekey_sign"]/a')
		time.sleep(3)
		self._click('xpath', '//div[@class="sign_detail_hd"]/a[@class="j_sign_btn sign_btn sign_btn_nonmember"]')

	# 百度知道签到
	def zhidaoSignIn(self):
		zhidao_url = "https://zhidao.baidu.com/"
		self._visit(zhidao_url)
		time.sleep(3)
		self._click('xpath', "//div[@class='sign-in-section']/a[@class='go-sign-in']")
		time.sleep(3)
		self._click("id", "sign-in-btn")
		time.sleep(3)


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

if "__main__" == __name__:
	run()
