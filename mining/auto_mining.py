
import hashlib
import requests
import time
import sys
import json
import os
from cpu import *
from miner import proof_of_work, valid_proof

sys.path.append('c:/Users/minhh/Documents/github/CS-Build-Week-2/traversal')
from visited import visited
from under_world_visited import under_world_visited
from movement import moving_function, room_search
from api_key import Min_KEY

# Import visited for wise movement
# Traversal that uses DFS, to find path
# Store at room id 1
store = 1
# Name Changer at 467
name_change = 467
# Well at 55
well = 555
# Shrines at 461, 374
shrine1 = 461
shrine2 = 374
# Mine location (decoded coordinates as room id)
# Add power abilites (STRETCH)

node = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": Min_KEY}

def get_current_location():
    node = "https://lambda-treasure-hunt.herokuapp.com/api"
    headers = {"Authorization": Min_KEY}
    r = requests.get(url=node + "/adv/init", headers=headers)
    try:
        print(r.json())
        print("cooldown:", r.json()["cooldown"])
        time.sleep(r.json()["cooldown"])
        return r.json()['room_id']
    except ValueError:
        print("Error:  Non-json response")
        print("next_room_id Response returned:")
        print(r)
    
    
    
    

def examine_well():
    node = "https://lambda-treasure-hunt.herokuapp.com/api"
    headers = {"Authorization": Min_KEY}
    while True:
        data = {"name": "Well"}
        r = requests.post(url=node + "/adv/examine", json=data, headers=headers)
        try:
            print(r.json())
            print("cooldown:", r.json()["cooldown"])
            time.sleep(r.json()["cooldown"])
            if len(r.json()["errors"]) == 0:
                return r.json()["description"]
        except ValueError:
            print("Error:  Non-json response")
            print("next_room_id Response returned:")
            print(r)
        

if __name__ == '__main__':
    # while True
    mined_coin = 0
    # get current location
    
    n=0
    while n < 1000:
        current_location_id = get_current_location()
        # go to the well
        print("current location: ",current_location_id)
        print("going to the well..........")
        room_search(under_world_visited, current_location_id, well)
        
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

        # go to the room
        print(f"going to room {room}..........")
        room_search(under_world_visited, well, room)
        
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
            if 'errors' in data and 'There is no coin here: +100s' in data['errors']:
                break
            if 'messages' in data and 'New Block Forged' in data['messages']:
                mined_coin += 1
                print(f"Total Mined Coins in this time: {mined_coin}")
                n += 1
                break
    

        
# while True

