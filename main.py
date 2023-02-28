from bs4 import BeautifulSoup
from requests import get
from time import sleep
from csv import DictWriter


def main():
    year = 2021
    year_end = 2021
    page = 1
    total_pages = 112

    fieldnames = ["name", "position", "pay"]
    while year <= year_end:
        data = list()
        baseurl = f"https://transparentcalifornia.com/salaries/{year}/sacramento/"
        while page <= total_pages:
            url = f"{baseurl}?page={page}"
            request = get(url)
            print(url)
            if request.ok:
                soup = BeautifulSoup(request.text, "html.parser")
                container = soup.find(name="div", id="container-wrapper")
                row = container.find("div", {"class": "row-fluid"})
                table = row.find("table")
                tbody = table.find("tbody")
                rows = tbody.find_all("tr")
                for row in rows:
                    datum = row.find_all("td")
                    name = datum[0].text.strip()
                    position = datum[1].text.strip().replace(f"\nSacramento, {year}", "")
                    pay = datum[-1].text.strip().replace("$", "").replace(",", "")
                    data.append({"name": name, "position": position, "pay": pay})
            page += 1
            sleep(0.5)
        with open(f"{year}.csv", "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        page = 1
        year += 1
if __name__ == "__main__":
    main()
