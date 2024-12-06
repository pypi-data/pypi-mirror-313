from cvargparse.parser import base

class GPUParser(base.BaseParser):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)
		self.add_argument(
			"--gpu", "-g", type=int, nargs="+", default=[-1],
			help="which GPU to use. select -1 for CPU only")
