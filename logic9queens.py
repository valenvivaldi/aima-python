from logic import *


def ninequeens(n):
    clauses = []
    # clausulas para asegurar que haya por lo menos una ficha en cada columna

    for i in range(0, n):
        casillas = []  # hacemos una lista de las casillas

        for j in range(0, n):
            casillas.append(expr("C{}{}".format(i, j)))
        clauses.append(
            bigOR(casillas))  # hacemos un or con esas casillas y agregamos esa expression a la lista de clausulas

    # repetimos pero para las filas
    for j in range(0, n):
        casillas = []  # hacemos una lista de las casillas

        for i in range(0, n):
            casillas.append(expr("C{}{}".format(i, j)))
        clauses.append(
            bigOR(casillas))  # hacemos un or con esas casillas y agregamos esa expression a la lista de clausulas

    # ahora vamos a agregar implicaciones de la forma   si una casilla X  es una reina -> ninguna casilla que conflictue lo sea
    for i in range(0,n):
        for j in range(0,n): #si Cij es true -> - (casillas conflictivas OR OR OR OR...)
            clauses.append(Expr('==>', expr("C{}{}".format(i, j) ),~(bigOR(conflictinbox(i, j, n)))))
    clauses = bigAND(clauses)
    print(clauses)
    bigclause =to_cnf(clauses)
    print(bigclause)
    return bigclause


def bigOR(expressions):
    for indx, c in enumerate(expressions):
        if (indx != 0):
            newbigexpr = newbigexpr | c
        else:
            newbigexpr = c
    return newbigexpr


def bigAND(expressions):
    for indx, c in enumerate(expressions):
        if (indx != 0):
            newbigexpr = newbigexpr & c
        else:
            newbigexpr = c
    return newbigexpr


def printboard (board,n):
    for j in range(0,n):
        line="| "
        for i in range(0,n):
            if board.get(expr("C{}{}".format(i, j))):
                line=line+"R | "
            else:
                line = line + "  | "
        print(line)

def conflictinbox (i,j,n): #devuelve dadas unas coordenadas, una lista de las expr que representan las casillas que no deberian tener reinas
    # si en la casilla (i,j) hay una reina
    boxes=[]
    for x in range(0, n):
        for y in range(0, n):
            if (j != y or i != x):
                if (j == y or  # same row
                    i == x or  # same column
                    j - i == y - x or  # same \ diagonal
                    j + i == y + x):
                    boxes.append(expr("C{}{}".format(x,y)))
    print("para la casilla ({},{}) estos son las casillas incompatibles {}".format(i,j,boxes))
    return boxes
ntest=8
reinassat = ninequeens(ntest)
print(reinassat)

result =dpll_satisfiable(reinassat)
printboard(result,ntest)



