from logic import *


def mycoloringSAT(colors,neighbors):
    if isinstance(neighbors,str):
        neighbors=parse_neighbors(neighbors)
    clauses = []
    for n in neighbors.keys():
        print(n)
        newclause=[]
        for indx,c in enumerate(colors):
            if (indx != 0):
                newclause = newclause | expr(n+"_"+c)
            else:
                newclause=expr(n+"_"+c)
       # print("newclause {}".format(newclause))
        clauses.append(newclause)

        for c in colors:
            #obtenemos un elemento especifico, ahora vamos a obtener los vecinos y los otros colores que pueden
            #tomar los vecinos
            vecinos = neighbors[n]
            #othercolors= [ col for col in neighbors.key() if col !=n]
            for v in vecinos:
                clauses.append(expr(n+"_"+c+'  ==>  ~'+v+"_"+c))
        #        print(clauses)



    print(clauses)
    return clauses
australia_sat =mycoloringSAT(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
#australia_sat =mycoloringSAT(list('RGB'), """SA: WA NT Q NSW V """)
bigcnf=australia_sat[0];

for cl in australia_sat:
    bigcnf =bigcnf & cl

print("resulado ")
print(bigcnf)
print("lo paso a cnf")
bigcnf= to_cnf(bigcnf)


print(dpll_satisfiable(bigcnf))