import requests
import json



def getPage(url):  # Retourne le code HTML de la page
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept-Language": "en-US,en;q=0.9",
    }

    session = requests.Session()
    session.headers.update(headers)

    reponse = session.get(url)
    return reponse.text


def getJson(url):
    page = getPage(url)
    split1 = page.split("var PRELOADED_STATE = ")[1] #tout ce qui vient après "var PRELOADED_STATE = "
    split2 = split1.split(";</script>")[0] #tout ce qui vient avant ";</script>"
    return json.loads(split2) #on a dont ce qui est compris entre les deux précédents donc on a le json

def getGames(url):
    json = getJson(url)
    games = []
    nombre_sport = int(url.split('/')[-1])
    for game in json['matches']:
        if(json['matches'][game]['sportId'] != nombre_sport or json['matches'][game]['status'] == 'ENDED'): #on degage les paris pas de foot et les paris de games terminées
            continue
        equipe1 = json['matches'][game]['competitor1Name']
        equipe2 = json['matches'][game]['competitor2Name']
        betId = json['matches'][game]['mainBetId']
        bet = json['bets'][str(betId)]['outcomes']

        if(len(bet) != 2): #on dégage les paris qui n'ont pas 3 cotes
            continue

        odds = [
            json['odds'][str(bet [0])],
            json['odds'][str(bet[1])],
        ]

        game = []
        game.append(equipe1)
        game.append(json['odds'][str(bet [0])])
        game.append(equipe2)
        game.append(json['odds'][str(bet[1])])

        games.append(game)
    return games


"""Winamax fonctionne, ya juste pas les dates mais osef à la limite
Pour obtenir le json, goto la page, clic droit puis obtenir code source, puis ctrl+f une cote pour trouver
la ligne avec le json"""
#######################################################
winamax_games = {}
print(getPage("https://www.winamax.fr/paris-sportifs/sports/10"))
# winamax_games["boxe"] = getGames("https://www.winamax.fr/paris-sportifs/sports/10")
# winamax_games["mma"] = getGames("https://www.winamax.fr/paris-sportifs/sports/117") 
# winamax_games["basket"] = getGames("https://www.winamax.fr/paris-sportifs/sports/2") 
# for sport in winamax_games:
#         for element in winamax_games[sport]:
#                 print(element)
#         print("--------------------------------------------")
#######################################################