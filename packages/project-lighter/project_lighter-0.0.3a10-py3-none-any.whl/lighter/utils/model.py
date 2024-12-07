from typing import Dict, List

import torch
from loguru import logger
from torch.nn import Identity, Module, Sequential

from lighter.utils.misc import setattr_dot_notation


def replace_layer_with(model: Module, layer_name: str, new_layer: Module) -> Module:
    """Replaces the specified layer of the network with another layer.

    Args:
        model (Module): PyTorch model to be edited
        layer_name (string): Name of the layer which will be replaced.
            Dot-notation supported, e.g. "layer10.fc".

    Returns:
        PyTorch model with the new layer set at the specified location.
    """
    setattr_dot_notation(model, layer_name, new_layer)
    return model


def replace_layer_with_identity(model: Module, layer_name: str) -> Module:
    """Replaces any layer of the network with an Identity layer.
    Useful for removing layers of a network to be used as a backbone.

    Args:
        model (Module): PyTorch model to be edited
        layer_name (string): Name of the layer which will be replaced with an
            Identity function. Dot-notation supported, e.g. "layer10.fc".

    Returns:
        PyTorch model with Identity layer at the specified location.
    """
    return replace_layer_with(model, layer_name, Identity())


def remove_n_last_layers_sequentially(model: Module(), num_layers=1) -> Sequential:
    """Remove a number of last layers of a network and return it as an nn.Sequential model.
    Useful when a network is used as a backbone of an SSL model.

    Args:
        model (Module): PyTorch model object.
        num_layers (int, optional): Number of last layers to be removed. Defaults to 1.

    Returns:
        PyTorch Sequential model with the last layer removed.
    """
    return Sequential(*list(model.children())[:-num_layers])


def adjust_prefix_and_load_state_dict(
    model: Module, ckpt_path: str, ckpt_to_model_prefix: Dict[str, str] = None, layers_to_ignore: List[str] = None
) -> Module:
    """Load state_dict from a checkpoint into a model using `torch.load(strict=False`).
    `ckpt_to_model_prefix` mapping allows to rename the prefix of the checkpoint's state_dict keys
    so that they match those of the model's state_dict. This is often needed when a model was trained
    as a backbone of another model, so its state_dict keys won't be the same to those of a standalone
    version of that model. Prior to defining the `ckpt_to_model_prefix`, it is advised to manually check
    for mismatch between the names and specify them accordingly.

    Args:
        model (Module): PyTorch model instance to load the state_dict into.
        ckpt_path (str): Path to the checkpoint.
        ckpt_to_model_prefix (Dict[str, str], optional): A dictionary that maps keys in the checkpoint's
            state_dict to keys in the model's state_dict. If None, no key mapping is performed. Defaults to None.
        layers_to_ignore (List[str], optional): A list of layer names that won't be loaded into the model.
            Specify the names as they are after `ckpt_to_model_prefix` is applied. Defaults to None.
    Returns:
        The model instance with the state_dict loaded.

    Raises:
        ValueError: If there is no overlap between checkpoint's and model's state_dict.
    """

    # Load checkpoint
    ckpt = torch.load(ckpt_path)

    # Check if the checkpoint is a model's state_dict or a LighterSystem checkpoint.
    # A LighterSystem checkpoint contains the model’s entire internal state, we only need its state_dict.
    if "state_dict" in ckpt:
        ckpt = ckpt["state_dict"]
        # Remove the "model." prefix from the checkpoint's state_dict keys. This is characteristic to LighterSystem.
        ckpt = {key.replace("model.", ""): value for key, value in ckpt.items()}

    # Adjust the keys in the checkpoint's state_dict to match the the model's state_dict's keys.
    if ckpt_to_model_prefix is not None:
        for ckpt_prefix, model_prefix in ckpt_to_model_prefix.items():
            # Add a dot at the end of the prefix if necessary.
            ckpt_prefix = ckpt_prefix if ckpt_prefix == "" or ckpt_prefix.endswith(".") else f"{ckpt_prefix}."
            model_prefix = model_prefix if model_prefix == "" or model_prefix.endswith(".") else f"{model_prefix}."
            if ckpt_prefix != "":
                # Replace ckpt_prefix with model_prefix in the checkpoint state_dict
                ckpt = {key.replace(ckpt_prefix, model_prefix): value for key, value in ckpt.items() if ckpt_prefix in key}
            else:
                # Add the model_prefix before the current key name if there's no specific ckpt_prefix
                ckpt = {f"{model_prefix}{key}": value for key, value in ckpt.items() if ckpt_prefix in key}

    # Check if the checkpoint's and model's state_dicts have no overlap.
    model_keys = list(model.state_dict().keys())
    ckpt_keys = list(ckpt.keys())
    if not set(ckpt_keys) & set(model_keys):
        raise ValueError(
            "There is no overlap between checkpoint's and model's state_dict."
            f"\nModel keys: '{model_keys[0]}', ..., '{model_keys[-1]}', "
            f"\nCheckpoint keys: '{ckpt_keys[0]}', ..., '{ckpt_keys[-1]}'"
        )

    # Remove the layers that are not to be loaded.
    if layers_to_ignore is not None:
        for layer in layers_to_ignore:
            ckpt.pop(layer)

    # Load the adjusted state_dict into the model instance.
    incompatible_keys = model.load_state_dict(ckpt, strict=False)

    # Log the incompatible keys during checkpoint loading.
    if len(incompatible_keys.missing_keys) > 0 or len(incompatible_keys.unexpected_keys) > 0:
        logger.info(f"Encountered incompatible keys during checkpoint loading. If intended, ignore.\n{incompatible_keys}")
    else:
        logger.info("Checkpoint loaded successfully.")

    return model
