import __main__ as main

class Installer(object):
	def __init__(self, game=None, core=None, game_instance=None, config=None):
		if self.game_instance is None:
			print "instance none"
		if not game is None:
			self.game = game
		if not game_instance is None:
			self.game_instance = game_instance
		else :
			self.game_instance = core.game_instance
		if not core is None:
			self.core = core
		self.config = core.config
		if not config is None:
			dict_merge(self.config,config)
		self.installer_run(game=game,game_instance=game_instance)

	def installer_run(self, game=None, game_instance=None):
		if game is None:
			game = self.game
		if game_instance is None:
			game_instance = self.game_instance
		print "Installer"
		print self.game
		print self.game_instance
