## IMDb Movie Rating Scraper
------------------------------
## Features

* Automated Data Extraction: Collects movie titles, release years, IMDb ratings, vote counts, and direct links from IMDb charts.
* Data Processing & Cleaning: Uses Pandas to structure, validate, and convert raw text into clean data types (e.g., float ratings, integer years).
* Structured Output: Exports the cleaned dataset directly to a structured .csv file for immediate analysis. [1, 2, 3] 

------------------------------
## Prerequisites

* Python 3.8+
* Required Python libraries:

pip install requests beautifulsoup4 html5lib pandas

(Optional: Selenium if scraping dynamically rendered JavaScript pages). [1, 2, 4] 

------------------------------
## Installation & Usage

   1. Clone the Repository
   
   git clone https://github.com
   cd imdb-movie-rating-scraper
   
   2. Run the Scraper Script
   
   python scraper.py
   
   3. Check the Output
   * The script will parse the target IMDb page and generate a clean CSV file named imdb_top_250_movies.csv (or your custom filename) in your project directory. [3, 5] 
   
------------------------------
## Code Overview
The script follows a standard extraction and parsing workflow:

   1. HTTP Request: Sends a GET request with custom headers to the target IMDb URL using requests.
   2. HTML Parsing: Parses the raw HTML response via BeautifulSoup.
   3. Data Extraction: Iterates over target CSS selectors (e.g., li.ipc-metadata-list-summary-item) to pull titles, years, and ratings.
   4. Data Export: Loads the extracted tuples/dictionaries into a Pandas DataFrame and saves it to CSV. [1, 3, 6] 

