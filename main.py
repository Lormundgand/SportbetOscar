import sys
import logging
import winamax
import betclic
import arbitrage

sys.stdout.reconfigure(encoding='utf-8')
# On retire le logging pour les perfs
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


"""
Fonctionnement du code:
1. Les fichiers Bookmakers crééent chacun un dictionnaire xxx_games, pour lesquels on associe 
    aux clés des tableaux sous la forme [equipe1, coteequipe1; equipe2, coteequipe2]. 
    Chacun fonctionne de son coté, ils s'exécutent lors de l'import dans le main.
2. Une fois chacun des dictionnaires récupérés, il faut les parcourir et comparer. 
    Il va faloir optimiser cela afin que cela se fasse le plus rapidement possible. 
"""




"""
On peut arbitrer, voici les deux cas de figure.
Exemple winamax vs betclic où Arbitrage possible :"""
winamaxpos = ["brest", 2 , "nantes", 1.8]
betclicpos = ["brest", 2.1, "nantes", 2.5]
# print(arbitrage.possible(winamaxpos, "winamax", betclicpos, "betclic"))

"""
Exemple winamax vs betclic où Arbitrage impossible""" 
winamaximpos = ["brest", 2 , "nantes", 1.8]
betclicimpos = ["brest", 2.1, "nantes", 0.7]
# print(arbitrage.possible(winamaximpos, "winamax", betclicimpos, "betclic"))


"""
A faire dimanche : Calculer les mises nécessaires, trouver moyen de run le code 
24/24 et faire aller les logs sur discord ou telegram peu importe
Pmu ne fonctionne pas, peutetre commencer a extraire les données si 
le temps le permet"""

