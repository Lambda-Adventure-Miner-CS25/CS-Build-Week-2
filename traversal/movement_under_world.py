import hashlib
import requests
import time
import sys
import json
from api_key import Min_KEY
from visited import visited
from under_world_visited import under_world_visited


# Import visited for wise movement 
# Traversal that uses DFS, to find path 
# Store at room id 1
store = 1
# Name Changer at 467
name_change = 467
# Well at 55 
well = 555

    # Mine location (decoded coordinates as room id)
# Add power abilites (STRETCH)

node = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": Min_KEY}

# def wise_map(visited):
#     # Get the current room information
#     r = requests.get(url=node + "/adv/init", headers=headers)
#     curr = r.json()
#     print(curr)
#     # Pass in the direction being moved
#     # Grab the room_id of room going into
#     # Run moving function

player_data = requests.post(url=node + "/adv/status", headers=headers)
player = player_data.json()

visited_map = under_world_visited

def sell(player):
    if len(player['inventory']) > 0:
        data = {"name":"treasure"}
        r = requests.post(url=node + "/adv/sell",
                            json=data, headers=headers)
        # Handle non-json response
        print("data", data)
        try:
            print("cooldown", r.json()["cooldown"])
            time.sleep(r.json()["cooldown"])
            data = {"name":"treasure", "confirm":"yes"}
            r = requests.post(url=node + "/adv/sell",
                            json=data, headers=headers)
            try:
                print("cooldown", r.json()["cooldown"])
                time.sleep(r.json()["cooldown"])
                data = {"name":"treasure", "confirm":"yes"}
                r = requests.post(url=node + "/adv/sell",
                                json=data, headers=headers)
            except ValueError:
                print("Error:  Non-json response")
                print("next_room_id Response returned:")
                print(r)
        except ValueError:
            print("Error:  Non-json response")
            print("next_room_id Response returned:")
            print(r)
            sell(player)
    else:
        print('No more to sell!')


def moving_function(traversal_path, rooms_id_list=None):
    print(rooms_id_list)
    room_list = []
    i = 0

    while i < len(traversal_path):
        direction = traversal_path[i]
        while i < len(traversal_path) and traversal_path[i] == direction:
            room_list.append(str(rooms_id_list[i]))
            i += 1
            
        next_rooms = ",".join(room_list)

        data = {"direction": direction,
                    "next_room_id": next_rooms}
        if len(room_list) == 1:
            node = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move"
            data = {"direction": direction,
                    "next_room_id": next_rooms}
        else:
            node = "https://lambda-treasure-hunt.herokuapp.com/api/adv/dash"
            data = {"direction": direction, "num_rooms": str(len(room_list)),
                    "next_room_ids": next_rooms}
        r = requests.post(url=node, json=data, headers=headers)
        # Handle non-json response
        try:
            print(data)
            print("cooldown:", r.json()["cooldown"])
            time.sleep(r.json()["cooldown"])
        except ValueError:
            print("Error:  Non-json response")
            print("next_room_id Response returned:")
            print(r)
        room_list = []


r = requests.get(url=node + "/adv/init", headers=headers)
time.sleep(r.json()["cooldown"])
starting_room = r.json()['room_id']


def room_search(visited_map, start, target):
    queue = []
    visited_rooms = set()
    # print("start", start)
    queue.append(start)
    rooms_id_list=[[]]
    paths = [[]]
    while len(queue) > 0:
        path = paths.pop(0)
        rooms_id = rooms_id_list.pop(0)
        last_room = queue.pop(0)

        if last_room == target:
            print("path", path)
            # print("last_room", last_room)
            return moving_function(path, rooms_id)

        else:
            if last_room not in visited_rooms:
                visited_rooms.add(last_room)
                for d in visited_map[last_room]:
                    if visited_map[last_room][d] not in visited_rooms:
                        new_path = path.copy()
                        new_path.append(d)
                        new_rooms_id = rooms_id.copy()
                        new_rooms_id.append(visited_map[last_room][d])
                        rooms_id_list.append(new_rooms_id)

                        paths.append(new_path)
                        queue.append(visited_map[last_room][d])
            else:
                pass


if __name__ == '__main__':

    room_search(visited_map, starting_room, 986)
    # sell(player)
