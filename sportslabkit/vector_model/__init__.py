from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union
from collections.abc import Sequence

import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchmetrics
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchmetrics.functional import accuracy
from torchvision import models, transforms
from torchvision.datasets import ImageFolder

from sportslabkit.vector_model.base import BaseVectorModel
from sportslabkit.vector_model.sklearn import SklearnVectorModel
from sportslabkit.logger import logger
from sportslabkit.types.detection import Detection


def inheritors(cls):
    """
    Get all subclasses of a given class.

    Args:
        cls (type): The class to find subclasses of.

    Returns:
        set[type]: A set of the subclasses of the input class.
    """
    subclasses = set()
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def show_available_models():
    """
    Print the names of all available BaseDetectionModel models.

    The models are subclasses of BaseDetectionModel. The names are printed as a list to the console.
    """
    return sorted([cls.__name__ for cls in inheritors(BaseVectorModel)])


def load(model_name, **model_config):
    """
    Load a model by name.

    The function searches subclasses of BaseDetectionModel for a match with the given name. If a match is found, an instance of the model is returned. If no match is found, a warning is logged and the function returns None.

    Args:
        model_name (str): The name of the model to load.

    Returns:
        BaseDetectionModel: An instance of the requested model, or None if no match was found.
    """
    for cls in inheritors(BaseVectorModel):
        if model_name in [cls.__name__.lower(), cls.__name__]:
            config = {k.lower(): v for k, v in model_config.items()}
            return cls(**config)
    logger.warning(
        f"Model {model_name} not found. Available models: {[cls.__name__ for cls in inheritors(BaseVectorModel)]} (lowercase is allowed)"
    )
