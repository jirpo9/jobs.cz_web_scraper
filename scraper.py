import requests  # Pro odesílání HTTP požadavků (stahování obsahu webových stránek).
from bs4 import BeautifulSoup  # Pro parsování (analýzu) HTML kódu stažených webových stránek.
import os  # Pro práci se soubory a správu cest k souborům.
import textwrap  # Pro zalamování dlouhých textů na více řádků pro lepší čitelnost.
import hashlib  # Pro hashování dat (pro kontrolu jedinečnosti) 
import logging          
# Knihovna pro logování - zaznamenávání průběhu programu
import random          
# Knihovna pro generování náhodných čísel
from selenium import webdriver                  
# Hlavní nástroj pro ovládání prohlížeče
from selenium.webdriver.common.by import By    
# Třída pro způsoby vyhledávání elementů na stránce
from selenium.webdriver.chrome.service import Service    
# Třída pro správu ChromeDriver služby
from selenium.webdriver.chrome.options import Options    
# Třída pro nastavení Chrome prohlížeče
from selenium.webdriver.support.ui import WebDriverWait  
# Třída pro čekání na elementy
from selenium.webdriver.support import expected_conditions as EC  
# Importuje podmínky pro čekání na elementy
from webdriver_manager.chrome import ChromeDriverManager  
# Importuje správce ChromeDriveru pro automatickou aktualizaci
import time # Knihovna pro práci s časem a prodlevami
import concurrent.futures # Knihovna pro paralelní zpracování
from selenium.common.exceptions import TimeoutException, NoSuchElementException # Importuje specifické výjimky Selenia
logging.basicConfig(# Nastavuje základní konfiguraci logování
    level=logging.INFO,  
    # Nastavuje úroveň logování na INFO (bude zobrazovat všechny INFO zprávy a vyšší)
    format='%(asctime)s - %(levelname)s - %(message)s'  
    # Definuje formát logů: čas - úroveň - zpráva
)
logger = logging.getLogger(__name__)  
# Vytváří logger specifický pro tento modul

def compute_job_hash(job_data):
    """ Vytvoří unikátní hash pro inzerát na základě názvu, firmy a popisu """
    job_string = f"{job_data['title']}{job_data['company']}{job_data.get('description', '')}"
    return hashlib.md5(job_string.encode('utf-8')).hexdigest()

def load_existing_hashes(file_path):
    """ Načte existující hashe ze souboru jobs.txt """
    hashes = set()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("Hash:"):
                    hashes.add(line.strip().split(": ")[1])  # Uloží hash do množiny
    return hashes


def setup_selenium_driver():    
# Definuje funkci pro nastavení webového prohlížeče
    chrome_options = Options()  
    # Vytváří nový objekt pro nastavení Chrome
    chrome_options.add_argument("--headless")  
    # Nastavuje Chrome pro běh bez grafického rozhraní
    chrome_options.add_argument("--no-sandbox")  
    # Vypíná sandbox pro lepší výkon
    chrome_options.add_argument("--disable-dev-shm-usage")  
    # Řeší problémy s pamětí v kontejnerech
    chrome_options.add_argument("--disable-extensions")  
    # Vypíná rozšíření prohlížeče
    chrome_options.add_argument("--disable-plugins")    
    # Vypíná pluginy prohlížeče
    chrome_options.add_argument("--disable-images")     
    # Vypíná načítání obrázků
    chrome_options.page_load_strategy = 'eager'         
    # Nastavuje rychlejší strategii načítání stránek    
    service = Service(ChromeDriverManager().install())  
    # Inicializuje ChromeDriver s automatickou správou verzí
    driver = webdriver.Chrome(service=service, options=chrome_options)  
    # Vytváří instanci ChromeDriveru s nastavenými možnostmi
    return driver  # Vrací instanci ChromeDriveru

def human_like_delay():  # Definuje funkci pro simulaci lidského zpoždění
    time.sleep(random.uniform(1, 2))  # Náhodně čeká mezi 1 a 2 sekundami

def get_page_urls(base_url="https://www.jobs.cz/prace/python-vyvojar/"):  # Definuje funkci pro získání URL stránek
    urls = [base_url]  # Vytváří seznam s výchozí URL
    for page in range(2, 11):  # Pro každou stránku od 2 do 10
        urls.append(f"{base_url}?profession%5B0%5D=201100585&page={page}")  
        # Přidává URL stránky do seznamu
    return urls  # Vrací seznam URL

def scrape_main_page():  # Definuje funkci pro scrapování hlavní stránky
    driver = setup_selenium_driver()  # Nastavuje a inicializuje webdriver
    jobs_data = []  # Vytváří prázdný seznam pro ukládání dat o pracovních pozicích
    seen_urls = set()  # Vytváří prázdnou množinu pro sledování již navštívených URL
    seen_titles = set()  # Vytváří prázdnou množinu pro sledování již zpracovaných titulů
    page_urls = get_page_urls()  # Získává seznam URL stránek
    previous_page_titles = set()  # Vytváří prázdnou množinu pro sledování titulů z předchozí stránky
    
    try:
        for page_num, page_url in enumerate(page_urls, 1):  # Pro každou URL stránky
            logger.info(f"Starting scraping from page {page_num}: {page_url}")  # Loguje začátek scrapování stránky
            driver.get(page_url)  # Načítá stránku
            
            try:
                wait = WebDriverWait(driver, 10)  # Vytváří instanci WebDriverWait s timeoutem 10 sekund
                result_container = wait.until(  # Čeká na přítomnost kontejneru s výsledky
                    EC.presence_of_element_located((By.ID, "search-result-container"))
                )
                
                human_like_delay()  # Simuluje lidské zpoždění
                page_source = driver.page_source  # Získává zdrojový kód stránky
                soup = BeautifulSoup(page_source, "html.parser")  # Parsuje HTML pomocí BeautifulSoup
                
                page_duplicate_count = 0  # Inicializuje počet duplicit na stránce
                new_jobs_on_page = 0  # Inicializuje počet nových pracovních pozic na stránce
                current_page_titles = set()  # Vytváří prázdnou množinu pro sledování titulů na aktuální stránce
                
                job_cards = soup.select("#search-result-container > div.Stack.Stack--hasIntermediateDividers.Stack--hasStartDivider > article")  # Selektuje karty pracovních pozic
                
                if not job_cards:  # Pokud nejsou nalezeny žádné karty pracovních pozic
                    logger.info(f"No job cards found on page {page_num}, stopping pagination")  # Loguje informaci a ukončuje stránkování
                    break
                
                logger.info(f"Found {len(job_cards)} job cards on page {page_num}")  # Loguje počet nalezených karet pracovních pozic
                
                for job in job_cards:  # Pro každou kartu pracovních pozic
                    title_tag = job.select_one("header > h2")  # Selektuje tag s titulem
                    if title_tag:  # Pokud je tag s titulem nalezen
                        job_title = title_tag.get_text(strip=True)  # Získává text titulu
                        current_page_titles.add(job_title)  # Přidává titul do množiny titulů na aktuální stránce
                
                duplicate_with_previous = len(current_page_titles.intersection(previous_page_titles))  # Počítá počet duplicitních titulů s předchozí stránkou
                if duplicate_with_previous > len(current_page_titles) * 0.5:  # Pokud je více než polovina titulů duplicitní
                    logger.info(f"Found {duplicate_with_previous} duplicate jobs from previous page, stopping pagination")  # Loguje informaci a ukončuje stránkování
                    break
                
                for idx, job in enumerate(job_cards, 1):  # Pro každou kartu pracovních pozic
                    try:
                        title_tag = job.select_one("header > h2")  # Selektuje tag s titulem
                        job_title = title_tag.get_text(strip=True) if title_tag else None  # Získává text titulu
                        
                        company_tag = job.select_one("footer > ul > li:nth-child(1) > span")  # Selektuje tag s názvem společnosti
                        company_name = company_tag.get_text(strip=True) if company_tag else None  # Získává text názvu společnosti
                        
                        link_tag = job.find("a", class_="SearchResultCard__titleLink", href=True)  # Selektuje tag s odkazem na detail pozice
                        detail_url = link_tag["href"] if link_tag else None  # Získává URL detailu pozice
                        if detail_url and not detail_url.startswith("http"):  # Pokud URL neobsahuje protokol
                            detail_url = "https://www.jobs.cz" + detail_url  # Přidává protokol k URL
                        
                        if job_title in seen_titles or detail_url in seen_urls:  # Pokud je titul nebo URL již zpracována
                            page_duplicate_count += 1  # Zvyšuje počet duplicit na stránce
                            continue  # Pokračuje na další kartu
                        
                        seen_titles.add(job_title)  # Přidává titul do množiny zpracovaných titulů
                        seen_urls.add(detail_url)  # Přidává URL do množiny zpracovaných URL
                        new_jobs_on_page += 1  # Zvyšuje počet nových pracovních pozic na stránce
                        
                        if job_title and company_name:  # Pokud je titul a název společnosti nalezen
                            jobs_data.append({  # Přidává data o pracovní pozici do seznamu
                                "title": job_title,
                                "company": company_name,
                                "url": detail_url
                            })
                            logger.info(f"Found new job {new_jobs_on_page} on page {page_num}: {job_title} at {company_name}")  # Loguje informaci o nalezené pracovní pozici
                    
                    except Exception as e:  # Pokud nastane výjimka
                        logger.error(f"Error processing job card {idx} on page {page_num}: {str(e)}")  # Loguje chybu
                        continue  # Pokračuje na další kartu
                
                previous_page_titles = current_page_titles  # Aktualizuje množinu titulů z předchozí stránky
                
                if page_duplicate_count >= len(job_cards) * 0.5:  # Pokud je více než polovina karet duplicitní
                    logger.info(f"Found {page_duplicate_count} duplicate jobs out of {len(job_cards)} on page {page_num}, stopping pagination")  # Loguje informaci a ukončuje stránkování
                    break
                
                if new_jobs_on_page == 0:  # Pokud nejsou nalezeny žádné nové pracovní pozice
                    logger.info("No new unique jobs found on this page, stopping pagination")  # Loguje informaci a ukončuje stránkování
                    break
                
                human_like_delay()  # Simuluje lidské zpoždění
                
            except Exception as e:  # Pokud nastane výjimka
                logger.error(f"Error processing page {page_num}: {str(e)}")  # Loguje chybu
                break  # Ukončuje stránkování
                
        logger.info(f"Successfully scraped total of {len(jobs_data)} unique jobs")  # Loguje úspěšné scrapování
        return jobs_data  # Vrací data o pracovních pozicích
        
    except Exception as e:  # Pokud nastane výjimka
        logger.error(f"Error in main scraping process: {str(e)}")  # Loguje chybu
        return []  # Vrací prázdný seznam
        
    finally:
        driver.quit()  # Ukončuje webdriver

def scrape_job_detail(url, existing_data):
    logger.info(f"Starting to scrape job detail: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_data = extract_job_details(soup, existing_data)
            if job_data:
                return job_data  # Pokud se podaří scrapnout přes BeautifulSoup, vrátíme data
    except requests.RequestException as e:
        logger.warning(f"Failed to scrape {url} with BeautifulSoup: {e}, switching to Selenium")
    
    # Pokud BeautifulSoup selže, použijeme Selenium
    driver = setup_selenium_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: any([
            d.find_elements(By.CLASS_NAME, "typography-body-medium-text-regular"),
            d.find_elements(By.CLASS_NAME, "jobad__body"),
            d.find_elements(By.CLASS_NAME, "jobad__content")
        ]))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        return extract_job_details(soup, existing_data)
    except TimeoutException:
        logger.error(f"Timeout while scraping {url} with Selenium")
        return existing_data
    finally:
        driver.quit()

def extract_job_details(soup, existing_data):
    job_data = existing_data.copy()
    
    job_body_tag = (soup.find("div", attrs={"data-test": "jd-body-richtext"}) or
                    soup.find("div", class_="jobad__body") or
                    soup.find("div", class_="jobad__content") or
                    soup.select_one(".jobad__html-content"))
    job_data["description"] = job_body_tag.get_text(strip=True).replace("Pracovní nabídka", "").strip() if job_body_tag else "Detail pozice nenalezen"
    
    contact_name_tag = (soup.find("a", attrs={"data-test": "jd-contact-company"}) or
                         soup.find("div", class_="jobad__contact-person") or
                         soup.select_one("[data-test='jd-contact-name']"))
    job_data["contact"] = contact_name_tag.get_text(strip=True) if contact_name_tag else "Kontaktní osoba nenalezena"
    
    contact_phone_tag = (soup.find("p", attrs={"data-test": "jd-contact-phone"}) or
                          soup.find("div", class_="jobad__contact-phone") or
                          soup.select_one("[data-test='jd-contact-phone']"))
    job_data["phone"] = contact_phone_tag.get_text(strip=True) if contact_phone_tag else "Telefon nenalezen"
    
    return job_data

counter = {"value": 0}
def save_job_to_file(job_data, file, existing_hashes):
    """ Uloží inzerát do souboru pouze pokud ještě neexistuje """
    job_hash = compute_job_hash(job_data)
    
    if job_hash in existing_hashes:
        counter["value"] += 1 
        logger.info(f"Skipping duplicate job: {job_data['title']} at {job_data['company']}")
        return  # Nepřidá inzerát, pokud už existuje

    # Přidáme nový inzerát do souboru
    template = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 {title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 Společnost: {company}

📍 Lokalita: {location}

📋 Detail pozice:

  {description}

👤 Kontakt: {contact}

📞 Telefon: {phone}

"""
    try:
        wrapped_description = textwrap.fill(
            job_data.get('description', 'Detail pozice nenalezen'),
            width=80, initial_indent="  ", subsequent_indent="  "
        )
        
        file.write(template.format(
            title=job_data.get('title', 'Název pozice nenalezen'),
            company=job_data.get('company', 'Firma nenalezena'),
            location=job_data.get('location', 'Lokalita nenalezena'),
            description=wrapped_description,
            contact=job_data.get('contact', 'Kontaktní osoba nenalezena'),
            phone=job_data.get('phone', 'Telefon nenalezen')
        ))
        logger.info(f"Saved new job: {job_data['title']} at {job_data['company']}")
    except Exception as e:
        logger.error(f"Error writing job data to file: {str(e)}")

def scrape_jobs():
    """ Hlavní funkce pro scrapování pracovních pozic s hashováním """
    main_page_jobs = scrape_main_page()
    
    if not main_page_jobs:
        logger.error("No jobs found on main page")
        return

    successful_jobs = []
    file_path = os.path.join(os.getcwd(), "jobs.txt")
    existing_hashes = load_existing_hashes(file_path)  # Načte existující hashe

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        scrape_details = [executor.submit(scrape_job_detail, job['url'], job) for job in main_page_jobs]
        completed_jobs = concurrent.futures.as_completed(scrape_details)

        with open(file_path, "a", encoding="utf-8") as file:  # "a" = append mode
            for future in completed_jobs:
                detailed_job_data = future.result()
                if detailed_job_data:
                    save_job_to_file(detailed_job_data, file, existing_hashes)
                    successful_jobs.append(detailed_job_data)

    logger.info(f"Scraping completed. Successfully scraped {len(successful_jobs)- counter["value"]} jobs, {counter['value']} duplicates skipped.")
    logger.info(f"Data saved to '{file_path}'")

if __name__ == "__main__":  # Pokud je tento skript spuštěn jako hlavní
    scrape_jobs()  # Spouští hlavní funkci pro scrapování pracovních pozic
