#!/usr/bin/env python

import datetime
import os

# Config data structures

class Gamedata(object):
	default_config = {
		"config": {
			"cachedir": "%(lgsm_dir)s/tmp", 
			"lgsm_script": "lgsm.py", 
			"date": datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"), 
			"gamedata_dir": "%(lgsm_dir)s/gamedata", 
			"git_update": False, 
			"github_branch": "master", 
			"lgsm_repo": "lgsm-python", 
			"github_user": "jaredballou", 
			"lgsm_dir": "%(root_dir)s/lgsm", 
			"game_script_dir": "%(lgsm_dir)s/servers/%(game_script_name)s", 
			"log_dir": "%(lgsm_dir)s/servers/%(game_script_name)s/log", 
			"parserdir": "%(game_script_dir)s/tmp", 
			"root_dir": os.path.dirname(os.path.realpath(__file__)), 
			"game_script_cfg_dir": "%(game_script_dir)s/cfg", 
			"game_script_path": os.path.realpath(__file__), 
			"game_script_name": os.path.basename(os.path.realpath(__file__)), 
			"instance_name": os.path.basename(__file__), 
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
