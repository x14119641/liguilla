# Scrip "liguilla"

Scrip para generar los datos de los jugadores para la liguilla desde transfermarkt.es, el formato que queremos y la data es:
`pos;name;pais1;pais2;num;edad;`
Cuando se lanza el script por ligas o batches se añade el nombre del equipo:
`pos;name;pais1;pais2;num;edad;team_name;`


Como funciona:
```
# Basico: Extrae data por id del equipo
python main.py team --team-id 418 # output exports/418.csv
# Con nombre del eqipo para cambiar el nombre del output
python main.py team --team-id 418 --team-name olympiacos # output exports/olympiacos.csv

# Con argumentos como season (default = 2025) 
python main.py team --team-id 418 --season 2024 

# Liga completa
python main.py league --competition-id ES1

# Liga completa con otra temporada y con otro delay
python main.py league --competition-id ES1 --season 2024 --delay 3

# Predifined batches
python main.py batch --batch-name other
python main.py batch --batch-name missing

```


# Las ligas (y sus codigos)
```
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
```

# Otros equipos (sacamos los codigos manualmente)
```
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

ISSING_TEAMS = [
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

```
