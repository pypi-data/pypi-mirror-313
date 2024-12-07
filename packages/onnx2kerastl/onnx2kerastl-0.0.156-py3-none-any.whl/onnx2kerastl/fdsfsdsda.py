from keras.layers.core.tf_op_layer import TFOpLambda
import tensorflow as tf
import logging
logger = logging.getLogger('onnx2keras.tfops_funcs1')

layer_names_counter = {}


def enforce_kwarg_init(original_init):
    def new_init(self, *args, **kwargs):
        print(args)
        original_init(self, *args, **kwargs)
        if tf_name is None or tf_name == "" or not isinstance(tf_name, str):
            raise ValueError(f"The layer {self} with name"
                             f" {self.name} was provided with an empty or None Name")
        if tf_name not in layer_names_counter:
            layer_names_counter[tf_name] = 0
        else:
            layer_names_counter[tf_name] = layer_names_counter[tf_name] + 1
            tf_name = tf_name + f"_{layer_names_counter[tf_name]}"
            logger.debug(f"The op {self.symbol} with name"
                             f"{self.name} has a duplicate name {tf_name}")
    return new_init


TFOpLambda.__init__ = enforce_kwarg_init(TFOpLambda.__init__)

# Replace the __init__ method of ExistingClass with enforce_kwarg_init
res = tf.add(tf.keras.Input((300, 300)), 1, tf_name='3')

import tensorflow as tf
import keras
from copy import deepcopy
inpt = tf.keras.layers.Input((300, 300, 3))
a = keras.layers.Multiply(name='fdsfsd')
print(1)


