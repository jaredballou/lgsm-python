import __main__ as main
import datetime
import tarfile
import zipfile

from .gamedata import *
from .download import *
from .gameconfig import *
from .sourcemod import *
from .steam import *



#import importlib
#mod_gamedata = importlib.import_module(".gamedata", __package__)

#from pprint import pprint

default_config = {
	"lgsm_script": "lgsm",
	"date": datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"),
	"root_dir": os.path.realpath(os.path.dirname(main.__file__)),
	"platform": sys.platform,
	"game_script_path": os.path.realpath(main.__file__),
	"instance_name": os.path.basename(main.__file__),
	"lgsm_dir": "%(root_dir)s/lgsm",
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
	"game_script_name": os.path.basename(os.path.realpath(main.__file__)),
	"game_script_dir": "%(lgsm_dir)s/games/%(game_script_name)s",
	"game_script_cfg_dir": "%(game_script_dir)s/cfg",
}


config_dirs = [
	"root_dir",
	"lgsm_dir",
	"gamedata_dir",
	"game_script_dir",
	"game_script_cfg_dir",
]

class LGSM(object):
	def __init__(self, game=os.path.basename(main.__file__)):
		self.config = default_config
		self.platform = sys.platform
		script_config_file = os.path.realpath(os.path.join(os.path.dirname(main.__file__),'config.yaml'))
		if os.path.isfile(script_config_file):
			with open(script_config_file, 'r') as ymlfile:
				script_config = yaml.load(ymlfile)
			dict_merge(self.config, script_config)
		self.set_game(game)

	def clone_from_github(self,url):
		try:
			git.Repo.clone_from(gitlab_ssh_URL, local_path)
		except git.GitCommandError as exception:
			print(exception)
			if exception.stdout:
				print('!! stdout was:')
				print(exception.stdout)
			if exception.stderr:
				print('!! stderr was:')
				print(exception.stderr)

	def interpolate_config(self,data=None):
		if data is None:
			data = self.config
		for key in data.keys():
			data[key] = self.getval(key=key, dict=data)
		return data

	def installer_run(self):
		print "Installer"

	# TODO: Create _default _common and instance config YAML files
	#def gameserver_create_config(self,name,data):

	def extract_file(compressed_file, target_path):
		"""
		extract_file(compressed_file, target_path)
	
		extracts the compressed_file to target_path
		"""
	
		if os.path.exists(compressed_file):
			print "Extracting %s to %s\n" % (compressed_file, target_path)
	
			if zipfile.is_zipfile(compressed_file):
				with zipfile.ZipFile(compressed_file, "r") as z:
						z.extractall(path=target_path)
	
			if tarfile.is_tarfile(compressed_file):
				tar = tarfile.open(compressed_file)
				tar.extractall(path=target_path)
				tar.close()
	
			print "Cleaning up\n"
			os.remove(compressed_file)
	
			print "Done!\n"
		else:
			print "%s does not exist, cannot extract" % compressed_file

	def set_game(self, game=None, game_instance=None):
		if game_instance is None:
			game_instance = self.config["instance_name"]
		if game == default_config['lgsm_script']:
			self.installer_run()
			return
		elif game == 'insserver':
			self.game = game
			self.gamedata = GameData(parent=self, game=game)
		        self.gameconfig = GameConfig(parent=self, game=game, game_instance=game_instance)
