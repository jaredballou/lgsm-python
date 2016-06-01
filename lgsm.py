#!/usr/bin/env python

from config import Config, ConfigMerger, ConfigList, Mapping
from pprint import pprint
import os

class Gamedata:
	def __init__(self, filename, cfg_path = 'gamedata', cfg_suffix = '.cfg'):
		self.config = Config()
		self.filename = filename
		self.cfg_path = cfg_path
		self.cfg_suffix = cfg_suffix
		self.get_default_settings()
		self.includes = self.get_includes(filename)
		self.cfg_list = self.get_config_list()
		self.load_data()

	def get_default_settings(self):
		merger = ConfigMerger()
		if not 'settings' in self.config.keys():
			self.config.addMapping('settings',{'rootdir': os.path.realpath(__file__)},None,False)
#			def = Config(file('def'))
#			merger.merge(self.config,def)

	def get_config_list(self):
		cfg_list = ConfigList()
		for include in self.includes:
			cfg_file = "%s/%s%s" % (self.cfg_path,include,self.cfg_suffix)
			cfg_list.append(Config(cfg_file))
		return cfg_list

	def dedupe(self,items):
		seen = set()
		for item in items:
			if item not in seen:
				yield item
				seen.add(item)

	def get_includes(self,filename,level=0):
		includes = [filename]
#		if level == 0:
#			includes += filename
		cfg_file = "%s/%s%s" % (self.cfg_path,filename,self.cfg_suffix)
#		print "Loading %s at level %d" % (cfg_file,level)
		cfg = Config(file(cfg_file))
		if 'include' in cfg.keys():
			includes += cfg.include
			for incfile in cfg.include:
				includes += self.get_includes(incfile,level+1)
		return list(self.dedupe(includes))
	def load_data(self):
		merger = ConfigMerger()
		for filename in reversed(self.includes):
			cfg_file = "%s/%s%s" % (self.cfg_path,filename,self.cfg_suffix)
			print "Loading %s" % cfg_file
			cfg = Config(file(cfg_file))
#			if 'settings' in cfg.keys() and not 'rootdir' in cfg.settings.keys():
#				if 'settings' in self.config.keys() and not 'rootdir' in self.config.settings.keys():
#					cfg.settings.rootdir = self.rootdir
			merger.merge(self.config,cfg)



gamedata = Gamedata('games/insserver/gamedata')
pprint(gamedata.includes)
pprint(gamedata.cfg_list.getByPath('settings'))
pprint(gamedata.config)
