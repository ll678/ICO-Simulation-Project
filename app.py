from flask import Flask, render_template
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets
import os
import json
import socket  
import random
import mysql.connector
import time
from math import log10, floor
from models import BTC, ETH

app = Flask(__name__)

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)
    
def btctrans(dest):
    try: 
        amnt = float(random.randrange(1, 500))/100
        #dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        amount = round_sig((amnt/1000), 4) 
        fee = 8000
        tx = BTC_process(dest, '93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', fee, amnt)
        btx = tx[-1]
        btcfl = ""
        #print(btx)
        return BTC(dest, amount, btx)
    except:
        tx = "unable to make transaction"
        amount = "N/A"
        dest = "unable to make transaction"
        btcfl = "(Failed)"
        raise

def ethtrans(to_address):
    try:
        val = random.randint(10000, 10000000)
        ethamount = round_sig((val / (10**18)), 4)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        #to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key)
        ethfl = ''
        #print(ethtx)
        return ETH(to_address, ethamount, ethtx)
    except:
        ethtx = "unable to make transaction"
        val = "unable to make transaction"
        to_address = "unable to make transaction"
        ethfl = "(Failed)"

@app.route("/")
def hello():
    # try:
    #     visits = redis.incr("counter")
    # except RedisError:
    #     visits = "<i>cannot connect to Redis, counter disabled</i>"
    try:
        wallets = full_wallets(4, 4)
        btcs = wallets[0]
        eths = wallets[1]
    except:
        btcs = []
        eths = []

    print(btcs)
    print(eths)
    btc_trans = []
    eth_trans = []

    for address in btcs:
        print(address)
        trans = btctrans(address)
        btc_trans.append(trans)
        time.sleep(60)
    
    print(btc_trans)

    for address in eths:
        print(address)
        trans = ethtrans(address)
        eth_trans.append(trans)
        time.sleep(60)

    print(eth_trans)

# def connect():
#     config = {
#             'user': 'root',
#             'password': 'HorcruX8!',
#             'host': 'localhost',
#             'port': '3306',
#             'database': 'BROVIS'
#         }
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO bitcoin "
#                    "(name, mission) "
#                    "VALUES ('B-style', 'Brovis')")
#     connection.commit()
#     cursor.execute('SELECT name, mission FROM charity')
#     results = [{name: mission} for (name, mission) in cursor]
#     cursor.close()
#     connection.close()
#     print(results)

    #data = 'Hello World'
    #connect()
    #return json.dumps({'data': connect()})
    #return render_template('home.html',hostname=socket.gethostname(), btcs=btcs, eths=eths, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)

#Testing
    

    return render_template('home.html', hostname=socket.gethostname(), btcs=btcs, eths=eths, btc_trans=btc_trans, eth_trans=eth_trans)
    # return html.format(hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # pk=pk, ad=ad, sk=sk, Bpk=Bpk, Bsk=Bsk, Badd=Badd,
    #return render_template('home.html', data=data)

if __name__ == "__main__":
  #hello()
   app.run(host='0.0.0.0', port=80)