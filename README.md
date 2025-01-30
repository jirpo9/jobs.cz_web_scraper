# Jobs.cz Python Developer Scraper

Tento nástroj je určen pro automatické získávání pracovních nabídek pro Python vývojáře z portálu Jobs.cz. Skript automaticky prochází nabídky práce, extrahuje detailní informace o každé pozici a ukládá je do strukturovaného textového souboru.

## Hlavní funkce

- Automatické procházení stránek s nabídkami práce
- Detekce a přeskakování duplicitních nabídek
- Extrakce detailních informací o každé pozici včetně:
  - Názvu pozice
  - Jména společnosti
  - Popisu pozice
  - Kontaktních informací
  - Telefonního čísla
- Paralelní zpracování pro rychlejší běh
- Ukládání dat do čitelného formátu
- Ošetření chybových stavů a logování

## Požadavky

```
requests
beautifulsoup4
selenium
webdriver-manager
```

## Instalace

1. Naklonujte tento repozitář:
```bash
git clone [URL vašeho repozitáře]
```

2. Přejděte do adresáře projektu:
```bash
cd [název-adresáře]
```

3. Nainstalujte potřebné závislosti:
```bash
pip install -r requirements.txt
```

## Použití

Spusťte skript příkazem:
```bash
python scraper.py
```

Skript vytvoří soubor `jobs.txt` v aktuálním adresáři, který bude obsahovat všechny nalezené pracovní nabídky.

## Struktura výstupu

Každá pracovní nabídka je v souboru oddělena oddělovačem a obsahuje následující informace:
- Název pozice
- Jméno společnosti
- Lokalitu
- Detailní popis pozice
- Kontaktní osobu
- Telefonní číslo

## Funkce proti duplicitám

Skript používá hashování pro detekci duplicitních nabídek a přeskakuje již existující pozice. Toto zajišťuje, že se stejná nabídka práce neuloží vícekrát.

## Logování

Skript poskytuje detailní logování procesu scrapování, včetně:
- Informací o začátku scrapování každé stránky
- Počtu nalezených pracovních nabídek
- Chybových hlášení
- Statistik o duplicitních nabídkách

## Omezení

- Skript je nastaven na procházení maximálně 10 stránek výsledků
- Je implementováno zpoždění mezi požadavky pro simulaci lidského chování
- V případě nedostupnosti BeautifulSoup parseru se automaticky přepne na Selenium

## Přispívání

Pokud chcete přispět k vývoji, postupujte následovně:
1. Forkněte repozitář
2. Vytvořte novou větev pro vaše změny
3. Commitněte vaše změny
4. Vytvořte Pull Request

## Licence

[Doplňte vaši licenci]

## Autor

[Vaše jméno/kontakt]

## Poznámky

- Skript používá headless prohlížeč pro scrapování
- Implementováno ošetření různých formátů stránek s detaily pozic
- Obsahuje mechanismy pro detekci konce výsledků
