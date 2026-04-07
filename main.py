import argparse

import requests
import re
import pandas as pd
from lxml import html
from typing import Any
from pathlib import Path
from time import sleep


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.transfermarkt.es/",
}


DEFAULT_SEASON = 2025
DEFAULT_DELAY_SECONDS = 5
EXPORT_DIR = Path("exports")

OTHER_TEAMS = [
    {"team_id": 197, "team_name": "ac_sparta_praga"},
    {"team_id": 697, "team_name": "slovan_liberec"},
    {"team_id": 941, "team_name": "viktoria_plzen"},
    {"team_id": 62, "team_name": "sk_slavia_praga"},
    {"team_id": 501, "team_name": "fk_bodo_glimt"},
    {"team_id": 687, "team_name": "molde_fk"},
    {"team_id": 1091, "team_name": "paok_de_salonica"},
    {"team_id": 2441, "team_name": "aek_athenas"},
    {"team_id": 683, "team_name": "olympiacos_el_pireo"},
    {"team_id": 265, "team_name": "panathinaikos_fc"},
    {"team_id": 409, "team_name": "red_bull_salzburgo"},
    {"team_id": 413, "team_name": "lask"},
    {"team_id": 170, "team_name": "sk_rapid_viena"},
    {"team_id": 122, "team_name": "sk_sturm_graz"},
    {"team_id": 2300, "team_name": "jagiellonia_bialystok"},
    {"team_id": 238, "team_name": "lech_poznan"},
    {"team_id": 255, "team_name": "legia_de_varsovia"},
    {"team_id": 2976, "team_name": "hapoel_beer_sheva"},
    {"team_id": 1064, "team_name": "maccabi_haifa"},
    {"team_id": 119, "team_name": "maccabi_tel_aviv"},
    {"team_id": 2784, "team_name": "apoel_fc"},
    {"team_id": 829, "team_name": "omonia_nicosia"},
    {"team_id": 1044, "team_name": "djurgardens_if"},
    {"team_id": 496, "team_name": "malmoe_ff"},
    {"team_id": 419, "team_name": "gnk_dinamo_zagreb"},
    {"team_id": 159, "team_name": "estrella_roja_de_belgrado"},
    {"team_id": 10690, "team_name": "zorya_lugansk"},
    {"team_id": 660, "team_name": "shakhtar_donetsk"},
    {"team_id": 338, "team_name": "fc_dynamo_kyiv"},
    {"team_id": 279, "team_name": "ferencvaros_tc"},
    {"team_id": 301, "team_name": "fcsb"},
    {"team_id": 540, "team_name": "slovan_bratislava"},
    {"team_id": 31614, "team_name": "ludogorets_razgrad"},
    {"team_id": 10625, "team_name": "qarabag_fk"},
    {"team_id": 2481, "team_name": "fc_sheriff_tiraspol"},
    {"team_id": 22220, "team_name": "fc_astana"},
]

MISSING_TEAMS = [
    {"team_id": 41274, "team_name": "Beerschot VA", "league": "BE1"},
    {"team_id": 601, "team_name": "KV Kortrijk", "league": "BE1"},
    {"team_id": 1245, "team_name": "KAS Eupen", "league": "BE1"},
    {"team_id": 54189, "team_name": "RWDM Brussels", "league": "BE1"},
    {"team_id": 1053, "team_name": "Aalborg BK", "league": "DK1"},
    {"team_id": 369, "team_name": "Lyngby Boldklub", "league": "DK1"},
    {"team_id": 1124, "team_name": "Fakel Voronezh", "league": "RU1"},
    {"team_id": 11127, "team_name": "Ural Ekaterimburgo", "league": "RU1"},
    {"team_id": 2759, "team_name": "Ross County FC", "league": "SC1"},
    {"team_id": 2578, "team_name": "St. Johnstone FC", "league": "SC1"},
    {"team_id": 3840, "team_name": "Adana Demirspor", "league": "TR1"},
    {"team_id": 44006, "team_name": "Bodrum FK", "league": "TR1"},
    {"team_id": 7775, "team_name": "Hatayspor", "league": "TR1"},
    {"team_id": 2381, "team_name": "Sivasspor", "league": "TR1"},
    {"team_id": 924, "team_name": "Istanbulspor", "league": "TR1"},
    {"team_id": 1090, "team_name": "AZ Alkmaar", "league": "NL1"},
]


def clean_name(value: str) -> str:
    """Cleans string, replaces spaces, guions, slashes, points or more than one underscore with only one underscore
    """
    value = value.strip().lower()
    value = value.replace(" ", "_").replace("-", "_").replace("/", "_")
    value = value.replace(".", "")
    value = re.sub(r"_+", "_", value)
    return value


def create_session() -> requests.Session:
    """Creates request session"""
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    return session


def fetch_page(
    session: requests.Session,
    url: str,
    retries: int = 3,
    retry_delay: int = DEFAULT_DELAY_SECONDS,
) -> bytes:
    """Fetch page from transfermrkt

    Args:
        session (requests.Session): 
        url (str)
        retries (int, optional): Defaults to 3.
        retry_delay (int, optional): Defaults to DEFAULT_DELAY_SECONDS.

    Returns:
        bytes: Page content in Bytes.
    """
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as exc:
            last_error = exc
            print(f"[WARNING] intento {attempt}/{retries}, error: {exc}")
            if attempt < retries:
                sleep(retry_delay)
    raise RuntimeError(f"No se pudo descargar la pagina: {url}") from last_error


def get_team_squad_page(
    session: requests.Session, team_id: int, season: int = DEFAULT_SEASON
) -> bytes:
    """Get team full squad page in Bytes.

    Args:
        session (requests.Session)
        team_id (int)
        season (int, optional): Defaults to DEFAULT_SEASON.

    """
    url = f"https://www.transfermarkt.es/-/kader/verein/{team_id}/saison_id/{season}/plus/1"
    return fetch_page(session=session, url=url)


def get_competition_page(
    session: requests.Session, competition_id: str, season: int = DEFAULT_SEASON
) -> bytes:
    """Gets competition page in Bytes.

    Args:
        session (requests.Session): _description_
        competition_id (str): _description_
        season (int, optional): _description_. Defaults to DEFAULT_SEASON.

    """
    url = f"https://www.transfermarkt.es/-/startseite/wettbewerb/{competition_id}/plus/?saison_id={season}"
    return fetch_page(session=session, url=url)


def parse_competition_teams(page_content: bytes) -> list[dict[str, Any]]:
    """Parse competition page to get urls for every team.

    Args:
        page_content (bytes)

    Returns:
        list[dict[str, Any]]: [{team_id:"example", "team_name": "team_name_example"}]
    """
    tree = html.fromstring(page_content)
    hrefs = tree.xpath(
        '//td[contains(@class,"hauptlink")]/a[contains(@href,"/verein/")]/@href'
    )

    teams: list[dict[str, Any]] = []
    seen_team_ids = set()

    for href in hrefs:
        # print(href)
        # example: /fc-augsburg/startseite/verein/167/saison_id/2025
        match = re.search(r"/([^/]+)/startseite/verein/(\d+)", href)
        if not match:
            print(f"[WARNING] Skipping malformed href: {href}")
            continue

        team_slug = match.group(1)
        team_id = int(match.group(2))
        if team_id in seen_team_ids:
            continue
        seen_team_ids.add(team_id)
        teams.append(
            {
                "team_id": team_id,
                "team_name": clean_name(team_slug),
            }
        )

    return teams


def parse_players(page_content: bytes) -> list[dict[str, str]]:
    """Parse full squad players data

    Args:
        page_content (bytes)

    Returns:
        list[dict[str, str]]: [{
                "pos": "Portero",
                "name": "Bla,
                "pais1": "Spain",
                "pais2": "Ecuador",
                "num": 12,
                "edad": "02/05/1980,
            },]
    """
    tree = html.fromstring(page_content)
    table = tree.xpath('(//table[contains(@class,"items")])[1]')

    if not table:
        print("[WARNING] No table found")
        return []

    rows = table[0].xpath(".//tbody/tr[td]")
    players: list[dict[str, str]] = []

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

        nationality1 = row.xpath(
            'string((.//img[contains(@class,"flaggenrahmen")])[1]/@title)'
        )

        nationality2 = row.xpath(
            'string((.//img[contains(@class,"flaggenrahmen")])[2]/@title)'
        )

        # Hay gente que no tiene "edad"
        age_nodes = row.xpath(
            ".//td[contains(@class,'zentriert')][contains(normalize-space(.),'/') and contains(normalize-space(.),'(')]/text()"
        )
        age_date = age_nodes[0].split("(")[0].strip() if age_nodes else ""

        num = row.xpath('normalize-space(.//div[contains(@class,"rn_nummer")])')

        players.append(
            {
                "pos": position.strip(),
                "name": name.strip(),
                "pais1": nationality1.strip(),
                "pais2": nationality2.strip(),
                "num": num.strip(),
                "edad": age_date.strip(),
            }
        )
    return players


def save_df_to_csv(df: pd.DataFrame, output_path: Path) -> Path:
    """Saves df to csv ouput path"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, sep=";", index=False, encoding="utf-8-sig")
    return output_path


def get_team_squad(
    session: requests.Session, team_id: int, season: int = DEFAULT_SEASON
) -> list[dict[str, str]]:
    """Gets players data from full squad page for a team id url"""
    page_content = get_team_squad_page(session=session, team_id=team_id, season=season)
    return parse_players(page_content)


def export_team_squad(
    session: requests.Session,
    team_id: int,
    team_name: str | None = None,
    season: int = DEFAULT_SEASON,
) -> Path:
    """Saves players data for a team by team_id and stores as csv with the team_id or the team_name variable if this one exists"""
    players = get_team_squad(session=session, team_id=team_id, season=season)

    if not players:
        raise ValueError(f"No players found for team {team_id}")

    output_name = clean_name(team_name) if team_name else str(team_id)

    df = pd.DataFrame(players, columns=["pos", "name", "pais1", "pais2", "num", "edad"])

    output_path = EXPORT_DIR / f"{output_name}.csv"
    save_df_to_csv(df, output_path)
    print(f"[OK] Team Saved: {team_id} -> {output_path}")
    return output_path


def export_competition_squad(
    session: requests.Session,
    competition_id: str,
    season: int = DEFAULT_SEASON,
    delay_seconds: int = DEFAULT_DELAY_SECONDS,
) -> Path:
    """Saves all competition players data by competition_id and year"""
    competition_page = get_competition_page(
        session=session, competition_id=competition_id, season=season
    )
    teams = parse_competition_teams(competition_page)

    if not teams:
        raise ValueError(f"No teams found for competition {competition_id}")

    df = build_batch_teams_df(
        session=session, teams=teams, season=season, delay_seconds=delay_seconds
    )
    output_path = EXPORT_DIR / f"{competition_id}.csv"
    save_df_to_csv(df, output_path=output_path)
    print(f"[OK] League saved: {competition_id} -> {output_path}")
    return output_path


def export_batch(
    session: requests.Session,
    teams: list[dict[str, Any]],
    name: str,
    season: int = DEFAULT_SEASON,
    delay_seconds: int = DEFAULT_DELAY_SECONDS,
) -> Path:
    """Saves dataframe of a list of players"""
    df = build_batch_teams_df(
        session=session, teams=teams, season=season, delay_seconds=delay_seconds
    )
    output_path = EXPORT_DIR / f"{name}.csv"
    save_df_to_csv(df, output_path=output_path)
    print(f"[OK] Batch saved: {name} -> {output_path}")
    return output_path


def build_batch_teams_df(
    session: requests.Session,
    teams: list[dict[str, Any]],
    season: int = DEFAULT_SEASON,
    delay_seconds: int = DEFAULT_DELAY_SECONDS,
) -> pd.DataFrame:
    """Builds dataframe for a list of teams by season"""
    total = len(teams)

    all_players: list[dict[str, str]] = []

    for idx, team in enumerate(teams, start=1):
        print(f"[{idx}/{total}] Downloading {team['team_name']} ({team['team_id']})")
        players = get_team_squad(session, team_id=team["team_id"], season=season)
        for player in players:
            player["team_name"] = clean_name(team["team_name"])
        all_players.extend(players)
        sleep(delay_seconds)

    df = pd.DataFrame(
        all_players, columns=["pos", "name", "pais1", "pais2", "num", "edad", "team_name"]
    )  

    return df


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple scraper for transfermarkt")

    subparsers = parser.add_subparsers(dest="command")

    team_parser = subparsers.add_parser("team", help="Export a team by id")
    team_parser.add_argument(
        "--team-id", type=int, required=True, help="Team id in transfermakt url"
    )
    team_parser.add_argument("--team-name", type=str, help="Team name to save file")
    team_parser.add_argument(
        "--season", type=int, help="Season number", default=DEFAULT_SEASON
    )

    league_parser = subparsers.add_parser(
        "league", help="Save competition by id (you can find it in the url)"
    )
    league_parser.add_argument(
        "--competition-id", type=str, required=True, help="Ex: ES1, GB1, IT1"
    )
    league_parser.add_argument(
        "--season", type=int, help="Season number", default=DEFAULT_SEASON
    )
    league_parser.add_argument(
        "--delay", type=int, help="Optimal =< 3", default=DEFAULT_DELAY_SECONDS
    )

    batch_parser = subparsers.add_parser("batch", help="Save predefined lists")
    batch_parser.add_argument(
        "--batch-name",
        type=str,
        choices=["other", "missing"],
        required=True,
        help="Exports predifined lists",
    )
    batch_parser.add_argument(
        "--season", type=int, help="Season number", default=DEFAULT_SEASON
    )
    batch_parser.add_argument(
        "--delay", type=int, help="Optimal =< 3", default=DEFAULT_DELAY_SECONDS
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    session = create_session()

    if args.command == "team":
        export_team_squad(
            session=session,
            team_name=args.team_name,
            team_id=args.team_id,
            season=args.season,
        )
        return

    if args.command == "league":
        export_competition_squad(
            session=session,
            competition_id=args.competition_id,
            season=args.season,
            delay_seconds=args.delay,
        )
        return

    if args.command == "batch":
        if args.batch_name == "other":
            export_batch(
                session=session,
                teams=OTHER_TEAMS,
                name=args.batch_name,
                season=args.season,
                delay_seconds=args.delay,
            )
            return
        if args.batch_name == "missing":
            export_batch(
                session=session,
                teams=MISSING_TEAMS,
                name=args.batch_name,
                season=args.season,
                delay_seconds=args.delay,
            )
            return
    parser.print_help()


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
        # Grupo 2 RFEF = "E3G2"

        main()

    except Exception as e:
        print(f"[Error] {str(e)}")
