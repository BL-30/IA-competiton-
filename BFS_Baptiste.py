# %%
"""
<h1><b><center>How to use this file with PyRat?</center></b></h1>
"""

# %%
"""
Google Colab provides an efficient environment for writing codes collaboratively with your group. For us, teachers, it allows to come and see your advancement from time to time, and help you solve some bugs if needed.

The PyRat software is a complex environment that takes as an input an AI file (as this file). It requires some resources as well as a few Python libraries, so we have installed it on a virtual machine for you.

PyRat is a local program, and Google Colab is a distant tool. Therefore, we need to indicate the PyRat software where to get your code! In order to submit your program to PyRat, you should follow the following steps:

1.   In this notebook, click on *Share* (top right corner of the navigator). Then, change sharing method to *Anyone with the link*, and copy the sharing link;
2.   On the machine where the PyRat software is installed, start a terminal and navigate to your PyRat directory;
3.   Run the command `python ./pyrat.py --rat "<link>" <options>`, where `<link>` is the share link copied in step 1. (put it between quotes), and `<options>` are other PyRat options you may need.
"""

# %%
"""
<h1><b><center>Pre-defined constants</center></b></h1>
"""

# %%
"""
A PyRat program should -- at each turn -- decide in which direction to move. This is done in the `turn` function later in this document, which should return one of the following constants:
"""

# %%
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

# %%
"""
<h1><b><center>Your coding area</center></b></h1>
"""

# %%
"""
Please put your functions, imports, constants, etc. between this text and the PyRat functions below. You can add as many code cells as you want, we just ask that you keep things organized (one function per cell, commented, etc.), so that it is easier for the teachers to help you debug your code!
"""

# %%
def create_structure():
  return []

# %%
def push_to_structure (structure, element) :
  structure.append(element)


# %%
def pop_from_structure (structure) :
  ## supprime le premier élément de la liste et le renvoit (création d'une file)
  sauv = structure[0]
  del structure[0]
  return sauv
  

# %%
def neighbors(graph, current_vertex): 
  ## renvoit tous les voisins d'un certain sommet
  neighbors = [] ## contient des couples (voisin, parent)
  for voisin in graph[current_vertex]:
    neighbors.append((voisin,current_vertex))
  return neighbors
  

# %%
def traversal (start_vertex, graph):
  ## create a spaning tree of the graph and return its routing table

  structure = create_structure() # Contient les couples (enfant,parent)
  push_to_structure(structure,(start_vertex,None)) #Initiatisation de la file
  explored_vertices = [] #liste contenant les sommets dejà explorés
  routing_table = {}

  while len(structure) > 0 :
    (current_vertex,parent) = pop_from_structure(structure)

    if current_vertex not in explored_vertices:
       explored_vertices.append(current_vertex)
       routing_table[current_vertex] = parent #On complète la table de routage en liant un enfant à un parent

       for couple_voisin_parent in neighbors(graph, current_vertex): #On passe en revu les voisins du sommet considéré

          if couple_voisin_parent[0] not in explored_vertices : ##On va traiter les sommets qui n'ont pas encore étés traités, qui sont donc les enfants 
            push_to_structure(structure, couple_voisin_parent)
        
  return routing_table



# %%
def find_route(routing_table, source_location, target_location): 
  #permet de renvoyer un chemin liant deux sommets grâce à une table de routage
  route = [target_location]
  current_location = target_location
  while current_location != source_location:
    route.append(routing_table[current_location]) ##on rajoute le parent de current_location au chemin
    current_location = routing_table[current_location]
  route.reverse()
  del route[0] ##afin que le rat ne bouge pas sur place 
  return route
  
  

# %%
list_of_moves = [] ##donne les sommets par où le rat doit passer

# %%
def find_list_of_moves(locations,pieces_of_cheese,player_location,BFS) : 
  #remplit la list_of_moves en prenant en compte la situation du rat et la position du fromage
  global list_of_moves
  target_location = pieces_of_cheese[0]
  source_location = player_location
  list_of_moves = find_route(BFS,source_location,target_location)



# %%
def move_from_locations (source_location, target_location) :
  #renvoit le mouvement que doit faire le rat pour aller à une case voisine
    difference = (target_location[0] - source_location[0], target_location[1] - source_location[1])
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        raise Exception("Impossible move")

# %%
def rat_movement(player_location):
  ##Lit la list_of_moves et la traduit en mouvements pour le rat
  global list_of_moves
  next_location = list_of_moves.pop(0)
  return move_from_locations(player_location,next_location)

# %%
"""
<h1><b><center>PyRat functions</center></b></h1>
"""

# %%
"""
The `preprocessing` function is called at the very start of a game. It is attributed a longer time compared to `turn`, which allows you to perform intensive computations. If you store the results of these computations into **global** variables, you will be able to reuse them in the `turn` function.

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][0, 1)]`.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The initial location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The initial location of your opponent's character in the maze.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The initial location of all pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take for preprocessing before the game starts checking for moves.

*Output:*
*   This function does not output anything.
"""

# %%
def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    
    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program
    BFS = traversal(player_location,maze_map)
    find_list_of_moves(maze_map,pieces_of_cheese,player_location,BFS)
    

    print("maze_map", type(maze_map), maze_map)
    print("maze_width", type(maze_width), maze_width)
    print("maze_height", type(maze_height), maze_height)
    print("player_location", type(player_location), player_location)
    print("opponent_location", type(opponent_location), opponent_location)
    print("pieces_of_cheese", type(pieces_of_cheese), pieces_of_cheese)
    print("time_allowed", type(time_allowed), time_allowed)


# %%
"""
The `turn` function is called each time the game is waiting
for the player to make a decision (*i.e.*, to return a move among those defined above).

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze. It is the same as in the `preprocessing` function, just given here again for convenience.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The current location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The current location of your opponent's character in the maze.
*   `player_score` -- **float** -- Your current score.
*   `opponent_score` -- **float** -- The opponent's current score.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The location of remaining pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take to return a move to apply before another time starts automatically.

*Output:*
*   A chosen move among `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT` or `MOVE_RIGHT`.
"""

# %%

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    return rat_movement(player_location)