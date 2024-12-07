""" General utilities for constructing models from CSV files """

import re
from pydantic import BaseModel, Field
from typing import Union, List, Type, Any
from typing_extensions import Annotated


def to_class_name_underscored(name: str) -> str:
    """Convert a name to a valid class name by capitalizing and removing non-alphanumeric characters."""
    return "_" + re.sub(r"\W+", "_", name.title()).replace(" ", "")


def to_class_name(name: str) -> str:
    """Convert a name to a valid class name by capitalizing and removing non-alphanumeric characters."""
    return re.sub(r"\W|^(?=\d)", "_", name.title()).replace(" ", "")


def one_of_instance(instances: List[Type[BaseModel]], discriminator="name") -> Annotated[Union[Any], Field]:
    """
    Make an annotated union of class instances
    Parameters
    ----------
    instances : List[Type[BaseModel]]
      A list of class instances.
    discriminator : str
      Each model in instances should have a common field name where each item
      is unique to the model. This will allow pydantic to know which class
      should be deserialized. Default is 'name'.

    Returns
    -------
    Annotated[Union[Any], Field]
      An annotated field that can be used to define a type where a choice from a
      possible set of classes can be selected.

    """
    return Annotated[Union[tuple(type(i) for i in instances)], Field(discriminator=discriminator)]
