#!/usr/bin/python
#-*- coding:utf-8 -*-
import time
from splinter import Browser
import logging
import settings

class Site(object):
	def __init__(self, logname="Site.log", sitename="Site", browser_params=settings.browser_params):
		""" 
		initial http related info and log object
			logname: string, name of log file
			sitename: string, identify a site
			loginurl: string, a url string to login
		return: None
		"""
		self._browser_params = browser_params
		self._browser = Browser(**self._browser_params) if self._browser_params else Browser()
		# site info
		self._sitename = sitename
		# log object
		self._logger = logging.getLogger(sitename)
		self._logger.setLevel(logging.INFO)
		self._handler = logging.FileHandler(logname)
		self._handler.setLevel(logging.INFO)
		self._handler.setFormatter(logging.Formatter('%(asctime)s - ' + sitename + ' - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
		self._logger.addHandler(self._handler)

	def _visit(self, url):
		"""visit {url}"""
		self._browser.visit(url)

	def _click(self, find_type, selector):
		"""
		find an item whose value of {find_type} is {selector}
		:param find_type str find_by_{find_type}, value: css / id / name / tag / text / value /xpath
		:param selector str value of {find_type}
		"""
		allowed_find_type = ("css", "id",
							"name", "tag",
							"text", "value",
							"xpath")
		if find_type not in allowed_find_type:
			raise Exception("find_type {} is invalid.".format(find_type))
		finder = getattr(self._browser, "find_by_{}".format(find_type))
		finder(selector).first.click()

	def _process_form(self, form_data, btn, **kws):
		"""
		process form
		:param form_data dict key is field name while value is field value
		:param btn list/tuple with two element. the first one is type while the second is value. this one is used to click the form button. 
		"""

		for k, v in form_data.items():
			self._browser.fill(k, v)

		self._click(*btn)

		return 

	def _login(self, url, data, btn, click_login=None, delay_time=3, **kws):
		"""
		login the site
		:param url str login url
		:param data dict data for login
		:param btn list/tuple with two element. the first one is type while the second is value. e.g. login button
		:param click_login list/tuple with two element. like btn. but this one is used to show the login form
		:param delay_time int time to delay
		"""
		self._logger.info("begin to login in {0}, user is: {1}".format(self._sitename,data.get("username")))

		self._visit(url)
		time.sleep(delay_time)

		# if we should click to show login form
		if click_login:
			self._click(*click_login)
			time.sleep(delay_time)

		self._process_form(data, btn, **kws)
		time.sleep(delay_time)
		#self._logger.info("login resultCode is {0}, resultMsg is {1}".format(code, msg))
		#return (code, msg)


	def _daka(self, url):
		"""
		daka
		"""
		self._visit(url)

	def __del__(self):
		self._browser.quit()
