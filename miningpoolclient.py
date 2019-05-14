import hashlib
import requests

class MiningPoolClient(object):
    @classmethod
    def pool_mine(cls, pool_peer, address, header, target, nonces, special_min, debug=False):

        lowest = (0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 0, '')
        nonce = nonces[0]
        while nonce < nonces[1]:
            hash_test = hashlib.sha256(hashlib.sha256(header.format(nonce=nonce).encode('utf-8')).digest()).digest()[::-1].hex()

            text_int = int(hash_test, 16)
            if text_int < target or special_min:
                lowest = (text_int, nonce, hash_test)
                break

            if text_int < lowest[0]:
                lowest = (text_int, nonce, hash_test)
            nonce += 1
        nonce = lowest[1]
        lhash = lowest[2]

        if nonce and lhash or special_min:
            try:
                return requests.post("{pool}/pool-submit".format(pool=pool_peer), json={
                    'nonce': str(hex(nonce)[2:]),
                    'hash': lhash,
                    'address': address
                }, headers={'Connection':'close'}, verify=False)
            except Exception as e:
                if debug:
                    print(e)
