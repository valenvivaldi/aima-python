from search import *

class NQueensProblem(Problem):

    """The problem of placing N queens on an NxN board with none attacking
    each other.  A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet.  We fill in columns left to right.
    #>>> depth_first_tree_search(NQueensProblem(8))
    <Node (7, 3, 0, 2, 5, 1, 6, 4)>
    """

    def __init__(self, N, initial = None):
        self.N = N
        if initial == None:
            self.initial = tuple([0] * N)
        else:
            self.initial = initial
        Problem.__init__(self, self.initial)

    def actions(self, state):
        """Todos los posible movimientos de cada reina en la misma columna."""
        if  state == None:
            return []
        #print(state)
        actions = []
        for colum in range(self.N):
            for row in range(self.N):
       #         print("columna: {} fila: {} valor actual en columna: {}".format(colum, row, state[colum]))
                if state[colum] != row:
        #            print("valor agregado por distinto")
                    actions.append((colum, row))
        return actions


    def result(self, state, move):
        new = list(state[:])
        new[move[0]] = move[1]
        #print("SE MUEVE LA REINA EN LA COLUMNA {} DE LA FILA {} A LA FILA {}".format(move[0], state[move[0]], move[1]))
        return tuple(new) #PREGUNTAR PORQUE DEVUELVE UNA TUPLA!!!!!!!

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)   # same / diagonal

    def goal_test(self, state):
        return not any(self.conflicted(state, state[col], col) # no existe ningun conflicto... ver si hay que considerar algo mas
                       for col in range(len(state)))

    def h(self, state):
        """Return number of conflicting queens for a given node"""
        """number of pairs of queens that are attacking each other, either directly or indirectly"""
        num_conflicts = 0
        for (r1, c1) in enumerate(state):
            for (r2, c2) in enumerate(state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return num_conflicts

    def value(self, state):
        """number of pairs of queens that are attacking each other, either directly or indirectly"""
        return (-1 * (self.h(state)/2)) # se divide por dos xq tenes el par (x, y) y (y, x)...ver si esta bien... o (n*(n-1))/2


def generate_random_state(n):
    nState = []
    value = 0
    for x in range(n):
        value = random.randint(0, n-1) # busqueda local completa(todas las reinas)
        #print(value)
        nState.append(value)
    print("Generamos un estado aleatorio {}".format(nState))
    return nState

def generator(n, cant):
    # genera configuraciones(cant) de tablero de n-queens
    configs = []
    for nroConfig in range(cant):
        configs.append(generate_random_state(n))
    return configs

def hill_climbing_sideway_moves(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""
    sideway_moves = 10 # cantidad de movimientos tolerados hacia los lados(sin ir a un mejor estado, sino que igual)
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) < problem.value(current.state):
            break
        if problem.value(neighbor.state) == problem.value(current.state):
            if sideway_moves > 0:
                sideway_moves -= 1
            else:
                break
        current = neighbor
    return current.state




def hill_climbing_random_restart(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""
    restarts = 10 # cantidad de reinicios aleatorios al llegar a un estado inmejorable
    current = Node(problem.initial)
    best = current  #se lleva la cuenta del mejor estado hasta el momento
    while True:
        if problem.goal_test(current.state):
            break
        if (problem.value(current.state) > problem.value(best.state)):
            best = current

        neighbors = current.expand(problem)

        if neighbors:
            neighbor = argmax_random_tie(neighbors,key=lambda node: problem.value(node.state))
            if problem.value(neighbor.state)>problem.value(current.state):
                current=neighbor
            else:
                if restarts > 0:
                    restarts -= 1
                    current = Node(generate_random_state(problem.N))
                else:
                    break


        else:
            if restarts > 0:
                restarts -= 1
                current = Node(generate_random_state(problem.N))
            else:
                break
    return current.state

n = 8
#generate_state(n)

#eight_queens_problem = NQueensProblem(n, generate_state(n))
#hill_climbing(eight_queens_problem)
state = [2, 1, 2, 1,3,2,3,2]
#state = [2, 0, 2, 1]
print("PROBAMOS CON ESTADO INICIAL {}".format(state))

eight_queens_problem = NQueensProblem(8,state)

print("hill climbing")
solution = hill_climbing(eight_queens_problem)
print("solucion: {} con heuristica {}".format(solution,eight_queens_problem.value(solution)))
 # devuelve una state no un nodo , entonces no puedo ver el camino, sino al estado al cual llega




eight_queens_problem = NQueensProblem(8,state)

print("hill climbing con reinicios aleatorios")
solution = hill_climbing_random_restart(eight_queens_problem)
print("solucion: {} con heuristica {}".format(solution,eight_queens_problem.value(solution)))
