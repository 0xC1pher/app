--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-02-21 18:20:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16845)
-- Name: acudiente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acudiente (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    correo character varying(255) NOT NULL
);


ALTER TABLE public.acudiente OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16892)
-- Name: asistencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asistencia (
    id_asistencia integer NOT NULL,
    estado character varying(50) NOT NULL,
    id_estudiante integer NOT NULL,
    id_clase integer NOT NULL,
    id_profesor integer NOT NULL,
    justificacion text,
    CONSTRAINT asistencia_estado_check CHECK (((estado)::text = ANY ((ARRAY['Presente'::character varying, 'Ausente'::character varying, 'Justificada'::character varying])::text[])))
);


ALTER TABLE public.asistencia OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16891)
-- Name: asistencia_id_asistencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asistencia_id_asistencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asistencia_id_asistencia_seq OWNER TO postgres;

--
-- TOC entry 4899 (class 0 OID 0)
-- Dependencies: 225
-- Name: asistencia_id_asistencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asistencia_id_asistencia_seq OWNED BY public.asistencia.id_asistencia;


--
-- TOC entry 235 (class 1259 OID 17009)
-- Name: clase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clase (
    id_clase integer NOT NULL,
    fecha date NOT NULL,
    id_curso integer NOT NULL
);


ALTER TABLE public.clase OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17008)
-- Name: clase_id_clase_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.clase ALTER COLUMN id_clase ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.clase_id_clase_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 218 (class 1259 OID 16838)
-- Name: curso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curso (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    id_profesor integer NOT NULL
);


ALTER TABLE public.curso OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16837)
-- Name: curso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.curso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curso_id_seq OWNER TO postgres;

--
-- TOC entry 4900 (class 0 OID 0)
-- Dependencies: 217
-- Name: curso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.curso_id_seq OWNED BY public.curso.id;


--
-- TOC entry 233 (class 1259 OID 16971)
-- Name: curso_materia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curso_materia (
    id_curso integer NOT NULL,
    id_materia integer NOT NULL
);


ALTER TABLE public.curso_materia OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16852)
-- Name: estudiante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estudiante (
    id integer NOT NULL,
    nombre character varying(80) NOT NULL,
    apellido character varying(80) NOT NULL,
    id_acudiente integer,
    id_curso integer,
    correo character varying(255)
);


ALTER TABLE public.estudiante OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16851)
-- Name: estudiante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estudiante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estudiante_id_seq OWNER TO postgres;

--
-- TOC entry 4901 (class 0 OID 0)
-- Dependencies: 221
-- Name: estudiante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estudiante_id_seq OWNED BY public.estudiante.id;


--
-- TOC entry 232 (class 1259 OID 16950)
-- Name: materia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materia (
    id_materia integer NOT NULL,
    nombre character varying(255) NOT NULL
);


ALTER TABLE public.materia OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16949)
-- Name: materia_id_materia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materia_id_materia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.materia_id_materia_seq OWNER TO postgres;

--
-- TOC entry 4902 (class 0 OID 0)
-- Dependencies: 231
-- Name: materia_id_materia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materia_id_materia_seq OWNED BY public.materia.id_materia;


--
-- TOC entry 219 (class 1259 OID 16844)
-- Name: padre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.padre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.padre_id_seq OWNER TO postgres;

--
-- TOC entry 4903 (class 0 OID 0)
-- Dependencies: 219
-- Name: padre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.padre_id_seq OWNED BY public.acudiente.id;


--
-- TOC entry 230 (class 1259 OID 16930)
-- Name: profesor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profesor (
    id integer NOT NULL,
    nombre character varying(80) NOT NULL,
    apellido character varying(80) NOT NULL,
    correo character varying(120) NOT NULL
);


ALTER TABLE public.profesor OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16929)
-- Name: preceptor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.preceptor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.preceptor_id_seq OWNER TO postgres;

--
-- TOC entry 4904 (class 0 OID 0)
-- Dependencies: 229
-- Name: preceptor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.preceptor_id_seq OWNED BY public.profesor.id;


--
-- TOC entry 228 (class 1259 OID 16917)
-- Name: reporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    tipo character varying(50),
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    id_profesor integer NOT NULL,
    CONSTRAINT reporte_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['diario'::character varying, 'semanal'::character varying, 'mensual'::character varying, 'anual'::character varying])::text[])))
);


ALTER TABLE public.reporte OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16916)
-- Name: reporte_id_reporte_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reporte_id_reporte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reporte_id_reporte_seq OWNER TO postgres;

--
-- TOC entry 4905 (class 0 OID 0)
-- Dependencies: 227
-- Name: reporte_id_reporte_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reporte_id_reporte_seq OWNED BY public.reporte.id_reporte;


--
-- TOC entry 224 (class 1259 OID 16869)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre character varying(255) NOT NULL,
    "contraseña" character varying(255) NOT NULL,
    rol character varying(50) NOT NULL,
    correo_email character varying(255) NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16868)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 4906 (class 0 OID 0)
-- Dependencies: 223
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- TOC entry 4686 (class 2604 OID 16848)
-- Name: acudiente id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acudiente ALTER COLUMN id SET DEFAULT nextval('public.padre_id_seq'::regclass);


--
-- TOC entry 4689 (class 2604 OID 16895)
-- Name: asistencia id_asistencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia ALTER COLUMN id_asistencia SET DEFAULT nextval('public.asistencia_id_asistencia_seq'::regclass);


--
-- TOC entry 4685 (class 2604 OID 16841)
-- Name: curso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso ALTER COLUMN id SET DEFAULT nextval('public.curso_id_seq'::regclass);


--
-- TOC entry 4687 (class 2604 OID 16855)
-- Name: estudiante id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiante ALTER COLUMN id SET DEFAULT nextval('public.estudiante_id_seq'::regclass);


--
-- TOC entry 4692 (class 2604 OID 16953)
-- Name: materia id_materia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materia ALTER COLUMN id_materia SET DEFAULT nextval('public.materia_id_materia_seq'::regclass);


--
-- TOC entry 4691 (class 2604 OID 16933)
-- Name: profesor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesor ALTER COLUMN id SET DEFAULT nextval('public.preceptor_id_seq'::regclass);


--
-- TOC entry 4690 (class 2604 OID 16920)
-- Name: reporte id_reporte; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte ALTER COLUMN id_reporte SET DEFAULT nextval('public.reporte_id_reporte_seq'::regclass);


--
-- TOC entry 4688 (class 2604 OID 16872)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- TOC entry 4878 (class 0 OID 16845)
-- Dependencies: 220
-- Data for Name: acudiente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acudiente (id, nombre, apellido, correo) FROM stdin;
1	Carlos	Gómez	carlosgomez@school.com
2	María	Rodríguez	mariarodriguez@school.com
3	Juan	Pérez	juanperez@school.com
4	Ana	Fernández	anafernandez@school.com
5	Luis	Martínez	luismartinez@school.com
6	Carmen	Torres	carmentorres@school.com
7	Pedro	Ramírez	pedroramirez@school.com
8	Laura	Díaz	lauradiaz@school.com
9	Jorge	Herrera	jorgeherrera@school.com
10	Patricia	Morales	patriciamorales@school.com
11	Ricardo	Jiménez	ricardojimenez@school.com
12	Sandra	Rojas	sandrarojas@school.com
13	Andrés	Castro	andrescastro@school.com
14	Gabriela	Méndez	gabrielamendez@school.com
15	Fernando	Vargas	fernandovargas@school.com
16	Natalia	Romero	nataliaromero@school.com
17	Raúl	Suárez	raulsuarez@school.com
18	Silvia	Mendoza	silviamendoza@school.com
19	Diego	Paredes	diegoparedes@school.com
20	Mónica	León	monicaleon@school.com
21	Oscar	Guzmán	oscarguzman@school.com
22	Valeria	Castaño	valeriacastano@school.com
23	Daniel	Orozco	danielorozco@school.com
24	Adriana	Salazar	adrianasalazar@school.com
25	Sebastián	Rincón	sebastianrincon@school.com
26	Liliana	Sepúlveda	lilianasepulveda@school.com
27	Manuel	Chávez	manuelchavez@school.com
28	Carolina	Espinosa	carolinaespinosa@school.com
29	Francisco	Cárdenas	franciscocardenas@school.com
30	Andrea	Giraldo	andreagiraldo@school.com
31	Alejandro	Naranjo	alejandronaranjo@school.com
32	Beatriz	Quintero	beatrizquintero@school.com
33	Mauricio	Velásquez	mauriciovelasquez@school.com
34	Marcela	Barrera	marcelabarrera@school.com
35	Gustavo	Arias	gustavoarias@school.com
36	Paola	Beltrán	paolabeltran@school.com
37	Edgar	Bustos	edgarbustos@school.com
38	Fabiola	Montoya	fabiolamontoya@school.com
39	Iván	Lozano	ivanlozano@school.com
40	Jessica	Valderrama	jessicavalderrama@school.com
41	Cristian	Peñaloza	cristianpenaloza@school.com
42	Alexandra	Villalobos	alexandravillalobos@school.com
43	Felipe	Londoño	felipelondono@school.com
44	Lucía	Restrepo	luciarestrepo@school.com
45	Ramiro	Correa	ramirocorrea@school.com
46	Diana	Burgos	dianaburgos@school.com
47	Héctor	Pacheco	hectorpacheco@school.com
48	Verónica	Olaya	veronicaolaya@school.com
49	Enrique	Cifuentes	enriquecifuentes@school.com
50	Marcelo	Zambrano	marcelozambrano@school.com
\.


--
-- TOC entry 4884 (class 0 OID 16892)
-- Dependencies: 226
-- Data for Name: asistencia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asistencia (id_asistencia, estado, id_estudiante, id_clase, id_profesor, justificacion) FROM stdin;
\.


--
-- TOC entry 4893 (class 0 OID 17009)
-- Dependencies: 235
-- Data for Name: clase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clase (id_clase, fecha, id_curso) FROM stdin;
\.


--
-- TOC entry 4876 (class 0 OID 16838)
-- Dependencies: 218
-- Data for Name: curso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.curso (id, nombre, id_profesor) FROM stdin;
1	Primero A	1
2	Primero B	2
3	Segundo A	3
4	Segundo B	4
5	Tercero A	5
6	Tercero B	6
7	Cuarto A	7
8	Cuarto B	8
9	Quinto A	9
10	Quinto B	10
\.


--
-- TOC entry 4891 (class 0 OID 16971)
-- Dependencies: 233
-- Data for Name: curso_materia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.curso_materia (id_curso, id_materia) FROM stdin;
\.


--
-- TOC entry 4880 (class 0 OID 16852)
-- Dependencies: 222
-- Data for Name: estudiante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estudiante (id, nombre, apellido, id_acudiente, id_curso, correo) FROM stdin;
101	Fabian	Ortiz	17	10	fabian.ortiz@school.com
102	Eduardo	Lopez	16	3	eduardo.lopez@school.com
103	Javier	Espinoza	6	8	javier.espinoza@school.com
104	Lucas	Fuentes	36	9	lucas.fuentes@school.com
105	Samuel	Avila	36	4	samuel.avila@school.com
106	Gabriel	Rodriguez	49	3	gabriel.rodriguez@school.com
107	Emiliano	Sanchez	5	10	emiliano.sanchez@school.com
108	Alejandro	Diaz	15	7	alejandro.diaz@school.com
109	Sebastian	Fernandez	49	4	sebastian.fernandez@school.com
110	Leonardo	Perez	12	7	leonardo.perez@school.com
111	Mateo	Gomez	46	8	mateo.gomez@school.com
112	Santiago	Ramirez	39	4	santiago.ramirez@school.com
113	Joaquin	Torres	39	1	joaquin.torres@school.com
114	Adrian	Flores	47	2	adrian.flores@school.com
115	Benjamin	Vargas	48	6	benjamin.vargas@school.com
116	Isaac	Castro	19	3	isaac.castro@school.com
117	Luis	Ortiz	13	9	luis.ortiz@school.com
118	Antonio	Morales	24	10	antonio.morales@school.com
119	Fernando	Herrera	33	9	fernando.herrera@school.com
120	Ricardo	Mendoza	40	1	ricardo.mendoza@school.com
121	Hector	Guerrero	14	9	hector.guerrero@school.com
122	Andres	Delgado	44	7	andres.delgado@school.com
123	Javier	Ramos	10	3	javier.ramos@school.com
124	Raul	Romero	37	4	raul.romero@school.com
125	Manuel	Medina	3	1	manuel.medina@school.com
126	Cristian	Chavez	24	3	cristian.chavez@school.com
127	Diego	Vega	35	8	diego.vega@school.com
128	Julio	Silva	11	5	julio.silva@school.com
129	Ruben	Cabrera	27	9	ruben.cabrera@school.com
130	Ernesto	Reyes	1	9	ernesto.reyes@school.com
131	Martin	Escobar	48	4	martin.escobar@school.com
132	Rodrigo	Fuentes	24	10	rodrigo.fuentes@school.com
133	Pablo	Valencia	34	8	pablo.valencia@school.com
134	Esteban	Pena	36	2	esteban.pena@school.com
135	Cesar	Mejia	42	2	cesar.mejia@school.com
136	Vicente	Campos	17	2	vicente.campos@school.com
137	Alvaro	Rojas	46	3	alvaro.rojas@school.com
138	Mario	Bermudez	42	6	mario.bermudez@school.com
139	Gustavo	Quintero	35	7	gustavo.quintero@school.com
140	Tomas	Suarez	18	9	tomas.suarez@school.com
141	Fabian	Montoya	21	4	fabian.montoya@school.com
142	Eduardo	Avila	37	7	eduardo.avila@school.com
143	Hugo	Espinoza	31	5	hugo.espinoza@school.com
144	Ramon	Aguilar	9	10	ramon.aguilar@school.com
145	Raul	Pacheco	6	8	raul.pacheco@school.com
146	Emilio	Zambrano	21	6	emilio.zambrano@school.com
147	Jorge	Peralta	10	8	jorge.peralta@school.com
148	Ivan	Acosta	8	9	ivan.acosta@school.com
149	Jaime	Cortes	19	1	jaime.cortes@school.com
150	Oscar	Benitez	3	2	oscar.benitez@school.com
\.


--
-- TOC entry 4890 (class 0 OID 16950)
-- Dependencies: 232
-- Data for Name: materia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materia (id_materia, nombre) FROM stdin;
1	Español
2	Matematicas
3	Ciencias Naturales
4	Ciencias Sociales
5	Educacion Fisica
6	Ciencias Sociales
7	Artistica
8	Ingles
9	Religion
10	Informatica
11	Religion
12	Etica y Valores
\.


--
-- TOC entry 4888 (class 0 OID 16930)
-- Dependencies: 230
-- Data for Name: profesor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profesor (id, nombre, apellido, correo) FROM stdin;
1	Juan	Perez	juan.perez@school.com
2	Maria	Gomez	maria.gomez@school.com
3	Carlos	Rodriguez	carlos.rodriguez@school.com
4	Ana	Martinez	ana.martinez@school.com
5	Luis	Fernandez	luis.fernandez@school.com
6	Laura	Ramirez	laura.ramirez@school.com
7	Andres	Torres	andres.torres@school.com
8	Patricia	Castro	patricia.castro@school.com
9	Fernando	Gonzalez	fernando.gonzalez@school.com
10	Claudia	Sanchez	claudia.sanchez@school.com
\.


--
-- TOC entry 4886 (class 0 OID 16917)
-- Dependencies: 228
-- Data for Name: reporte; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reporte (id_reporte, tipo, fecha_inicio, fecha_fin, id_profesor) FROM stdin;
\.


--
-- TOC entry 4882 (class 0 OID 16869)
-- Dependencies: 224
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, nombre, "contraseña", rol, correo_email) FROM stdin;
3	padre1	padre123	padre	padre2@gmail.com
2	profesor1	profesorpassword	profesor	profesor@empresa.com
4	admin1	admin123	administrador	admin@gmail.com
\.


--
-- TOC entry 4907 (class 0 OID 0)
-- Dependencies: 225
-- Name: asistencia_id_asistencia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asistencia_id_asistencia_seq', 1, false);


--
-- TOC entry 4908 (class 0 OID 0)
-- Dependencies: 234
-- Name: clase_id_clase_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clase_id_clase_seq', 1, false);


--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 217
-- Name: curso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.curso_id_seq', 11, true);


--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 221
-- Name: estudiante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estudiante_id_seq', 150, true);


--
-- TOC entry 4911 (class 0 OID 0)
-- Dependencies: 231
-- Name: materia_id_materia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materia_id_materia_seq', 12, true);


--
-- TOC entry 4912 (class 0 OID 0)
-- Dependencies: 219
-- Name: padre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.padre_id_seq', 50, true);


--
-- TOC entry 4913 (class 0 OID 0)
-- Dependencies: 229
-- Name: preceptor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.preceptor_id_seq', 1, false);


--
-- TOC entry 4914 (class 0 OID 0)
-- Dependencies: 227
-- Name: reporte_id_reporte_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reporte_id_reporte_seq', 1, false);


--
-- TOC entry 4915 (class 0 OID 0)
-- Dependencies: 223
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 3, true);


--
-- TOC entry 4708 (class 2606 OID 16900)
-- Name: asistencia asistencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_pkey PRIMARY KEY (id_asistencia);


--
-- TOC entry 4718 (class 2606 OID 17013)
-- Name: clase clase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT clase_pkey PRIMARY KEY (id_clase);


--
-- TOC entry 4716 (class 2606 OID 16975)
-- Name: curso_materia curso_materia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_materia
    ADD CONSTRAINT curso_materia_pkey PRIMARY KEY (id_curso, id_materia);


--
-- TOC entry 4696 (class 2606 OID 16843)
-- Name: curso curso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso
    ADD CONSTRAINT curso_pkey PRIMARY KEY (id);


--
-- TOC entry 4702 (class 2606 OID 16857)
-- Name: estudiante estudiante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiante
    ADD CONSTRAINT estudiante_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 16955)
-- Name: materia materia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materia
    ADD CONSTRAINT materia_pkey PRIMARY KEY (id_materia);


--
-- TOC entry 4698 (class 2606 OID 16937)
-- Name: acudiente padre_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acudiente
    ADD CONSTRAINT padre_correo_key UNIQUE (correo);


--
-- TOC entry 4700 (class 2606 OID 16850)
-- Name: acudiente padre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acudiente
    ADD CONSTRAINT padre_pkey PRIMARY KEY (id);


--
-- TOC entry 4712 (class 2606 OID 16935)
-- Name: profesor preceptor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesor
    ADD CONSTRAINT preceptor_pkey PRIMARY KEY (id);


--
-- TOC entry 4710 (class 2606 OID 16923)
-- Name: reporte reporte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (id_reporte);


--
-- TOC entry 4704 (class 2606 OID 16878)
-- Name: usuario usuario_correo_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_correo_email_key UNIQUE (correo_email);


--
-- TOC entry 4706 (class 2606 OID 16876)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4723 (class 2606 OID 16901)
-- Name: asistencia asistencia_id_estudiante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_id_estudiante_fkey FOREIGN KEY (id_estudiante) REFERENCES public.estudiante(id);


--
-- TOC entry 4724 (class 2606 OID 16911)
-- Name: asistencia asistencia_id_profesor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_id_profesor_fkey FOREIGN KEY (id_profesor) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4720 (class 2606 OID 16863)
-- Name: estudiante estudiante_idpadre_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiante
    ADD CONSTRAINT estudiante_idpadre_fkey FOREIGN KEY (id_acudiente) REFERENCES public.acudiente(id);


--
-- TOC entry 4721 (class 2606 OID 16991)
-- Name: estudiante fk_acudiente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiante
    ADD CONSTRAINT fk_acudiente FOREIGN KEY (id_acudiente) REFERENCES public.acudiente(id) ON DELETE SET NULL;


--
-- TOC entry 4725 (class 2606 OID 17019)
-- Name: asistencia fk_asistencia_clase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT fk_asistencia_clase FOREIGN KEY (id_clase) REFERENCES public.clase(id_clase);


--
-- TOC entry 4729 (class 2606 OID 17014)
-- Name: clase fk_clase_curso; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT fk_clase_curso FOREIGN KEY (id_curso) REFERENCES public.curso(id);


--
-- TOC entry 4727 (class 2606 OID 16976)
-- Name: curso_materia fk_curso; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_materia
    ADD CONSTRAINT fk_curso FOREIGN KEY (id_curso) REFERENCES public.curso(id) ON DELETE CASCADE;


--
-- TOC entry 4719 (class 2606 OID 17024)
-- Name: curso fk_curso_profesor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso
    ADD CONSTRAINT fk_curso_profesor FOREIGN KEY (id_profesor) REFERENCES public.profesor(id);


--
-- TOC entry 4722 (class 2606 OID 16986)
-- Name: estudiante fk_estudiante_curso; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiante
    ADD CONSTRAINT fk_estudiante_curso FOREIGN KEY (id_curso) REFERENCES public.curso(id) ON DELETE SET NULL;


--
-- TOC entry 4728 (class 2606 OID 16981)
-- Name: curso_materia fk_materia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_materia
    ADD CONSTRAINT fk_materia FOREIGN KEY (id_materia) REFERENCES public.materia(id_materia) ON DELETE CASCADE;


--
-- TOC entry 4726 (class 2606 OID 16924)
-- Name: reporte reporte_id_profesor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_id_profesor_fkey FOREIGN KEY (id_profesor) REFERENCES public.usuario(id_usuario);


-- Completed on 2025-02-21 18:20:30

--
-- PostgreSQL database dump complete
--

CREATE TYPE tipo_rol AS ENUM ('Padre', 'Profesor', 'Administrador');

