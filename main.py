"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Radek Neckař
email: neckar@plastika.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Výchozí URL pro OKRES JESENÍK
URL_3 = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101'
DEFAULT_OUTPUT = 'vysledky.csv'


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
    # Pro úplné zobrazení stran přidáme parametr xf=1 pokud je dostupný
    soup = get_soup(url)
    if soup.find('a', string=lambda t: t and 'úplné zobrazení' in t):
        sep = '&' if '?' in url else '?'
        soup = get_soup(url + sep + 'xf=1')

    # Kód a název obce
    code = url.split('=')[-1]
    headings = soup.find_all('h3')
    name = headings[1].text.strip() if len(headings) > 1 else 'Neznámá obec'

    # Základní statistiky
    stats = soup.find('table')
    tds = stats.find_all('td')
    registered = int(tds[3].text.replace('\xa0', '').replace(' ', ''))
    envelopes = int(tds[4].text.replace('\xa0', '').replace(' ', ''))
    valid = int(tds[7].text.replace('\xa0', '').replace(' ', ''))

    data = {
        'code': code,
        'location': name,
        'registered': registered,
        'envelopes': envelopes,
        'valid': valid,
    }

    # Hlasy stran
    for table in soup.find_all('table'):
        header = table.find('th')
        if header and 'Strana' in header.text:
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) >= 3 and cells[1].text.strip():
                    party = cells[1].text.strip()
                    try:
                        votes = int(cells[2].text.replace('\xa0', '').replace(' ', ''))
                        data[party] = votes
                    except ValueError:
                        continue
            break

    return data


def main():
    # Pokud nebyly předány argumenty, použij výchozí URL a název souboru
    if len(sys.argv) == 1:
        input_url = URL_3
        output_filename = DEFAULT_OUTPUT
    elif len(sys.argv) == 3:
        input_url = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        print(f"Použití: python {sys.argv[0]} [<URL> <výstupní_soubor.csv>]")
        print(f"Nebyl zadán argument, bude použit výchozí: {DEFAULT_OUTPUT}")
        input_url = URL_3
        output_filename = DEFAULT_OUTPUT

    print(f"Stahuji data z: {input_url}")
    links = get_obec_links(input_url)
    all_data = [get_obec_data(link) for link in links]

    df = pd.DataFrame(all_data)
    df.to_csv(output_filename, index=False, encoding='utf-8-sig', sep=';')

    print(f"Hotovo! Data uložena do souboru: {output_filename}")


if __name__ == "__main__":
    main()
