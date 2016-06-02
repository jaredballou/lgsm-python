#!/usr/bin/env python

import datetime
import os

# Config data structures

class Gamedata(object):
	default_config = {
		"config": {
			"cachedir": "%(lgsmdir)s/tmp", 
			"core_script": "lgsm.py", 
			"date": datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"), 
			"gamedatadir": "%(lgsmdir)s/gamedata", 
			"git_update": False, 
			"githubbranch": "master", 
			"githubrepo": "lgsm-python", 
			"githubuser": "jaredballou", 
			"lgsmdir": "%(rootdir)s/lgsm", 
			"lgsmserverdir": "%(lgsmdir)s/servers/%(selfname)s", 
			"logdir": "%(lgsmdir)s/servers/%(selfname)s/log", 
			"parserdir": "%(lgsmserverdir)s/tmp", 
			"rootdir": os.path.dirname(os.path.realpath(__file__)), 
			"scriptcfgdir": "%(lgsmserverdir)s/cfg", 
			"scriptpath": os.path.realpath(__file__), 
			"selfname": os.path.basename(os.path.realpath(__file__)), 
			"servicename": os.path.basename(__file__), 
		}
	}
	def dict_merge(self,dct, merge_dct):
		""" Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
		updating only top-level keys, dict_merge recurses down into dicts nested
		to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
		``dct``.
		:param dct: dict onto which the merge is executed
		:param merge_dct: dct merged into dct
		:return: None
		"""
		for k, v in merge_dct.iteritems():
			if (k in dct and isinstance(dct[k], dict)
					and isinstance(merge_dct[k], dict)):
				self.dict_merge(dct[k], merge_dct[k])
			else:
				dct[k] = merge_dct[k]


class ConfigNode(object):
	def __init__(self,name,desc=None):
		self.name = name
		self.desc = desc

class ConfigValue(ConfigNode):
	def __init__(self,name,desc=None,value=None,default=None):
		ConfigNode.__init__(self,name,desc)
		self.default = default
		self.value = value

class Setting(ConfigValue):
	def __init__(self,name,desc=None,value=None,default=None,format=None,parm=None):
		ConfigValue.__init__(self,name,desc,value,default)
		self.format = format
		self.parm = parm
	
class ScriptAction(ConfigNode):
	def __init__(self,name,desc=None,command=None,aliases=None):
		ConfigNode.__init__(self,name,desc)
		self.command = command
		self.aliases = aliases
	
class Parm(ConfigValue):
	def __init__(self,name,desc=None,value=None,default=None):
		ConfigValue.__init__(self,name,desc,value,default)

class Dependency(ConfigNode):
	def __init__(self,name,desc=None,checksum=None):
		ConfigNode.__init__(self,name,desc)
		self.checksum = checksum
