import requests
from bs4 import BeautifulSoup

# Vyhledání všech pracovních nabídek (např. v kontejnerech div nebo článcích)
jobs = soup.findall("div", class="job--item")


# Načtení HTML stránky
url = "https://www.jobs.cz/prace/?q%5B%5D=python%20junior"
response = requests.get(url)

if response.status_code == 200:
    

# Inicializace BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
else:
    print("Chyba při načítání stránky.")


# Vyhledání všech pracovních nabídek (např. v kontejnerech div nebo článcích)
jobs = soup.findall("div", class="job--item")  # Upravit podle HTML struktury stránky


# Filtrování a výpis nabídek obsahujících "junior" a "Python"
with open("jobs.txt", "w", encoding="utf-8") as file:
    for job in jobs:
        title = job.find("h2")  # Najděte nadpis nebo název pozice
        if title and "junior" in title.text.lower() and "python" in title.text.lower():
            print(f"Název pozice: {title.text.strip()}")
        # Přidání odkazu, pokud je k dispozici
            link = job.find("a", href=True)
            if link:
                file.write(f"Odkaz: {link['href']}\n")

            description = job.find("p")  # Upravit podle HTML, kde je text inzerátu
            if description:
                file.write(f"Popis: {description.text.strip()}\n")

            file.write("-" * 40 + "\n")  # Oddělení inzerátů

