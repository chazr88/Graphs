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

    '''
      10
     /
    1   2   4  11
     \ /   / \ /
      3   5   8
       \ / \   \
        6   7   9
    '''
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

def earliest_ancestor(ancestors, starting_node):
    #Transform the input into a graph
    graph = Graph()
    for pair in ancestors: #Pulling out each set from the list of sets.... (parent, child)
        parent = pair[0]# Grab parent
        child = pair[1]#Grab child
        #Make them both vertexes
        graph.add_vertex(parent)
        graph.add_vertex(child)
        #Build out the edge
        graph.add_edge(child, parent)#Adding the child then parent, allows us to tarverse backwards thru time... child to parent to find the ancestors
    #Do a BFS
    visited_neighbors = set()
    neighbors_to_visit = Queue()
    neighbors_to_visit.enqueue(#Storing path as dictionary 
        {
            'vertex': starting_node,
            'path_so_far': [starting_node]#Extra information for us to use when we need it
        }

    )
    #Here we store the longes path so far. If the code below never runs this will still be 1 so we start it at 1
    max_path_len = 1
    earliest_ancestor = -1 #If the input has no parents, the function should return -1
    while neighbors_to_visit.size() > 0:
        vertex_and_path = neighbors_to_visit.dequeue()
        current_vertex = vertex_and_path['vertex']
        current_path = vertex_and_path['path_so_far']
        #Check if visited
        if (current_vertex not in visited_neighbors):
            #Add to visited
            visited_neighbors.add(current_vertex)
            #Check if current path is longer than max path. If so update it
            #Also if its the same length as the longest one, if the ancestor has smaller ID, use it
            if ((len(current_path) >= max_path_len and current_vertex < earliest_ancestor) 
            or (len(current_path) > max_path_len)):
                earliest_ancestor = current_vertex
                max_path_len = len(current_path)

            for neighbor in graph.vertices[current_vertex]:
                path_copy = list(current_path)
                path_copy.append(neighbor)
                neighbors_to_visit.enqueue({
                    'vertex': neighbor,
                    'path_so_far': path_copy
                })
    return earliest_ancestor























    #First try
    # ancestors_to_visit = Stack()
    # ancestors_to_visit.push(starting_node)
    # # create a Set for visited_people
    # visited_people = set()
    # # while the ancestors_to_visit stack is not Empty:
    # while ancestors_to_visit.size() > 0:
    #     # pop the first vertex from the stack
    #     current_person = ancestors_to_visit.pop()
    #     # if its not been visited
    #     if current_person not in visited_people:
    #         # print the vertex
    #         print(current_person)
    #         # mark it as visited, (add it to visited_people)   
    #         visited_people.add(current_person)
    #         # add all unvisited neighbors to the stack
    #         for edges in ancestors:
    #             if current_person in edges:
    #                 if len(edges) > 1:
    #                     for p in edges:
    #                         if p != current_person:
    #                             ancestors_to_visit.push(p)
    # print(ancestors_to_visit)                
    #         # for person in ancestors:
    #         #     if person not in visited_people:
    #         #         ancestors_to_visit.push(person)
    #         # # for neighbor in get_neighbors(current_person):
    #         # #     if neighbor not in visited_people:
    #         # #         ancestors_to_visit.push(neighbor)

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 2)