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
