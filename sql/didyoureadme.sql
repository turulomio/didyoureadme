--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: lo_readall(oid); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION lo_readall(oid) RETURNS bytea
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


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE documents (
    id bigint NOT NULL,
    datetime timestamp with time zone DEFAULT now() NOT NULL,
    title text NOT NULL,
    comment text,
    filename text,
    hash text NOT NULL,
    expiration timestamp with time zone DEFAULT (now() + '3 mons'::interval) NOT NULL,
    fileb bytea
);


--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE documents_id_seq OWNED BY documents.id;


--
-- Name: globals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE globals (
    id_globals integer NOT NULL,
    global text,
    value text
);


--
-- Name: groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE groups (
    id bigint NOT NULL,
    name text NOT NULL,
    members bigint[]
);


--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE posts_id_seq OWNED BY groups.id;


--
-- Name: userdocuments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE userdocuments (
    id_users bigint NOT NULL,
    id_documents bigint NOT NULL,
    read timestamp with time zone,
    sent timestamp with time zone,
    numreads bigint DEFAULT 0 NOT NULL
);


--
-- Name: COLUMN userdocuments.read; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN userdocuments.read IS 'First time user read';


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id bigint NOT NULL,
    datetime timestamp with time zone DEFAULT now() NOT NULL,
    name text,
    mail text NOT NULL,
    hash text NOT NULL,
    post text,
    active boolean NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents ALTER COLUMN id SET DEFAULT nextval('documents_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY groups ALTER COLUMN id SET DEFAULT nextval('posts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: documents_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_pk PRIMARY KEY (id);


--
-- Name: pk_posts; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT pk_posts PRIMARY KEY (id);


--
-- Name: userdocuments_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_pk PRIMARY KEY (id_users, id_documents);


--
-- Name: users_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- Name: userdocuments_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_fk_documents FOREIGN KEY (id_documents) REFERENCES documents(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: userdocuments_fk_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_fk_users FOREIGN KEY (id_users) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: documents; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE documents FROM PUBLIC;
REVOKE ALL ON TABLE documents FROM postgres;
GRANT ALL ON TABLE documents TO postgres;
GRANT ALL ON TABLE documents TO didyoureadme_user;


--
-- Name: documents_id_seq; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON SEQUENCE documents_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE documents_id_seq FROM postgres;
GRANT ALL ON SEQUENCE documents_id_seq TO postgres;
GRANT ALL ON SEQUENCE documents_id_seq TO didyoureadme_user;


--
-- Name: globals; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE globals FROM PUBLIC;
REVOKE ALL ON TABLE globals FROM postgres;
GRANT ALL ON TABLE globals TO postgres;
GRANT ALL ON TABLE globals TO didyoureadme_user;


--
-- Name: groups; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE groups FROM PUBLIC;
REVOKE ALL ON TABLE groups FROM postgres;
GRANT ALL ON TABLE groups TO postgres;
GRANT ALL ON TABLE groups TO didyoureadme_user;


--
-- Name: posts_id_seq; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON SEQUENCE posts_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE posts_id_seq FROM postgres;
GRANT ALL ON SEQUENCE posts_id_seq TO postgres;
GRANT ALL ON SEQUENCE posts_id_seq TO didyoureadme_user;


--
-- Name: userdocuments; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE userdocuments FROM PUBLIC;
REVOKE ALL ON TABLE userdocuments FROM postgres;
GRANT ALL ON TABLE userdocuments TO postgres;
GRANT ALL ON TABLE userdocuments TO didyoureadme_user;


--
-- Name: users; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM postgres;
GRANT ALL ON TABLE users TO postgres;
GRANT ALL ON TABLE users TO didyoureadme_user;


--
-- Name: users_id_seq; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON SEQUENCE users_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE users_id_seq FROM postgres;
GRANT ALL ON SEQUENCE users_id_seq TO postgres;
GRANT ALL ON SEQUENCE users_id_seq TO didyoureadme_user;


--
-- PostgreSQL database dump complete
--

COPY groups (id, name, members) FROM stdin;
1	Todos	\N
\.
SELECT pg_catalog.setval('posts_id_seq', 8, true);
--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- Data for Name: globals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO globals VALUES (1, 'version_date', '201501281524');
INSERT INTO globals VALUES (6, 'Admin mode', 'ca0e3137f40fb8f1a536ff64cc994c53');


--
-- PostgreSQL database dump complete
--

