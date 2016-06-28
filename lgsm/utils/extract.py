import __main__ as main
import tarfile
import zipfile

class Extract(object):
	def __init__(self, compressed_file, target_path):
		"""
		__init__(compressed_file, target_path)

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
