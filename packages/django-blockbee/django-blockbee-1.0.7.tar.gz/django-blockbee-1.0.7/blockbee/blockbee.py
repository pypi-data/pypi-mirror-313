import requests

BLOCKBEE_URL = 'https://api.blockbee.io/'
BLOCKBEE_HOST = 'api.blockbee.io'


def get_info(apikey, coin=''):
    params = {
        'apikey': apikey
    }

    _info = process_request(coin, endpoint='info', params=params)

    if _info:
        return _info

    return None


def get_supported_coins(apikey):
    _info = get_info(apikey, '')

    _info.pop('fee_tiers', None)

    _coins = {}

    for ticker, coin_info in _info.items():

        if 'coin' in coin_info.keys():
            _coins[ticker] = coin_info['coin']
        else:
            for token, token_info in coin_info.items():
                _coins[ticker + '_' + token] = token_info['coin'] + ' (' + ticker.upper() + ')'

    return _coins


def get_logs(coin, callback_url, apikey):
    if coin is None or callback_url is None:
        return None

    params = {
        'callback': callback_url,
        'apikey': apikey
    }

    _logs = process_request(coin, endpoint='logs', params=params)

    if _logs:
        return _logs

    return None


def get_qrcode(coin, address, apikey, value='', size=300):
    if coin is None:
        return None

    params = {
        'address': address,
        'size': size,
        'apikey': apikey
    }

    if value:
        params = {
            'address': address,
            'size': size,
            'value': value,
            'apikey': apikey
        }

    _qrcode = process_request(coin, endpoint='qrcode', params=params)

    if _qrcode:
        return _qrcode

    return None


def get_conversion(origin, to, value, apikey):
    params = {
        'from': origin,
        'to': to,
        'value': value,
        'apikey': apikey
    }

    _value = process_request('', endpoint='convert', params=params)

    if _value:
        return _value

    return None


def get_estimate(coin, apikey):
    params = {
        'addresses': 1,  # Change this according your number of addresses
        'priority': 'default',  # Change this according the priority you want to define
        'apikey': apikey
    }

    _estimate = process_request(coin, endpoint='estimate', params=params)

    if _estimate:
        return _estimate

    return None


def get_address(coin, params):
    # Must provide API Key in the "params"
    _address = process_request(coin, endpoint='create', params=params)

    if _address:
        return _address

    return None


def process_request(coin='', endpoint='', params=None):
    if coin != '':
        coin += '/'

    response = requests.get(
        url="{base_url}{coin}{endpoint}/".format(
            base_url=BLOCKBEE_URL,
            coin=coin.replace('_', '/'),
            endpoint=endpoint,
        ),
        params=params,
        headers={'Host': BLOCKBEE_HOST},
    )

    url = response.url

    response = response.json()

    if endpoint == 'create':
        response['raw_request_url'] = url  # For debugging purposes

    return response
