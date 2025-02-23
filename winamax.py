import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

def getPage(url):
    # Configuration des options Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")   #Exécution en mode headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Configuration de l'user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    #Ne pas afficher les logs
    logging.getLogger("selenium").setLevel(logging.CRITICAL)

    # Initialisation du webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Naviguer vers l'URL
        driver.get(url)
        
        # Attendre que la page soit complètement chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Récupérer le HTML complet
        html_content = driver.page_source
        
        return html_content
    
    except Exception as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return None
    
    finally:
        # Fermer le navigateur
        driver.quit()

def getJson(url):
    page = getPage(url)
    if not page:
        return None
    
    try:
        split1 = page.split("var PRELOADED_STATE = ")[1]
        split2 = split1.split(";</script>")[0]
        return json.loads(split2)
    except Exception as e:
        print(f"Erreur lors de l'extraction du JSON : {e}")
        return None

def getGames(url):
    json_data = getJson(url)
    if not json_data:
        return []
    
    games = []
    nombre_sport = int(url.split('/')[-1])
    
    for game in json_data['matches']:
        if (json_data['matches'][game]['sportId'] != nombre_sport or 
            json_data['matches'][game]['status'] == 'ENDED'):
            continue
        
        equipe1 = json_data['matches'][game]['competitor1Name']
        equipe2 = json_data['matches'][game]['competitor2Name']
        betId = json_data['matches'][game]['mainBetId']
        bet = json_data['bets'][str(betId)]['outcomes']
        
        if len(bet) != 2:
            continue
        
        game_info = [
            equipe1,
            json_data['odds'][str(bet[0])],
            equipe2,
            json_data['odds'][str(bet[1])]
        ]
        
        games.append(game_info)
    
    return games

# Exemple d'utilisation
if __name__ == "__main__":
    winamax_games = {}
    sports = {
        "boxe": "https://www.winamax.fr/paris-sportifs/sports/10",
        "mma": "https://www.winamax.fr/paris-sportifs/sports/117",
        "basket": "https://www.winamax.fr/paris-sportifs/sports/2"
    }
    
    for sport, url in sports.items():
        winamax_games[sport] = getGames(url)
        
    for sport in winamax_games:
        for game in winamax_games[sport]:
            print(game)
        print("--------------------------------------------")