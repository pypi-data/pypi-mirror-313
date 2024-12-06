
def factory(func):
	"""
		Factory decorator. Executes the decorated
		method/function and returns 'self' at the end.
	"""
	def inner(self, *args, **kw):
		func(self, *args, **kw)
		return self
	return inner
