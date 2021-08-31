
from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup
import csv

def main(file: str):

    notebook_url = "https://www.mashina.kg/search/all/"

    def get_html(url: str):

        headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
        response = requests.get(url, headers=headers)

        return response.text

    def get_last_pages(html: str):

        soup_object = BeautifulSoup(html, 'lxml')

        all_pages = soup_object.find("ul", {"class": "pagination"})

        return all_pages

    def write_to_csv(dat: dict):
        with open(f"{file}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([
                dat["name"],
                dat["price"],
                dat["stats"],
                "https:" + dat["image"]
            ])

    def get_dat(url: str):
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        full_name = soup.find_all("div", {"class": "list-item list-label new-line"})

        for inf in full_name:
            dat = {}
            dat["name"] = inf.find("h2", {"class": "name"}).text.raplace()
            dat["stats"] = inf.find("div", {"class": "item-info-wrapper"}).text
            dat["price"] = inf.find("div", {"class": "position: relative"}).text
            dat["image"] = inf.find("div", {"class": "tmb-wrab-table"}).get("src")
            
            write_to_csv(dat)


    with open(f"{file}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name"
            "Brand"
            "Price"
            "Image"
        ])

    for i in range(1, get_last_pages(get_html(notebook_url))+1):
        url = notebook_url + f"?page={i}"

    return get_dat(url)


    
main("file")
