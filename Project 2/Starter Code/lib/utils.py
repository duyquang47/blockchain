import requests

from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

def send_from_custom_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin = create_txin(txid_to_spend, utxo_index)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)
    return broadcast_transaction(new_tx, network)

def create_txin(txid, utxo_index):
    return CMutableTxIn(COutPoint(lx(txid), utxo_index))

def create_txout(amount, scriptPubKey):
    return CMutableTxOut(amount*COIN, CScript(scriptPubKey))

def create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_signed_transaction(txin, txout, txin_scriptPubKey,
                              txin_scriptSig):
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def broadcast_transaction(tx, network):
    if network == 'btc-test3':
        # BlockCypher btc/test3 may not track the same active testnet chain.
        # Use mempool's testnet endpoint to broadcast raw tx hex directly.
        url = 'https://mempool.space/testnet/api/tx'
    elif network == 'bcy-test':
        url = 'https://api.blockcypher.com/v1/bcy/test/txs/push'
    else:
      raise InvalidArgumentException("Network must be one of either 'btc-test3', 'bcy-test'")

    raw_transaction = b2x(tx.serialize())
    if network == 'btc-test3':
        headers = {'content-type': 'text/plain'}
        return requests.post(url, headers=headers, data=raw_transaction)

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return requests.post(
        url,
        headers=headers,
        data='{"tx": "%s"}' % raw_transaction)
