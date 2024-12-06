'''
CryptoBob Kraken module.
'''

__all__ = (
    'KrakenClient',
)

from base64 import b64decode, b64encode
from hashlib import sha256, sha512
from hmac import digest as hmac_digest
from json import load
from logging import getLogger
from time import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from pyotp import parse_uri as otp_parse_uri

from .exceptions import ResponseError, StatusError

LOGGER = getLogger(__name__)


class KrakenClient:
    '''
    The API client to talk to the Kraken REST API.

    :param api_key: The API key retreived from Kraken
    :type api_key: None or str
    :param private_key: The private key retreived from Kraken
    :type private_key: None or str
    :param otp_uri: The 2FA / OTP URI retreived from Kraken (optional)
    :type otp_uri: None or str
    '''

    api_host = 'api.kraken.com'

    public_api_methods = [
        'AssetPairs',
        'Assets',
        'Depth',
        'OHLC',
        'Spread',
        'SystemStatus',
        'Ticker',
        'Time',
        'Trades',
    ]

    @classmethod
    def assets(cls):
        '''
        Return the available assets.

        :return: The asset ID & altname
        :rtype: generator
        '''
        for iid, item in cls().request('Assets').items():
            yield iid, item['altname']

    @classmethod
    def ticker(cls):
        '''
        Return the ticker information for all available markets.

        :return: The ticket information
        :rtype: dict
        '''
        return cls().request('Ticker')

    def __init__(self, api_key=None, private_key=None, otp_uri=None):
        self.api_key     = api_key
        self.private_key = b64decode(private_key) if private_key else None
        self.otp_uri     = otp_uri
        self.portfolio   = {}

    def _sign_request(self, endpoint, **data):
        '''
        Sign the HTTP request and return the new data string, as well as
        additional headers required for authentication.

        :param str endpoint: The API endpoint / path
        :param dict \\**data: The API data

        :return: The signed data & headers
        :rtype: tuple(str, list)
        '''
        # Use UNIX timestamp as nonce and append it do the data.
        data['nonce'] = str(int(time() * 1000))

        # Add OTP if OTP is set
        if self.otp_uri:
            data['otp'] = otp_parse_uri(self.otp_uri).now()

        # URL-encode data.
        data_encoded = urlencode(data)

        # Create SHA256 hash of nonce & data.
        hash_sha256 = sha256(f'{data["nonce"]}{data_encoded}'.encode('utf-8')).digest()

        # Create SHA512 HMAC digest for endpoint & SHA256-hashed nonce & data.
        hmac_sha512 = hmac_digest(
            key=self.private_key,
            msg=endpoint.encode('utf-8') + hash_sha256,
            digest=sha512
        )

        # Create headers.
        headers = {
            'API-Key': self.api_key,
            'API-Sign': b64encode(hmac_sha512),
        }

        return data_encoded, headers

    def _prepare_request(self, api_method, **data):
        '''
        Prepare the HTTP request and return the url & data.

        :param str api_method: The API method
        :param dict \\**data: The API data

        :return: The URL, urlencoded data, and headers
        :rtype: dict
        '''
        scope    = 'public' if api_method in self.public_api_methods else 'private'
        endpoint = f'/0/{scope}/{api_method}'

        kwargs = {
            'url': f'https://{self.api_host}{endpoint}',
            'headers': {
                'User-Agent': 'CryptoBob',
            }
        }

        if scope == 'private':
            data_encoded, add_headers = self._sign_request(endpoint=endpoint, **data)
            kwargs['data'] = data_encoded.encode('utf-8')
            kwargs['headers'].update(add_headers)
        elif data:
            data_encoded = urlencode(data)
            kwargs['url'] += f'?{data_encoded}'

        LOGGER.debug('HTTP request:')
        LOGGER.debug('    URL:     %r', kwargs['url'])
        LOGGER.debug('    Data:    %r', kwargs.get('data', b'').decode('utf-8'))
        LOGGER.debug('    Headers: %r', kwargs['headers'])

        return kwargs

    def request(self, api_method, **data):
        '''
        Make a request to the Kraken API.

        :param str api_method: The API method
        :param dict \\**data: The API data

        :return: The response result
        :rtype: dict

        :raises ResponseError: When there was an error in the response
        '''
        kwargs  = self._prepare_request(api_method=api_method, **data)
        request = Request(**kwargs)

        with urlopen(request) as response:  # nosemgrep: dynamic-urllib-use-detected
            response_data  = load(response)

            LOGGER.debug('HTTP response: %r', response_data)

            response_error = response_data.get('error')
            if response_error:
                raise ResponseError(', '.join(response_error))

        return response_data['result']

    def assert_online_status(self):
        '''
        Assert that the exchange status is online (and not maintenance).

        :raises exceptions.StatusError: When system status isn't online
        '''
        LOGGER.debug('Asserting online system status')

        status = self.request('SystemStatus')['status']
        if status != 'online':
            raise StatusError(f'System status is {status!r}')

    def update_portfolio(self):
        '''
        Update the account portfolio.
        '''
        LOGGER.debug('Updating account portfolio')

        ticker   = self.ticker()
        balances = self.request('Balance').items()

        self.portfolio = {}

        for asset, balance in balances:
            balance = float(balance)

            if asset == 'ZUSD':
                ask_price = 1
            else:
                asset_ticker = ticker.get(f'{asset}USD') \
                    or ticker.get(f'USD{asset}')  \
                    or ticker.get(f'{asset}ZUSD')
                ask_price = float(asset_ticker['a'][0])

            self.portfolio[asset] = {
                'balance': balance,
                'balance_usd': balance * ask_price,
                'price': ask_price
            }
