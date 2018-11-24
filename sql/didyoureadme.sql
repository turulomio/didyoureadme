--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: lo_readall(oid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.lo_readall(oid) RETURNS bytea
    LANGUAGE sql STRICT
    AS $_$

SELECT loread(q3.fd, q3.filesize + q3.must_exec) FROM
	(SELECT q2.fd, q2.filesize, lo_lseek(q2.fd, 0, 0) AS must_exec FROM
		(SELECT q1.fd, lo_lseek(q1.fd, 0, 2) AS filesize FROM
			(SELECT lo_open($1, 262144) AS fd)
		AS q1)
	AS q2)
AS q3

$_$;


ALTER FUNCTION public.lo_readall(oid) OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id bigint NOT NULL,
    datetime timestamp with time zone DEFAULT now() NOT NULL,
    title text NOT NULL,
    comment text,
    filename text,
    hash text NOT NULL,
    expiration timestamp with time zone DEFAULT (now() + '3 mons'::interval) NOT NULL,
    fileb bytea
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: globals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.globals (
    global text NOT NULL,
    value text
);


ALTER TABLE public.globals OWNER TO postgres;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    id bigint NOT NULL,
    name text NOT NULL,
    members bigint[]
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.groups.id;


--
-- Name: userdocuments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userdocuments (
    id_users bigint NOT NULL,
    id_documents bigint NOT NULL,
    read timestamp with time zone,
    sent timestamp with time zone,
    numreads bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public.userdocuments OWNER TO postgres;

--
-- Name: COLUMN userdocuments.read; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.userdocuments.read IS 'First time user read';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    datetime timestamp with time zone DEFAULT now() NOT NULL,
    name text,
    mail text NOT NULL,
    hash text NOT NULL,
    post text,
    active boolean NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: documents documents_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pk PRIMARY KEY (id);


--
-- Name: globals globals_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.globals
    ADD CONSTRAINT globals_pk PRIMARY KEY (global);


--
-- Name: groups pk_posts; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT pk_posts PRIMARY KEY (id);


--
-- Name: userdocuments userdocuments_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdocuments
    ADD CONSTRAINT userdocuments_pk PRIMARY KEY (id_users, id_documents);


--
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- Name: userdocuments userdocuments_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdocuments
    ADD CONSTRAINT userdocuments_fk_documents FOREIGN KEY (id_documents) REFERENCES public.documents(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: userdocuments userdocuments_fk_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdocuments
    ADD CONSTRAINT userdocuments_fk_users FOREIGN KEY (id_users) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

COPY public.groups (id, name, members) FROM stdin;
1	Todos	\N
\.
SELECT pg_catalog.setval('public.posts_id_seq', 8, true);
CREATE ROLE didyoureadme_user;
CREATE ROLE didyoureadme_admin;
REVOKE ALL ON SCHEMA public FROM PUBLIC; 
REVOKE ALL ON SCHEMA public FROM postgres; 
REVOKE ALL ON SCHEMA public FROM didyoureadme_user; 
REVOKE ALL ON SCHEMA public FROM didyoureadme_admin; 
GRANT ALL ON SCHEMA public TO postgres; 
GRANT ALL ON SCHEMA public TO PUBLIC; 
REVOKE ALL ON TABLE public.documents FROM PUBLIC; 
REVOKE ALL ON TABLE public.documents FROM postgres; 
REVOKE ALL ON TABLE public.documents FROM didyoureadme_user; 
REVOKE ALL ON TABLE public.documents FROM didyoureadme_admin; 
GRANT ALL ON TABLE public.documents TO postgres; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.documents TO didyoureadme_user; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.documents TO didyoureadme_admin; 
REVOKE ALL ON SEQUENCE public.documents_id_seq FROM PUBLIC; 
REVOKE ALL ON SEQUENCE public.documents_id_seq FROM postgres; 
REVOKE ALL ON SEQUENCE public.documents_id_seq FROM didyoureadme_user; 
REVOKE ALL ON SEQUENCE public.documents_id_seq FROM didyoureadme_admin; 
GRANT ALL ON SEQUENCE public.documents_id_seq TO postgres; 
GRANT SELECT, UPDATE ON SEQUENCE public.documents_id_seq TO didyoureadme_user; 
GRANT SELECT, UPDATE ON SEQUENCE public.documents_id_seq TO didyoureadme_admin; 
REVOKE ALL ON TABLE public.globals FROM PUBLIC; 
REVOKE ALL ON TABLE public.globals FROM postgres; 
REVOKE ALL ON TABLE public.globals FROM didyoureadme_user; 
REVOKE ALL ON TABLE public.globals FROM didyoureadme_admin; 
GRANT ALL ON TABLE public.globals TO postgres; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.globals TO didyoureadme_user; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.globals TO didyoureadme_admin; 
REVOKE ALL ON TABLE public.groups FROM PUBLIC; 
REVOKE ALL ON TABLE public.groups FROM postgres; 
REVOKE ALL ON TABLE public.groups FROM didyoureadme_user; 
REVOKE ALL ON TABLE public.groups FROM didyoureadme_admin; 
GRANT ALL ON TABLE public.groups TO postgres; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.groups TO didyoureadme_user; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.groups TO didyoureadme_admin; 
REVOKE ALL ON SEQUENCE public.posts_id_seq FROM PUBLIC; 
REVOKE ALL ON SEQUENCE public.posts_id_seq FROM postgres; 
REVOKE ALL ON SEQUENCE public.posts_id_seq FROM didyoureadme_user; 
REVOKE ALL ON SEQUENCE public.posts_id_seq FROM didyoureadme_admin; 
GRANT ALL ON SEQUENCE public.posts_id_seq TO postgres; 
GRANT SELECT, UPDATE ON SEQUENCE public.posts_id_seq TO didyoureadme_user; 
GRANT SELECT, UPDATE ON SEQUENCE public.posts_id_seq TO didyoureadme_admin; 
REVOKE ALL ON TABLE public.userdocuments FROM PUBLIC; 
REVOKE ALL ON TABLE public.userdocuments FROM postgres; 
REVOKE ALL ON TABLE public.userdocuments FROM didyoureadme_user; 
REVOKE ALL ON TABLE public.userdocuments FROM didyoureadme_admin; 
GRANT ALL ON TABLE public.userdocuments TO postgres; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.userdocuments TO didyoureadme_user; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.userdocuments TO didyoureadme_admin; 
REVOKE ALL ON TABLE public.users FROM PUBLIC; 
REVOKE ALL ON TABLE public.users FROM postgres; 
REVOKE ALL ON TABLE public.users FROM didyoureadme_user; 
REVOKE ALL ON TABLE public.users FROM didyoureadme_admin; 
GRANT ALL ON TABLE public.users TO postgres; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users TO didyoureadme_user; 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users TO didyoureadme_admin; 
REVOKE ALL ON SEQUENCE public.users_id_seq FROM PUBLIC; 
REVOKE ALL ON SEQUENCE public.users_id_seq FROM postgres; 
REVOKE ALL ON SEQUENCE public.users_id_seq FROM didyoureadme_user; 
REVOKE ALL ON SEQUENCE public.users_id_seq FROM didyoureadme_admin; 
GRANT ALL ON SEQUENCE public.users_id_seq TO postgres; 
GRANT SELECT, UPDATE ON SEQUENCE public.users_id_seq TO didyoureadme_user; 
GRANT SELECT, UPDATE ON SEQUENCE public.users_id_seq TO didyoureadme_admin; 
--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: globals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.globals VALUES ('version_date', '201811240702');


--
-- PostgreSQL database dump complete
--

