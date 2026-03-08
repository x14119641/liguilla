import requests
import re
import pandas as pd
from lxml import html
from typing import List
from pathlib import Path
from time import sleep


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.transfermarkt.es/",
}


def get_data_transfermarket(id: int, season: int = 2025) -> bytes:
    url = f"https://www.transfermarkt.es/-/kader/verein/{id}/saison_id/{season}/plus/1"
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    r.raise_for_status()
    return r.content


def get_team_page_transfermarkt(competition_id: str, season_id:int=2025) -> bytes:
    url = f"https://www.transfermarkt.es/-/startseite/wettbewerb/{competition_id}/plus/?saison_id={season_id}"
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=30, allow_redirects=True)
    r.raise_for_status()
    return r.content


def get_team_ids_info_to_list_of_dicts(competition_id) -> List[dict[str, str]]:
    data = get_team_page_transfermarkt(competition_id)
    result = []
    tree = html.fromstring(data)
    hrefs = tree.xpath('//td[contains(@class,"hauptlink")]/a[contains(@href,"/verein/")]/@href')

    for href in hrefs:
        # print(href)
        # example: /fc-augsburg/startseite/verein/167/saison_id/2025
        match = re.search(r"/([^/]+)/startseite/verein/(\d+)", href)
        if not match:
            print(f"Skipping malformed href: {href}")
            continue

        team_slug = match.group(1)
        team_id = int(match.group(2))

        result.append({
            "team_id": team_id,
            "team": team_slug.replace("1-", "").replace("-", "_"),
        })
    print(result)
    return result


def first_or_empty(xs) -> str:
    return xs[0].strip() if xs else ""


def get_players_info_to_list_of_dicts(data):
    result = []
    tree = html.fromstring(data)

    table = tree.xpath('(//table[contains(@class,"items")])[1]')
    if not table:
        print("No table found")
        return
    table = table[0]

    rows = table.xpath(".//tbody/tr[td]")
    
    for row in rows:
        # print(row)
        position = row.xpath(
            'normalize-space(.//td[contains(@class,"posrela")]//tr[last()]/td[1])'
        )

        # player name: better from the link/title in hauptlink
        name = row.xpath('string((.//td[contains(@class,"hauptlink")]//a)[1]/@title)')
        if not name:
            name = row.xpath(
                'normalize-space((.//td[contains(@class,"hauptlink")]//a)[1])'
            )

        nationality = row.xpath(
            'string((.//img[contains(@class,"flaggenrahmen")])[1]/@title)'
        )

        # Hay gente que no tiene "edad"
        age_nodes = row.xpath(".//td[contains(@class,'zentriert')][contains(normalize-space(.),'/') and contains(normalize-space(.),'(')]/text()")
        age_date = age_nodes[0].split("(")[0].strip() if age_nodes else ""

        num = row.xpath('normalize-space(.//div[contains(@class,"rn_nummer")])')

        result.append(
            {
                "pos": position,
                "name": name,
                "pais": nationality,
                "num": num,
                "edad": age_date,
            }
        )

    return result


def get_squad_by_id_to_csv(team_id: int, team_name: str = None, league: str = None):
    out_dir = Path("exports")

    if league:
        out_dir = out_dir / league
    out_dir.mkdir(parents=True, exist_ok=True)
    if team_name:
        out_path = out_dir / f"{team_name}.csv"
    else:
        out_path = out_path = out_dir / f"{team_id}.csv"

    data = get_data_transfermarket(team_id)
    result = get_players_info_to_list_of_dicts(data)
    # for item in result:
    #     print(item)

    df = pd.DataFrame(data=result, columns=["pos", "name", "pais", "num", "edad"])
    df.to_csv(out_path, sep=";", index=False, encoding="utf-8-sig")

    print(f"Saved team {team_id}")



def get_squad_by_id(team_id: int):
    data = get_data_transfermarket(team_id)
    result = get_players_info_to_list_of_dicts(data)
    # for item in result:
    #     print(item)

    return result
    
    
def main(league: str):
    if not league:
        print("Needs league 'str' to continue")
        return

    out_dir = Path("exports")
    out_dir = out_dir / league
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{league}.csv"
    
    team_ids = get_team_ids_info_to_list_of_dicts(league)

    all_data = []
    if team_ids:
        for team in team_ids:
            data = get_squad_by_id(
                team_id=team["team_id"]
            )
            if data:
                all_data.extend(data)
            sleep(3)
    
    df = pd.DataFrame(data=all_data, columns=["pos", "name", "pais", "num", "edad"])
    df.to_csv(out_path, sep=";", index=False, encoding="utf-8-sig")


def run_other_teams():
    other_teams = [
        {"id": 197, "club": "ac_sparta_praga"},
        {"id": 697, "club": "slovan_liberec"},
        {"id": 941, "club": "viktoria_plzen"},
        {"id": 62, "club": "sk_slavia_praga"},
        {"id": 501, "club": "fk_bodo_glimt"},
        {"id": 687, "club": "molde_fk"},
        {"id": 1091, "club": "paok_de_salonica"},
        {"id": 2441, "club": "aek_athenas"},
        {"id": 683, "club": "olympiacos_el_pireo"},
        {"id": 265, "club": "panathinaikos_fc"},
        {"id": 409, "club": "red_bull_salzburgo"},
        {"id": 413, "club": "lask"},
        {"id": 170, "club": "sk_rapid_viena"},
        {"id": 122, "club": "sk_sturm_graz"},
        {"id": 2300, "club": "jagiellonia_bialystok"},
        {"id": 238, "club": "lech_poznan"},
        {"id": 255, "club": "legia_de_varsovia"},
        {"id": 2976, "club": "hapoel_beer_sheva"},
        {"id": 1064, "club": "maccabi_haifa"},
        {"id": 119, "club": "maccabi_tel_aviv"},
        {"id": 2784, "club": "apoel_fc"},
        {"id": 829, "club": "omonia_nicosia"},
        {"id": 1044, "club": "djurgardens_if"},
        {"id": 496, "club": "malmoe_ff"},
        {"id": 419, "club": "gnk_dinamo_zagreb"},
        {"id": 159, "club": "estrella_roja_de_belgrado"},
        {"id": 10690, "club": "zorya_lugansk"},
        {"id": 660, "club": "shakhtar_donetsk"},
        {"id": 338, "club": "fc_dynamo_kyiv"},
        {"id": 279, "club": "ferencvaros_tc"},
        {"id": 301, "club": "fcsb"},
        {"id": 540, "club": "slovan_bratislava"},
        {"id": 31614, "club": "ludogorets_razgrad"},
        {"id": 10625, "club": "qarabag_fk"},
        {"id": 2481, "club": "fc_sheriff_tiraspol"},
        {"id": 22220, "club": "fc_astana"},
    ]
    for team in other_teams:
        get_squad_by_id_to_csv(team["id"], team["club"])
        sleep(5)
    print("other teams finished")



def run_missing_teams():
    missing_teams = [
        {"id": 41274, "club": "Beerschot VA", "league": "BE1"},
        {"id": 601, "club": "KV Kortrijk", "league": "BE1"},
        {"id": 1245, "club": "KAS Eupen", "league": "BE1"},
        {"id": 54189, "club": "RWDM Brussels", "league": "BE1"},
        {"id": 1053, "club": "Aalborg BK", "league": "DK1"},
        {"id": 369, "club": "Lyngby Boldklub", "league": "DK1"},
        {"id": 1124, "club": "Fakel Voronezh", "league": "RU1"},
        {"id": 11127, "club": "Ural Ekaterimburgo", "league": "RU1"},
        {"id": 2759, "club": "Ross County FC", "league": "SC1"},
        {"id": 2578, "club": "St. Johnstone FC", "league": "SC1"},
        {"id": 3840, "club": "Adana Demirspor", "league": "TR1"},
        {"id": 44006, "club": "Bodrum FK", "league": "TR1"},
        {"id": 7775, "club": "Hatayspor", "league": "TR1"},
        {"id": 2381, "club": "Sivasspor", "league": "TR1"},
        {"id": 924, "club": "Istanbulspor", "league": "TR1"},
        {"id": 1090, "club": "AZ Alkmaar", "league": "NL1"},
    ]
    for team in missing_teams:
        get_squad_by_id_to_csv(team["id"], team["club"], league=team["league"])
        sleep(5)
    print("missing teams finished")
    
    
if __name__ == "__main__":
    try:
        # England = "GB1"
        # Bundesliga = "L1"
        # Ligue 1 = "FR1"
        # Eredivisie = "NL1"
        # Portugal = "PO1"
        # Belguica = "BE1"
        # Turquia = "TR1"
        # Escocia = "SC1"
        # Dinamarca = "DK1"
        # Suiza = "C1"
        # Rusia = "RU1"
        # Italia = "IT1"
        
        # España 1a division = "ES1"
        # Segunda española = "ES2"
        # Grupo 1 RFEF = "E3G1"
        # Grupo 1 RFEF = "E3G2"
        
        main(league="GB1")
        
        # run_other_teams()
        # run_missing_teams()

        #  One team if i know the id (to csv)
        # get_squad_by_id(738)
        # get_squad_by_id_to_csv(1091, "paok_de_salonica")
        # {"id": 683, "club": "olympiacos_el_pireo"},
        # get_squad_by_id_to_csv(683, "olympiacos_el_pireo")
    except Exception as e:
        print(str(e))
