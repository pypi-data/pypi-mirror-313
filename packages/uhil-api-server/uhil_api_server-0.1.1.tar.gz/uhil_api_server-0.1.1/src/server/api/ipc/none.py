from .interface import IIPC


class IPCNone(IIPC):

    def __init__(self, *args, **kwargs):
        pass

    def read_digital_input(self, channel: int) -> bool:
        print(f'reading digital input: {channel}')
        return True

    def read_analog_input(self, channel: int) -> float:
        print(f'reading analog input: {channel}')
        return 1.5

    def read_digital_output(self, channel: int) -> bool:
        print(f'reading digital output: {channel}')
        return True

    def write_digital_output(self, channel: int, value: bool) -> None:
        print(f'writing digital output: {channel}, {value}')

    def read_analog_output(self, channel: int) -> float:
        print(f'reading analog output: {channel}')
        return 1.8

    def write_analog_output(self, channel: int, value: int | float):
        print(f'writing analog output: {channel}, {value}')

    def close(self):
        pass
