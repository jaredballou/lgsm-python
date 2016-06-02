import __main__ as main
from .gamedata import *
from pprint import pprint

default_config = {
	"config": {
		"cachedir": "%(lgsmdir)s/tmp",
		"core_script": "lgsm",
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
		"rootdir": os.path.realpath(os.path.dirname(main.__file__)),
		"scriptcfgdir": "%(lgsmserverdir)s/cfg",
		"scriptpath": os.path.realpath(main.__file__),
		"selfname": os.path.basename(os.path.realpath(main.__file__)),
		"servicename": os.path.basename(main.__file__),
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
		if game == default_config['config']['core_script']:
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
