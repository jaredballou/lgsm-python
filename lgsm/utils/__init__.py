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

def equal_dicts(d1, d2, ignore_keys):
	ignored = set(ignore_keys)
	for k1, v1 in d1.iteritems():
		if k1 not in ignored and (k1 not in d2 or d2[k1] != v1):
			return False
	for k2, v2 in d2.iteritems():
		if k2 not in ignored and k2 not in d1:
			return False
	return True
