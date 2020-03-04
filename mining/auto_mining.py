import hashlib
import requests
import time
import sys
import json

from cpu import *
from miner import proof_of_work, valid_proof

sys.path.append('c:/Users/minhh/Documents/github/CS-Build-Week-2/traversal')
from visited import visited
from movement import moving_function, room_search
from api_key import Min_KEY

# Import visited for wise movement
# Traversal that uses DFS, to find path
# Store at room id 1
store = 1
# Name Changer at 467
name_change = 467
# Well at 55
well = 55
# Shrines at 461, 374
shrine1 = 461
shrine2 = 374
# Mine location (decoded coordinates as room id)
# Add power abilites (STRETCH)

node = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": Min_KEY}

def get_current_location():
    r = requests.get(url=node + "/adv/init", headers=headers)
    time.sleep(r.json()["cooldown"])
    starting_room = r.json()
    return starting_room

def examine_well():
    data = {"name": "well"}
    r = requests.post(url=node + "/adv/examine", json=data, headers=headers)
    time.sleep(r.json()["cooldown"])
    return r.json()["description"]

if __name__ == '__main__':
    # while True
    mined_coin = 0
    # get current location
    current_location_id = get_current_location()['room_id']
    while True:
        # go to the well
        print("current location: ",current_location_id)
        print("going to the well..........")
        room_search(visited, current_location_id, well)
        
        # examine the well, and get the clue
        print(f"looking for clue..........")
        clue = examine_well()[41:]
        print(clue)     
        # open ls8 file, and overwrite the clue on it
        f = open("mining/clue.ls8", "w")
        f.write(clue)
        f.close()
       
        # get the room id from ls8
        
        cpu = CPU()
        cpu.load()
        room = int("".join(cpu.run()[-3:]))
        print("Clue: room", room)
        # clean up the clue.ls8 file
        open("mining/clue.ls8", "w").close()

        # go to the room
        print(f"going to room {room}..........")
        room_search(visited, well, room)
        
        # start mining
        print("start mining.............")
        while True:
            node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
            headers = {"Authorization": Min_KEY}
            # Get the last proof from the server
            r = requests.get(url=node + "/last_proof", headers=headers)
            last_data = r.json()
            time.sleep(last_data["cooldown"])
            new_proof = proof_of_work(last_data['proof'], last_data['difficulty'])

            post_data = {"proof": new_proof}

            r = requests.post(url=node + "/mine", json=post_data, headers=headers)
            data = r.json()
            print(data)
            time.sleep(data["cooldown"])
            
            if 'messages' in data and 'New Block Forged' in data['messages']:
                mined_coin += 1
                print(f"Total Mined Coins in this time: {mined_coin}")
                current_location_id = room
                break
    

        
# while True

