#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from Baidu import Baidu
from Hujiang import Hujiang
from Mafengwo import Mafengwo
from LifeVC import LifeVC
from Zimuzu import Zimuzu
from ConfigParser import ConfigParser

if "__main__" == __name__:
	#read configuration file
	configFile = os.path.join(sys.path[0],"user_config.ini")
	#print "the configuration file is in ", configFile
	cf = ConfigParser()
	cf.read(configFile)
	#lifevc auto sign in
	username = cf.get("lifevc","username")
	pwd = cf.get("lifevc","password")
	lvc = LifeVC()
	lvc.login(username,pwd)
	lvc.daka()
	#hujiang atuo sign in
	username = cf.get("hujiang","username")
	pwd = cf.get("hujiang","password")
	hj = Hujiang()
	hj.login(username,pwd)
	hj.daka()
	username = cf.get("baidu","username")
	pwd = cf.get("baidu","password")
	#baidu auto sign in
	bd = Baidu()
	bd.login(username,pwd)
	bd.tiebaSignIn()
	#mafengwo auto sign in
	username = cf.get("mafengwo", "username")
	pwd = cf.get("mafengwo","password")
	mfw = Mafengwo()
	mfw.login(username,pwd)
	mfw.signIn()
	mfw.getHoney()
	#zimuzu auto sign in
	username = cf.get("zimuzu","username")
	pwd = cf.get("zimuzu","password")
	zmz = Zimuzu()
	zmz.login(username,pwd)
	zmz.daka()

