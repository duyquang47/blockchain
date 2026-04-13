from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    alice_secret_key_BTC, bob_secret_key_BTC, alice_secret_key_BCY,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


cust1_private_key = alice_secret_key_BTC
cust1_public_key = cust1_private_key.pub
cust2_private_key = bob_secret_key_BTC
cust2_public_key = cust2_private_key.pub
cust3_private_key = alice_secret_key_BCY
cust3_public_key = cust3_private_key.pub


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 3

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

Q3a_redeem_script = [
    my_public_key,
    OP_CHECKSIGVERIFY,
    OP_1,
    cust1_public_key,
    cust2_public_key,
    cust3_public_key,
    OP_3,
    OP_CHECKMULTISIG,
]

Q3a_txout_scriptPubKey = [
    OP_HASH160,
    Hash160(CScript(Q3a_redeem_script)),
    OP_EQUAL,
]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00017 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'ef207aab647564befec4ba738d75433ed8be29d8b59dc40201141fed24d1e283')
    utxo_index = 3 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, 
        utxo_index, Q3a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
