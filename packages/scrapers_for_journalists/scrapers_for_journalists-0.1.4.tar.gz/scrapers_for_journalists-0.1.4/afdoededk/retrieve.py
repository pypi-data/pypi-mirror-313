import re
from argparse import ArgumentParser

import pandas as pd
import requests
from base import BaseScraper
from bs4 import BeautifulSoup
from tqdm import tqdm


class AfdoedeScraper(BaseScraper):
    """
    Scraping dødsannoncer fra afdøde.dk
    """

    def get_pages(
        self, publish_date_from: str, publish_date_to: str
    ) -> list[tuple[str, str]]:
        """
        getting links to scrape
        """
        max_pages = 1001
        links = []

        for page_no in tqdm(range(1, max_pages)):
            response = requests.get(
                f"https://afdoede.dk/find-dodsannoncer?type=range&publish_date_from={publish_date_from}&publish_date_to={publish_date_to}&page={page_no}"
            )
            soup = BeautifulSoup(response.text, features="html.parser")
            new_links = [
                "https://afdøde.dk" + e.get("href")
                if "http" not in e.get("href")
                else e.get("href")
                for e in soup.select("h5 a.text-decoration-none[href*='/minde']")
            ]
            new_places_for_links = [e.text.strip() for e in soup.select("h5 + p + p")]

            if len(new_links) == 0:
                print(f"Got to the last page: {page_no}")
                return links

            links += [
                (link, place) for link, place in zip(new_links, new_places_for_links)
            ]

        return links

    def parse_death_page(self, soup: BeautifulSoup, url: str) -> dict:
        try:
            announcement_text = soup.select_one(
                "div#primaryAnnouncementText"
            ).text.strip()
        except AttributeError:
            announcement_text = ""

        try:
            name = soup.select_one("h1").text
        except AttributeError:
            name = ""

        try:
            year_of_birth, year_of_death = soup.select_one("h1 + small").text.split(
                " - "
            )
        except AttributeError:
            year_of_birth, year_of_death = "", ""

        try:
            age = int(year_of_death) - int(year_of_birth)
        except ValueError:
            age = None

        try:
            published_date = re.findall(
                r"\d{2}\.\d{2}\.\d{4}", soup.select_one("p.mb-0 small").text.strip()
            )[0]
        except AttributeError:
            published_date = ""

        return {
            "announcement_text": announcement_text,
            "name": name,
            "year_of_birth": year_of_birth,
            "year_of_death": year_of_death,
            "age": age,
            "published_date": published_date,
            "link": url,
        }

    def execute(self, publish_date_from: str, publish_date_to: str) -> pd.DataFrame:
        print(f"***Finding ads from {publish_date_from} to {publish_date_to}")

        # Get links and save locally
        print("*** Getting links for pages ***")
        pages_infos = self.get_pages(
            publish_date_from=publish_date_from, publish_date_to=publish_date_to
        )

        # Scrape pages
        print("*** Scraping pages ***")
        pages = []
        for link, place in tqdm(pages_infos):
            response = requests.get(link)
            soup = BeautifulSoup(response.text, features="html.parser")
            data = self.parse_death_page(soup, link)
            data["place"] = place
            pages.append(data)

        print("*** -> DONE <- ***")
        return pd.DataFrame(pages)


if __name__ == "__main__":
    parser = ArgumentParser(prog="DomStolScraper", description="Scrapes domstol.dk")
    parser.add_argument(
        "--outfile", help="the path to save the Excel-file. Must end with .xlsx"
    )
    parser.add_argument(
        "--from_date", help="filter only ads published from, format. YYYY-mm-dd"
    )
    parser.add_argument(
        "--to_date", help="filter only ads published to, format. YYYY-mm-dd"
    )
    args = parser.parse_args()
    print(args.from_date)
    scraper = AfdoedeScraper()
    df = scraper.execute(publish_date_from=args.from_date, publish_date_to=args.to_date)

    df.to_excel(args.outfile, engine="openpyxl", index=False)
