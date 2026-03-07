import requests
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

def get_data_transfermarket(id: int, season:int=2025) -> bytes:
    url = f"https://www.transfermarkt.es/-/kader/verein/{id}/saison_id/{season}/plus/1"
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    r.raise_for_status()
    return r.content

def get_team_page_transfermarkt(competition_id: str) ->bytes:
    url = f"https://www.transfermarkt.es/-/startseite/wettbewerb/{competition_id}"
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=30, allow_redirects=True)
    r.raise_for_status()
    return r.content


def get_team_ids_info_to_list_of_dicts(competition_id) -> List[dict[str,str]]:
    data = get_team_page_transfermarkt(competition_id)
    result = []
    tree = html.fromstring(data)
    hrefs = tree.xpath('//td[contains(@class,"hauptlink")]/a[contains(@href,"/verein/")]/@href')
    for href in hrefs:
        # print(href)
        # example: /fc-augsburg/startseite/verein/167/saison_id/2025
        result.append(
            {"team_id":href.split("/")[4],
            "team": href.split("/")[1].replace("1-", "").replace("-", "_"), 
            }
        )
    # print(result)
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
        position = row.xpath('normalize-space(.//td[contains(@class,"posrela")]//tr[last()]/td[1])')
        
        # player name: better from the link/title in hauptlink
        name = row.xpath('string((.//td[contains(@class,"hauptlink")]//a)[1]/@title)')
        if not name:
            name = row.xpath('normalize-space((.//td[contains(@class,"hauptlink")]//a)[1])')

        
        nationality = row.xpath('string((.//img[contains(@class,"flaggenrahmen")])[1]/@title)')
        
        age_cell = row.xpath(".//td[contains(@class,'zentriert')][contains(normalize-space(.),'/') and contains(normalize-space(.),'(')]/text()")[0]
        age_date = age_cell.split("(")[0].strip()
        

        num = row.xpath('normalize-space(.//div[contains(@class,"rn_nummer")])')

        result.append({
            "pos": position, "name":name, "pais":nationality, "num":num, "edad": age_date, 
        })
        
    return result


def get_squad_by_id(team_id:int, team_name:str=None, league:str=None):
    out_dir = Path("exports")

    if league:
        out_dir= out_dir / league
    out_dir.mkdir(parents=True, exist_ok=True)
    if team_name:
        out_path = out_dir / f"{team_name}.csv"
    else:
        out_path =  out_path = out_dir / f"{team_id}.csv"
        
    data = get_data_transfermarket(team_id)
    result = get_players_info_to_list_of_dicts(data)
    # for item in result:
    #     print(item)
    
    df = pd.DataFrame(data=result, columns=["pos","name","pais","num","edad"])
    df.to_csv(out_path,sep=";", index=False,  encoding="utf-8-sig")
    
    print(f"Saved team {team_id}")

def main(league:str):
    if not league:
        print("Needs league 'str' to continue")
        return
    
    team_ids = get_team_ids_info_to_list_of_dicts(league)
    
    if team_ids:
        for team in team_ids:
            get_squad_by_id(team_id=team["team_id"], team_name = team["team"], league=league)
            sleep(3)
    
    
    
if  __name__ ==  "__main__":
    try:
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
        main(league="RU1")
        
        
        #  One team if i know the id
        # get_squad_by_id(738)
        # get_squad_by_id(131, "barcelona")
    except Exception as e:
        print(str(e))
    