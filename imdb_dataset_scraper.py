from pathlib import Path
import requests
import pandas as pd

BASE_URL = "https://datasets.imdbws.com/"
BASICS_FILE = "title.basics.tsv.gz"
RATINGS_FILE = "title.ratings.tsv.gz"
OUTPUT_FILE = "imdb_top250_calculated.csv"
MIN_VOTES = 25_000
CHUNK_SIZE = 250_000


def download_dataset(filename):
    """Download a published IMDb dataset if it is not already present."""
    path = Path(filename)
    if path.exists() and path.stat().st_size > 0:
        print(f"Using existing file: {filename}")
        return path

    url = BASE_URL + filename
    print(f"Downloading {filename}. This may take a while...")
    try:
        with requests.get(url, stream=True, timeout=(20, 180)) as response:
            response.raise_for_status()
            with path.open("wb") as file:
                for part in response.iter_content(chunk_size=1024 * 1024):
                    if part:
                        file.write(part)
    except Exception:
        if path.exists():
            path.unlink()
        raise
    print(f"Downloaded: {filename}")
    return path


def main():
    try:
        basics_path = download_dataset(BASICS_FILE)
        ratings_path = download_dataset(RATINGS_FILE)

        print("Loading ratings and filtering titles with enough votes...")
        ratings = pd.read_csv(
            ratings_path,
            sep="\t",
            compression="gzip",
            na_values=[r"\N"],
            usecols=["tconst", "averageRating", "numVotes"],
            dtype={"tconst": "string"},
        )
        ratings = ratings.dropna(subset=["averageRating", "numVotes"])
        ratings = ratings[ratings["numVotes"] >= MIN_VOTES]

        print(f"Reading movie titles in chunks of {CHUNK_SIZE:,}...")
        best = pd.DataFrame()
        reader = pd.read_csv(
            basics_path,
            sep="\t",
            compression="gzip",
            na_values=[r"\N"],
            usecols=["tconst", "titleType", "primaryTitle", "startYear", "isAdult", "genres"],
            dtype={"tconst": "string", "titleType": "string", "primaryTitle": "string",
                         "startYear": "string", "isAdult": "string", "genres": "string"},
            chunksize=CHUNK_SIZE,
            low_memory=True,
        )

        for number, chunk in enumerate(reader, start=1):
            movies = chunk[(chunk["titleType"] == "movie") & (chunk["isAdult"] == "0")]
            if movies.empty:
                continue
            matched = movies.merge(ratings, on="tconst", how="inner")
            if matched.empty:
                continue
            best = pd.concat([best, matched], ignore_index=True)
            best = best.sort_values(
                ["averageRating", "numVotes"], ascending=[False, False]
            ).head(250)
            if number % 4 == 0:
                print(f"Processed approximately {number * CHUNK_SIZE:,} title rows...")

        if best.empty:
            print("No matching movies found. Check the downloaded dataset files.")
            return

        best = best.sort_values(
            ["averageRating", "numVotes"], ascending=[False, False]
        ).head(250).copy()
        best.insert(0, "Calculated Rank", range(1, len(best) + 1))
        best = best.rename(columns={
            "primaryTitle": "Title",
            "startYear": "Year",
            "averageRating": "IMDb Rating",
            "numVotes": "Number of Votes",
            "genres": "Genres",
        })
        best["Scraped On"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        best[["Calculated Rank", "Title", "Year", "IMDb Rating", "Number of Votes", "Genres", "Scraped On"]].to_csv(
            OUTPUT_FILE, index=False, encoding="utf-8-sig"
        )
        print(f"\nSuccess! Saved {len(best)} movies to {OUTPUT_FILE}")
        print("Reminder: this is a calculated ranking, not IMDb's official Top 250.")
        print(best[["Calculated Rank", "Title", "Year", "IMDb Rating", "Number of Votes"]].head(10).to_string(index=False))

    except requests.RequestException as error:
        print("Download/network error:", error)
        print("Check your internet connection and try again later.")
    except Exception as error:
        print("Something went wrong:", error)
        print("If the dataset download was interrupted, delete the incomplete .gz file and retry.")


if __name__ == "__main__":
    main()
