def calculmise(coefarbitrage, cote1, cote2):
    MiseA = (10*(1/cote1))/coefarbitrage
    MiseB = (10*(1/cote2))/coefarbitrage
    #Calcul screenés, sur arbitrageformule.py
    return "mise A : [miseA], mise B : [miseB]"

def possible(matchtab1, nomtableau1, matchtab2, nomtableau2):
    #On compare la cote 1 du match 1 à la cote 2 du match 2
    cotematch1e1 = matchtab1[1]
    cotematch2e2 = matchtab2[3]

    coefarbitrage = (1/cotematch1e1) + (1/cotematch2e2)
    if coefarbitrage < 1:
        return f"entre {matchtab1[0]} à {matchtab1[1]} sur {nomtableau1} et {matchtab2[2]} à {matchtab2[3]} sur {nomtableau2} caca"


    #On compare la cote 2 du match1 a la cote 1 du match 2 
    cotematch2e1 = matchtab2[1]
    cotematch1e2 = matchtab1[3]

    coefarbitrage = (1/cotematch2e1) + (1/cotematch1e2)
    if coefarbitrage < 1:
        return f"entre {matchtab1[2]} à {matchtab1[3]} sur {nomtableau1} et {matchtab2[0]} à {matchtab2[1]} sur {nomtableau2} prout"
    
    #Aucun arbitrage possible, on ne renvoie rien
    return None

