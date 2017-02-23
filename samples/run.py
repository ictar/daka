#!/usr/bin/python
#-*- coding:utf-8 -*-
import Baidu
import Hujiang
import Mafengwo
import Zimuzu
#import SFexpress
import Xiami

if "__main__" == __name__:
	for mdl in [Hujiang, Mafengwo, Zimuzu, Baidu, Xiami ]:
		try:
			mdl.run()
		except Exception, e:
			print e
