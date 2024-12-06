import logging
from typing import List, Dict, Union, Optional

import tensorflow as tf
from keras import Model
from keras.models import Functional
from keras.layers import Layer, InputLayer, Input
from keras.engine.keras_tensor import KerasTensor
from keras.layers.core import TFOpLambda
from tensorflow.python.keras.engine.node import Node, KerasHistory # pylint: disable=no-name-in-module

from leap_model_rebuilder.utils import is_custom_layer, is_lambda_layer, is_tfoplambda_layer

_logger = logging.getLogger(__name__)

"""The ModelExpander class expands custom layers inside keras models.
    The Expand process is using the call method of custom layers to expand to the logic inside them.
"""


def expand_model(model: Model, layer_replacement_dict: Dict[str, Layer]) -> Model:
    """
    Expanding model's custom layers

    :return: Expanded model
    :rtype: tensorflow.keras.Model
    """

    layer_cache: Dict[str, Layer] = {}
    tensor_cache: Dict[str, KerasTensor] = {}
    model_input_tensors: List[KerasTensor] = []
    output_tensors: List[KerasTensor] = []
    for out_index, out_tensor in enumerate(model.outputs):
        out_tensor_id = _get_tensor_id(out_tensor)
        expanded_tensor = tensor_cache.get(out_tensor_id)
        if expanded_tensor is None:
            expanded_tensor = _expand_tensor(out_tensor, tensor_cache, layer_cache, model_input_tensors,
                                             layer_replacement_dict, out_index)

        output_tensors.append(expanded_tensor)

    converted_model = tf.keras.Model(inputs=model_input_tensors, outputs=output_tensors)
    return converted_model


def _expand_tensor(tensor: KerasTensor, tensor_cache: Dict[str, KerasTensor], layer_cache: Dict[str, Layer],
                   model_input_tensors: List[KerasTensor], layer_replacement_dict: Dict[str, Layer],
                   out_index: Optional[int]) -> KerasTensor:
    tensor_id = _get_tensor_id(tensor)
    expanded_tensor = tensor_cache.get(tensor_id)
    if expanded_tensor is not None:
        return expanded_tensor

    current_node = _get_node_from_tensor(tensor)
    current_layer = _get_layer_from_tensor(tensor)

    # Creating first model input layer
    if isinstance(current_layer, InputLayer):
        input_tensor = _create_input_tensor(tensor)
        tensor_cache[tensor_id] = input_tensor
        model_input_tensors.append(input_tensor)
        return input_tensor

    # get all input tensors
    node_input_tensors = []
    parent_nodes = current_node.parent_nodes
    for parent_node in parent_nodes:
        output_tensor = parent_node.outputs
        node_input_tensor = _expand_tensor(
            output_tensor, tensor_cache, layer_cache, model_input_tensors, layer_replacement_dict, None)
        node_input_tensors.append(node_input_tensor)

    # squeeze node_input_tensors
    if len(node_input_tensors) == 1:
        node_input_tensors = node_input_tensors[0]

    if is_custom_layer(current_layer):
        expanded_tensor = current_layer.call(node_input_tensors)
    elif is_lambda_layer(current_layer):
        expanded_tensor = current_layer.function(node_input_tensors)
    elif current_layer.name in layer_replacement_dict:
        replacement_layer = layer_replacement_dict[current_layer.name]
        expanded_tensor = replacement_layer(node_input_tensors)
    elif is_tfoplambda_layer(current_layer):
        expanded_tensor = _call_tf_op_lambda_layer(current_layer, node_input_tensors)
    else:
        expanded_tensor = current_layer(node_input_tensors)

    expanded_tensor = _handle_many_outputs(expanded_tensor, tensor_cache, tensor_id, out_index)
    return expanded_tensor


def _handle_many_outputs(expanded_tensor, tensor_cache, tensor_id, out_index):
    if isinstance(expanded_tensor, list):
        if out_index is None:
            out_index = 0
        ex_tensor = expanded_tensor[out_index]
        ex_tensor_id = _get_tensor_id(ex_tensor)
        tensor_cache[ex_tensor_id] = ex_tensor
        selected_tensor = ex_tensor
        expanded_tensor = selected_tensor
    else:
        tensor_cache[tensor_id] = expanded_tensor
    return expanded_tensor


def _call_tf_op_lambda_layer(current_layer: TFOpLambda,
                             node_input_tensors: Union[KerasTensor, List[KerasTensor]]) -> KerasTensor:
    call_args = current_layer.inbound_nodes[-1].call_args
    call_kwargs = current_layer.inbound_nodes[-1].call_kwargs
    if current_layer.symbol == 'stack':
        return current_layer(node_input_tensors, *call_args[2:],
                             **call_kwargs)

    if isinstance(node_input_tensors, list):
        return current_layer(*node_input_tensors)

    if not isinstance(node_input_tensors, list):
        node_input_tensors = [node_input_tensors]

    new_tfoplambda_args = list(call_args)
    for i, arg in enumerate(call_args):
        if isinstance(arg, KerasTensor):
            try:
                tensor_index = [tensor.name for tensor in node_input_tensors].index(arg.name)
                new_tfoplambda_args[i] = node_input_tensors.pop(tensor_index)
            except (IndexError, ValueError):
                pass

    new_tfoplambda_kwargs = call_kwargs.copy()
    for key, arg in call_kwargs.items():
        if isinstance(arg, KerasTensor):
            try:
                tensor_index = [tensor.name for tensor in node_input_tensors].index(arg.name)
                new_tfoplambda_kwargs[key] = node_input_tensors.pop(tensor_index)
            except (IndexError, ValueError):
                pass

    return current_layer(*new_tfoplambda_args, **new_tfoplambda_kwargs)


def _get_layer_from_tensor(tensor: KerasTensor) -> Layer:
    history = _get_keras_history(tensor)
    layer = history.layer
    return layer


def _get_keras_history(tensor: KerasTensor) -> KerasHistory:
    # pylint: disable=protected-access
    return tensor._keras_history


def _get_node_from_tensor(tensor: KerasTensor) -> Node:
    history = _get_keras_history(tensor)
    layer = history.layer
    node_index = history.node_index
    node = layer.inbound_nodes[node_index]
    return node


def _create_input_tensor(input_tensor: KerasTensor) -> KerasTensor:
    history = _get_keras_history(input_tensor)
    input_layer = history.layer
    inp_config = input_layer.get_config()
    new_input_tensor = Input(**inp_config)
    _logger.debug(f"Input created, name: {new_input_tensor.name}, shape: {new_input_tensor.shape}")
    print(f"Input created, name: {new_input_tensor.name}, shape: {new_input_tensor.shape}")
    return new_input_tensor


def _get_tensor_id(tensor: KerasTensor) -> str:
    out_tensor_id = tensor.name
    if isinstance(tensor.node.layer, Functional):
        out_tensor_id = "/".join(tensor.name.split("/")[1:])

    return out_tensor_id
