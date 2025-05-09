# 🗳 Elections Scraper – Projekt 3

Tento projekt slouží k automatickému stažení výsledků voleb do Poslanecké sněmovny ČR z roku 2017. Na základě vstupního odkazu (např. okres Prostějov) stáhne data o všech obcích v daném územním celku a uloží je do `.csv` souboru.

---

## 🛠 Požadavky

Projekt využívá tyto knihovny:

- `requests`
- `beautifulsoup4`
- `pandas`

---

## 🧪 Instalace (Windows)

1. Otevři složku s projektem v **příkazovém řádku (CMD)**

2. Vytvoř virtuální prostředí:
python -m venv venv

3. Aktivuj prostředí:
venv\Scripts\activate

4. Nainstaluj knihovny:


pip install -r requirements.txt
Spuštění
Skript spustíš pomocí dvou argumentů:
python main.py "<URL na územní celek>" "<výstupní_soubor.csv>"

Kde vzít správný odkaz (URL)?
Otevři stránku:
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Klikni na požadovaný kraj
Pak klikni na okres
Jakmile se zobrazí seznam obcí, zkopíruj URL z prohlížeče

Např. pro okres Prostějov bude odkaz vypadat takto:
https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

Příklad spuštění:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"

 Výstup
CSV soubor bude obsahovat:

code – kód obce

location – název obce

registered – počet voličů v seznamu

envelopes – vydané obálky

valid – platné hlasy

