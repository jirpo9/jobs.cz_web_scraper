import requests
from bs4 import BeautifulSoup

# Načtení HTML stránky
url = "https://www.jobs.cz/prace/python-vyvojar/"
response = requests.get(url)

if response.status_code == 200:
    # Inicializace BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Vyhledání všech pracovních nabídek (např. v kontejnerech div nebo článcích)
    job_cards = soup.find_all("article", class_="SearchResultCard")  # Upravit podle HTML struktury stránky
    print(job_cards)

    with open("Scrap_projekt/jobs.txt", "w", encoding="utf-8") as file:
        for job in job_cards:
            # Název pozice
            title_tag = job.find("h2", class_="SearchResultCard__title")
            title = title_tag.get_text(strip=True) if title_tag else "Neznámý název"

            # Odkaz na nabídku
            link_tag = title_tag.find("a", href=True) if title_tag else None
            link = link_tag["href"] if link_tag else "Žádný odkaz"

            # Místo (například Praha, Brno)
            location_tag = job.find("li", class_="SearchResultCard__footerItem", attrs={"data-test": "serp-locality"})
            location = location_tag.get_text(strip=True) if location_tag else "Neznámá lokalita"

            # Výpis do souboru
            file.write(f"Název pozice: {title}\n")
            file.write(f"Odkaz: {link}\n")
            file.write(f"Lokalita: {location}\n")
            file.write("-" * 40 + "\n")

    print("Data byla úspěšně uložena do souboru 'Scrap_projekt/jobs.txt'")
else:
    print(f"Chyba při načítání stránky: {response.status_code}")
