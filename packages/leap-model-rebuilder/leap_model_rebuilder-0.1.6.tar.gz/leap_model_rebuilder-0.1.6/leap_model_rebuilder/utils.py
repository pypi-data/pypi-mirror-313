import logging
from typing import Tuple, Dict

import tensorflow as tf
from keras import Model, Input
from keras.layers import Layer
from keras.models import Functional


def is_custom_layers(model: Model) -> bool:
    return any(is_custom_layer(layer) for layer in model.layers)


def is_lambda_layers(model: Model) -> bool:
    return any(is_lambda_layer(layer) for layer in model.layers)


def should_replace_layers(model: Model, layer_replacement_dict: Dict[str, Layer]) -> bool:
    if layer_replacement_dict:
        for layer in model.layers:
            if layer.name in layer_replacement_dict:
                return True
    return False


def is_lambda_layer(layer: Layer) -> bool:
    return type(layer).__name__ == 'Lambda'


def is_tfoplambda_layer(layer: Layer) -> bool:
    return layer.__class__.__name__ == 'TFOpLambda'


def is_custom_layer(layer: Layer) -> bool:
    is_part_of_keras = layer.__module__.startswith("tensorflow") or layer.__module__.startswith("keras")
    is_model = layer.__class__.__name__ in ['Functional', 'Sequential']
    return not is_part_of_keras or is_model


def convert_subclassed_to_functional(model: Model, input_tensor_shape: Tuple[int, ...]) -> Functional:
    if not isinstance(model, Functional):
        input_tensor = Input(shape=input_tensor_shape)
        output_tensors = model.call(input_tensor)
        model = tf.keras.Model(inputs=input_tensor, outputs=output_tensors)

    return model


def configure_logger(verbose):
    logging_level = logging.INFO
    if verbose:
        logging_level = logging.DEBUG

    # pylint: disable=no-member
    loggers = [logging.getLogger(name)
               for name in logging.root.manager.loggerDict if name.startswith("leap_model_rebuilder")]
    root_logger = logging.getLogger()
    loggers.append(root_logger)
    for logger in loggers:
        logger.setLevel(logging_level)

    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging_level,
                        datefmt='%Y-%m-%d %H:%M:%S')
