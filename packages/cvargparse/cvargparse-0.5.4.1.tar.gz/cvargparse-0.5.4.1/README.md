# Wrapper for `argparse`

## Installation

`pip install cvargparse`

## Usage

Some sample code (with some pseudo DL framework):

```python
from cvargparse import GPUParser
from cvargparse import ArgFactory
from cvargparse import Arg

from dlframework import Model, LRSchedule, Updater, Iterator, to_gpu, load_data

def main(args):
    data = load_data(args.data, args.labels)
    model = Model(args.model_weights)
    # we can select multiple GPUs. use the first GPU for the initial model creation
    
    GPU = args.gpu[0]
    if GPU >= 0:
        to_gpu(model, GPU)
    
    lr_schedule = LRSchedule(args.lr, args.lr_shift, args.lr_decrease_rate, args.lr_target)
    
    updater = Updater(model, lr_schedule, decay=args.decay)
    
    it = Iterator(data, args.batch_size)
    
    for epoch in range(args.epochs):
        for batch in it:
            updater.train(model, batch)

ArgFactory([
	Arg("data", type=str),
	Arg("labels", type=str),
	Arg("model_weights", type=str),
])\
.epochs()\
.batch_size()\
.learning_rate(lr=1e-3)\
.weight_decay(5e-3)\
.seed()\
.debug()

parser = GPUParser(factory)

parser.init_logger()
main(parser.parse_args())
```

This script can be called as following:

```bash
python script.py path/to/data path/to/labels path/to/model \
    --gpu 0 1 \
    -lr 0.001 -lrs 30 -lrd 0.1 -lrt 1e-7 \
    --batch_size 32 \
    --epochs 90 \
    --loglevel DEBUG \
    --logfile path/to/logs    
```

## Main Features

### Argument Factory
* pre-defined frequently used arguments
* each factory method return the factory itself, hence one can chain the factory calls
* some factory methods support default value definition

```python
from cvargparse import GPUParser, ArgFactory, Arg

factory = ArgFactory([
    Arg("data", type=str),
    Arg("labels", type=str),
    Arg("model_weights", type=str),
])

facotry.epochs()
facotry.batch_size()
factory.weight_decay(5e-3)
factory.learning_rate(lr=1e-3)
factory.debug().seed()

parser = GPUParser(factory)
args = parser.parse_args()
```

### Argument Choices
* case insensitive
* default choice definition
* automatic argument generation
* pythonic way of argument-to-value access

```python
import logging
from cvargparse.utils import BaseChoiceType
from dlframework.models import VGG19, ResNet, InceptionV3
from dlframework.optimizers import Adam, RMSProp, MomentumSGD


class ModelTypes(BaseChoiceType):
    Default = ResNet
    Resnet = ResNet
    VGG = VGG19
    Inception = InceptionV3


class OptimizerTypes(BaseChoiceType):
    Default = Adam
    adam = Adam
    rms = RMSProp
    sgd = MomentumSGD
    

def main(args):

    model_type = ModelType.get(args.model_type)
    logging.info("Creating \"{}\" model".format(model_type.name))
    model_cls = model_type.value
    model = model_cls(args.model_weights)
    
    opt_type = OptimizerType.get(args.model_type)
    logging.info("Using \"{}\" optimizer".format(opt_type.name))
    opt_cls = opt_type.value
    opt = opt_cls(args.learning_rate, model)
    
    
    # further training / optimization code

factory = ArgFactory([
    Arg("data", type=str),
    Arg("labels", type=str),
    Arg("model_weights", type=str),
    
    ModelTypes.as_arg(name="model_type", short_name="mt", help_text="Model type selection"),
    OptimizerTypes.as_arg(name="optimizer", short_name="opt", help_text="Optimizer selection"),
])

facotry.epochs()
facotry.batch_size()
factory.weight_decay(5e-3)
factory.learning_rate(lr=1e-3)
factory.debug().seed()

parser = GPUParser(factory)
parser.init_logger()

main(parser.parse_args())
```

```bash
python script.py path/to/data path/to/labels path/to/model \
    --model_type resnet
    --optimizer adam
    ...
```
