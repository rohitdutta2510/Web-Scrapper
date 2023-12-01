import requests
import sqlite3
import random
import os
import time
from bs4 import BeautifulSoup

def getData(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur, con

# function to get urls for 2 random olympic years
def getOlympicsURL(url, headers):
    html_doc = getData(url, headers)

    soup = BeautifulSoup(html_doc, 'html.parser')
    # Find the "List of Summer Olympic Games" table
    table = soup.find('table', class_ = 'sortable wikitable')
    olympics_data = table.find_all('tr')[1:]  # Skip the header row
    olympics_data = olympics_data[20:33]
    selected_olympics = random.sample(olympics_data, 10)
    #selected_olympics = olympics_data

    olympics_urls = []
    num_athletes = []
    for olympics in selected_olympics:
        olympics_row = olympics.find_all('td')[1]
        athletes = olympics.find_all('td')[5].text
        olympics_link = olympics_row.find('a', href=True)
        olympics_url = 'https://en.wikipedia.org' + olympics_link['href']
        num_athletes.append(athletes)
        olympics_urls.append(olympics_url)

    return olympics_urls, num_athletes

# sqlite3 table creation
def createTable(cursor, connection):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SummerOlympics (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            WikipediaURL TEXT,
            Year INTEGER,
            HostCity TEXT,
            ParticipatingNations TEXT,
            Athletes INTEGER,
            Sports TEXT,
            Rank_1_nation TEXT,
            Rank_2_nation TEXT,
            Rank_3_nation TEXT,
            DONE_OR_NOT_DONE INTEGER
        )
    """)

    connection.commit()

def main_handler():
    url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    html_doc = getData(url, headers)

    # get 10 random olympics url and corresponding number of athletes
    olympics_urls, num_athletes = getOlympicsURL(url, headers)

    #print(olympics_urls)

    # Create a SQLite database
    cursor, conn = createDatabaseConnect('OlympicsData.db')
    createTable(cursor, conn)

    # Insert into Database
    for url in olympics_urls:
        cursor.execute('INSERT INTO SummerOlympics (WikipediaURL, DONE_OR_NOT_DONE) VALUES (?,?)', (url, 0))
        conn.commit()

    # Spawning three processes
    # Windows
    commands = [
        "start /B python Scraper.py",  # Process 1
        "start /B python Scraper.py",  # Process 2
        "start /B python Scraper.py",  # Process 3
        ]

    #Linux
    '''commands = [
        "python3 Scraper.py &",  # Process 1
        "python3 Scraper.py &",  # Process 2
        "python3 Scraper.py &",  # Process 3
        ]'''
    
    # Spawn the processes
    for command in commands:
        os.system(command)

    
startTime = time.time()
print("Start time : ", startTime)
main_handler()    
