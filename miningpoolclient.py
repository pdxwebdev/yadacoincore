import hashlib
import requests

class MiningPoolClient(object):
    @classmethod
    def pool_mine(cls, pool_peer, address, header, target, nonces, special_min):

        lowest = (0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 0, '')
        nonce = nonces[0]
        while nonce < nonces[1]:
            hash_test = hashlib.sha256(hashlib.sha256(header.format(nonce=nonce).encode('utf-8')).digest()).digest()[::-1].hex()

            text_int = int(hash_test, 16)
            if text_int < target or special_min:
                break

            if text_int < lowest[0]:
                lowest = (text_int, nonce, hash_test)
            nonce += 1
        nonce = lowest[1]
        lhash = lowest[2]

        if nonce and lhash:
            try:
                requests.post("http://{pool}/pool-submit".format(pool=pool_peer), json={
                    'nonce': nonce,
                    'hash': lhash,
                    'address': address
                }, headers={'Connection':'close'})
            except Exception as e:
                print (e)