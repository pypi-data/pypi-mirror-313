from cvargparse.argument import Argument
from cvargparse.argument import Argument as Arg
from cvargparse.argument import FileArgument
from cvargparse.factory import ArgFactory
from cvargparse.factory import BaseFactory
from cvargparse.parser.base import BaseParser
from cvargparse.parser.gpu_parser import GPUParser
from cvargparse.parser.mode_parser import ModeParserFactory
from cvargparse.utils.dataclass import cvdataclass
from cvargparse.utils.dataclass import Choices

__all__ = [
	"Arg",
	"ArgFactory",
	"Choices",
	"Argument",
	"BaseFactory",
	"BaseParser",
	"cvdataclass",
	"FileArgument",
	"GPUParser",
	"ModeParserFactory",
]



if __name__ == '__main__':
	@cvdataclass
	class Args:
		group_name = "args"

		train_samples: float = None
		test_samples: int = 2
		arg2: str = "something"

		arg3: Choices([1, 2, 3], int) = 1
		is_arg4: bool = False

	parser = BaseParser(Args(test_samples=20))
	print(parser.parse_args("--is_arg4".split()))
