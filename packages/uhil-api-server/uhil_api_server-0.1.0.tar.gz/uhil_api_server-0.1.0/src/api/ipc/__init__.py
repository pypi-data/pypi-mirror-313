import enum

from .interface import IIPC
from .none import IPCNone

try:
    from .spi import IPCSPI
except ModuleNotFoundError as e:
    from sys import platform

    if platform != 'win32':
        raise e


class IPCType(enum.Enum):
    NONE = 'none'
    SPI = 'spi'


def ipc_factory(ipc_type: str, *args, **kwargs) -> IIPC:
    if ipc_type.startswith(IPCType.SPI.value):
        return IPCSPI(*args, **kwargs)
    if ipc_type.startswith(IPCType.NONE.value):
        return IPCNone(*args, **kwargs)
    raise ValueError(f'Unsupported IPC type: {ipc_type}')
