# scrapers-for-journalists
Scraper(s) to help the journalists retrieve data or monitor sites for potential leads for stories.

## Using the scrapers

```
pip install scrapers_for_journalists==0.1.2
```

And then import a scraper, e.g. `from domstoldk.retrive import DomStolScrape`

Every file in `utils/`can be imported in your scrapers, as it is added as a package in pyproject.toml. For example, you can import the BaseScraper with generic utilities like: `from base import BaseScraper`.

## Description of current scrapers

### domstol.dk

This scrapers retrieves information about current court cases ("retslister") in Danish "byretter" (Currently, Højesteret etc. are not included). Civil cases and tvangsauktioner are filtered away. Relevance of the cases are estimated based on keywords and "gerningskoder" (types of crimes) from the Danish Police.

To run it manually, use:
```
poetry run python domstoldk/retrieve.py --outfile test.xlsx
```

### afdøde.dk

This scraper retrieves information about public "dødsannoncer" from afdøde.dk.

To run it manually, use:
```
poetry run python afdoededk/retrieve.py --outfile test.xlsx --from_date "2024-11-01" --to_date "2024-11-02"
```

# politi.dk

This scraper retrieves police reports ("døgnrapporter") from politi.dk.

To run it manually, use:
```
poetry run python doegnrapporter/retrieve.py --outfile test.xlsx --from_date "2024-11-01" --to_date "2024-11-01"
```
