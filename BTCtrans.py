from bit.network.services import NetworkAPI
from bit import PrivateKeyTestnet

import random 

ntwrk = NetworkAPI()
money = ntwrk.get_balance_testnet('myuUCjnJxRmCm6aC2gpmY2nyGGS29PApRx')
print(money) 
key = PrivateKeyTestnet('93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6')
print(key)
amount = float(random.randrange(1, 500))/100
print(amount)
dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
outputs = [(dest, amount, 'mbtc')]
unspents = ntwrk.get_unspent_testnet('myuUCjnJxRmCm6aC2gpmY2nyGGS29PApRx')
print("UNSPENTS: ", unspents)
tx = key.create_transaction(outputs, fee=8500, unspents=unspents)
print("TRANSACTION: ", tx)
# stx = ntwrk.broadcast_tx_testnet(tx)
# print("SUCCESS!")
# key.send(outputs, fee=8500, unspents=unspents)


# def get_unspent_testnet(cls, address)
# def broadcast_tx_testnet(cls, tx_hex)
# def create_transaction or send(self, outputs, fee=None, leftover=None, combine=True, message=None, unspents=None):