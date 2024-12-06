import abc
import typing as T

from cvargparse.utils import factory
from cvargparse.argument import Argument as Arg


class BaseFactory(abc.ABC):
	'''

	'''
	def __init__(self, initial: T.Optional[T.List[Arg]] = None):
		super(BaseFactory, self).__init__()
		self.args = initial or []

	@factory
	def add(self, *args, **kwargs):
		self.args.append(Arg(*args, **kwargs))

	def get(self):
		return self.args


class ArgFactory(BaseFactory):
	'''

	'''
	@factory
	def batch_size(self):
		self.add('--batch_size', '-b', type=int, default=32, help='batch size')


	@factory
	def epochs(self):
		self.add('--epochs', '-e', type=int, default=30, help='number of epochs')


	@factory
	def debug(self):
		self.add('--debug', action='store_true', help='enable debug mode')


	@factory
	def seed(self):
		self.add('--seed', type=int, default=None, help='random seed')


	@factory
	def weight_decay(self, default=5e-3):
		self.add('--decay', type=float, default=default, help='weight decay')


	@factory
	def learning_rate(self, lr=1e-2, lrs=10, lrd=1e-1, lrt=1e-6):
		self.add('--learning_rate', '-lr', type=float, default=lr, help='learning rate')
		self.add('--lr_shift', '-lrs', type=int, default=lrs, help='learning rate shift interval (in epochs)')
		self.add('--lr_decrease_rate', '-lrd', type=float, default=lrd, help='learning rate decrease')
		self.add('--lr_target', '-lrt', type=float, default=lrt, help='learning rate target')
