import sys
import os
import yaml
#import pyaml
import json
import logging
import datetime
import __main__ as main

from .github import *
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#import inspect

try:
	from collections import OrderedDict
except ImportError:
	# try importing the backported replacement
	# requires a: `pip-2.6 install ordereddict`
	from ordereddict import OrderedDict

class GameData(object):
	def __init__(self, core = None, file_prefix = 'gamedata/', file_suffix = '.yaml', game = None):
		if not core is None:
			self.core = core
		self.file_prefix = file_prefix
		self.file_suffix = file_suffix
		self.config = core.config
		if not game is None:
			self.game = game
		else:
			self.game = core.game
		self.load()
	
	def check(self):
		self.gamedata_dir = self.core.interpolate(key="gamedata_dir")
		pp = os.path.dirname(self.gamedata_dir)
		if not os.path.isdir(pp):
			os.makedirs(pp)
		#self.repo = 
		GitHub().clone(url="https://github.com/jaredballou/lgsm-gamedata.git", path=self.gamedata_dir)

	def load(self):
		self.check()
		# Load gamedata file for my game
		self.gamedata = self.load_file(file=self.game)

	def find_file(self, file,type='game'):
		conf = self.config
		test_files = [
			"%s%s" % (file, self.file_suffix),
			os.path.join(file,"%s%s" % (os.path.basename(file), self.file_suffix)),
		]
		test_paths = [
			'',
			type,
			"game",
			"engine",
			"platform"
		]
		test_prefixes = [
			'',
			self.core.interpolate(key='gamedata_dir',data=conf),
			self.core.interpolate(key='lgsm_dir',data=conf),
			self.core.interpolate(key='root_dir',data=conf),
			os.path.join(self.core.interpolate(key='root_dir',data=conf),self.file_prefix),
		]
		for tprefix in test_prefixes:
			for tpath in test_paths:
				for tfile in test_files:
					tf = os.path.join(tprefix, tpath, tfile)
					if os.path.isfile(tf):
						logging.debug("find_file %s returned %s" % (file, tf))
						return tf

	def load_file(self, file):
		bn = os.path.basename(file).split('.')[0]
		# Find the YAML file, bail if we cannot locate it
		yaml_file = self.find_file(file)
		if yaml_file == None or yaml_file == '':
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
		logging.debug("starting dict_merge(target=data, source=conf)")
		self.core.dict_merge(data, conf)
		# Handle importing files
		if "import" in data.keys():
			for impfile in data["import"]:
				impdata = self.load_file(impfile)
				if len(impdata.keys()) > 0:
					logging.debug("merging %s" % impfile)
					self.core.dict_merge(target=impdata, source=data)
					self.core.dict_merge(target=data, source=impdata)
		return data

