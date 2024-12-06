import abc


class IIPC(abc.ABC):

    @abc.abstractmethod
    def read_digital_input(self, channel: int) -> bool:
        pass

    @abc.abstractmethod
    def read_analog_input(self, channel: int) -> float:
        pass

    @abc.abstractmethod
    def read_digital_output(self, channel: int) -> bool:
        pass

    @abc.abstractmethod
    def write_digital_output(self, channel: int, value: bool) -> None:
        pass

    @abc.abstractmethod
    def read_analog_output(self, channel: int) -> float:
        pass

    @abc.abstractmethod
    def write_analog_output(self, channel: int, value: int | float):
        pass

    @abc.abstractmethod
    def close(self):
        pass
