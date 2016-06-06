import os

class SourceMod(object):
	def get_url(plugin):
		"""
		get_url(plugin)
	
		returns the download url for the specified plugin
		"""
		sm_version = subprocess.check_output(
			'curl -s http://www.sourcemod.net/smdrop/1.7/sourcemod-latest-linux',
			shell=True,
		)
	
		download_url = {
			'metamod': 'http://www.metamodsource.net/mmsdrop/1.10/mmsource-1.10.7-git948-linux.tar.gz',
			'sourcemod': "http://www.sourcemod.net/smdrop/1.7/%s" % sm_version,
		}
	
		return download_url[plugin]
	
	
	def download_plugins(game_path):
		"""
		download_plugins(game_path)
	
		wgets the plugins
		"""
		for plugin_name in ['metamod', 'sourcemod']:
			url = get_url(plugin=plugin_name)
			downloaded_plugin = "%s/%s" % (game_path, plugin_name)
	
			print "\nDownloading %s from %s\n" % (plugin_name, url)
			subprocess.call(
				"wget --quiet -O %s %s" % (downloaded_plugin, url), shell=True
			)
	
			# Extract the files
			extract_file(compressed_file=downloaded_plugin, target_path=game_path)
