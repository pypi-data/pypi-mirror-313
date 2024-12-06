import argparse
import sys
import typing
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from starlette.responses import RedirectResponse

from .api.ipc import ipc_factory
from .api.v1 import v1


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    args = app.state.args
    ipc_type = args.pop('subcommand')
    device = ipc_factory(ipc_type=ipc_type, **args)
    yield dict(device=device)
    device.close()


app = fastapi.FastAPI(lifespan=lifespan, debug=True)
app.mount('/v1', v1)


@app.get('/', include_in_schema=False)
def root_redirect(request: fastapi.Request):
    return RedirectResponse(url=f'{request.url}v1/')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='uhil_api', description='µHIL API server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='host name')
    parser.add_argument('--port', type=int, default=8000, help='port number')
    parser.add_argument('--log_level', type=str, default='debug', help='log level')

    sub_parser = parser.add_subparsers(title='subcommands', dest='subcommand', required=True)

    none_config = sub_parser.add_parser('none_config', help='None configuration')

    spi_config = sub_parser.add_parser('spi_config', help='SPI configuration')
    spi_config.add_argument('-bus', type=int, help='bus number (for example 0 for /dev/spidev0.1', default=0)
    spi_config.add_argument('-device', type=int, help='device number (for example 1 for /dev/spidev0.1', default=0)
    spi_config.add_argument('-speed', type=int, help='SPI communication speed in Hz', default=1000000)

    return parser


def main(args: typing.List[str] = tuple(sys.argv[1:])):
    args = vars(get_parser().parse_args(args))
    host = args.pop('host')
    port = args.pop('port')
    log_level = args.pop('log_level')

    app.state.args = args
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == '__main__':
    sys.exit(main())
