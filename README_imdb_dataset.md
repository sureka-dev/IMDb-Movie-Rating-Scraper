# IMDb Movie Ratings Dataset Project

This project uses IMDb's published non-commercial datasets instead of scraping the live website.

## Files
- `imdb_dataset_scraper.py` — downloads and processes the published datasets.
- `requirements_imdb_dataset.txt` — Python packages needed.
- `imdb_top250_calculated.csv` — generated after the script runs.

## Run on Windows PowerShell
Keep the Python script and requirements file in the same folder, then run:

```powershell
python -m pip install -r requirements_imdb_dataset.txt
python imdb_dataset_scraper.py
```

The script downloads `title.basics.tsv.gz` and `title.ratings.tsv.gz` from IMDb's official dataset host. The first run can take some time and needs enough disk space. The downloaded dataset files are reused on later runs.

The output is the 250 highest-rated non-adult feature films with at least 25,000 votes, ranked by rating and then vote count. **This is a calculated ranking, not IMDb's official Top 250 chart.** Dataset values are refreshed daily and can change.

## Terms
For personal and non-commercial use. Read IMDb's dataset details and terms:
https://developer.imdb.com/non-commercial-datasets/
