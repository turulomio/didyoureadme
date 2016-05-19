#!/bin/bash
MYUSER=${1:-postgres}
MYPORT=${2:-5432}
MYHOST=${3:-127.0.0.1}
DATABASE=${4:-didyoureadme}

echo "Debe ejecutarse desde el directorio sql"
pg_dump -s -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE --no-owner> didyoureadme.sql

echo "COPY groups (id, name, members) FROM stdin;" >> didyoureadme.sql
echo "1	Todos	\N" >> didyoureadme.sql
echo "\." >> didyoureadme.sql
echo "SELECT pg_catalog.setval('posts_id_seq', 8, true);" >> didyoureadme.sql

pg_dump -a -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE -t globals --insert >> didyoureadme.sql

