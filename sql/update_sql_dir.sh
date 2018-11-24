#!/bin/bash
MYUSER=${1:-postgres}
MYPORT=${2:-5432}
MYHOST=${3:-127.0.0.1}
DATABASE=${4:-didyoureadme}

echo "Debe ejecutarse desde el directorio sql"
pg_dump --no-privileges  -s -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE > didyoureadme.sql

echo "COPY public.groups (id, name, members) FROM stdin;" >> didyoureadme.sql
echo "1	Todos	\N" >> didyoureadme.sql
echo "\." >> didyoureadme.sql
echo "SELECT pg_catalog.setval('public.posts_id_seq', 8, true);" >> didyoureadme.sql

echo "CREATE ROLE didyoureadme_user;" >> didyoureadme.sql
echo "CREATE ROLE didyoureadme_admin;" >> didyoureadme.sql


NOTALL="SELECT, INSERT, UPDATE, DELETE"
NOTALLSEQ="SELECT, UPDATE"

echo "REVOKE ALL ON SCHEMA public FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON SCHEMA public FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON SCHEMA public FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON SCHEMA public FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON SCHEMA public TO postgres; " >> didyoureadme.sql
echo "GRANT ALL ON SCHEMA public TO PUBLIC; " >> didyoureadme.sql

echo "REVOKE ALL ON TABLE public.documents FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.documents FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.documents FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.documents FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON TABLE public.documents TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.documents TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.documents TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON SEQUENCE public.documents_id_seq FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.documents_id_seq FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.documents_id_seq FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.documents_id_seq FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON SEQUENCE public.documents_id_seq TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.documents_id_seq TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.documents_id_seq TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON TABLE public.globals FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.globals FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.globals FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.globals FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON TABLE public.globals TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.globals TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.globals TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON TABLE public.groups FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.groups FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.groups FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.groups FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON TABLE public.groups TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.groups TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.groups TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON SEQUENCE public.posts_id_seq FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.posts_id_seq FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.posts_id_seq FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.posts_id_seq FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON SEQUENCE public.posts_id_seq TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.posts_id_seq TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.posts_id_seq TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON TABLE public.userdocuments FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.userdocuments FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.userdocuments FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.userdocuments FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON TABLE public.userdocuments TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.userdocuments TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.userdocuments TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON TABLE public.users FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.users FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.users FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON TABLE public.users FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON TABLE public.users TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.users TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALL ON TABLE public.users TO didyoureadme_admin; " >> didyoureadme.sql

echo "REVOKE ALL ON SEQUENCE public.users_id_seq FROM PUBLIC; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.users_id_seq FROM postgres; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.users_id_seq FROM didyoureadme_user; " >> didyoureadme.sql
echo "REVOKE ALL ON SEQUENCE public.users_id_seq FROM didyoureadme_admin; " >> didyoureadme.sql
echo "GRANT ALL ON SEQUENCE public.users_id_seq TO postgres; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.users_id_seq TO didyoureadme_user; " >> didyoureadme.sql
echo "GRANT $NOTALLSEQ ON SEQUENCE public.users_id_seq TO didyoureadme_admin; " >> didyoureadme.sql

pg_dump -a -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE -t globals --insert >> didyoureadme.sql

