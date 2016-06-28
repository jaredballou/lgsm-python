import __main__ as main
import datetime
import sys
import os

from utils.version import get_version

VERSION = (0, 0, 1, 'alpha', 0)

__version__ = get_version(VERSION)

def get_default_config():
	root_dir = os.path.expanduser("~")

	script_instance_path = os.path.join(root_dir,"lgsm-core")
	script_game_path = os.path.realpath(script_instance_path)

	try:
		if __name__ != "__main__":
			script_instance_path = main.__file__
	except:
		pass

	#root_dir = os.path.dirname(script_game_path)

	date_format = "%Y-%m-%d-%H-%M-%S"
	date_string = datetime.datetime.today().strftime(date_format)
	arch = sys.platform

	config = {
		"lgsm_script": "lgsm-core",

		"date_format": date_format,
		"date_string": date_string,

		"root_dir": root_dir,
		"platform": "steam",
		"lgsm_dir": "%(root_dir)s/.lgsm",
		"lgsm_branch": "%(github_branch)s",
		"lgsm_repo": "lgsm-python",
		"lgsm_user": "%(github_user)s",

		"github_update": True,
		"github_user": "jaredballou",
		"github_branch": "master",

		"script_cfg": "%(lgsm_dir)s/config",

		"gamedata_dir": "%(lgsm_dir)s/gamedata",
		"gamedata_repo": "lgsm-gamedata",
		"gamedata_user": "%(github_user)s",
		"gamedata_branch": "%(github_branch)s",

		"script_game": os.path.basename(script_game_path),
		"script_game_path": script_game_path,
		"script_game_cfg_dir": "%(lgsm_dir)s/config/%(script_game)s",

		"script_instance": os.path.basename(script_instance_path),
		"script_instance_path": script_instance_path,
		"script_instance_cfg": "%(script_game_cfg_dir)s/%(script_instance)s",
	}
	return config
