from search import *


class Jarra(Problem):

    def __init__(self, initial):

        Problem.__init__(self, initial)

    def actions(self, state):
        result = []
        if (state[0] < 4):
            result.append("LlenarPrimera")
        if (state[1] < 3):
            result.append("LlenarSegunda")
        if (state[0] != 0):
            result.append("vaciarPrimera")
            if (state[1] < 3):
                result.append("VolcarPrimeraEnSegunda")
        if (state[1] != 0):
            result.append("vaciarSegunda")
            if (state[0] < 4):
                result.append("VolcarSegundaEnPrimera")
        return result

    def result(self, state, action):
        newa = state[0]
        newb = state[1]
        if (action == "LlenarPrimera"):
            newa = 4
        elif (action == "LlenarSegunda"):
            newb = 3
        elif (action == "vaciarPrimera"):
            newa = 0
        elif (action == "vaciarSegunda"):
            newb = 0
        elif (action == "VolcarPrimeraEnSegunda"):

            t = min(3 - newb, newa)
            newb += t
            newa -= t

        elif (action == "VolcarSegundaEnPrimera"):
            t = min(4 - newa, newb)
            newa += t
            newb -= t
        print("recibimos las jarras asi {} y la accion {} , las devolvemos asi {}".format(state, action, (newa, newb)))

        return (newa, newb)

    def goal_test(self, state):
        return state[0] == 2


if __name__ == "__main__":
    # print("Jarra")
    # jarraproblem = Jarra((0, 0))
    # #result = breadth_first_tree_search(jarraproblem)
    # #result = depth_limited_search(jarraproblem,6)
    # result = depth_limited_search(jarraproblem,200)
    # print(result.solution())
    # print("finish")

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

    initialcity = 'Arad'
    finalcity = 'Bucharest'
    romania_problem = GraphProblem(initialcity, finalcity, romania_map)


# print("El camino de {} a {} con depth first tree search es ".format(initialcity, finalcity))
#    result = breadth_first_graph_search(romania_problem)

# print(result.solution())
# print("El camino de {} a {} con depth first tree search es ".format(initialcity, finalcity))
#   result = uniform_cost_search(romania_problem)

#  print(result.solution())

class canibalesProblem(InstrumentedProblem):
    # state = (CanivalesLadoA,MisionerosLadoA,CanivaleLadoB,MisionerosLadoB)
    def __init__(self, initial):

        Problem.__init__(self, initial)
    def result(self, state, action):
        newa = state[0]
        newb = state[1]
        newc = state[2]
        newd = state[3]
        if action == "unoYunoA-B":
            newa += -1
            newb += -1
            newc += 1
            newd += 1
        if action == "unoYunoB-A":
            newa += 1
            newb += 1
            newc += -1
            newd += -1
        if action == "2canibalesA-B":
            newa += -2
            newc += 2
        if action == "2misionerosA-B":
            newb += -2
            newd += 2

        if action == "2canibalesB-A":
            newa += 2
            newc += -2

        if action == "2misionerosB-a":
            newb += 2
            newd += -2
        return(newa,newb,newc,newd)

    def invariant(self, state):
        if (state[0] > state[1] or state[2] > state[3]):
            return False
        return True

    def actions(self, state):
        possibleactions = []
        if (state[0] > 0 and state[1] > 0 and self.invariant(self.result(state,"unoYunoA-B"))):
            possibleactions.append("unoYunoA-B")

        if (state[0] > 1 and self.invariant(self.result(state,"2canibalesA-B"))):
            possibleactions.append("2canibalesA-B")

        if (state[1] > 1 and self.invariant(self.result(state,"2misionerosA-B"))):
            possibleactions.append("2misionerosA-B")

        if (state[2] > 0 and state[3] > 0 and self.invariant(self.result(state,"unoYunoB-A"))):
            possibleactions.append("unoYunoB-A")
        if (state[2] > 1 and self.invariant(self.result(state,"2canibalesB-A"))):
            possibleactions.append("2canibalesB-A")
        if (state[3] > 1 and self.invariant(self.result(state,"2misionerosB-A"))):
            possibleactions.append("2misionerosB-A")
        print("las posibles acciones para {} son: {}".format(state,possibleactions))
        return possibleactions



    def goal_test(self, state):
        if state[2] == 3 and state[3] == 3:
            return True
        return False


canibal = canibalesProblem((3, 3, 0,0))
result=breadth_first_tree_search(canibal)
print(result.solution())
#compare_searchers([canibal], "problema de los canibales")
