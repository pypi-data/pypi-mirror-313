#!/usr/bin/env python3
'''
The CLI module of CryptoBob.
'''

__all__ = (
    'CLI',
    'main',
)

import sys
from argparse import ArgumentParser, HelpFormatter
from logging import basicConfig, getLogger
from pathlib import Path

from pyotp import parse_uri as otp_parse_uri

from .config import Config
from .exceptions import CryptoBobError
from .kraken import KrakenClient
from .runner import Runner

LOGGER = getLogger(__name__)


class CLI:
    '''
    CryptoBob CLI class, which helps to create CLI thingy.
    '''

    @classmethod
    def init_logging(cls, level, simple=False):
        '''
        Initialise the logging config.

        :param int level: The logging level
        :param bool simple: Enable simple logging
        '''
        if simple:
            log_format = '%(message)s'
        else:
            log_format = '%(asctime)s - %(levelname)s - %(name)s: %(message)s'

        basicConfig(
            level=(4 - level) * 10,
            format=log_format,
        )

    def __init__(self):
        '''
        Constructor which initialises the parser.
        '''
        self.init_parser()

    def __call__(self):
        '''
        Parse the CLI arguments and run the builder.
        '''
        args   = vars(self.parser.parse_args())
        action = args.pop('action')

        self.init_logging(
            level=args.get('verbose') or 0,
            simple=args.get('simple')
        )

        try:

            config = Config(args.pop('config'))
            runner = Runner(config=config)

            if action == 'run':
                runner.run()

            elif action == 'buy':
                runner.buy()

            elif action == 'assets':
                sys.stdout.write('ID         | Altname\n-----------+-----------\n')
                sys.stdout.write('\n'.join(
                    f'{item[0]:10s} | {item[1]}' for item in KrakenClient.assets()
                ) + '\n')

            elif action == 'otp':
                sys.stdout.write(otp_parse_uri(config.otp_uri).now() + '\n')

        except CryptoBobError as ex:
            sys.stderr.write(f'ERROR: {ex}\n')
            sys.exit(1)

    def init_parser(self):
        '''
        Initialise the argument parser.
        '''
        def get_help_formatter(prog):  # pylint: disable=missing-return-doc,missing-return-type-doc
            return HelpFormatter(prog, max_help_position=30)

        self.parser = ArgumentParser(
            description='CryptoBob - The bot which buys & withdraws crypto automatically.',
            formatter_class=get_help_formatter
        )

        self.parser.add_argument(
            '-c', '--config',
            type=Path,
            default='~/.cryptobob.yml',
            help='path to the CryptoBob config',
        )

        self.parser.add_argument(
            '-s', '--simple',
            action='store_true',
            help='enable simple logging format (e.g. for systemd)',
        )

        self.parser.add_argument(
            '-v', '--verbose',
            action='count',
            help='enable verbose logging mode (repeat to increase verbosity, up to -vvv)',
        )

        self.parser.add_argument(
            'action',
            choices=['run', 'buy', 'assets', 'otp'],
            help='action to execute',
        )


def main():
    '''
    Main function for the CLI command execution.
    '''
    assert sys.version_info >= (3, 11), 'Python version must be 3.11 or greater'

    _cryptobob = CLI()
    _cryptobob()


if __name__ == '__main__':
    main()
