--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE documents (
    id bigint NOT NULL,
    datetime timestamp with time zone DEFAULT now() NOT NULL,
    title text NOT NULL,
    comment text,
    filename text,
    hash text NOT NULL,
    closed boolean NOT NULL,
    datetime_end timestamp with time zone DEFAULT (now() + '3 mons'::interval) NOT NULL,
    file oid
);


ALTER TABLE documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE documents_id_seq OWNED BY documents.id;


--
-- Name: globals; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE globals (
    id_globals integer NOT NULL,
    global text,
    value text
);


ALTER TABLE globals OWNER TO postgres;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groups (
    id bigint NOT NULL,
    name text NOT NULL,
    members bigint[]
);


ALTER TABLE groups OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE posts_id_seq OWNED BY groups.id;


--
-- Name: userdocuments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE userdocuments (
    id_users bigint NOT NULL,
    id_documents bigint NOT NULL,
    read timestamp with time zone,
    sent timestamp with time zone,
    numreads bigint DEFAULT 0 NOT NULL
);


ALTER TABLE userdocuments OWNER TO postgres;

--
-- Name: COLUMN userdocuments.read; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN userdocuments.read IS 'First time user read';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
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


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY documents ALTER COLUMN id SET DEFAULT nextval('documents_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groups ALTER COLUMN id SET DEFAULT nextval('posts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: documents_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_pk PRIMARY KEY (id);


--
-- Name: pk_posts; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT pk_posts PRIMARY KEY (id);


--
-- Name: userdocuments_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_pk PRIMARY KEY (id_users, id_documents);


--
-- Name: users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- Name: userdocuments_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_fk_documents FOREIGN KEY (id_documents) REFERENCES documents(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: userdocuments_fk_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY userdocuments
    ADD CONSTRAINT userdocuments_fk_users FOREIGN KEY (id_users) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


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

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: globals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO globals VALUES (1, 'Version', '201501261042');


--
-- PostgreSQL database dump complete
--

