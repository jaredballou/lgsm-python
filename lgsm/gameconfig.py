import sys
import os
import yaml
#import pyaml
import json
import logging
import datetime
import __main__ as main

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#import inspect
#from pprint import pprint
try:
	from collections import OrderedDict
except ImportError:
	# try importing the backported replacement
	# requires a: `pip-2.6 install ordereddict`
	from ordereddict import OrderedDict

class GameConfig(object):
	def __init__(self, parent=None, game=None, game_instance=None):
		if not parent is None:
			self.__parent__ = parent
			self.config = parent.config
			self.gamedata = parent.gamedata
			self.game = parent.game
		if not game is None:
			self.game = game
		if game_instance is None:
			self.game_instance = self.game
		else:
			self.game_instance = game_instance
		self.gameconfig_load()

	def gameconfig_load(self,game=None,game_instance=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		print self.config
		print self.game
		print self.game_instance

	def gameconfig_merge_settings_to_config(self,game=None,gamedata=None,game_instance=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		if gamedata is None:
			gamedata = self.gamedata
		# this is me doing something stupid so I can interpolate the config
		if ("settings" in self.gamedata.keys()):
			for setting in self.gamedata["settings"].keys():
				if "default" in self.gamedata["settings"][setting].keys():
					self.config[setting] = self.gamedata["settings"][setting]["default"]
				else:
					self.config[setting] = ""

	def config_dump(self, format='yaml'):
		print "Dumping config as %s" % format
		if format == 'yaml':
			return yaml.dump(self.config, indent=4, width=120, default_flow_style=False)
		if format == 'json':
			return json.dumps(self.config, indent=4, sort_keys=True)
		return self.config_print()

	def config_print(self, path='', conf=None):
		if conf is None:
			conf = self.config
		for key in conf.keys():
			kt = type(conf[key])
			if kt in [str, int, list, set, tuple]:
				print "%s%s: %s" % (path, key, val) 
			val = self.getval(key=key,dict=conf)
			if kt in [OrderedDict, dict]:
				self.config_print(path="%s%s/" % (path, key), conf=conf[key])

	def getval(self, key, dict=None):
		val = ""
		if dict is None:
			dict = self.config['config']
		if not key in dict.keys():
			return
		kt = type(dict[key])
		if kt in [str, int]:
			val = dict[key]
		if kt in [list]:
			val = ', '.join(map(str, dict[key]))
		if kt in [set,tuple]:
			val = dict[key].join(", ")
		if kt in [OrderedDict, dict]:
			vals = OrderedDict()
			for skey in dict[key].keys():
				vals[key] = self.getval(key=skey,dict=dict[key])
			return vals
		try:
			while (val.find('%') != -1):
				val = (val) % dict
		except:
			return val
		return val

def dict_merge(dct, merge_dct):
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
			dict_merge(dct[k], merge_dct[k])
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

