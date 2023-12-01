import requests
import sys
import sqlite3
import re
from bs4 import BeautifulSoup
import time

def getData(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

# extract alpha-numeric characters only
def extract(string):
    return ''.join(letter for letter in string if letter.isalnum())

# function to get top 3 nations
def getTopNations(olympic_soup):
    top_nations = olympic_soup.find('table', class_ = 'wikitable sortable plainrowheaders jquery-tablesorter').find_all('tr')[1:4]
    rank_1 = extract(top_nations[0].find('th').text)
    rank_2 = extract(top_nations[1].find('th').text)
    rank_3 = extract(top_nations[2].find('th').text)
    return rank_1, rank_2, rank_3

# function to get the list of participating nations
def getParticipatingNations(olympic_soup, year):
    pattern = r'^([A-Za-z\s]+)\s*\(.*\)$' #regular expression to extract participating countries name
    participating_nations = [] # list storing name of the participating nations

    if year == 1976:
        nations = olympic_soup.find_all('table', class_ = ['wikitable collapsible', 'wikitable mw-collapsible'])[1]
        nations = nations.find_all('tr')[1].find('td').find('div', class_ = 'div-col').find('ul').find_all('li')
    else:
        nations = olympic_soup.find('table', class_ = ['wikitable collapsible', 'wikitable mw-collapsible'])
        nations = nations.find_all('tr')[1].find('td').find('div', class_ = 'div-col').find('ul').find_all('li')
    
    for countries in nations:
        text = countries.text.strip()
        match = re.match(pattern, text)
        if match:
            country_name = match.group(1)
            # Remove any non-breaking space (\xa0) characters if present
            country_name = country_name.replace('\xa0', ' ').strip()
            participating_nations.append(country_name)

    return ', '.join(participating_nations)

# function to get number of athletes
def getNumAthletes(olympic_soup, year):
    box = olympic_soup.find_all(class_='infobox')[0].find_all('tr')
    if year in ['1968','1980']:
        ath_pos = 3
    else:
        ath_pos = 4
    temp1 = list(box[ath_pos].find('td').strings)[0]
    return int(extract(temp1.split()[0]))

# function to get number of sports
def getSports(olympic_soup):
    heading = olympic_soup.find('span', id = 'Calendar')
    table1 = heading.find_next('table')
    table2 = table1.find_next('table')

    # Now going through the table2 under Calendar heading to find the sports from table2
    sports_rows_tr = table2.find_all('tr')[2:-3]
    return len(sports_rows_tr)

# record scrapper start time
startTime = time.time()

print('\nScraper running ...')
headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

# Connect with SQLite DB
conn = sqlite3.connect('OlympicsData.db')
cursor = conn.cursor()


while True:
    query = "SELECT ID FROM SummerOlympics WHERE DONE_OR_NOT_DONE = 0 ORDER BY RANDOM() LIMIT 1" 
    result = cursor.execute(query)
    random_id = cursor.fetchone()
    print(random_id)

    if random_id:
        random_id = random_id[0]
        query = "UPDATE SummerOlympics SET DONE_OR_NOT_DONE = 1 WHERE ID = "  + str(random_id)
        cursor.execute(query)
        conn.commit()

        query = "SELECT WikipediaURL FROM SummerOlympics WHERE ID = " + str(random_id)
        cursor.execute(query)
        url = cursor.fetchone()[0]
        print(url)

        # Fetch Wiki page using url
        response = getData(url, headers)
        
        olympic_soup = BeautifulSoup(response, 'html.parser')

        # get name 
        name = olympic_soup.find("h1", class_ = 'firstHeading').text.strip()

        # get year
        year = int(name.split()[0])

        # get the host city
        host_city = olympic_soup.find('table', class_ = 'infobox').find_all('tr')[1].find('td').text.split(',')[0]
        
        # get number of athletes
        athletes = getNumAthletes(olympic_soup, str(year))

        # get the top ranked nations
        rank_1, rank_2, rank_3 = getTopNations(olympic_soup)

        # get the list of participating nations
        nation_list = getParticipatingNations(olympic_soup, year)

        # Getting the no.of.sports
        no_of_sports = getSports(olympic_soup)

        # Parsing completed
        query = "UPDATE SummerOlympics SET Year = ?, HostCity = ?, ParticipatingNations = ?, Athletes = ?, Sports = ?, Rank_1_nation = ?, Rank_2_nation = ?, Rank_3_nation = ? WHERE ID = ?"
        cursor.execute(query, (year, host_city, nation_list, athletes, no_of_sports, rank_1, rank_2, rank_3, random_id))
        conn.commit() 
        
             
    else:
        endTime = time.time()
        print("\nScraper End Time : ", endTime)
        print("Scraper Execution time : ", endTime-startTime)
        sys.exit()