import struct

import spidev

from .interface import IIPC


class IPCSPI(IIPC):

    def __init__(self, bus: int, device: int, speed=1000000):
        self._device = spidev.SpiDev()
        self._device.open(bus, device)
        self._device.max_speed_hz = speed

    def read_digital_input(self, channel: int):
        result = self._device.xfer([0x22, 0x00, channel])
        print(f'reading digital input: {channel}')

    def read_analog_input(self, channel: int):
        result = self._device.xfer([0x22, 0x01, channel])
        print(f'reading analog input: {channel}')

    def read_digital_output(self, channel: int) -> bool:
        result = self._device.xfer([0x22, 0x02, channel])
        print(f'reading analog input: {channel}')
        return True

    def write_digital_output(self, channel: int, value: bool):
        result = self._device.xfer([0x2E, 0x02, channel, int(value)])
        print(f'writing digital output: {channel}, {value}')

    def write_analog_output(self, channel: int, value: int | float):
        result = self._device.xfer([0x2E, 0x01, channel] + [int(b) for b in bytearray(struct.pack("f", float(value)))])
        print(f'writing digital output: {channel}, {value}')

    def close(self):
        self._device.close()
