import __main__ as main
import datetime
import git

class GitHub(object):
	def __init__(self, url=None, repo=None, user=None, branch=None, file=None, dest=None):
		pass

	def clone(self, url=None, path=None):
		try:
			git.Repo.clone_from(url, path)
		except git.GitCommandError as exception:
			print(exception)
			if exception.stdout:
				print('!! stdout was:')
				print(exception.stdout)
			if exception.stderr:
				print('!! stderr was:')
				print(exception.stderr)
