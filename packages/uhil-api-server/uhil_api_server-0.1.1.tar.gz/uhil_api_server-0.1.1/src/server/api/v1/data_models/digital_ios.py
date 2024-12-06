import typing

import pydantic

from .constants import *


class ValueModel(pydantic.BaseModel):
    internal: typing.Optional[float] = pydantic.Field(description='', default=None)
    physical: typing.Optional[float] = pydantic.Field(description='', default=None)


class InputModel(pydantic.BaseModel):
    name: typing.Optional[pydantic.constr(max_length=64)] = pydantic.Field(description='', default=None)
    index: int = pydantic.Field(description='', ge=0, le=8, default=-1)
    value: ValueModel = pydantic.Field(description='', default=ValueModel())


class DigitalInputModel(pydantic.BaseModel):
    index: int = pydantic.Field(description='', ge=0, le=NUMBER_OF_DIGITAL_INPUTS - 1)
    value: bool = pydantic.Field(description='')


class AnalogInputModel(InputModel):
    index: int = pydantic.Field(description='', ge=0, le=NUMBER_OF_ANALOG_INPUTS - 1)
    value: float = pydantic.Field(description='')


class DigitalOutputModel(DigitalInputModel):
    index: int = pydantic.Field(description='', ge=0, le=NUMBER_OF_DIGITAL_INPUTS - 1)
    value: bool = pydantic.Field(description='')