--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';
SET default_with_oids = false;

---
--- drop tables
---

DROP TABLE IF EXISTS cliente cascade;
DROP TABLE IF EXISTS plano cascade;
DROP TABLE IF EXISTS produto cascade;
DROP TABLE IF EXISTS aporteExtra cascade;
DROP TABLE IF EXISTS resgate cascade;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cliente (
    cliente_id SERIAL PRIMARY KEY, 
    cliente_nome character varying(30) NOT NULL,
    cliente_cpf character varying(11) NOT NULL,
    cliente_email character varying(20) NOT NULL,
    cliente_sexo character varying(5) NOT NULL,
    cliente_dataDeNascimento date,
    cliente_rendaMensal real
);

--
-- Name: produto; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE produto (
    produto_id SERIAL PRIMARY KEY,
    produto_nome character varying(30) NOT NULL,
    produto_susep character varying(20) NOT NULL,
    produto_expiracaoDeVenda date,
    produto_valorMinimoAporteInicial real,
    produto_valorMinimoAporteExtra real,
    produto_idadeDeEntrada smallint,
    produto_idadeDeSaida smallint,
    produto_carenciaInicialDeResgate smallint,
    produto_carenciaEntreResgates smallint
);

--
-- Name: plano; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE plano (
    plano_id SERIAL PRIMARY KEY, 
	produto_id SERIAL NOT NULL,
    cliente_id SERIAL NOT NULL,
    aporte real NOT NULL,
    dataDaContratacao date not NULL,
    CONSTRAINT fk_plano_produto FOREIGN KEY (produto_id) REFERENCES produto(produto_id),
    CONSTRAINT fk_plano_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id)
);

--
-- Name: resgate; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE resgate (
    resgate_id SERIAL PRIMARY KEY, 
    plano_id smallint NOT NULL,
    valorResgate real NOT NULL,
    datadoresgate date,
    CONSTRAINT fk_resgate_plano FOREIGN KEY (plano_id) REFERENCES plano(plano_id)
);

--
-- Name: aporteExtra; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE aporteExtra (
    aporteExtra_id SERIAL PRIMARY KEY, 
    plano_id smallint NOT NULL,
    cliente_id smallint NOT NULL,
    valorAporte real NOT NULL,
    CONSTRAINT fk_aporteExtra_plano FOREIGN KEY (plano_id) REFERENCES plano(plano_id),
    CONSTRAINT fk_aporteExtra_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id)

);

--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO cliente VALUES (DEFAULT, 'José da Silva', '45645645600', 'jose@cliente.com','M','2010-01-01', 2899.5);

--
-- Data for Name: produto; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO produto VALUES (DEFAULT, 'Longo Prazo', '15414.900840/2018-17', '2024-01-01', 1000, 100, 18, 60, 60, 30);

--
-- Data for Name: plano; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO plano VALUES (DEFAULT, 1, 1, 2000.00, '2022-04-05');

--
-- Data for Name: aporteExtra; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO aporteExtra VALUES (DEFAULT, 1, 1, 1000.00);

--
-- Data for Name: resgate; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO resgate VALUES (DEFAULT, 1, 1000.00, '2021-01-01');

--
-- PostgreSQL database dump complete
--
