
import requests
from bs4 import BeautifulSoup
import csv


def main(filename: str) -> csv:
    """
    Функция, запускает все остальные. Принимает строку, 
    возвращает csv файл с соответствующим названием.
    """

    notebooks_url = "https://kg.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki" # ?sort=popular&page=1
    
    def get_html(url: str) -> str:
        """
        Принимает ссылку, возвращает html код страницы.
        """
        headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
        response = requests.get(url, headers=headers)

        return response.text

    def get_last_page(html: str) -> int:
        """
        Принимает html код, возвращает номер последней страницы.
        """
        soup_object = BeautifulSoup(html, "lxml")

        all_pages = soup_object.find(
            "div", {"class":"pageToInsert catalog-pagination__wrapper"}
            )
        
        last_page = all_pages.find_all("a", {"class":"pagination-item"})[-1].text

        return int(last_page)

    
    def write_to_csv(data: dict) -> csv:
        """
        Принимает словарь, записывает его значения в csv файл.
        """

        with open(f"{filename}.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                data["brand"],
                data["price"],
                data["stats"],
                "https" + data["image"],,
            ])
    

    def get_data(url: str) -> csv:
        """
        Принимает ссылку, вытаскивает нужные значения и записывает их в словарь.
        Затем, используя другую функцию, сразу записывает значения словаря в csv формат
        """
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        full_page = soup.find_all(
            "a", {"class": "product-card__main j-open-full-product-card"}
        )

        for info in full_page:
            data = {}

            data["brand"] = info.find("strong", {"class": "brand-name"}).text.replace("/", ": ")
            
            data["stats"] = info.find("span", {"class": "goods-name"}).text .replace("/", ", ")
            
            data["price"] = info.find("span", {"class":"price-localized"}).text

            data["image"] = info.find("img", {"class": "j-thumbnail thumbnail"}).get("src")

            write_to_csv(data)
        

    with open(f"{filename}.csv", 'a') as f:
        """
        Создает разделы с соответствующими названиями, 
        для упрощения ориентации в будущем.
        """
        writer = csv.writer(f)
        writer.writerow([
            "Brand",
            "Price",
            "Characteristics",
            "Image"
        ])
        

    for i in range(1, get_last_page(get_html(notebooks_url))+1):
        """
        Запускает процесс, который каждый раз меняет страницу на следующую, 
        а затем вытаскивает значения и записывает в csv
        """
        url = notebooks_url + f"?sort=popular&page={i}"
        get_data(url)


main("file")

