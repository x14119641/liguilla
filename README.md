# Scrip "liguilla"

Scrip para generar los datos de los jugadores para la liguilla desde transfermarkt.es, el formato que queremos y la data es:
`pos;name;pais;num;edad`

El script funciona "manualmente", se ha de cambiar las llamadas en el main. Se podria añadir que el script funcionase por "args" pero de momento asi me esta bien.

Como funciona:
```
# Busca los equipos de la liga a traves del codigo y  por cada equipo extrae la data de los jugadores
main(league="RU1")

# Solo queremos los datos de un equipo si sabemos el codigo (to csv)
# (mejor si le añadimos como argumento extra el nombre del equipo, esto guardara el csv con el nombre en vez de la id)
get_squad_by_id_to_csv(131)
get_squad_by_id_to_csv(131, "barcelona")
```

Los datos son guardados en `/exports/{codigo_liga}/{codigo_liga}.csv`
Si el script es llamado para un equipo por id estara e `/exports/{codigo_o_nombre_equipo}.csv`

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
other_teams = [
        {"id": 197, "club": "ac_sparta_praga"},
        {"id": 697, "club": "slovan_liberec"},
        {"id": 941, "club": "viktoria_plzen"},
        {"id": 62, "club": "sk_slavia_praga"},
        {"id": 501, "club": "fk_bodo_glimt"},
        {"id": 687, "club": "molde_fk"},
        {"id": 1091, "club": "paok_de_salonica"},
        {"id": 2441, "club": "aek_athenas"},
        {"id": 105461, "club": "olympiacos_fc"},
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
```
