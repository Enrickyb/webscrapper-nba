from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

def getGamesInfo(html):
    games_info = []
    game_cards = html.find_all("div", class_="GameCard_gc__UCI46")

    for card in game_cards:
        home_team_elem = card.find("span", class_="MatchupCardTeamName_teamName__9YaBA")
        away_team_elem = card.find_all("span", class_="MatchupCardTeamName_teamName__9YaBA")[1]
        date_elem = card.find("p", class_="GameCardMatchup_gcmDate__fXKRQ")
        time_elem = card.find("p", class_="GameCardMatchupStatusText_gcsText__PcQUX")
        
        # Verifica se todos os elementos foram encontrados
        if home_team_elem and away_team_elem and date_elem:
            home = home_team_elem.text.strip()
            visitor = away_team_elem.text.strip()
            date = date_elem.text.strip()
            date_parts = date.split(', ')[1]  # Divide a data no separador ", " e pega a segunda parte
            day, month = date_parts.split('/')  # Divide os componentes da data pelo "/"
            print(date_parts)
            print(month)
            print("day" + day)
            print("len " + str(len(day)))
    
            # Acrescentando um zero ao dia, se necessário
            if len(day) == 1:
                day = '0' + day

            # Reunindo o mês e o dia formatados
            formatted_date = day + '/' + month 

            startTime = time_elem.text.strip()
            
            games_info.append({"home": home, "visitor": visitor, "date": formatted_date, "startTime": startTime})
            
    return games_info


@app.route('/api', methods=['GET'])
def api():
    date = request.args.get('date')
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.nba.com/games?date=" + date)
    
    # Wait for content to load
    time.sleep(5)  # Adjust the sleep time as needed
    
    html = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    games_info = getGamesInfo(html)
    return jsonify(games_info)

if __name__ == '__main__':
    app.run(debug=True)
