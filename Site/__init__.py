#!/usr/bin/python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals

import cookielib
import urllib2,urllib
import re
import logging
from settings import *

class Site(object):
	def __init__(self, logname="Site.log", sitename="", loginurl=""):
		""" 
		initial http related info and log object
			logname: string, name of log file
			sitename: string, identify a site
			loginurl: string, a url string to login
		return: None
		"""
		self._cookie = cookielib.LWPCookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))
		# site info
		self._sitename = sitename
		self.LOGIN_URL = loginurl
		# log object
		self._logger = logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler(logname)
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)

	def _process(self, url, method="GET", headers=settings.headers, data={}, respParserFunc=None):
		"""
		process request and return resultCode and resultMsg
			url: string, a url string to send request
			method: string, with value "GET/POST"
			headers: dict, request will access the url with it. the default value is set in settings.py
			data: dict, contains request data
			respParserFunc: function, used to parse the response. 
		return: response code and message
		"""
		resp = self._get(url,headers,data) if "GET" == method else self._post(url, headers, data)
		if respParserFunc is None: respParserFunc = self._respParserFunc
		code, msg = respParserFunc(resp)
		return (code, msg)

	def _post(self, url, headers, data):
		""" 
		using method "POST"
		"""
		req = urllib2.Request(url, headers = headers)
		return self._opener.open(req, urllib.urlencode(data).encode("utf-8"))

	def _get(self, url, headers, data):
		""" 
		using method "Get"
		"""
		#print "{0}?{1}".format(url, urllib.urlencode(data))
		url = "{0}?{1}".format(url, urllib.urlencode(data)) if url else url
		req = urllib2.Request(url, headers = headers)
		return self._opener.open(req)

	def _respParserFunc(self,resp):
		raise AttributeError

	def _login(self,method="GET",headers=settings.headers, data={"username":"","password":""}, respParserFunc=None):
		"""
		login the site
		"""
		self._logger.info("begin to login in {0}, user is: {1}".format(self._sitename,data.get("username")))
		code, msg = self._process(self.LOGIN_URL,method, headers, data, respParserFunc)
		self._logger.info("login resultCode is {0}, resultMsg is {1}".format(code, msg))
		return (code, msg)


	def _daka(self, url, method="GET", headers=settings.headers, data={}, respParserFunc=None):
		"""
		daka
		"""
		code, msg = self._process(url,method, headers, data, respParserFunc)
		self._logger.info("daka resultCode is {0}, resultMsg is {1}".format(code,msg))

