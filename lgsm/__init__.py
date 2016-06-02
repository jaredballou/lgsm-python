import __main__ as main
from .gamedata import *
from pprint import pprint

default_config = {
	"config": {
		"lgsm_script": "lgsm",
		"date": datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"),
		"gamedata_dir": "%(lgsm_dir)s/gamedata",
		"gamedata_repo": "lgsm-gamedata",
		"gamedata_user": "%(github_user)s",
		"gamedata_branch": "%(github_branch)s",
		"github_update": True,
		"github_user": "jaredballou",
		"github_branch": "master",
		"lgsm_branch": "%(github_branch)s",
		"lgsm_repo": "lgsm-python",
		"lgsm_user": "%(github_user)s",
		"lgsm_dir": "%(root_dir)s/lgsm",
		"root_dir": os.path.realpath(os.path.dirname(main.__file__)),
		"game_script_cfg_dir": "%(game_script_dir)s/cfg",
		"game_script_path": os.path.realpath(main.__file__),
		"game_script_name": os.path.basename(os.path.realpath(main.__file__)),
		"game_script_dir": "%(lgsm_dir)s/games/%(game_script_name)s",
		"log_dir": "%(game_script_dir)s/log",
		"instance_name": os.path.basename(main.__file__),
	}
}

class LGSM(object):
	def __init__(self, game=os.path.basename(main.__file__)):
		self.config = default_config
		script_config_file = os.path.realpath(os.path.join(os.path.dirname(main.__file__),'config.yaml'))
		if os.path.isfile(script_config_file):
			with open(script_config_file, 'r') as ymlfile:
				script_config = yaml.load(ymlfile)
			dict_merge(self.config, script_config)
		pprint(self.config)
		self.set_game(game)

	def interpolate_config(self,data=None):
		if data is None:
			data = self.config["config"]
		for key in data.keys():
			data[key] = self.getval(key=key, dict=data)
		return data

	def installer_run(self):
		print "Installer"

	# TODO: Create _default _common and instance config YAML files
	#def gameserver_create_config(self,name,data):

	def set_game(self, game):
		if game == default_config['config']['lgsm_script']:
			self.installer_run()
		elif game == 'insserver':
			self.game = game
			self.gamedata = GameData(self)
		return

"""
		if script_config_file is not None:
			logging.debug(script_config_file)
		self.gamedata_merge_settings_to_config()
"""
