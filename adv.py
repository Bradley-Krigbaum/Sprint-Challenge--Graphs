from room import Room
from player import Player
from world import World
from collections import deque

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

############################
###   START OF MY CODE   ###
############################

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

not_visited = set()

def path_traversal(player):
    # standard setup
    visited = set()
    queue = deque()
    queue.append([('s', player.current_room.id)]) # adding 's' as a direction

    # standard while loop setup
    while len(queue) > 0:
        curr_path = queue.popleft()
        current_room = curr_path[-1]
        if player.current_room not in visited:
            visited.add(player.current_room.id)

        # like get_neighbor
        # if a direction in the current room exists
        for direction in world.rooms[current_room[1]].get_exits():
            # get rooms direction
            room_direction = world.rooms[current_room[1]].get_room_in_direction(direction)
            # if the rooms direction has not been visited, then add it to the current path and return
            if room_direction not in not_visited:
                curr_path.append((direction, room_direction.id))
                print("current path: ", curr_path)
                return curr_path
            # if the rooms directions id is not in visited
            # then set a new path
            # append the directions id
            # add it to the visited set
            # append the new path to the queue
            if room_direction.id not in visited:
                new_room = room_direction
                new_path = curr_path.copy()
                new_path.append((direction, new_room.id))
                visited.add(new_room.id)
                queue.append(new_path)

# path traversal function
def travel(path):

    # for the index of the paths item
    for i in range(1, len(path)):
        # set direction to path[paths index][first item is the direction]
        direction = path[i][0]
        # tell the player to travel in the direction
        player.travel(direction)
        # append the direction to the traversal path
        traversal_path.append(direction)
    # add the players current room to the not visited set
    not_visited.add(player.current_room)

# while loop to keep the player moving
while len(not_visited) != len(room_graph):
    travel(path_traversal(player))

###########################
####   END OF MY CODE   ###
###########################

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
