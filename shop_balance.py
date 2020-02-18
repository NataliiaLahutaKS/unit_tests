import uuid
import hashlib
import unittest
import requests
import datetime

import config

now = datetime.datetime.now ()
class PiastrixTest(unittest.TestCase):

    def test_shop_balance(self):
        piastrix_api = PiastrixAPIClient(config.SECRET, config.URL)
        endpoint = 'shop_balance'
        data = {
            'now': now.strftime('%Y-%m-%d-%H:%M:%S'),
            'shop_id': config.SHOP_ID,
        }
        keys = sorted(['now', 'shop_id'])
        resp = piastrix_api.send_request(endpoint, data, 'POST', keys)

        print(resp.text)

        self.assertTrue(resp.status_code, 200)


class PiastrixAPIClient:
    def __init__(self, secret, url):
        self._secret = secret
        self._url = url

    def _request(self, url, data, method='POST'):
        if method == 'GET':
            resp = requests.get(url, json=data)
        else:
            resp = requests.post(url, json=data)

        return resp

    def send_request(self, endpoint, data, method, keys):
        data_signed = self._sign_request(data, keys)
        url = self._url + endpoint
        resp = self._request(url, data_signed, method)

        return resp

    def _sign_request(self, data, keys):
        values = [str(data[k]) for k in sorted(keys)]
        string_to_encode = ':'.join(values) + self._secret
        data['sign'] = hashlib.sha256(str(string_to_encode).encode('utf-8')).hexdigest()
        return data
