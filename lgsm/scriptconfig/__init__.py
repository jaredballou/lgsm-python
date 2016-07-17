import sys
import os
import yaml
#import pyaml
import json
import logging
import datetime
import __main__ as main
from pprint import pprint
from lgsm.utils import *

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#import inspect
#from pprint import pprint
try:
	from collections import OrderedDict
except ImportError:
	# try importing the backported replacement
	# requires a: `pip-2.6 install ordereddict`
	from ordereddict import OrderedDict

class ScriptConfig(object):
	def __init__(self, core=None, game=None, game_instance=None, create_configs=True):
		self.create_configs = create_configs
		if not core is None:
			self.core = core
			self.config = core.config
			self.gamedata = core.gamedata
			self.game = core.game
		if not game is None:
			self.game = game
		if game_instance is None:
			self.game_instance = self.game
		else:
			self.game_instance = game_instance
		self.load()

	def load(self,game=None,game_instance=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance

		self.merge_gamedata(config=self.core.config,gamedata=self.core.gamedata.gamedata)

		if self.create_configs:
			self.create_file(game=game,game_instance=game_instance,cfg_file="_default")
			self.create_file(game=game,game_instance=game_instance,cfg_file="_common")
			self.create_file(game=game,game_instance=game_instance,cfg_file=game_instance)

	def merge_gamedata(self,game=None,gamedata=None,game_instance=None,config=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		if gamedata is None:
			gamedata = self.gamedata.gamedata
		if config is None:
			config = self.config
		try:
			if ("settings" in gamedata.keys()):
				for setting in gamedata["settings"].keys():
					if "default" in gamedata["settings"][setting].keys():
						config[setting] = gamedata["settings"][setting]["default"]
					else:
						if not setting in config.keys():
							config[setting] = ""
		except:
			pass
		return config

	def create_file(self, game=None, game_instance=None, cfg_file=None, config=None, cfg_path=None, force=False):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		if cfg_file is None:
			cfg_file = "_default"
		if config is None:
			config = self.config
		cfg_yaml = yaml.dump(self.config, indent=4, width=120, default_flow_style=False)
		# TODO: Make this append the commented default config?
		if cfg_file != "_default":
			cfg_yaml = "%s config. This will not be changed by the script, save all changes here" % cfg_file
		if cfg_path is None:
			cfg_path = os.path.join(self.core.interpolate(key="script_game_cfg_dir",data=self.config),"%s%s" % (cfg_file,".yaml"))
		try:
			if not os.path.isdir(os.path.dirname(cfg_path)):
				os.makedirs(os.path.dirname(cfg_path))
		except:
			pass
		if os.path.exists(cfg_path):
			# Only make changes to an existing default config file
			if cfg_file != "_default":
				return
			try:
				with open(cfg_path, 'r') as ymlfile:
					existing_cfg = yaml.load(ymlfile)
				if (equal_dicts(self.config,existing_cfg,["date_string"])):
					return
			except:
				print "error comparing configs! Bailing out!"
				return
		print "Creating %s" % cfg_path
		with open(cfg_path, 'w') as outfile:
			outfile.write(cfg_yaml)


#date_string
""" This is not yet wired up, but the idea is to represent all the gamedata and config file contents inside a data structure
"""
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

