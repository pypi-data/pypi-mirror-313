'''
CryptoBob exceptions.
'''


class CryptoBobError(Exception):
    '''
    Base exception for all CryptoBob errors.
    '''


class ConfigError(CryptoBobError):
    '''
    Exception which is thrown when there's an error in the configuration file.
    '''


class ResponseError(CryptoBobError):
    '''
    Exception which is thrown when there's an error in an HTTP response.
    '''


class StatusError(ResponseError):
    '''
    Exception which is thrown when system status isn't online / normal.
    '''


class TradePlanError(CryptoBobError):
    '''
    Exception which is thrown when there's an error in the trade plan.
    '''
