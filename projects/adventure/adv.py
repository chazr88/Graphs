from room import Room
from player import Player
from world import World

import random
from random import randrange
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

#Grabbed graph from previous project as it is needed to graph the data we are given   
class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist!")

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#Graph the directions for current room
graph = Graph()


#Going to use this to store the dict of {room.id{direction:next_room.id}}
room_and_exits = {}
#This will be used to backtrack for dead ends. 
back_steps = Stack()
#Dict that gives you the opposite direction. 
reverse_direction = {'n':'s', 's':'n', 'w':'e', 'e':'w'}


#Builds the dict for the exits...{'n':'?', 's':'?'}
def dict_of_exits():
    #Get all exits for current room
    exits = player.current_room.get_exits()
    exit_list = {}
    for each_exit in exits:
        exit_list.update({
            each_exit: "?"
        })
    return exit_list

#Goes thru the exit_list and looks for '?'. If it finds one, it returns that direction. If not it returns None
def get_next_direction(exit_list, curr_room):
    for direction, room_id in exit_list.items():#Loop through exit list
        next_room = curr_room.get_room_in_direction(direction)
        if room_id == "?" and next_room.id not in room_and_exits:#When the loop comes to a direction with "?" as value, return that direction
            return direction
    return None


def explore_maze():
    count = 0
    while len(room_and_exits) < len(world.rooms) and count < 2000:#Runs until all rooms explorex, or count reaches 2000
        curr_room = player.current_room#Get current room
        if curr_room.id not in room_and_exits:#Adds the id of the current room to the dict
            exit_list = dict_of_exits()
            room_and_exits[curr_room.id] = exit_list
        next_direction = get_next_direction(room_and_exits[curr_room.id], curr_room)
        #If we reach a dead, end this pops a direction off the back_steps stack so we can go back to that room and run the scripts on it again
        if next_direction == None:
                direction = back_steps.pop()#Pop a previous (opposite) direction off the stack
                traversal_path.append(direction)#Add direction to traversal_path
                player.travel(direction)#Make player go that direction
                count += 1
        #If we are given a next direction from get_next_direction do stuff....
        else:
            next_room = curr_room.get_room_in_direction(next_direction)#Grab info about room in next_direction
            room_and_exits[curr_room.id][next_direction] = next_room.id#Add next_room.id to the room_and_exits dict for that next_direction
            back_steps.push(reverse_direction[next_direction])#Push this next_direction with reverse_direction dict to reverse it into the back_steps Stack.
            traversal_path.append(next_direction)#Add next_direction to the traversal_path
            player.travel(next_direction)#Move player to the next_direction
            count += 1



explore = explore_maze()


#Get room in direction
# get_room_in_direction

# #Grab current room

# #Store visited rooms
# print(player.current_room.id)
# rooms_to_visit = Queue()
# visited_rooms = set()
# previous_room = None
# rooms_to_visit.enqueue({curr_room: exit_list})
# #Loop until all rooms are visited
# while len(visited_rooms) != len(room_graph):
#     if curr_room not in graph.vertices:
#         graph.add_vertex(curr_room)
#         current_path = rooms_to_visit.dequeue() 
#         current_vertex = current_path[-1]
#     for i in exit_list:#Loop through exit list
#         while '?' in exit_list[i]:#If there is '?' as a exit_list {'n':'?'}
#             visited_rooms.push({curr_room:exit_list})
#             previous_room = curr_room
#             previous_exit_taken = exit_list[i]#Storing so I can update ?
#             copy_of_direction_taken = i#If i went N save that
#             player.travel(i)
#             previous_exit_taken = player.current_room.id
#             curr_room = player.current_room.id
            
            






        






# print(exit_list)
# print(room_map)







# traversal_path.append(direction)

# #If you can go in a direction, go that way and get all its exits
# rooms_to_visit = Queue()
# visited_rooms = {}
# rooms_to_visit.enqueue([player.current_room])
# while rooms_to_visit.size() > 0:
#     current_path = rooms_to_visit.dequeue()
#     current_room = current_path[-1]
#     if current_room not in visited_rooms:
#         for next_direction in exits:
#             visited_rooms[current_room] = [current_path: next_direction]
#             new_path = list(current_path)
#             new_path.append(next_direction)
#             rooms_to_visit.enqueue(new_path)

        





# for exit in exits:
    
#     traversal_path.append(exit)

# TRAVERSAL TEST
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
