from room import Room
from player import Player
from world import World

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Use a DFT Recrusive solution
def recrusive_graph_path(starting_room, already_visited=set()):
    # Create a set of traversed vertices
    visited = set()
    # Next if statement for in range of movement
    for rooms in already_visited:
        visited.add(rooms)
    path = []
    opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    def add_paths(rooms, backtrack=None):
        visited.add(rooms)
        # Call the function recrusively -- on rooms not visited 
        for direction in rooms.get_exits():
            # next room not in visited
            if rooms.get_room_in_direction(direction) not in visited:
                path.append(direction)
                add_paths(rooms.get_room_in_direction(direction), opposite_direction[direction])
        # Set Boolean equal to True
        if backtrack == path.append(backtrack):
            return
        # if a node has no unvisited neighbors (nodes), do nothing
        # essentially base case
    add_paths(starting_room)
    return path

def create_path(starting_room, visited=set()):
    # Store path
    path = []
    # Add opposite directions for backtracking 
    opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    def add_paths(rooms, backtrack=None):
        visited.add(rooms)
        # Add dictionary
        a_dict = {}
        for direction in rooms.get_exits():
            a_dict[direction] = len(recrusive_graph_path(rooms.get_room_in_direction(direction), visited))
        traversal_order = []
        # Use key as first built-in function that modifies a list in place while the latter accepts and return iterable.
        # Use inline function to take input x return x[1] which is the second element of x.
        # items() returns the list with all dictionary keys with values.
        # Return a new list containing all items from the iterable in ascending order.
        # A custom key function can be supplied to customize the sort order.
        for key, value in sorted(a_dict.items(), key=lambda variable: variable): traversal_order.append(key)
        # Traverse through the rooms
        for direction in traversal_order:
            if rooms.get_room_in_direction(direction) not in visited:
                path.append(direction)
                add_paths(rooms.get_room_in_direction(direction), opposite_direction[direction])
        # When going through the rooms, if you hit a dead end, move backtrack and continue forward
        if len(visited) == len(world.rooms):
            return
        else:
            path.append(backtrack)
    add_paths(starting_room)
    return path
traversal_path = create_path(world.starting_room)



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