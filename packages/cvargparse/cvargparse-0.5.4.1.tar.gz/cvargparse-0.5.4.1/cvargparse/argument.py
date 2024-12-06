import argparse

class Argument(object):
	def __init__(self, *args, **kw):
		super(Argument, self).__init__()
		self.args = args # positional arugments
		self.kw = kw # keyword arguments

	@classmethod
	def int(cls, *args, **kw):
		arg_type = kw.pop("type", int)
		return cls(*args, type=arg_type, **kw)

	@classmethod
	def float(cls, *args, **kw):
		arg_type = kw.pop("type", float)
		return cls(*args, type=arg_type, **kw)

	@classmethod
	def flag(cls, *args, **kw):
		action = kw.pop("action", "store_true")
		return cls(*args, action=action, **kw)

class FileArgument(Argument):
	def __init__(self, *args, **kw):
		super(FileArgument, self).__init__(*args, **kw)

	@classmethod
	def mode(cls, file_mode, encoding=None):
		def wrapper(*args, **kw):
			obj = cls(*args, **kw)
			obj.kw["type"] = argparse.FileType(file_mode, encoding=encoding)
			return obj
		return wrapper
