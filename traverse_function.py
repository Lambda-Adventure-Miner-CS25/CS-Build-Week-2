import hashlib
import requests
import time
import sys
import json


if __name__ == '__main__':
    # The server address
    node = "https://lambda-treasure-hunt.herokuapp.com/api"
    headers = {"Authorization": "Token 926411256868a26f67393e2aad26dbaef6fc0bb6"}

    def moving_function(direction, room_id=None):
        if room_id is None:
            data = {"direction": direction}
            r = requests.post(url=node + "/adv/move",
                              json=data, headers=headers)
            # Handle non-json response
            try:
                result = r.json()
                print("cooldown", r.json()["cooldown"])
                time.sleep(r.json()["cooldown"])
                return result
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(r)

        else:
            data = {"direction": direction, "next_room_id": str(room_id)}
            r = requests.post(url=node + "/adv/move",
                              json=data, headers=headers)
            # Handle non-json response
            print("data", data)
            try:
                result = r.json()
                print("cooldown", r.json()["cooldown"])
                time.sleep(r.json()["cooldown"])
                return result
            except ValueError:
                print("Error:  Non-json response")
                print("next_room_id Response returned:")
                print(r)

    def pick_up_function(treasure):
        data = {"name": treasure}
        r = requests.post(url=node + "/adv/take", json=data, headers=headers)
        # Handle non-json response
        try:
            result = r.json()
            time.sleep(r.json()["cooldown"])
            return result
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)

    def get_player_status_function():
        r = requests.post(url=node + "/adv/status", headers=headers)
        # Handle non-json response
        try:
            result = r.json()
            time.sleep(r.json()["cooldown"])
            return result
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)

    r = requests.get(url=node + "/adv/init", headers=headers)
    # Handle non-json response
    try:
        starting_room = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    cooldown = starting_room["cooldown"]
    print("cooldown ", cooldown)
    time.sleep(cooldown)

    # get player status
    player = get_player_status_function()
    print("player status", player)

    # Create an empty stack
    stack = []
    # Add the starting room to the stack
    stack.append(starting_room)
    print("start", stack)
    # Create an empty dict to store visited nodes
    visited = dict()
    while len(stack) > 0:
        # pop, the first room
        room = stack.pop()
        # Check if it's been visited
        # If it has not been visited...
        if room["room_id"] not in visited:
            # Mark it as visited
            print("stack", room["room_id"])
            print("room visited", len(visited))
            visited[room["room_id"]] = dict()

            for d in room["exits"]:
                visited[room["room_id"]][d] = "?"

        # if there is items in the room, take up item
        if len(room["items"]) > 0:

            for t in room["items"]:
                pick_up_function(t)
                print(f"picked up {t}")
                player["encumbrance"] += 1
            if player["encumbrance"] >= player["strength"]:
                print("Stop! your inventory is full, go to the store")
                break

        # check if its neighbors have been visited
        # if not, go to one of the directions
        if "w" in visited[room["room_id"]] and visited[room["room_id"]]["w"] == "?":
            room_w_to = moving_function("w")

            stack.append(room_w_to)
            visited[room["room_id"]]["w"] = room_w_to["room_id"]
            if room_w_to["room_id"] not in visited:
                # Mark it as visited
                print("room visited", len(visited))

                visited[room_w_to["room_id"]] = dict()
                for d in room_w_to["exits"]:
                    visited[room_w_to["room_id"]][d] = "?"
                visited[room_w_to["room_id"]]["e"] = room["room_id"]
            else:
                visited[room_w_to["room_id"]]["e"] = room["room_id"]

        elif "e" in visited[room["room_id"]] and visited[room["room_id"]]["e"] == "?":
            room_e_to = moving_function("e")

            stack.append(room_e_to)
            visited[room["room_id"]]["e"] = room_e_to["room_id"]
            if room_e_to["room_id"] not in visited:
                # Mark it as visited
                print("room visited", len(visited))
                visited[room_e_to["room_id"]] = dict()
                for d in room_e_to["exits"]:
                    visited[room_e_to["room_id"]][d] = "?"
                visited[room_e_to["room_id"]]["w"] = room["room_id"]
            else:
                visited[room_e_to["room_id"]]["w"] = room["room_id"]

        elif "n" in visited[room["room_id"]] and visited[room["room_id"]]["n"] == "?":
            room_n_to = moving_function("n")

            stack.append(room_n_to)
            visited[room["room_id"]]["n"] = room_n_to["room_id"]
            if room_n_to["room_id"] not in visited:
                # Mark it as visited
                print("room visited", len(visited))
                visited[room_n_to["room_id"]] = dict()
                for d in room_n_to["exits"]:
                    visited[room_n_to["room_id"]][d] = "?"
                visited[room_n_to["room_id"]]["s"] = room["room_id"]
            else:
                visited[room_n_to["room_id"]]["s"] = room["room_id"]

        elif "s" in visited[room["room_id"]] and visited[room["room_id"]]["s"] == "?":
            room_s_to = moving_function("s")

            stack.append(room_s_to)
            visited[room["room_id"]]["s"] = room_s_to["room_id"]
            if room_s_to["room_id"] not in visited:
                # Mark it as visited
                print("room visited", len(visited))
                visited[room_s_to["room_id"]] = dict()
                for d in room_s_to["exits"]:
                    visited[room_s_to["room_id"]][d] = "?"
                visited[room_s_to["room_id"]]["n"] = room["room_id"]
            else:
                visited[room_s_to["room_id"]]["n"] = room["room_id"]

        elif len(visited) == 500:
            print(visited)
            break

        else:
            # if all neighbors have been visited, use bfs to find the first room that has explored neighbor
            # dfs
            # Create an empty queue
            queue = []
            paths = []
            for d in room["exits"]:
                    paths.append([d])
                    queue.append(visited[room["room_id"]][d])
            # While the stack is not empty...
            while len(queue) > 0:
                # pop, the first room
                room_id = queue.pop(0)
                path = paths.pop(0)

                # check this visited_room to see if it has unexplored neighbor
                if ("s" in visited[room_id] and visited[room_id]["s"] == "?") or ("n" in visited[room_id] and visited[room_id]["n"] == "?") or ("w" in visited[room_id] and visited[room_id]["w"] == "?") or ("e" in visited[room_id] and visited[room_id]["e"] == "?"):
                    print("queue", room_id)
                    queue.clear()
                    current_room = room
                    for p in path:
                        new_room = moving_function(
                            p, visited[current_room["room_id"]][p])
                        current_room = new_room

                    stack.append(current_room)
                else:
                    # add neighbor to the queue
                    if "s" in visited[room_id]:
                        new_path = path.copy()
                        new_path.append("s")
                        paths.append(new_path)
                        queue.append(visited[room_id]["s"])
                    if "n" in visited[room_id]:
                        new_path = path.copy()
                        new_path.append("n")
                        paths.append(new_path)
                        queue.append(visited[room_id]["n"])
                    if "w" in visited[room_id]:
                        new_path = path.copy()
                        new_path.append("w")
                        paths.append(new_path)
                        queue.append(visited[room_id]["w"])
                    if "e" in visited[room_id]:
                        new_path = path.copy()
                        new_path.append("e")
                        paths.append(new_path)
                        queue.append(visited[room_id]["e"])
