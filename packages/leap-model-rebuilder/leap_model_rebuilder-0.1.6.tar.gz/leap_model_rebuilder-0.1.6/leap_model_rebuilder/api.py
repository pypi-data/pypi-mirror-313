from typing import Tuple, Optional, Dict

from keras.models import Model
from keras.layers import Layer

from leap_model_rebuilder.modelexpander import expand_model
from leap_model_rebuilder.utils import is_custom_layers, convert_subclassed_to_functional, should_replace_layers, \
    is_lambda_layers


def rebuild_model(model: Model, input_tensor_shape: Optional[Tuple[int, ...]] = None,
                  layer_replacement_dict: Optional[Dict[str, Layer]] = None) -> Model:
    """
        Rebuild keras models from Subclassed to Functional and Expands custom layers inside

        :param model: keras model to rebuild in Functional way
        :type model: tensorflow.keras.Model
        :param input_tensor_shape: shape of input tensor
        :type input_tensor_shape: Tuple[int, ...]gst
        :param layer_replacement_dict: dictionary to replace layers.
               keys are the layer names and the value the layer to replace with.
        :return: rebuilt Functional keras model
        :rtype: tensorflow.keras.Model
        """
    if layer_replacement_dict is None:
        layer_replacement_dict = {}
    if input_tensor_shape is not None:
        model = convert_subclassed_to_functional(model, input_tensor_shape)
    while is_custom_layers(model) or is_lambda_layers(model) or should_replace_layers(model, layer_replacement_dict):
        model = expand_model(model, layer_replacement_dict)

    return model
