import pytest
from unittest import TestCase
from unittest.mock import patch
import BTCtrans
import ETHtrans
import web3
from web3 import Web3, HTTPProvider, utils
# from BTCtrans import round_sig, create_transaction, failed_broadcast

from bit.network.services import NetworkAPI, BitpayAPI, InsightAPI
from bit.transaction import calc_txid
from bit import PrivateKeyTestnet
from bit.network.meta import Unspent
import requests
import traceback
from math import log10, floor

import random 
import time
from models import BTC, ETH
from ETHtrans import send_eth, construct_tx
from GenAddrs import btc_wallet, eth_wallet

#bitcoin variables
key = PrivateKeyTestnet('92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j')
url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
res = requests.get(url)
destination = ['mpqX5Dfy89zLrVFbo6JDkdH4NTcRKbFebK', 'mgYPRGum3A7Rsb2eP93vDGwyWjguRbK4ns']
destsamnts = []
BTCS = []
fee = 5

def mock_create_transaction(destination, destsamnts, key, fee=5):
    data = {'address': 'mnQCmXfohuwBKjXtSKoHbxcZmQmveCdXtk', 'txid': 'dbbfbf43d47b12913dff041e2770eec236b0aec7ea6df071f4f7a1fe0b1c6526', 'vout': 1, 'scriptPubKey': '76a9144b820d01817f597d072a333776f4d672499ed57388ac', 'amount': 4.59801327, 'satoshis': 459801327, 'confirmations': 0, 'ts': 1531728453}
    v = int(float(data['amount']) * (10**8))
    unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
    outputs = []
    for x in destination:
        amnt = 500
        amount = BTCtrans.round_sig((amnt/1000), 4) 
        outputs.append((x, amnt, 'mbtc'))
        destsamnts.append((x, amount))

    tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
    return tx

class TestBitcoin(TestCase):

    def test_round_sig():
        assert BTCtrans.round_sig(1234560, 4) == 1235000
        assert BTCtrans.round_sig(0.000456, 2) == 0.00046

    def test_create_transaction():
        assert mock_create_transaction(destination, destsamnts, key, fee=5) == '010000000126651c0bfea1f7f471f06deac7aeb036c2ee70271e04ff3d91127bd443bfbfdb010000008b48304502210086b9842ccb485378f3ef7a0627e8cbde4c2100258f6d677ef5b96259f467be2c022048c341b2d158ab61ef08ed62ca9a04f204b76cd4c07dbff898e1ae2792cf804e0141049b3249d74128dd68277a63c11cb09956dcc167904e8a6993779abaa416fbff22f5558d59c17aa836013b8a43c425aacfc19b96011cebc85fd1e7a7a390a23636ffffffff0380f0fa02000000001976a914663bfb4ddb23d714258cf9e7c868da5aade7a31e88ac80f0fa02000000001976a9140b3d83be5c38c473c2aefc14095284d0dc6555f288ac3b1c7215000000001976a9144b820d01817f597d072a333776f4d672499ed57388ac00000000'

    # def test_success_broadcast():
    #     BTCS = []
    #     txid = 'a6ba7075d42e8a3b6f40437c08e6c2480da522725dad4fdc482c5b4f49dfabe6'
    #     for x in range(len(destination)):
    #         BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))
    #     assert BTCS[-1].txid == 'a6ba7075d42e8a3b6f40437c08e6c2480da522725dad4fdc482c5b4f49dfabe6'

    def test_failed_broadcast():
        assert BTCtrans.failed_broadcast(11, ['mpqX5Dfy89zLrVFbo6JDkdH4NTcRKbFebK', 'mgYPRGum3A7Rsb2eP93vDGwyWjguRbK4ns'], [])
    
    @patch('BTCtrans.broadcast')
    def test_addtoBTCS(self, mock_broadcast):
        mock_broadcast.return_value = 12 #(<Response [200]>, [('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.9e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 4.33e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 3.53e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.83e-07), ('mpYCitAEcTYXr6ayqjvioxFngBW8MhM48U', 1.94e-07)], True)
        x = BTCtrans.addtoBTCS
        print(x)

# Ethereum Tests
class TestEthereum(TestCase):

    def test_construct_tx_happy_case():
        from_addr = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        val = '5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        nonce = '1'
        web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))
        response = construct_tx(from_addr, to_address, val, nonce, web3)
        expected_results = {'nonce': '1', 'chainId': 4, 'to': '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5', 'data': '', 'value': '5', 'gas': 24000, 'gasPrice': 1000000000}
        assert response == expected_results

    def test_construct_tx_failing_case():
        from_addr = '0xde055ecab590e0e7f2cb06445dd6272fb7d65129'
        to_address = '0x6f544455d57caA0787A5200da1fc379fc00b5da5'
        val = '5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        nonce = '1'
        web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))
        response = construct_tx(from_addr, to_address, val, nonce, web3)
        expected_results = False
        assert response == expected_results

# Address Generation Tests
class TestAddresses(TestCase):
    def test_btc_wallet_happy_case():
        btc_num = 5
        xpub = 'tpubDAK3K7sXsKqVs6XNCnBUZQVj2Yy5Sc98XV4Sy9xVfTcaGv8AGm4x585DUYpbBx61zURUoyFsJWAokuZY8Edm5PqJ9wza7i4pxVPKCttKjZH'
        response = btc_wallet(btc_num, xpub)
        expected_results =  ['mgDryTfWY7PBBV1DH8vkFr2KHMHduwzct4', 'mpYCitAEcTYXr6ayqjvioxFngBW8MhM48U', 'n2f8do8bCGtgQgkCv43efBsnvjV181x6a4', 'mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 'mzVu2YP4b67mJC5mfm3nbBYdQiCsBUXdtG']
        assert response == expected_results
    
    def test_btc_wallet_failing_case():
        btc_num = 5
        xpub = 'failDAK3K7sXsKqVs6XNCnBUZQVj2Yy5Sc98XV4Sy9xVfTcaGv8AGm4x585DUYpbBx61zURUoyFsJWAokuZY8Edm5PqJ9wza7i4pxVPKCttKjZH'
        try:
            btc_wallet(btc_num, xpub)
        except:
            return True
        raise AssertionError
    
    def test_eth_wallet_happy_case():
        eth_num = 5
        xpub = 'xpub6EPXZc2brBKKFUNH3bxcg17g5mi5Uo5YmHHe2j1dWqqzV5WEN8dQYWXSvFpXz1PNrW9G8de6qoPun3Eiz4qKmaLXmViVYEHmrXRF6JbQXUE'
        response = eth_wallet(eth_num, xpub)
        expected_results = ['0xbD6E27f76BC5590A511B7722ab9ae18bF1B0CCD2', '0xc7f5bf77C2306253bD36BF933a12C3B91e8EFDBA', '0xbBc8c60c155f041a82d86A1fbae075aBA333faCC', '0xa4Eaf144ED98D300cFD9a2484102C2292bF61911', '0x974c757595dB0Cb277a8916357cf73459112a487']
        assert response == expected_results
    
    def test_eth_wallet_failing_case():
        eth_num = 5
        xpub = 'fail6EPXZc2brBKKFUNH3bxcg17g5mi5Uo5YmHHe2j1dWqqzV5WEN8dQYWXSvFpXz1PNrW9G8de6qoPun3Eiz4qKmaLXmViVYEHmrXRF6JbQXUE'
        try:
            eth_wallet(eth_num, xpub)
        except:
            return True
        raise AssertionError
    
if __name__ == "__main__":
    # TestBitcoin.test_round_sig()
    # TestBitcoin.test_create_transaction()
    # TestBitcoin.test_failed_broadcast()
    # TestEthereum.test_construct_tx_happy_case()
    # TestEthereum.test_construct_tx_failing_case()
    # TestAddresses.test_btc_wallet_happy_case()
    # TestAddresses.test_btc_wallet_failing_case()
    # TestAddresses.test_eth_wallet_happy_case()
    # TestAddresses.test_eth_wallet_failing_case()