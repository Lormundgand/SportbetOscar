import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool, cpu_count
import re




def init_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    # Ajouter des options de log pour réduire l'affichage de DevTools et TensorFlow
    chrome_options.add_argument("--log-level=3")  # Erreurs seulement
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Désactiver les messages de log
    chrome_options.add_argument("--disable-logging")  # Option supplémentaire pour limiter les messages internes

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'popin_tc_privacy_button_2'))
        )
        accept_button.click()
        time.sleep(0.3)  # Reduced sleep time
    except Exception as e:
        logging.error(f"Error accepting cookies: {e}")

def navigate_to_home_and_back(driver, url): #IMPORTANT car lors de l'acces simple via url le nombre d ematchs est limité, ce qui n'est pas le cas lors d'un retour en arrière.
    # Accéder à l'URL initiale (matchs)
    driver.get(url)
    accept_cookies(driver)
    time.sleep(0.5)  # Laisser la page initiale charger

    # Aller à l'accueil de Betclic
    try:
        driver.get("https://www.betclic.fr/")
        time.sleep(0.5)  # Pause pour charger la page d'accueil

        # Utiliser le bouton "back" pour revenir à la page de départ
        driver.back()
        time.sleep(0.5)  # Pause pour recharger la page avec tous les matchs
    except Exception as e:
        logging.error(f"Erreur lors de la navigation vers l'accueil et retour : {e}")

def scroll_to_bottom(driver):
    """Scrolls to the bottom of the page to load all dynamic content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 0
    
    while retries < 10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)  # Further reduced sleep time
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            retries += 1
        else:
            last_height = new_height
            retries = 0

        if retries >= 2:
            break

def clean_text(text):
    text = text.replace('\n', '')
    return text.replace('\xa0', ' ')

def extraire_sport(lien):
    match = re.search(r'\.fr/([^/-]+)-', lien)
    return match.group(1) if match else None

def scrape_betclic(url):
    results = []
    driver = init_driver()
    sport = extraire_sport(url)
    navigate_to_home_and_back(driver, url)
    try:
        # Charger la page et simuler le retour
        scroll_to_bottom(driver)  # Défilement pour charger tout le contenu

        # Analyser la page après retour en arrière
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        groupes = soup.find_all("div", {"class": "groupEvents"})

        if not groupes:
            logging.warning("No events found.")
        else:
            for groupe in groupes:
                date = groupe.find("div", {"class": "groupEvents_head"}).get_text()
                cartes = groupe.find_all("div", {"class": "cardEvent_content"})
                
                for carte in cartes:
                    try:
                        texte = carte.find_all(class_="btnWrapper")
                        if texte:
                            for btn in texte:
                                spans = btn.find_all(class_="btn_label")
                                if len(spans) == 4 and date != "Maintenant":
                                    name1 = clean_text(spans[0].get_text(strip=True))
                                    cote1 = clean_text(spans[1].get_text(strip=True))
                                    name2 = clean_text(spans[2].get_text(strip=True))
                                    cote2 = clean_text(spans[3].get_text(strip=True))
                                    date = clean_text(date)
                                    results.append([name1, cote1, name2, cote2, date, sport])
                                    # results.append([name1, cote1, name2, cote2])
                    except Exception as e:
                        logging.error(f"Error parsing event: {e}")
    except Exception as main_exception:
        logging.error(f"Critical error in scrape_site: {main_exception}")
    finally:
        driver.quit()
    return results
    
"""
Cas betclic, Ca fonctionne nickel, à l'avenir peut-etre arbitrer sport par sport et non site par site
pour éviter les problèmes de rafraichissement des cotes"""
########################################################

betclic_games = {}
urls = [ "https://www.betclic.fr/mma-s23"
      ,"https://www.betclic.fr/boxe-s16"
      ,"https://www.betclic.fr/basketball-s4"
      ]
for url in urls:
    sport = url.split('/')[-1].split('-')[0] #prend le sport (basketball, boxe, mma)
    results = scrape_betclic(url)
    betclic_games[sport] = results
    print(" ")
    for element in results:
        print(element)
#########################################################

# urls = [ "https://www.betclic.fr/mma-s23"
#     ,"https://www.betclic.fr/boxe-s16"
#     ,"https://www.betclic.fr/basketball-s4"
#     ]