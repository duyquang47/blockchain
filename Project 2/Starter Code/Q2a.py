from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
Q2a_redeem_script = [
        OP_2DUP,
        OP_ADD,
        27,
        OP_EQUALVERIFY,
        OP_SUB,
        91,
        OP_EQUAL,
    ]

Q2a_txout_scriptPubKey = [
        OP_HASH160,
        Hash160(CScript(Q2a_redeem_script)),
        OP_EQUAL,
    ]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00020 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'ef207aab647564befec4ba738d75433ed8be29d8b59dc40201141fed24d1e283')
    utxo_index = 2 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
