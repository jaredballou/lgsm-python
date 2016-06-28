def dict_merge(target, source, overwrite=True):
	""" Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
	updating only top-level keys, dict_merge recurses down into dicts nested
	to an arbitrary depth, updating keys. The ``source`` is merged into
	``target``.
	:param target: dict onto which the merge is executed
	:param source: dict merged into target
	:param overwrite: overwrite values in target even if the keys exist
	:return: None
	"""
	for k, v in source.iteritems():
		if (k in target and isinstance(target[k], dict)
				and isinstance(source[k], dict)):
			dict_merge(target=target[k], source=source[k])
		else:
			if not k in target.keys() or overwrite:
				target[k] = source[k]
