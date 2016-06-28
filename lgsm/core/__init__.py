import __main__ as main
import datetime
import argparse

from lgsm.core import *
from lgsm.engine import *
from lgsm.gamedata import *
from lgsm.installer import *
from lgsm.platform import *
from lgsm.scriptconfig import *
from lgsm.utils import *

from lgsm.utils.version import get_version

from lgsm.default_config import get_default_config

class LGSM(object):
	config = get_default_config()
	def __init__(self, game=None, config_file = None, argv=None):
		for cp in ["root_dir", "lgsm_dir"]:
			cf = os.path.join(self.interpolate(key=cp),'config.yaml')
			if os.path.exists(cf):
				break
		self.config_file = cf
		self.parser = argparse.ArgumentParser(description='Install, update, and manage game servers.')
		self.argv = argv or sys.argv[:]
		self.prog_name = os.path.basename(self.argv[0])
		if not game is None:
			self.game = game
		if not config_file is None:
			self.config_file = config_file
		self.parse_arguments()
		self.load_config()
		if self.interpolate(key="script_game") == "lgsm-core" or __name__ == "__main__":
			self.installer = Installer(core=self, game=game)
		else:
			self.set_game(game)

	def execute_from_command_line(self):
		pass

	def load_config(self):
		if os.path.isfile(self.config_file):
			with open(self.config_file, 'r') as ymlfile:
				script_config = yaml.load(ymlfile)
			dict_merge(target=self.config, source=script_config)

	def set_game(self, game=None, game_instance=None):
		if game_instance is None:
			game_instance = self.interpolate(key="game_instance")
		if game is None:
			game = self.interpolate(key="game_script_name")
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
		"""parse_arguments(self)

		Parses the arguments passed to the script and calls appropriate functions
		"""

		#self.parser.add_argument("--%s" % var, action='store', type=str, default=self.interpolate(key=var), help=help)
		self.parser.add_argument("--config", action='store', type=str, metavar="path/to/config.yaml", default=self.config_file, help='Config file to load for LGSM script')
		self.parser.add_argument("--game", action='store', type=str, default="insserver", help='Game to use')
		self.parser.add_argument("--root_dir", action='store', type=str, metavar=".", default=self.interpolate(key="root_dir"), help='Root directory for LGSM')
		self.parser.add_argument("--platform", action='store', type=str, default="steam", help='Platform to use for deploying game')
		self.parser.add_argument("--game_instance", action='store', type=str, default=self.interpolate(key="game_instance"), help='Instance name')
		self.parser.add_argument("--lgsm_dir", action='store', type=str, metavar="~/.lgsm", default="%(root_dir)s/lgsm", help='Directory where all LGSM files will be placed')

		self.parser.add_argument("-v", "--verbose", help="Debugging Mode", action='store_true')
		self.parser.add_argument("-d", "--debug", help="Debugging Mode", action='store_true')
		self.parser.add_argument("-i", "--interactive", help="Interactive Mode", action='store_true')

		self.parser.add_argument("--gamedata_dir", action='store', type=str, metavar="./lgsm/gamedata", default="%(lgsm_dir)s/gamedata", help='Path to install game data files')

		"""self.parser.add_argument("--gamedata_repo", action='store', type=str, default="lgsm-gamedata", help='GitHub repo for game data')
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
"""		install_steamcmd(steamcmd_path=args.path)
		install_dedicated_server(
			steam_path=args.path,
			game=args.game,
			sourcemod=args.sourcemod
		)
"""

def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    core = LGSM(argv=argv)
    core.execute()
