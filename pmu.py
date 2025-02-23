from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def getPage():
    url = "https://paris-sportifs.pmu.fr/pari/competition/169/football/ligue-1-conforama"
    
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for the page to load (optional: you can add explicit waits for specific elements if needed)
    driver.implicitly_wait(10)
    
    html = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return html

def getGames():
    html = getPage()
    games = html.select(".pmu-event-list-grid-highlights-formatter-row")
    if not games:
        print("No games found. The selector might be incorrect or content is dynamically loaded.")
    else:
        for game in games:
            print(game)


