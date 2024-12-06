from typing import List

from cvargparse.parser.base import BaseParser
from cvargparse.parser.gpu_parser import GPUParser

class ModeParserFactory(object):

	def __init__(self, *args,
		parser_cls=BaseParser,
		subp_parent_cls=BaseParser,
		**kwargs) -> None:

		self._parser = parser_cls(*args, **kwargs)

		self._subparsers = self._parser.add_subparsers(dest="mode",
			help="get the help messages for the sub commands with <mode> -h")

		self._subparser_parent = None
		if subp_parent_cls is not None:
			self._subparser_parent = subp_parent_cls(add_help=False, nologging=True)

	def parse_args(self, *args, **kwargs):
		return self._parser.parse_args(*args, **kwargs)

	@property
	def subp_parent(self):
		return self._subparser_parent


	def add_mode(self, mode: str, *, parents: List = []) -> BaseParser:
		if self._subparser_parent is not None:
			parents = parents + [self._subparser_parent]
		parser = self._subparsers.add_parser(mode, parents=parents)
		return parser
