import pydantic

NUMBER_OF_DIGITAL_INPUTS = 8
NUMBER_OF_ANALOG_INPUTS = 8
NUMBER_OF_DIGITAL_OUTPUTS = 8
NUMBER_OF_ANALOG_OUTPUTS = 32


class HardwareConfigurationModel(pydantic.BaseModel):
    number_of_digital_inputs: int = pydantic.Field(description='Number of digital inputs available in hardware',
                                                   default=NUMBER_OF_DIGITAL_INPUTS)
    number_of_analog_inputs: int = pydantic.Field(description='Number of analog inputs available in hardware',
                                                  default=NUMBER_OF_ANALOG_INPUTS)
    number_of_digital_outputs: int = pydantic.Field(description='Number of digital outputs available in hardware',
                                                   default=NUMBER_OF_DIGITAL_OUTPUTS)
    number_of_analog_outputs: int = pydantic.Field(description='Number of analog outputs available in hardware',
                                                  default=NUMBER_OF_ANALOG_OUTPUTS)
