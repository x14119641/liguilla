# Scrip "liguilla"

Scrip para generar los datos de los jugadores para la liguilla desde transfermarkt.es, el formato que queremos y la data es:
´´´pos;name;pais;num;edad´´´

El script funciona "manualmente", se ha de cambiar las llamadas en el main. Se podria añadir que el script funcionase por "args" pero de momento asi me esta bien.

Como funciona:
´´´
# Busca los equipos de la liga a traves del codigo y  por cada equipo extrae la data de los jugadores
main(league="RU1")

# Solo queremos los datos de un equipo si sabemos el codigo 
# (mejor si le añadimos como argumento extra el nombre del equipo, esto guardara el csv con el nombre en vez de la id)
get_squad_by_id(131)
get_squad_by_id(131, "barcelona")
´´´

Los datos son guardados en `/exports/{codigo_liga}/{nombre_equipo}.csv`
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
[
  {"id": 197, "club": "ac_sparta_praga"},
  {"id": 697, "club": "slovan_liberec"},
  {"id": 667, "club": "viktoria_plzen"},
  {"id": 266, "club": "sk_slavia_praga"},
  {"id": 2619, "club": "fk_bodo_glimt"},
  {"id": 687, "club": "molde_fk"},
  {"id": 109, "club": "paok_de_salonica"},
  {"id": 2432, "club": "aek_athenas"},
  {"id": 683, "club": "olympiacos"},
  {"id": 1458, "club": "panathinaikos"},
  {"id": 409, "club": "red_bull_salzburgo"},
  {"id": 446, "club": "lask_linz"},
  {"id": 33, "club": "sk_rapid_viena"},
  {"id": 277, "club": "sk_sturm_graz"},
  {"id": 257, "club": "jagiellonia_bialystok"},
  {"id": 1041, "club": "lech_poznan"},
  {"id": 338, "club": "legia_de_varsovia"},
  {"id": 400, "club": "hapoel_beer_sheva"},
  {"id": 1134, "club": "maccabi_haifa"},
  {"id": 754, "club": "maccabi_tel_aviv"},
  {"id": 3512, "club": "apoel_fc"},
  {"id": 3662, "club": "omonia_nicosia"},
  {"id": 433, "club": "djurgardens_if"},
  {"id": 496, "club": "malmoe_ff"},
  {"id": 419, "club": "gnk_dinamo_zagreb"},
  {"id": 159, "club": "estrella_roja_de_belgrado"},
  {"id": 6990, "club": "zorya_lugansk"},
  {"id": 660, "club": "shakhtar_donetsk"},
  {"id": 338, "club": "fc_dynamo_kyiv"},
  {"id": 279, "club": "ferencvaros_tc"},
  {"id": 301, "club": "fcsb"},
  {"id": 1063, "club": "slovan_bratislava"},
  {"id": 316, "club": "ludogorets_razgrad"},
  {"id": 3737, "club": "qarabag_fk"},
  {"id": 18544, "club": "fc_sheriff_tiraspol"},
  {"id": 3783, "club": "fc_astana"}
]
```
