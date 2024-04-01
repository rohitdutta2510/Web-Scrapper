# Summer Olympics Data Scraper

## Overview
This project aims to scrape data from the Summer Olympics Wikipedia pages, focusing on the events from the last 50 years (1968 to 2020). It collects information on the name, year, host city, participating nations, number of athletes, sports, and top-ranking nations for each Summer Olympics during this period. The collected data is stored in a SQLite database named `OlympicsData.db`.

## How It Works
The project consists of three main scripts:
1. `handler.py`: Collects main Summer Olympics Wikipedia page data, creates the database, and seeds it with URLs of individual Olympic event pages to be scraped.
2. `scraper.py`: Scrapes detailed information from each Olympic event page and updates the database accordingly.
3. `checker.py`: Checks if the data collection is complete and reports on the dataset.

### Database Schema
The SQLite database `OlympicsData.db` includes a table named `SummerOlympics` with the following columns:
- `Name`: Title of the Wikipedia page (e.g., "2012 Summer Olympics").
- `WikipediaURL`: URL to the event's Wikipedia page.
- `Year`: Year the event was conducted.
- `HostCity`: City where the event was hosted.
- `ParticipatingNations`: List of participating nations.
- `Athletes`: Number of athletes.
- `Sports`: List of sports.
- `Rank_1_nation`: Top-ranking nation.
- `Rank_2_nation`: Second top-ranking nation.
- `Rank_3_nation`: Third top-ranking nation.
- `DONE_OR_NOT_DONE`: Status flag (1 if fetched, 0 otherwise).

## Setup and Usage
### Requirements
- Python 3.x
- Libraries: `requests`, `bs4` (BeautifulSoup4), `sqlite3`

### Setting Up Your Environment
1. Clone the repository:
```
git clone https://github.com/rohitdutta2510/Web-Scrapper.git
```
2. Install the required Python libraries:
```
pip install requests bs4 sqlite3
```
