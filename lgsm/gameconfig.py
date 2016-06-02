import sys
import os
import yaml
#import pyaml
import json
import logging
import datetime

try:
	from collections import OrderedDict
except ImportError:
	# try importing the backported replacement
	# requires a: `pip-2.6 install ordereddict`
	from ordereddict import OrderedDict

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


class GameConfig:
	def __init__(self, game=os.path.basename(os.path.realpath(__file__)), gamedata_prefix = 'gamedata/', gamedata_suffix = '.yaml'):
		self.game = 'insserver'
		self.gamedata_prefix = gamedata_prefix
		self.gamedata_suffix = gamedata_suffix
		self.config = default_config
#		self.set_game(game)
#	for item in [self.game, self.gamedata_prefix, self.gamedata_suffix, self.config]:
#		logging.debug(item)
		self.load_data()
	
	def find_gamedata_file(self, file):
		test_paths = [
			file, 
			"%s%s" % (file, self.gamedata_suffix), 
			os.path.join("games", file), 
			os.path.join("games", "%s%s" % (file, self.gamedata_suffix)), 
			os.path.join("games", os.path.basename(file)),
			os.path.join("games", "%s%s" % (os.path.basename(file), self.gamedata_suffix)),
		]
		test_prefixes = [
			".",
			self.gamedata_prefix,
			os.path.join(default_config['config']['gamedatadir']),
			os.path.join(default_config['config']['lgsmdir'],self.gamedata_prefix),
			os.path.join(default_config['config']['lgsmdir']),
			os.path.join(default_config['config']['rootdir']),
		]
		for tprefix in test_prefixes:
			for tpath in test_paths:
				tf = os.path.join(tprefix, tpath)
				if os.path.isfile(tf):
					logging.debug("find_gamedata_file %s returned %s" % (file, tf))
					return tf

	def set_game(self, game):
		test_files = [
			game,
			os.path.basename(os.path.realpath(__file__)),
			default_config["config"]["servicename"],
		]
		for gamefile in test_files:
			if self.find_gamedata_file(gamefile) != "":
				self.game = gamefile
				return

	def load_data(self):
		# Load gamedata file for my game
		dict_merge(self.config, self.load_gamedata_file(self.game))
		# If there is a config.yaml file with user settings, load that over the defaults
		default_cfg_file = self.find_gamedata_file('config.yaml')
		if default_cfg_file is not None:
			logging.debug(default_cfg_file)
			dict_merge(self.config, self.load_gamedata_file(default_cfg_file))
		self.config = self.generate_config()

	def load_gamedata_file(self, file):
		bn = os.path.basename(file).split('.')[0]
		# Find the YAML file, bail if we cannot locate it
		yaml_file = self.find_gamedata_file(file)
		if yaml_file == "":
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
				impdata = self.load_gamedata_file(impfile)
				if len(impdata.keys()) > 0:
					logging.debug("merging %s" % impfile)
					logging.debug(impdata)
					logging.debug(data)
					dict_merge(impdata, data)
					dict_merge(data, impdata)
		return data

	def generate_config(self,data=None):
		if data is None:
			data = self.config
		if not "config" in data.keys():
			data["config"] = dict()
		# this is me doing something stupid so I can interpolate the config
		if ("settings" in data.keys()):
			for setting in data["settings"].keys():
				if "default" in data["settings"][setting].keys():
					data["config"][setting] = data["settings"][setting]["default"]
				else:
					data["config"][setting] = ""
		return data

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
			if kt in [str, int]:
				print "%s%s: %s" % (path, key, self.getval(key,conf))
			if kt in [list]:
				print "%s%s: [%s]" % (path, key, ', '.join(map(str, conf[key])))
			if kt in [set,tuple]:
				print "%s%s: [%s]" % (path, key, conf[key].join(", "))
			if kt in [OrderedDict, dict]:
				self.print_config("%s%s/" % (path, key), conf[key])

	def getval(self, key, dict=None):
		val = ""
		if dict is None:
			dict = self.config['config']
		if not key in dict.keys():
			return
		val = dict[key]
		try:
			while (val.find('%') != -1):
				val = (val) % dict
		except:
			return val
		return val

