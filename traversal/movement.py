import hashlib
import requests
import time
import sys
import json
from api_key import Ty_KEY
from visited import visited

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
headers = {"Authorization": Ty_KEY}

# def wise_map(visited):
#     # Get the current room information
#     r = requests.get(url=node + "/adv/init", headers=headers)
#     curr = r.json()
#     print(curr)
#     # Pass in the direction being moved
#     # Grab the room_id of room going into
#     # Run moving function


def moving_function(traversal_path, room_id=None):
    for i in traversal_path:
        # data = {"direction": i, "next_room_id": str(room_id)}
        data = {"direction": i}
        r = requests.post(url=node + "/adv/move",
                            json=data, headers=headers)
        # Handle non-json response
        print("data", data)
        try:
            result = r.json()
            print("cooldown", r.json()["cooldown"])
            time.sleep(r.json()["cooldown"])
        except ValueError:
            print("Error:  Non-json response")
            print("next_room_id Response returned:")
            print(r)

r = requests.get(url=node + "/adv/init", headers=headers)
starting_room = r.json()

def room_search(visited, starting_room, target):
    backwards = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    queue = []
    visited_rooms = set()
    start = starting_room['room_id']
    queue.append(start)
    paths = [[]]
    while len(queue) > 0:
        path = paths.pop(0)
        last_room = queue[-1]
        print(f'Path {paths}')           
        if last_room == target:
            print(path)
            return moving_function(path)
        else:
            if last_room not in visited_rooms:
                visited_rooms.add(last_room)
                connected_room = []
                for d in visited[str(last_room)]:
                    connected_room.append(d)
                    new_path = path.copy()
                    new_path.append(d)
                    paths.append(new_path)
                # print(f'Connected {connected_room}')
                for connection in connected_room:
                    # print(f'TESTING {visited[str(start)][connection]}')
                    # copy_path = list(path)
                    # copy_path.append(connection)
                    queue.append(visited[str(last_room)][connection])
            # else:
            #     last_move = backwards[path[-1]]
            #     queue.pop()
            #     new_path = path.copy()
            #     new_path.append(last_move)
            #     paths.append(new_path)
            # connected_room = []
            # for d in visited[str(last_room)]:
            #     connected_room.append(d)
            #     new_path = path.copy()
            #     new_path.append(d)
            #     paths.append(new_path)
            # for connection in connected_room:
            #     queue.append(visited[str(last_room)][connection])
            # print(path)
            # break

room_search(visited, starting_room, 98)
