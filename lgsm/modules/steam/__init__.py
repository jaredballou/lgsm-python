import urllib2
import os
from lgsmcore.download import *
import tarfile
import zipfile
import subprocess

class Steam(object):
	steamcmd_path = "/home/jballou/games/steamcmd"
	steam_path = "/home/jballou/games/serverfiles"
	steamcmd_url="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
	steamcmd_cmd="steamcmd.sh"
	appid=None
	steamcmd_options = {
		"+login": "anonymous",
	}

	def __init__(self, steamcmd_path=None, steamcmd_url=None, parent=None, steam_path=None, appid=None, steamcmd_options=None):
		"""
		steamcmd_install(steamcmd_path=None)
	
		Grabs the correct build of steamcmd for the platform and unzips it
		"""
		if not parent is None:
			self.__parent__ = parent
		if not steamcmd_path is None:
			self.steamcmd_path = steamcmd_path
		if not steamcmd_url is None:
			self.steamcmd_url = steamcmd_url
		if not steam_path is None:
			self.steam_path = steam_path
		if not appid is None:
			self.appid = appid
		if not steamcmd_options is None:
			for key in steamcmd_options.keys():
				self.steamcmd_options[key] = steamcmd_options[key]
		self.update_variables()
		self.steamcmd_install()
		if (self.appid is not None):
			self.app_install(appid=self.appid)

	def update_variables(self):
		self.steamcmd_executable = os.path.join(self.steamcmd_path,self.steamcmd_cmd)
		self.steamcmd_options["+force_install_dir"] = self.steam_path

	def extract_file(self,compressed_file, target_path):
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

	def steamcmd_install(self):
		if os.path.exists("%s/steamcmd.sh" % self.steamcmd_path):
			return
	
		if not os.path.exists(self.steamcmd_path):
			print "%s does not exist, creating path before downloading steamcmd\n"\
				% self.steamcmd_path
			os.makedirs(self.steamcmd_path)
	
		steamcmd_tar = "%s/steamcmd.tar.gz" % self.steamcmd_path
	
		print "Grabbing steamcmd from %s. Saving to %s\n" % (steamcmd_url,steamcmd_tar)
		dl_file = Download(steamcmd_url,steamcmd_tar)

		self.extract_file(compressed_file=steamcmd_tar, target_path=self.steamcmd_path)

	def steamcmd_command(self,command=None):
		options = ''.join(['%s "%s" ' % (key, value) for (key, value) in self.steamcmd_options.items()])
		command = "%s %s%s +quit" % (self.steamcmd_executable, options, command)
		subprocess.call(command,shell=True)

	def app_update(self, appid=None):
		self.steamcmd_command("+app_update %s" % (appid))

	def app_install(self, appid=None):
		"""
		app_install(appid=None)
	
		Executes the steamcmd script and begins downloading a dedicated server
		"""
		self.app_update(appid=appid)

