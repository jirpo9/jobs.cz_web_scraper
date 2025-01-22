# test
import requests
from bs4 import BeautifulSoup
import os
import textwrap

def scrape_job_detail(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_title_tag = soup.find("h1", class_="typography-heading-medium-text")
        job_title = f"Název pozice: {job_title_tag.get_text(strip=True)}\n" if job_title_tag else "Název pozice: Název nenalezen\n"
        
        company_tag = soup.find("p", class_="typography-body-medium-text-regular")
        company_name = company_tag.get_text(strip=True) if company_tag else "Firma nenalezena"
        
        location_tag = soup.find("a", class_="link-secondary link-underlined", attrs={"data-test": "jd-info-location"})
        location = location_tag.get_text(strip=True) if location_tag else "Lokalita nenalezena"
        
        job_body_tag = soup.find("div", attrs={"data-test": "jd-body-richtext"})
        if job_body_tag:
            job_body = job_body_tag.get_text(strip=True)
            # Odstranění "Pracovní nabídka" z začátku textu
            job_body = job_body.replace("Pracovní nabídka", "").strip()
        else:
            job_body = "Detail pozice nenalezen"
        
        contact_name_tag = soup.find("a", class_="link-primary text-primary", attrs={"data-test": "jd-contact-company"})
        contact_name = contact_name_tag.get_text(strip=True) if contact_name_tag else "Kontaktní osoba nenalezena"
        
        contact_phone_tag = soup.find("p", attrs={"data-test": "jd-contact-phone"})
        contact_phone = contact_phone_tag.get_text(strip=True) if contact_phone_tag else "Telefon nenalezen"
        
        return {
            "title": job_title,
            "company": company_name,
            "location": location,
            "description": job_body,
            "contact": contact_name,
            "phone": contact_phone
        }
    return None

def save_job_to_file(job_data, file):
    file.write(job_data['title'])
    file.write(f"Firma: {job_data['company']}\n")
    file.write(f"Lokalita: {job_data['location']}\n")
    file.write("Detail pozice:\n")
    
    # Zalamování dlouhého textu na více řádků s odsazením
    wrapped_description = textwrap.fill(job_data['description'], 
                                      width=80,  # Maximální šířka řádku
                                      initial_indent="  ",  # Odsazení prvního řádku
                                      subsequent_indent="  "  # Odsazení dalších řádků
                                      )
    file.write(f"{wrapped_description}\n")
    
    file.write(f"Kontakt: {job_data['contact']}\n")
    file.write(f"Telefon: {job_data['phone']}\n")
    file.write("-" * 80 + "\n\n")

def scrape_jobs():
    url = "https://www.jobs.cz/prace/python-vyvojar/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("article", class_="SearchResultCard")
        
        os.makedirs("Scrap_projekt", exist_ok=True)
        
        with open("Scrap_projekt/jobs.txt", "w", encoding="utf-8") as file:
            for job in job_cards:
                link_tag = job.find("a", class_="SearchResultCard__titleLink", href=True)
                if link_tag and link_tag.get("href"):
                    job_url = link_tag["href"]
                    if not job_url.startswith("http"):
                        job_url = "https://www.jobs.cz" + job_url
                    
                    job_data = scrape_job_detail(job_url)
                    if job_data:
                        save_job_to_file(job_data, file)
        
        print("Data byla úspěšně uložena do souboru 'Scrap_projekt/jobs.txt'")
    else:
        print(f"Chyba při načítání stránky: {response.status_code}")

if __name__ == "__main__":
    scrape_jobs()
