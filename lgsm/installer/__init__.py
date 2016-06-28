import os
import sys
import __main__ as main
# as dict_merge
from pprint import pprint
from lgsm.gamedata import *
from lgsm.menu import *
from lgsm.utils import dict_merge

class Installer(object):
	def __init__(self, core, game=None):
		self.core = core
		if game is None:
			game = self.select_game()
			if not game:
				print "ERROR: No game selected!"
				return
		self.game = game
		self.installer_run()

	def select_game(self):
		games = OrderedDict()
		for game in sorted(os.listdir(os.path.join(self.core.interpolate("gamedata_dir"),"game"))):
			self.core.set_game(game=game,create_configs=False)
			gamename = self.core.interpolate(key="gamename")
			if gamename is None or gamename == '' or gamename in games.keys():
				gamename = game
			games[gamename] = game
		menu = Menu(menudata=games)
		result = menu.get_selection()
		return result

	def installer_run(self):
		self.core.set_game(game=self.game,create_configs=True)
		print self.core.interpolate(key="appid")

