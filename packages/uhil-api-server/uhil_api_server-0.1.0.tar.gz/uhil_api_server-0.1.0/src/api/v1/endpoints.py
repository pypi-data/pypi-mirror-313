import os
import typing

import fastapi
from starlette.responses import RedirectResponse

from .data_models import *
from ..ipc import IIPC

with open(os.path.join(os.path.dirname(__file__), 'description.md'), 'rb') as fp:
    description = fp.read().decode('utf-8')
v1 = fastapi.FastAPI(title='µHIL API', description=description)


@v1.get('/', include_in_schema=False)
async def root_redirect(request: fastapi.Request):
    return RedirectResponse(url=f'{request.url}docs')


@v1.get('/config/hardware_info',
        response_model=ConstantModel,
        response_model_exclude_none=False,
        tags=['Configuration'],
        description='Returns the constants defined by the underlying hardware.')
async def get_constants():
    return ConstantModel()


@v1.get('/io/inputs/digital/{index}',
        response_model=DigitalInputModel,
        response_model_exclude_none=False,
        tags=['I/O'],
        description='Returns the value of the requested digital input.')
async def read_digital_input_value(request: fastapi.Request,
                                   index: typing.Annotated[int, fastapi.Path(ge=0, le=NUMBER_OF_DIGITAL_INPUTS - 1)]):
    spi: IIPC = request.state.device
    value = spi.read_digital_input(index)
    return DigitalInputModel(index=index, value=value)


@v1.get('/io/inputs/analog/{index}',
        response_model=AnalogInputModel,
        response_model_exclude_none=False,
        tags=['I/O'],
        description='Returns the value of the requested analog input.')
async def read_analog_input_value(request: fastapi.Request,
                                  index: typing.Annotated[int, fastapi.Path(ge=0, le=NUMBER_OF_ANALOG_INPUTS - 1)]):
    spi: IIPC = request.state.device
    value = spi.read_analog_input(index)
    return AnalogInputModel(index=index, value=value)


@v1.get('/io/outputs/digital/{index}',
        response_model=DigitalOutputModel,
        response_model_exclude_none=False,
        tags=['I/O'],
        description='Sets the value of the requested digital output.')
async def read_digital_output_value(request: fastapi.Request,
                                    index: typing.Annotated[int, fastapi.Path(ge=0, le=NUMBER_OF_DIGITAL_OUTPUTS - 1)]):
    spi: IIPC = request.state.device
    result = spi.read_digital_output(index)
    return DigitalOutputModel(index=index, value=result)


@v1.put('/io/outputs/digital/{index}',
        tags=['I/O'],
        description='Sets the value of the requested digital output.')
async def write_digital_output_value(request: fastapi.Request,
                                     index: typing.Annotated[int, fastapi.Path(ge=0, le=NUMBER_OF_DIGITAL_INPUTS - 1)],
                                     value: bool):
    spi: IIPC = request.state.device
    result = spi.write_digital_output(index, value)


@v1.put('/io/outputs/analog/{index}',
        tags=['I/O'],
        description='Sets the value of the requested analog output.')
async def write_analog_output_value(request: fastapi.Request,
                                    index: typing.Annotated[int, fastapi.Path(ge=0, le=NUMBER_OF_DIGITAL_INPUTS - 1)],
                                    value: float):
    spi: IIPC = request.state.device
    result = spi.write_analog_output(index, value)
