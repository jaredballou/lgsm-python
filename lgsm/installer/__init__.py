import os
import sys
import __main__ as main
from lgsm.utils import dict_merge
# as dict_merge
from pprint import pprint

from simplemenus import IdentifierMenu
import menu

class Installer(object):
	def __init__(self, core, game=None):
		self.core = core
		if game is None:
			if not self.select_game():
				print "ERROR: FAILURE"
				return
		else:
			self.game = game
		self.installer_run()

	def select_game(self):
		games = os.listdir(os.path.join(self.core.interpolate("gamedata_dir"),"game"))
		if not games is None:
			#menu = IdentifierMenu(options=games)
			#menu.get_response()
			mainMenu = menu.Menu("Select Game",update=updateFunction)
			mainMenu.submenu = menu.Menu("Submenu",update=updateFunction)
			options = [{"name":"firstOption","function":firstFunc},
				{"name":"secondOption","function":secondFunc},
				{"name":"thirdOption","function":thirdFunc}]
			mainMenu.addOptions(options)
			mainMenu.open()
		return False

	def installer_run(self):
		print "Installer"
		print self.game
def updateFunction(data):
	print "update"
#	pprint(data)
#	return True
def firstFunc():
	print "firstFunc"
def secondFunc():
	print "secondFunc"
def thirdFunc():
	print "thirdFunc"
