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
from pprint import pprint
try:
	from collections import OrderedDict
except ImportError:
	# try importing the backported replacement
	# requires a: `pip-2.6 install ordereddict`
	from ordereddict import OrderedDict

class GameData(object):
	def __init__(self, parent, gamedata_prefix = 'gamedata/', gamedata_suffix = '.yaml'):
		self.__parent__ = parent
		self.gamedata_prefix = gamedata_prefix
		self.gamedata_suffix = gamedata_suffix
		self.config = parent.config
		self.gamedata_load()
	
	def gamedata_find_file(self, file):
		conf = self.__parent__.config['config']
		test_paths = [
			"%s%s" % (file, self.gamedata_suffix),
			"%s/gamedata%s" % (file, self.gamedata_suffix),
			os.path.join("games", "%s%s" % (file, self.gamedata_suffix)),
			os.path.join("games", "%s/gamedata%s" % (file, self.gamedata_suffix)),
			os.path.join("games", "%s%s" % (os.path.basename(file), self.gamedata_suffix)),
			os.path.join("games", "%s/gamedata%s" % (os.path.basename(file), self.gamedata_suffix)),
			file,
			os.path.join("games", file),
			os.path.join("games", os.path.basename(file)),
		]
		test_prefixes = [
			self.gamedata_prefix,
			self.getval(key='gamedata_dir',dict=conf),
			self.getval(key='lgsm_dir',dict=conf),
			self.getval(key='root_dir',dict=conf),
			os.path.join(self.getval(key='root_dir',dict=conf),self.gamedata_prefix),
		]
		for tprefix in test_prefixes:
			for tpath in test_paths:
				tf = os.path.join(tprefix, tpath)
				#pprint("searching for %s" % tf)
				if os.path.isfile(tf):
					logging.debug("gamedata_find_file %s returned %s" % (file, tf))
					return tf

	def gamedata_load(self):
		# Load gamedata file for my game
		#pprint(self.__parent__.game)
		dict_merge(self.config, self.gamedata_load_file(self.__parent__.game))
		# If there is a config.yaml file with user settings, load that over the defaults
		default_cfg_file = self.gamedata_find_file('config.yaml')
		if default_cfg_file is not None:
			logging.debug(default_cfg_file)
			dict_merge(self.config, self.gamedata_load_file(default_cfg_file))
		self.gamedata_merge_settings_to_config()


	def gamedata_load_file(self, file):
		bn = os.path.basename(file).split('.')[0]
		# Find the YAML file, bail if we cannot locate it
		yaml_file = self.gamedata_find_file(file)
		if yaml_file == None:
			return
		logging.debug("yaml_file %s is %s" % (file, yaml_file))
		with open(yaml_file, 'r') as ymlfile:
			conf = yaml.load(ymlfile)
		# Create an empty OrderedDict
		data = OrderedDict()
		# If the only key is eponymous, use that as the new root
		if len(conf.keys()) == 1 and conf.keys()[0] == bn:
			conf = conf[conf.keys()[0]]
		# Merge new data into our OrderedDict
		logging.debug("starting dict_merge(data, conf)")
		dict_merge(data, conf)
		# Handle importing files
		if "import" in data.keys():
			for impfile in data["import"]:
				impdata = self.gamedata_load_file(impfile)
				if len(impdata.keys()) > 0:
					logging.debug("merging %s" % impfile)
					logging.debug(impdata)
					logging.debug(data)
					dict_merge(impdata, data)
					dict_merge(data, impdata)
		return data

	def gamedata_merge_settings_to_config(self):
		if not "config" in self.config.keys():
			self.config["config"] = dict()
		# this is me doing something stupid so I can interpolate the config
		if ("settings" in self.config.keys()):
			for setting in self.config["settings"].keys():
				if "default" in self.config["settings"][setting].keys():
					self.config["config"][setting] = self.config["settings"][setting]["default"]
				else:
					self.config["config"][setting] = ""

	def dump_config(self, format='yaml'):
		print "Dumping config as %s" % format
		if format == 'yaml':
			return yaml.dump(self.config, indent=4, width=120, default_flow_style=False)
		if format == 'json':
			return json.dumps(self.config, indent=4, sort_keys=True)
		return self.print_config()

	def print_config(self, path='', conf=None):
		if conf is None:
			conf = self.config
		for key in conf.keys():
			kt = type(conf[key])
			if kt in [str, int, list, set, tuple]:
				print "%s%s: %s" % (path, key, val) 
			val = self.getval(key=key,dict=conf)
			if kt in [OrderedDict, dict]:
				self.print_config(path="%s%s/" % (path, key), conf=conf[key])

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

