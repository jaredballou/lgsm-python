import sys
import os
import yaml
#import pyaml
import json
import logging
import datetime
import __main__ as main
from pprint import pprint

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
	def __init__(self, core=None, game=None, game_instance=None):
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
		#print self.config
		#print game
		#print game_instance
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
		if ("settings" in gamedata.keys()):
			for setting in gamedata["settings"].keys():
				if "default" in gamedata["settings"][setting].keys():
					config[setting] = gamedata["settings"][setting]["default"]
				else:
					if not setting in config.keys():
						config[setting] = ""
		return config

	def create_file(self, game=None, game_instance=None, cfg_file=None, config=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		if cfg_file is None:
			cfg_file = "_default"
		if config is None:
			config = self.config
		cfg_path = os.path.join(self.core.interpolate(key="game_script_cfg_dir",data=self.config),"%s%s" % (cfg_file,".yaml"))
		if not os.path.isdir(os.path.dirname(cfg_path)):
			os.makedirs(os.path.dirname(cfg_path))

		if cfg_file == "_default":
			print "Creating %s" % cfg_path
			conf = self.merge_gamedata(config=self.config,gamedata=self.gamedata.gamedata)
			with open(cfg_path, 'w') as outfile:
				outfile.write( yaml.dump(self.config, indent=4, width=120, default_flow_style=False) )

