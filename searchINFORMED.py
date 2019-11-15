from search import *

romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))

romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))


class class_problem_romania(GraphProblem):
    def a(self):
        print("a")


romania_problem = class_problem_romania("Arad", "Bucharest", romania_map)

result = best_first_graph_search(romania_problem, romania_problem.h)

print(result.solution())
result = greedy_best_first_graph_search(romania_problem, romania_problem.h)
print(result.solution())


def astar_search_graph(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


result = astar_search_graph(romania_problem)
print(result.solution())

# romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)


# Heuristics for 8 Puzzle Problem
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def linear(node):
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])


def manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd


def sqrt_manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
        for j in range(2):
            mhd = (index_goal[i][j] - index_state[i][j]) ** 2 + mhd

    return math.sqrt(mhd)


def gaschnigRECURSIVE(state, num):
    liststate = [state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7], state[8]]
    #print("gaschnig de {}".format(liststate))
    result = 0
    #print("calculamos gaschnig de {}".format(liststate))
    while liststate != [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        # buscamos el indice donde esta el blanco
        indexOfBlank = 0
        while (indexOfBlank < 9) and (liststate[indexOfBlank] != 0):
            indexOfBlank += 1
     ##   print("El espacio vacio esta en la posicion {}".format(indexOfBlank))
        # buscamos la ficha que deberia estar donde esta el blanco
        indexOfWrong = 0
        if (indexOfBlank != 8):  # si el blanco esta en l
            while (indexOfWrong < 9) and (liststate[indexOfWrong] != indexOfBlank + 1):
                indexOfWrong += 1
       ##         print("La ficha {} esta en la posicion {}".format(liststate[indexOfWrong], indexOfWrong))
        else:
            while (indexOfWrong < 9) and (liststate[indexOfWrong] == indexOfWrong + 1):
                indexOfWrong += 1
         ##       print("La ficha {} esta en la posicion {}".format(liststate[indexOfWrong], indexOfWrong))
        # intercambio
        liststate[indexOfBlank] += liststate[indexOfWrong]
        liststate[indexOfWrong] -= liststate[indexOfBlank]
        ##print("Swapeamos!el elemento pos{} con el pos {} {}".format(indexOfBlank, indexOfWrong, liststate))
        result += 1
    #print(" es {}".format(result))
    return result


def gaschnig(node):
    state = node.state

    return gaschnigRECURSIVE(state, 0)


def max_heuristic(node):
    score1 = manhattan(node)
    score2 = gaschnig(node)
    return max(score1, score2)


puzzle = EightPuzzle( (6,1,4,8,3,2,0,7,5))

print("solvability? {}".format(puzzle.check_solvability(
    (6,1,4,8,3,2,0,7,5))))  # checks whether the initialized configuration is solvable or not

result = astar_search(puzzle, gaschnig)

print("con gaschin {}".format(result.solution()))

result = astar_search(puzzle, max_heuristic)

print("con maxxx {}".format(result.solution()))