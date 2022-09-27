from bs4 import BeautifulSoup
from requests import get
from time import sleep
from csv import DictWriter


def main():
    baseurl = "https://transparentcalifornia.com/salaries/2021/sacramento/"
    page = 1
    total_pages = 112
    data = list()
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
                position = datum[1].text.strip().replace("\nSacramento, 2021", "")
                pay = datum[-1].text.strip().replace("$", "").replace(",", "")
                data.append({"name": name, "position": position, "pay": pay})
        page += 1
        sleep(1)
    with open("data.csv", "w") as csvfile:
        fieldnames = ["name", "position", "pay"]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    main()
