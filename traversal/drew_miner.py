import hashlib
import requests

import sys
import json
from api_key import Andrew_KEY
from uuid import uuid4
import time
from timeit import default_timer as timer

import random


def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    
    #add 1 to proof if valid_proof false
    while valid_proof(last_proof, proof, difficulty) is False:
        proof +=1
    

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    # set guess to encoded proof
    guess = f'{last_proof}{proof}'.encode()
    # set guess_hash to hashed guess
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return when the last six of guess_hash = first six of last_hash
    
    if guess_hash[:difficulty] == '0'*difficulty:
        return True
    else:
        return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
        headers = {"Authorization": Andrew_KEY}

    coins_mined = 0

    # Load or create ID
    # f = open("my_id.txt", "r")
    # id = f.read()
    # print("ID is", id)
    # f.close()

    # if id == 'NONAME\n':
    #     print("ERROR: You must change your name in `my_id.txt`!")
    #     exit()
    # # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers=headers)
        
        print(f'R: {r}')
        data = r.json()
        time.sleep(data["cooldown"])
        print(f'Data: {data}')
        new_proof = proof_of_work(data['proof'], data['difficulty'] )

        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine",json=post_data, headers=headers)
        data = r.json()
        print(f'Data: {data}')
        time.sleep(data["cooldown"])
        # new_proof = proof_of_work(data['proof'])
        # if data.get('message') == 'New Block Forged':
        #     coins_mined += 1
        #     print("Total coins_mineds mined: " + str(coins_mined))
        # else:
        #     print(data.get('message'))