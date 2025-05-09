"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Radek Neckař
email: neckar@plastika.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    """Vrátí BeautifulSoup objekt ze zadané URL."""
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit(f"Chyba při stahování URL: {url}")
    return BeautifulSoup(response.text, 'html.parser')


def get_obec_links(main_url):
    """Vrátí seznam URL všech obcí z daného územního celku."""
    soup = get_soup(main_url)
    links = soup.select('td.cislo a')
    return ['https://www.volby.cz/pls/ps2017nss/' + link['href'] for link in links]


def get_obec_data(url):
    """Získá a vrátí volební data pro jednu obec jako slovník."""
    soup = get_soup(url)

    # Získání kódu obce z URL
    code = url.split('=')[-1]

    # Získání názvu obce (druhý nadpis <h3>)
    name_heading = soup.find_all('h3')
    name = name_heading[1].text.strip() if len(name_heading) > 1 else "Neznámá obec"

    # Základní statistiky (voliči, obálky, platné hlasy)
    tds = soup.select('td')
    registered = int(tds[3].text.replace('\xa0', '').replace(' ', ''))
    envelopes = int(tds[4].text.replace('\xa0', '').replace(' ', ''))
    valid = int(tds[7].text.replace('\xa0', '').replace(' ', ''))

    # Hlasy pro jednotlivé strany
    parties = [td.text.strip() for td in soup.select('td.overflow_name')]
    vote_cells = soup.select('td.number.right')
    votes = [int(td.text.replace('\xa0', '').replace(' ', '')) for td in vote_cells if td.text.strip().isdigit()]

    # Složení dat do slovníku
    data = {
        'code': code,
        'location': name,
        'registered': registered,
        'envelopes': envelopes,
        'valid': valid,
    }

    for party, vote in zip(parties, votes):
        data[party] = vote

    return data


def main():
    # Kontrola argumentů
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL> <výstupní_soubor.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_filename = sys.argv[2]

    if "xjazyk=CZ" not in input_url:
        print("Neplatný odkaz. Zkontroluj URL.")
        sys.exit(1)

    print("Stahuji data, chvíli strpení...")

    # Získání odkazů na obce
    links = get_obec_links(input_url)

    # Získání dat z jednotlivých obcí
    all_data = [get_obec_data(link) for link in links]

    # Převedení do DataFrame a export do .csv se středníkem pro Excel
    df = pd.DataFrame(all_data)
    df.to_csv(output_filename, index=False, encoding='utf-8-sig', sep=';')

    print(f"Hotovo! Data uložena do souboru: {output_filename}")


if __name__ == "__main__":
    main()
