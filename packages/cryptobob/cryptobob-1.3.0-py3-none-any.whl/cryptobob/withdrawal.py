'''
CryptoBob withdrawal module.
'''

__all__ = (
    'Withdrawal',
)

from logging import getLogger

LOGGER = getLogger(__name__)


class Withdrawal:
    '''
    The withdrawal class.

    :param runner.Runner runner: The runner
    :param str asset: The asset ID
    :param float threshold: The threshold when the withdrawal should be triggered
    :param str key: The address key (must be configured on Kraken)
    :param str address: The address to which the asset should be transferred
    :param amount: The amount
    :type amount: None or float
    '''

    configuration_attribute = 'withdrawals'

    def __init__(self, runner, asset, threshold, key, address, amount=None, usd=False):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.runner    = runner
        self.asset     = asset
        self.threshold = threshold
        self.key       = key
        self.address   = address
        self.amount    = amount
        self.usd       = usd

    def __str__(self):
        '''
        The informal string version of the object.

        :return: The informal string version
        :rtype: str
        '''
        return self.asset

    def __repr__(self):
        '''
        The official string version of the object.

        :return: The informal string version
        :rtype: str
        '''
        return f'<{self.__class__.__name__}: {self.asset}>'

    def __call__(self):
        '''
        Check if the withdrawal threshold is exceeded, then automatically
        withdraw the asset to the defined address.
        '''
        LOGGER.debug('Evaluating %r', self)

        asset  = self.asset
        symbol = 'USD' if self.usd else self.asset
        balance, balance_usd = self.balance

        LOGGER.debug('%s balance is %f (%f USD), configured withdrawal threshold is %f %s',
                     self.asset, balance, balance_usd, self.threshold, symbol)

        if not self.withdrawal_required:
            LOGGER.debug('%s threshold not exceeded, skipping withdrawal', asset)
            return

        amount, amount_usd = self.withdrawal_amount
        address            = self.address
        key                = self.key

        LOGGER.info('Initiating withdrawal of %f %s (%f USD) to %s',
                    amount, asset, amount_usd, address)

        if not self.runner.config.get('test', False):
            self.runner.client.request(
                'Withdraw',
                asset=asset,
                key=key,
                address=address,
                amount=amount,
            )

    @property
    def balance(self):
        '''
        The asset / portfolio balance.

        :return: Native & USD balance
        :rtype: tuple
        '''
        asset = self.runner.client.portfolio.get(self.asset)

        if asset:
            return asset['balance'], asset['balance_usd']
        return 0, 0

    @property
    def withdrawal_required(self):
        '''
        Check if the withdrawal should be executed.

        :return: Withdrawal required
        :rtype: bool
        '''
        balance = self.balance[1] if self.usd else self.balance[0]
        return 0 < balance >= self.threshold

    @property
    def withdrawal_amount(self):
        '''
        The withdrawal amount.

        :return: Withdrawal amount
        :rtype: tuple
        '''
        amount               = self.amount or 0.0
        balance, balance_usd = self.balance
        price                = self.runner.client.portfolio[self.asset]['price']

        if not amount:
            return balance, balance_usd

        if self.usd:
            amount /= price

        withdraw_amount = min(amount or balance, balance)

        return withdraw_amount, withdraw_amount * price
