import __main__ as main
import datetime
import argparse

#try:
#	from collections import OrderedDict
#except ImportError:
#	from ordereddict import OrderedDict


from config import *
from download import *
from extract import *
from gamedata import *
from github import *
from installer import *
from scriptconfig import *

#import importlib
#mod_gamedata = importlib.import_module(".gamedata", __package__)

#from pprint import pprint

class LGSMCore(object):
	lgsm_script = "lgsm"
	game = os.path.basename(main.__file__)
	game_script = os.path.basename(os.path.realpath(main.__file__))
	instance = os.path.basename(main.__file__)

	date_format = "%Y-%m-%d-%H-%M-%S"
	date_string = datetime.datetime.today().strftime(date_format)
	root_dir = os.path.realpath(os.path.dirname(main.__file__))
	lgsm_dir = os.path.join(root_dir,"lgsm")

	config_file = os.path.join((lgsm_dir if os.path.exists(lgsm_dir) else root_dir),'config.yaml')

	arch = sys.platform


	# Core config fields that cannot be modified. These will be omitted from all
	# config files, but will still be merged into the processed config data.
	immutable_config = ["lgsm_script","date","os"]

	# Default core configuration.

	config = {
		"lgsm_script": "lgsm",
		"date_format": date_format,
		"date_string": date_string,

		"root_dir": os.path.realpath(os.path.dirname(main.__file__)),

		"platform": "steam",
		"lgsm_dir": "%(root_dir)s/lgsm",
		"lgsm_branch": "%(github_branch)s",
		"lgsm_repo": "lgsm-python",
		"lgsm_user": "%(github_user)s",

		"github_update": True,
		"github_user": "jaredballou",
		"github_branch": "master",

		"gamedata_dir": "%(lgsm_dir)s/gamedata",
		"gamedata_repo": "lgsm-gamedata",
		"gamedata_user": "%(github_user)s",
		"gamedata_branch": "%(github_branch)s",

		"game_script_path": os.path.realpath(main.__file__),
		"game_script_name": os.path.basename(os.path.realpath(main.__file__)),
		"game_script_cfg_dir": "%(lgsm_dir)s/config/%(game_script_name)s",
		"instance_name": os.path.basename(main.__file__),
		"instance_cfg": "%(game_script_cfg_dir)s/%(instance_name)s",
	}

	parser = argparse.ArgumentParser(description='Install, update, and manage game servers.')

	def __init__(self, game=None, config_file = None):
		if not game is None:
			self.game = game
		if not config_file is None:
			self.config_file = config_file
		self.parse_arguments()
		self.load_config()
		self.set_game(game)

	def load_config(self):
		if os.path.isfile(self.config_file):
			with open(self.config_file, 'r') as ymlfile:
				script_config = yaml.load(ymlfile)
			self.dict_merge(target=self.config, source=script_config)

	def set_game(self, game=None, game_instance=None):
		if game_instance is None:
			game_instance = self.config["instance_name"]
		if game is None:
			game = self.config["game_script_name"]
		if game == self.config['lgsm_script']:
			self.installer = Installer(game=self.game, core=self, game_instance=self.game_instance, config=self.config)
			return
		else:
			self.game = game
			self.game_instance = game_instance
			self.gamedata = GameData(core=self, game=game)
		        self.scriptconfig = ScriptConfig(core=self, game=game, game_instance=game_instance)

	def interpolate(self, key=None, data=None, interpolate_data=None):
		val = ""
		if data is None:
			data = self.config
		if interpolate_data is None:
			interpolate_data = self.config

		if key is None:
			item = data
		else:
			if not key in data.keys():
				return
			item = data[key]

		kt = type(item)
		if kt in [str, int]:
			val = item
		if kt in [list]:
			val = ', '.join(map(str, item))
		if kt in [set,tuple]:
			val = item.join(", ")
		if kt in [OrderedDict, dict]:
			vals = dict()
			for skey in item.keys():
				vals[skey] = self.interpolate(key=skey,data=item,interpolate_data=interpolate_data)
			return vals
 		try:
			while (val.find('%') != -1):
				val = (val) % interpolate_data
		except:
			return val
		return val

	def dict_merge(self, target, source, overwrite=True):
		""" Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
		updating only top-level keys, dict_merge recurses down into dicts nested
		to an arbitrary depth, updating keys. The ``source`` is merged into
		``target``.
		:param target: dict onto which the merge is executed
		:param source: dict merged into target
		:param overwrite: overwrite values in target even if the keys exist
		:return: None
		"""
		for k, v in source.iteritems():
			if (k in target and isinstance(target[k], dict)
					and isinstance(source[k], dict)):
				self.dict_merge(target=target[k], source=source[k])
			else:
				if not k in target.keys() or overwrite:
					target[k] = source[k]

	def merge_gamedata_to_config(self,config=None,gamedata=None,overwrite=True):
		if config is None:
			config = self.config
		if gamedata is None:
			gamedata = self.gamedata.gamedata
		if not "settings" in gamedata.keys():
			return
		for setting in gamedata["settings"].keys():
			if setting in config.keys() and overwrite != True:
				continue
			if "default" in gamedata["settings"][setting].keys():
				config[setting] = gamedata["settings"][setting]["default"]
			else:
				config[setting] = ""

	def dump(self, data, format='yaml'):
		print "Dumping config as %s" % format
		if format == 'yaml':
			return yaml.dump(data, indent=4, width=120, default_flow_style=False)
		if format == 'json':
			return json.dumps(data, indent=4, sort_keys=True)
		return self.print_tree(data=data)

	def print_tree(self, path='', data=None, interpolated=False):
		if data is None:
			data = self.config
		if interpolated != True:
			data = self.interpolate(data=data)
			interpolated = True
		for key in data.keys():
			kt = type(data[key])
			if kt in [str, int, list, set, tuple]:
				print "%s%s: %s" % (path, key, data[key]) 
			if kt in [OrderedDict, dict]:
				self.print_tree(path="%s%s/" % (path, key), data=data[key], interpolated=interpolated)

	def parse_arguments(self):
		"""
		parse_arguments(self)
	
		Parses the arguments passed to the script and calls appropriate functions
		"""
		self.parser.add_argument("--config", action='store', type=str, metavar="path/to/config.yaml", default=self.config_file, help='Config file to load for LGSM script')
		self.parser.add_argument("--game", action='store', type=str, default="insserver", help='Game to use')
		self.parser.add_argument("--root_dir", action='store', type=str, metavar=".", default=os.path.realpath(os.path.dirname(main.__file__)), help='Root directory for LGSM')
		self.parser.add_argument("--platform", action='store', type=str, default="steam", help='Platform to use for deploying game')
		self.parser.add_argument("--instance", action='store', type=str, default=os.path.basename(main.__file__), help='Instance name')
		self.parser.add_argument("--lgsm_dir", action='store', type=str, metavar="./lgsm", default="%(root_dir)s/lgsm", help='Directory where all LGSM files will be placed')

		self.parser.add_argument("-v", "--verbose", help="Debugging Mode", action='store_true')
		self.parser.add_argument("-d", "--debug", help="Debugging Mode", action='store_true')
		self.parser.add_argument("-i", "--interactive", help="Interactive Mode", action='store_true')


		self.parser.add_argument("--gamedata_dir", action='store', type=str, metavar="./lgsm/gamedata", default="%(lgsm_dir)s/gamedata", help='Path to install game data files')
		"""
		self.parser.add_argument("--gamedata_repo", action='store', type=str, default="lgsm-gamedata", help='GitHub repo for game data')
		self.parser.add_argument("--gamedata_user", action='store', type=str, default="%(github_user)s", help='GitHub user for game data')
		self.parser.add_argument("--gamedata_branch", action='store', type=str, default="%(github_branch)s", help='GitHub branch for game data')

		self.parser.add_argument("--github_update", action='store_true', default=True, help='Update gamedata and modules from GitHub')
		self.parser.add_argument("--github_user", action='store', type=str, default="jaredballou", help='Default GitHub user')
		self.parser.add_argument("--github_branch", action='store', type=str, default="master", help='Default GitHub branch')
		self.parser.add_argument("--lgsm_branch", action='store', type=str, default="%(github_branch)s", help='GitHub LGSM branch')
		self.parser.add_argument("--lgsm_repo", action='store', type=str, default="lgsm-python", help='GitHub LGSM repo')
		self.parser.add_argument("--lgsm_user", action='store', type=str, default="%(github_user)s", help='GitHub LGSM user')
		self.parser.add_argument("--game_script_name", action='store', type=str, default=os.path.basename(os.path.realpath(main.__file__)), help='Game script name')
		self.parser.add_argument("--game_script_cfg_dir", action='store', type=str, default="%(lgsm_dir)s/config/%(game_script_name)s", help='LGSM config path for this game')
		"""
		# required=True,
		#choices=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#action='store_true',
	
		self.args = self.parser.parse_args()
		#pprint(self.args)

#		print args.accumulate(args.integers)
"""	
		install_steamcmd(steamcmd_path=args.path)
	
		install_dedicated_server(
			steam_path=args.path,
			game=args.game,
			sourcemod=args.sourcemod
		)
"""
