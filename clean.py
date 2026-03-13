import pandas as pd
import re

# 1. 在这三个引号中间，直接粘贴你的所有原始文本数据！
RAW_DATA = """
	A	B	C	D	E	F	G	H	I	J	K	L	M	N
1
Timestamp	Berkeley id or email?	Is your UCSD #3 prestige banner there?	Can you log in to the UCI link?	Did you apply for financial aid?	GPA(UC UW)?	GPA(UC W)	GPA(UC W capped)	Rate your piqs on a scale of 1-10	Rate your ec's on a scale of 1-10	UCB major?	UCSD major?	UCI major?	Best college you've already gotten accepted to(not required)
2
3/8/2026 10:55:51	Id	No	Yes	Yes	4	4.31	Idk	7	7	Chemistry	Chemistry	Chemistry	
3
3/8/2026 10:56:01	Id	Yes	Yes	Yes	3.86	4.14	4.34	7	5	Bioengineering	Bioengineering	Biomedical Engineering	UC Berkeley
4
3/8/2026 10:57:21	Id	Yes	Yes	Yes	3.6	4.2	3.9	8	8	Applied Math	Applied Math	Computational Math	Hong Kong University
5
3/8/2026 10:57:47	Email	No	No	Yes	3.88	4.38	4.21	7	8	applied math	ICAM	applied math	
6
3/8/2026 11:03:10	Email	No	No	Yes	4	4.4	4.3	8	8	EECS	ECE	Comp eng	
7
3/8/2026 11:06:53	Email	No	Yes	Yes	4	4.6	4.31	8	9	Data Science	CS	CS	
8
3/8/2026 11:07:09	Id	No	Yes	No	4	4.91	4.33	8	6	Chemical biology	Biochem	Biological sciences	
9
3/8/2026 11:07:56	Email	Yes	No	No	3.92	4.24	4.24	7	8	Molecular and Cell Biology	Biochemistry	Biological Sciences	
10
3/8/2026 11:08:45	Email	Yes	No	No	3.83	4.3	4.18	9	7	Cognitive Science	Cognitive Science	Cognitive Science	
11
3/8/2026 11:09:38	Id	No	Yes	Yes	4	4.5	4.3	8	7	Astrophysics	Astrophysics	Physics	
12
3/8/2026 11:10:43	Id	No	Yes	Yes	4	4.78	4.32	9	8	mcdb	human bio	bio sci	ucd
13
3/8/2026 11:14:16	Id	Yes	No	No	4	4.5	4.33	7	7	Electrical and Computer Engineering	Electrical Engineering	Electrical Engineering	
14
3/8/2026 11:15:04	Id	Yes	Yes	Yes	3.92	4.25	4.25	6	6	Mechancial Engineering	Mechanical Engineering	Mechanical Engineering	San Diego State University
15
3/8/2026 11:15:07	Id	No	Didn't apply	No	4	4.47	4.27	7	9	Political Science	Public Policy	N/A	Babson Presidential Scholarship
16
3/8/2026 11:18:06	Id	No	Yes	No	4	4.77	4.35	7	8	ME	ME	ME	
17
3/8/2026 11:18:34	Id	Yes	Yes	Yes	3.9	4.57	4.23	8	6	Economics	Business Economics	Economics	University of Washington
18
3/8/2026 11:18:45	Id	Yes	Yes	Yes	3.9	4.3	4.3	7	9	Civil Engineering	Aerospace Engineering	Aerospace Engineering	Northeastern University
19
3/8/2026 11:21:49	Didn't apply	Yes	Didn't apply	No	3.78	4.25	4.04	9	7	Na	Anthropology	Na	UCD, Tamu engineering, sdsu
20
3/8/2026 11:23:38	Id	Yes	Yes	Yes	4	5	4.3	8	8	data science	cs w/ specialization in bioinformatics	data science	case western reserve university (~32% acceptance rate)
21
3/8/2026 11:23:47	Id	Yes	Yes	Yes	4	4.56	4.28	7	7	Mechanical engineering	mechanical engineering	mechanical engineering	purdue
22
3/8/2026 11:24:00	Id	Yes	Yes	No	3.7	3.7	4	8	5	global relations	international buissness	finance	tulane ea
23
3/8/2026 11:24:19	Id	Yes	No	Yes	3.93	4.59	4.19	8	7	Statistics	Data Science	Data Science	UIUC
24
3/8/2026 11:24:25	Email	Yes	Yes	Yes	3.88	4.41	4.17	7	8	Chemistry B.S.	Chemistry B.S.	Chemistry B.S.	
25
3/8/2026 11:26:38	Id	Didn't apply	Didn't apply	Yes	3.73	3.95	3.93	7	8	Mechanical Engineering	N/A	N/A	
26
3/8/2026 11:27:28	Id	No	No	Yes	3.88	4.28	4.19	8	8	Undeclared life sciences	Global health	Public health	SDSU
27
3/8/2026 11:27:37	Id	No	No	No	3.96	4.58	4.29	7	8	bio	bio	bio	uc davis
28
3/8/2026 11:28:33	Email	Yes	No	Yes	4	4.167	4.25	8	1	undeclared	CompSci/Undeclared	CompSci/Undeclared	SDSU/UCR (CompSci)
29
3/8/2026 11:30:13	Didn't apply	No	Yes	Yes	3.78	4.38	4.03	8	8	Didn’t apply	Nano engineering	Chemical engineering	Csulb ( the hard ones haven’t came up yet)
30
3/8/2026 11:30:29	Id	No	Yes	Yes	4	4.5	4.3	7	5	ECE	ECE	Computer Engineering	
31
3/8/2026 11:30:33	Id	Yes	Yes	Yes	3.84	4.4	4.16	7	7	Applied Math	Data Science	Applied Math	
32
3/8/2026 11:31:07	Id	No	No	No	3.95	4.38	4.26	8	7	Bio	Bio	Bio	
33
3/8/2026 11:31:43	Email	Yes	No	Yes	3.6	3.96	3.92	8	7	Aerospace Engineering	Aerospace Engineering	Aerospace Engineering	
34
3/8/2026 11:32:31	Didn't apply	Yes	Didn't apply	Yes	4	4.9	4.9	10	8	Aerospace	Aerospace	AE	u of wash
35
3/8/2026 11:32:54	Id	No	Didn't apply	Yes	3.95	4.3	4.5	8	6	History	Theater	NA	Occidental
36
3/8/2026 11:34:11	Id	No	No	Yes	3.91	4.57	4.27	7	8	molecular cell bio	molecular cell bio	biological sciences	
37
3/8/2026 11:34:14	Id	No	Yes	Yes	3.78	4.37	4	8	6	BS Chemistry in College of Chemistry	Environmental Chemistry	Environmental Science and Policy	University of Michigan LSA
38
3/8/2026 11:35:07	Email	Yes	No	No	3.8	4.29	4.13	8	4	Undeclared - humanities	Undeclared - humanities	Undeclared - humanities	UC Davis
39
3/8/2026 11:36:24	Email	No	No	No	4	4	4	7	8	Electrical engineering	Electrical engineering	Electrical engineering	
40
3/8/2026 11:36:51	Email	No	Didn't apply	Yes	4	4.9	4.7	7	7	environmental engineering	environmental engineering	n/a	ucsb (reception)
41
3/8/2026 11:37:38	Id	Didn't apply	Didn't apply	No	3.86	4.5	4.14	8	8	cs	none	none	georgia tech (cs, oos)
42
3/8/2026 11:38:04	Id	No	Yes	No	4	4.93	4.27	8	8	Bioengineering	Computer Science	Computer Science and Engineering	
43
3/8/2026 11:38:27	Id	No	No	Yes	4	4.5	4.29	7	5	Conservation and Resource Studies	Marine Biology (Scripps)	Environmental Science/Ecology	University of Florida
44
3/8/2026 11:39:03	Id	Yes	No	Yes	4,0	4.6	4,4	10	8	Mcb	Biochemistry	Biochemistry	UC Berkeley Early admit
45
3/8/2026 11:39:12	Id	Yes	No	No	3.88	4.58	4.19	5	6	EECS	EE	EE	
46
3/8/2026 11:40:31	Didn't apply	No	Yes	Yes	3.95	4.35	4.35	7	5	Data Science	Biology with Specialization in Bioinformatics	Biological Sciences	University of Rochester
47
3/8/2026 11:40:47	Id	No	Yes	No	3.93	4.62	4.16	7	7	EECS	CS plus Bioinformatics	CS	UW CS, also UCSB Chancellors
48
3/8/2026 11:41:10	Id	Yes	Yes	Yes	4	4.6	4.36	7	8	Molecular biology	Bioengineering	Biomedical engineering	University of Washington, University of Toronto
49
3/8/2026 11:59:32	Didn't apply	Yes	Didn't apply	Yes	4	4.91	4.36	4	4	N/A	Astronomy & Astrophysics	N/A	MIT (Not attending....)
50
3/8/2026 11:44:10	Id	No	No	Yes	3.98	4.51	4.2	8	7	Integrative Biology	Human Biology	Biological Sciences	LMU
51
3/8/2026 11:44:37	Email	No	Didn't apply	No	4	4.78	4.2	6	5	Mechanical Engineering	Mech E/History alt	n/a	Purdue or UDUB (for MechE)
52
3/8/2026 11:45:18	Id	No	Yes	No	4	4.6	4.5	7	7	japanese	business economics	business economics	usc (ea)
53
3/8/2026 11:45:20	Id	Yes	Yes	No	3.98	4.7	4.14	8	8	Industrial Engineering	Computer Science	Computer Science	UIUC CS
54
3/8/2026 11:47:46	Id	No	Yes	Yes	3.95	4.6	4.25	9	6	Chemical Engineering	Chemical Engineering	Chemical Engineering	
55
3/8/2026 11:49:12	Id	Yes	Yes	No	3.96	4.8	4.12	9	10	EECS	CS	CS	
56
3/8/2026 11:50:16	Id	No	Yes	Yes	4	4.84	4.2	8	8	MET/Engineering Undeclared	CSE - AI/Engineering: Electrical Engineering & Society	Computer Science	USC, UIUC Eng. Undeclared, UCSC, Smith likely, UW Seattle CS
57
3/8/2026 11:50:20	Id	Didn't apply	Didn't apply	No	3.94	4.89	4.19	5	5	EECS			
58
3/8/2026 11:50:35	Id	No	Yes	Yes	4	4.44	4	7	7	Global Management	Computer Science	Business Information Management	Northeastern (ea) UIUC (rd)
59
3/8/2026 11:50:39	Id	No	No	Yes	3.9	4.44	4.25	7	7	MCB	Bioengineering	Biomedical engineering	UIUC/UC Davis (US) University of Toronto International
60
3/8/2026 11:51:45	Id	No	No	Yes	4	4.57	4.18	7	8	ECE	EE	EE	Umich
61
3/8/2026 11:51:59	Id	Yes	Didn't apply	No	3.9	4.48	4.29	8	7	EECS	ECE	N/A	UMichigan for CS
62
3/8/2026 11:54:50	Id	Yes	No	No	4	4.46	4.31	9	7	Civil Engineering	Mechanical Engineering	Civil Engineering	UC Davis, Civil Engineering (only applied UCs and CSUs)
63
3/8/2026 11:56:23	Id	No	Didn't apply	No	4	4.4	4.3	6	7	Economics	Economics + Mathematics	N/A	UMich
64
3/8/2026 11:57:09	Id	No	No	No	4	4.48	4.29	8	9	Economics	Business Economics	Business Admin	Kelley
65
3/8/2026 11:58:28	Email	Yes	No	Yes	3.7	4.27	3.97	8	8	Chemistry	Pharmacological Chemistry	Pharmaceutical Sciences	Udub
66
3/8/2026 11:59:07	Id	No	Yes	No	3	3.02	3.02	10	10	molecular and cell bio	public health and med sciences	archi and enviro design and planning	
67
3/8/2026 11:59:21	Id	Yes	Yes	Yes	3.95	4.45	4.19	6	5	Applied Math	Math-CS	Mathematics of Computation	Washington ACMS/Purdue CS
68
3/8/2026 11:59:24	Id	No	Yes	No	4	4.6	4.3	9	8	EECS	CS	CS	UCB
69
3/8/2026 12:02:24	Id	Yes	Didn't apply	No	4	4.6	4.25	9	9	Environmental eng	Marine biology	N/a	Harvard
70
3/8/2026 12:02:45	Email	No	Didn't apply	Yes	3.88	4.25	4.08	8	8	Data science	Statistics and probability	NA	UIUC
71
3/8/2026 12:04:05	Id	No	Yes	Yes	4	4.8	4.36	6	6	Chemical Biology	Biochemistry	Biological Sciences	
72
3/8/2026 12:05:37	Didn't apply	Yes	Yes	Yes	4	4.42	4.33	8	7	N/A	Business Economics	Business Administration	got accepted to CSULB, UCR, UCM, UCSC
73
3/8/2026 12:07:09	Id	No	Yes	Yes	3.88	N/A	4.15	8	8	Economics	International Studies - Economics	Economics	
74
3/8/2026 12:08:05	Email	Yes	Didn't apply	No	4	4.93	4.57	8	8	ECE	ECE	N/A	UIUC EE
75
3/8/2026 12:09:24	Id	No	No	Yes	3.95	4.52	4.27	8	7	Ancient Greek and Roman studies	Marine bio	Polisci	UCD, UWM, UW
76
3/8/2026 12:09:47	Email	Yes	Yes	No	3.93	4.71	4.21	6	6	stats	stats	Data Science	UIUC
77
3/8/2026 12:10:29	Email	Yes	Yes	Yes	3.93	4.37	4.2	7	6	Political Science	Political Science - Public Policy	Social Policy and Public Service	Uc Davis
78
3/8/2026 12:10:43	Id	No	No	No	3.9	4.33	4.27	9	7	linguistics	linguistics	linguistics	uiuc honors, uw&m, uc davis (apparently impressive now lol), uoft, all linguistics
79
3/8/2026 12:14:13	Id	No	Yes	Yes	3.93	4.4	4.12	5	6	Philosophy (2nd choice undecided social sciences)	Comp Sci (business psych 2nd choice)	Psych (2nd choice Game design)	Berkeley (got rlly lucky 🥹)
80
3/8/2026 12:15:39	Id	No	No	Yes	3.95	4.5	4.31	7	5	Political Econ	Econ and Math (Joint major)	Business Admin	
81
3/8/2026 12:21:33	Id	No	No	No	3.82	4.6	4.17	7	8	Econ	Business Econ	Business Admin	
82
3/8/2026 12:22:43	Id	Yes	No	Yes	3.89	4.43	4.22	7	5	cognitive science	cognitive science	cognitive science	ucsc
83
3/8/2026 12:23:59	Id	No	Yes	No	4	4.5	4.12?	8	8	Data Science	Data Science	Data Science	Gatech CS oos
84
3/8/2026 12:24:36	Id	No	Yes	Yes	4	4.7	4.32	9	7	ECE	ECE	CSE	Georgia tech compe or umich cs
85
3/8/2026 12:27:10	Id	Yes	No	Yes	3.98	4.29	4.29	6	7	biochem	biochem	chem	
86
3/8/2026 12:28:06	Id	Yes	Yes	Yes	3.8	4.4	4.2	5	4	Cognitive Science	Human Developmental Sciences	Public Health Sciences	sdsu
87
3/8/2026 12:28:43	Id	No	Yes	No	3.9	4.1	4.1	7	10	Undecided	Undecided	Public health	CSULB
88
3/8/2026 12:28:59	Id	No	Didn't apply	No	97%	-	-	8	9	Mechanical Engineering	Mechanical Engineering	-	UW MADISON OR UW SEATTLE
89
3/8/2026 12:30:51	Id	Yes	No	No	3.49	3.97	3.7	8	10	Native Studies	Anthropology with Concentration in Sociocultural Anthropology	Anthropology	Davis or Northeastern
90
3/8/2026 12:31:07	Id	No	Didn't apply	Yes	4.16	4.4	4.16	8	8	Data Science	Buissnes Econ	Didn’t apply	Santa Clara University, UC Davis
91
3/8/2026 12:31:45	Email	Yes	Yes	No	4	4.27	4.27	8	8	Undeclared	Undeclared	Undeclared	SDSU
92
3/8/2026 12:33:58	Id	Yes	No	Yes	3.93	4.45	4.21	9	10	Electrical Engineering & Computer Science	Electrical and Computer Engineering	Computer Engineering	University of Michigan (EE)
93
3/8/2026 12:35:11	Id	No	Yes	Yes	3.92	4.23	4.62	7	8	Engineering Mathematics and Statistics	Mathematics - Computer Science	Electrical Engineering	UC Davis
94
3/8/2026 12:36:12	Id	No	Yes	Yes	4	4.93	4.3	8	6	Molecular and Cell Biology	Bioengineering	Biomedical Engineering	UC Davis
95
3/8/2026 12:36:13	Id	No	Didn't apply	No	4	4.8	4.27	5	8	Bio	Bio	Bio	USC (scholarship), UC Davis (honors, no scholarship)
96
3/8/2026 12:36:58	Email	Didn't apply	Yes	Yes	3.7	4	4	9	6	History	N/A	History	University of Washington
97
3/8/2026 12:40:57	Id	Yes	No	Yes	3.93	4.36	4.21	8	7	psych	psych	psych	UCSC
98
3/8/2026 12:42:14	Id	No	Yes	Yes	4	4.88	4.5	8	7	Genetics and Plant Biology	Environmental Chemistry	Biological Sciences	
99
3/8/2026 12:46:27	Id	Yes	No	Yes	3.63	3.92	3.79	7	7	Engineering Undeclared	Mechanical Engineering	Mechanical Engineering	
100
3/8/2026 12:43:52	Id	No	Yes	No	4	4.67	4.27	8	8	Bioengineering	Bioengineering: biotechnology	Biomedical engineering	UW or UCD
101
3/8/2026 12:44:08	Email	Yes	No	No	4	4.56	4.33	5	6	Electrical and Computer Engineering	Electrical Engineering	Electrical Engineering	
102
3/8/2026 12:46:06	Id	Didn't apply	Didn't apply	No	4	4.3	4.3	8	8	Civil Engineering	N/A	N/A	UT Austin
103
3/8/2026 12:46:41	Id	No	No	Yes	4	4.69	4.27	8	8	Environmental Engineering	Mechanical Engineering	Civil Engineering	UIUC/Purdue/Davis Mechanical Engineering
104
3/8/2026 12:48:01	Id	No	No	Yes	4	4.54	4.31	9	8	Civil Engineering	Structural Engineering	Civil Engineering	UIUC engineering
105
3/8/2026 12:50:29	Id	Yes	No	Yes	3.87	4.4	4.09	8	6	EECS	CS	CS	
106
3/8/2026 12:53:07	Id	No	Yes	Yes	4	4.69	4.31	9	8	chem e	chem e	chem e	g tech
107
3/8/2026 12:53:36	Id	Didn't apply	Didn't apply	Yes	3.77	3.89	4.05	8	9	Chemistry (College of Chem)	N/A	N/A	UCD
108
3/8/2026 12:54:32	Email	Yes	Yes	Yes	3.95	3.57	3.32	9	7	Undeclared biological science	Neuroscience/ undeclared	Biomedical engineering	UCD
109
3/8/2026 12:57:34	Email	Yes	Yes	Yes	4	4.34	4.29	8	8	Aerospace Engineering	Aerospace Engineering	Aerospace Engineering	UIUC
110
3/8/2026 12:57:48	Email	Yes	Yes	Yes	3.66	3.9	3.85	8	7	Undeclared science	Undeclared science	Social Ecology	SDSU
111
3/8/2026 12:58:43	Id	Yes	Yes	No	3.91	4.5	4.27	7	5	media studies	media industries and comms	film and digital media	ucsc
112
3/8/2026 12:59:18	Didn't apply	Yes	Didn't apply	Yes	3.82	4.11	4.11	7	5	n/a	Political Science	n/a	
113
3/8/2026 13:05:21	Email	No	Didn't apply	No	4	4.36	4.29	9	7	Civil Engineering	Structural Engineering	N/A	UCSB (I got reception email)
114
3/8/2026 13:08:27	Id	Yes	Yes	Yes	4	4.32	4.48	7	6	bioengineering	bioengineering	bioengineering	Northeastern
115
3/8/2026 13:11:06	Id	Yes	No	Yes	3.78	4.59	Idk	7	8	Physics	Mechanical Engineering	Mech E	Umd
116
3/8/2026 13:11:14	Email	No	No	Yes	3.9	4.35	4.27	7	4	Chemistry B.A.	Public Health	Chemistry B.S.	San Diego State University
117
3/8/2026 13:12:04	Id	No	Yes	No	4	4	4	5	7	Chemistry	Chemistry	Chemistry	UIUC
118
3/8/2026 13:15:15	Id	No	No	No	4	4.67	4.33	7	6	Engineering Physics	Electrical Engineering	Electrical Engineering	
119
3/8/2026 13:17:30	Email	Yes	Yes	Yes	3.72	4.1	3.92	9	6	Studio Art	Studio Art	Studio Art	UCSC, UCR, UCM (rejected from UCD)
120
3/8/2026 13:24:05	Email	Yes	No	No	4	5	4.14	8	9	Bioengineering	Bioengineering	Bioengineering	California Institute of Technology
121
3/8/2026 13:26:08	Id	No	Didn't apply	No	4	4.571	4.286	7	7	Mech E	Mech E	n/a	UW probably
122
3/8/2026 13:28:25	Id	Didn't apply	Didn't apply	Yes	4	4.34	4.23	7	8	Plant Biology and Genetics	N/A	N/A	
123
3/8/2026 13:30:15	Id	Yes	No	Yes	3.57	4.17	3.91	8	7	COGNITIVE SCIENCE	HUMAN BIOLOGY	COGNITIVE SCIENCES	
124
3/8/2026 13:35:40	Didn't apply	Yes	No	Yes	3.79	4	3.86	5	4	why is this required??	Biology	Biology	I applied to nowhere. I'm cooked 😨😨
125
3/8/2026 13:38:43	Id	Yes	Yes	No	3.83	4.17	4.17	8	9	Econ	Finance	Finance	
126
3/8/2026 13:44:31	Didn't apply	Didn't apply	No	No	4	4.13	4.13	6	7			cognitive science	uChicago (EA)
127
3/8/2026 13:47:37	Email	Yes	Didn't apply	Yes	3.9	4	4.1	8	7	Buisness	Idk	none	
128
3/8/2026 13:48:47	Id	Yes	Didn't apply	Yes	4	4.94	4.19	5	5	Chemistry	Chemistry	------	Stanford
129
3/8/2026 13:53:18	Didn't apply	Yes	No	No	3.37	4.01	3.52	5	2	n / a	cs	cs	yale (early legacy) .
130
3/8/2026 13:54:25	Id	Yes	No	Yes	3.8	4.2	4.4	6	8	media studies	media studies and communication	media studies	
131
3/8/2026 13:54:54	Id	No	No	Yes	4	4.44	4.22	8	6	Data Science	Data Science	Data Science	UIUC (Cs & Stats) {this is more selective than cs + x, but less selective than pure cs}
132
3/8/2026 13:56:29	Id	No	No	No	3.5	3.54	3.54	10	8	Applied Math	Chemistry	Electrical Engineering	
133
3/8/2026 13:57:28	Email	No	Yes	Yes	3.83	4.13	3.98	5	6	Political Science	Political Science	Political Science	UCSC, UCR, UCD
134
3/8/2026 13:58:44	Id	No	Yes	Yes	4	4.4	4.33	8	8	Molecular and Cell Biology	Human Biology	Biological Sciences	UC Berkeley
135
3/8/2026 13:59:46	Id	Didn't apply	Didn't apply	No	3.97	4.5	4.3	8	9	Bio	NA	NA	
136
3/8/2026 14:01:31	Id	Yes	No	Yes	4	4.99	4.18	8	8	Applied Math	Applied Math	Applied Math	MIT
137
3/8/2026 14:01:49	Id	No	Yes	Yes	4	5.35	4.62	9	7	Molecular and Cell Biology, B.A.	Cognitive Science: Cognitive & Behavioral Neuroscience (joint major), B.S.	Cognitive Sciences, B.S. School of Social Sciences	UW
138
3/8/2026 14:02:21	Email	Yes	No	Yes	3.61	4.22	3.93	8	9	neuro	neuro	neuro	Usfca, ucsc, ucr, ucm (rejected from davis)
139
3/8/2026 14:05:58	Id	No	Yes	Yes	4	4.73	4.27	9	8	Neuroscience, B.A	Neurobiology, B.S.	Biological Sciences, B.S.	
140
3/8/2026 14:06:18	Id	No	Yes	Yes	4	4.34	4.18	4	10	Bio	Bio	Bio	Princeton (Restrictive Early Action)
141
3/8/2026 14:07:18	Didn't apply	No	Yes	Yes	4	4.72	4.3	7	8	Interdisciplinary Studies	Human Developmental Sciences	Social Policy & Public Service	UC Davis
142
3/8/2026 14:08:25	Id	No	Yes	Yes	3.7	4.16	3.94	7	9	Poli Sci	Poli Sci	Business	Georgetown
143
3/8/2026 14:08:45	Email	No	No	Yes	3.77	4.25	4	8	7	Urban studies	Media industries and communication	Literary journalism	SDSU
144
3/8/2026 14:10:24	Id	Yes	Didn't apply	Yes	3.4	3.4	3.4	8	9	chemistry	pharmacological chemistry	N/a	N/a
145
3/8/2026 14:10:38	Id	No	Yes	Yes	3.99	4.45	4.3	9	6	Anthropology	Anthropology - Sociocultural Anthropology	Anthropology	
146
3/8/2026 14:11:03	Id	No	Yes	Yes	4	4.67	4.27	9	8	Neuroscience, B.A.	Neurobiology, B.S.	Neuroscience, B.S.	University of Washington
147
3/8/2026 14:11:59	Didn't apply	Yes	Didn't apply	Yes	3.63	3.72	3.72	1	3	//////////////////	chemistry	/////////////////////////////////////////////	NYU ED2 but I'm not going because $$$ 💸💸💸 </3 so free from binding
148
3/8/2026 14:14:43	Id	Didn't apply	Didn't apply	No	3.8	4.35	4.1	9	8	Undeclared social sciences	n/a	n/a	UF oos
149
3/8/2026 14:16:07	Id	No	Didn't apply	Yes	4	4.24	4.24	8	9	Electrical and Comp Engineering	Electrical and Comp Engineering	n/a	Stanford
150
3/8/2026 14:18:32	Id	No	Didn't apply	Yes	3.8	4.48	4.12	6	4	Cognitive science	Applied math		Yale, UC Berkeley
151
3/8/2026 14:23:35	Id	No	Yes	No	3.91	4.77	4.27	4	8	Computer Science	Computer Science	Computer Science	UMich
152
3/8/2026 14:24:15	Email	Yes	Yes	No	3.86	4.29	4.15	8	6	Physics	Physics	Applied physics	UCSB (reception)
153
3/8/2026 14:28:38	Id	No	No	No	3.88	4.45	4:26	3	3	Finance	Economics	Business	
154
3/8/2026 14:30:19	Id	Didn't apply	Didn't apply	No	4	4.99	4.1	2	2	chem	nope	nope	caltech
155
3/8/2026 14:30:38	Email	No	Didn't apply	No	4	4	4	6	8	Mech eng	Mech eng	Na	UIUC
156
3/8/2026 14:35:31	Email	Didn't apply	Didn't apply	Yes	3.37	3.37	3.37	8	8	Applied math	N/A	N/A	Uc merced
157
3/8/2026 14:35:58	Id	Didn't apply	Didn't apply	No	3.15	3.73	3.26	6	4	Mechanical Engineering			UC Berkeley
158
3/8/2026 14:43:00	Id	No	No	No	3.7	4	4.3	6	8	EEP	Econ	Idk	
159
3/8/2026 14:44:02	Id	No	Didn't apply	Yes	3.93	4.5	4.15	5	10	idr	cognitive/behavioral neuroscience	didn't apply	unc (in state)
160
3/8/2026 14:44:10	Email	Didn't apply	Didn't apply	No	4	4.61	4.14	5	7	Economics			Fordham
161
3/8/2026 14:49:17	Id	No	Didn't apply	No	4	dk	dk	9	7	Economics	Urban planning	Economics	Umich Econ
162
3/8/2026 14:50:58	Id	Didn't apply	No	No	3.8	4.37	3.93	6	5	econ	n/a	math	Yale
163
3/8/2026 14:54:05	Id	Yes	Didn't apply	No	3.73	4.18	4.04	9	9	Data Science	Aerospace Engineering	N/A	Northeastern University
164
3/8/2026 14:59:07	Id	Yes	No	Yes	3.85	4.45	4.15	7	5	english	english	english	n/a
165
3/8/2026 15:01:51	Didn't apply	Yes	No	No	1.93	2.04	2.04	8	7	d	compeuter sceince	compeuter sceince	
166
3/8/2026 15:15:51	Id	Yes	No	No	4	4.98	4.15	9	10	Political Science	Public Policy	Business	Harvard, UCBerk Early, UCDavis, UIUC
167
3/8/2026 15:16:16	Didn't apply	Didn't apply	No	Yes	3.5	3.7	3.7	7	8	None	None	Civil Engineering	Santa Clara university
168
3/8/2026 15:16:53	Id	No	Didn't apply	No	4	N/A (intl student, no APs)	N/A	8	9	Molecular and Cell Biology	Molecular and Cell Biology	N/A	
169
3/8/2026 15:26:29	Id	No	Didn't apply	Yes	4	4.38	4.19	6	7	Political Science	International Relations / Political Science	N/A	
170
3/8/2026 15:26:37	Email	Yes	Yes	Yes	3.86	4.14	4.14	8	7	Molecular Cell Biology	Neurobiology	Pharmaceutical Sciences	UC Davis
171
3/8/2026 15:26:42	Id	Yes	Yes	No	3.97	4.6	4.3	8	8	cs	cs	cs	
172
3/8/2026 15:27:37	Didn't apply	No	Didn't apply	Yes	3.6	4.21	3.81	6	6	I did not apply	Data Science	I did not apply	CUNYs (Baruch & Hunter), Brandeis
173
3/8/2026 15:28:55	Email	Yes	Yes	No	4	4.33	4.33	8	8	Applied Math	CS	CSE	
174
3/8/2026 15:29:02	Id	No	Didn't apply	Yes	3.94	4.74	4.19	7	6	Integrative Biology	General Biology	N/A	UC Davis
175
3/8/2026 15:33:03	Didn't apply	Yes	Didn't apply	No	4	4.9	4.03	8	8	N/A	CS	N/A	
176
3/8/2026 15:33:42	Id	No	No	Yes	3.73	4.27	4.04	7	6	Nutrition and Metabolic Biology	Human Biology	Biology	UC Davis
177
3/8/2026 15:35:46	Email	Yes	No	No	4	4.86	4.86	10	8	biology	biology	biology	umich
178
3/8/2026 15:40:04	Id	No	Yes	Yes	4	4.99	4.03	9	10	Mechanical Engineering	Applied Math	Electrical Engineering	MIT
179
3/8/2026 15:46:35	Id	No	Yes	Yes	3.71	3.86	3.86	6	7	Poli Sci	Poli Sci	Poli Sci	UC Davis
180
3/8/2026 15:49:03	Didn't apply	Yes	No	No	4	4.09	4.09	4	8	NONE	Biology	Biology	UC Davis
181
3/8/2026 15:49:33	Email	Yes	Didn't apply	Yes	3.85	4.1	4.05	7	7	Nuclear Engineering	Chemical Engineering	N/A	
182
3/8/2026 15:53:29	Email	Yes	No	Yes	3.85	4.77	4.15	6	6	Biology	Public Health	Public Health	
183
3/8/2026 16:07:10	Id	No	No	Yes	4	4.4	4.29	9	9	poli sci	poli sci	poli sci	sdsu/uc davis
184
3/8/2026 16:11:17	Email	Didn't apply	No	Yes	3.84	4.12	4.12	8	8	Pol econ (undeclared)	DId not apply	Business Econ	UCSC lmao
185
3/8/2026 16:20:47	Id	No	No	No	3.98	4.4	4.15	8	8	neuroscience	cognitive science	neuro adjacent (forgot the specifics)	note: international student
186
3/8/2026 16:22:57	Didn't apply	Didn't apply	Yes	No	4	4.88	4.24	6	6			Biology	
187
3/8/2026 16:24:29	Email	Yes	No	No	3.74	4.53	3.95	7	9	Data Science	Data Science	Data Science	UC Davis
188
3/8/2026 16:35:02	Email	Yes	Yes	Yes	3.87	4.13	4.08	7	7	Enviromental Engineering	Structural Engineering	Enviromental Engineering	UC Davis
189
3/8/2026 16:41:42	Email	No	No	No	3.79	4.28	4.03	6	7	Ece	Ee	Ee	
190
3/8/2026 16:44:21	Id	Yes	Didn't apply	Yes	3.97	3.97	3.97	8	5	Economics	Economics	Economics	
191
3/8/2026 16:46:35	Id	No	Yes	Yes	4	4.09	4.09	6	4	Economics	Economics	Economics	University of Notre Dame
192
3/8/2026 16:51:12	Didn't apply	Yes	Yes	No	3.82	4.06	4	5	5	N/a	Economics	economics	
193
3/8/2026 16:51:29	Id	No	Yes	Yes	4	4.98	4.18	10	10	bioengineering	bioengineering	biology	harvard college
194
3/8/2026 16:54:35	Id	Yes	No	Yes	4	4.4	4.33	7	3	Economics	Business Economics	Business Admin	UC Davis
195
3/8/2026 16:57:47	Id	No	No	No	3.9	4.3	4.4	9	9	Bio	Bio	Bio	
196
3/8/2026 16:58:27	Didn't apply	No	Didn't apply	Yes	4	4.9	4.1	2	3	-	Mechanical Engineering	-	UMichigan (honestly I'm quite of a dumbass)
197
3/8/2026 17:03:02	Id	Didn't apply	Didn't apply	Yes	4	4.95	4.1	6	7	History	N/A	N/A	i only applied to the ucs.
198
3/8/2026 17:08:01	Id	Didn't apply	Yes	No	4	5	4.15	9	7	Data Science	-/-/-/-	Civil Engineering	
199
3/8/2026 17:10:06	Didn't apply	Didn't apply	Yes	No	4	4.32	4.24	3	4			economics	
200
3/8/2026 17:12:28	Id	No	Yes	Yes	4	4.28	4.28	7	4	Statistics	Econ+Math	Math	
201
3/8/2026 17:12:33	Id	No	Yes	No	3.88	3.98	3.98	5	5	Computer Science	Computer Science	Computer Science	Pace University, SUNY Binghamton, SUNY Stony Brook
202
3/8/2026 17:14:41	Email	No	No	Yes	3.69	3.72	3.72	8	10	History	Economics	Economics	UCD
203
3/8/2026 17:16:14	Didn't apply	Didn't apply	Yes	Yes	4	4.36	4.13	5	6			Economics	Georgetown U.
204
3/8/2026 17:17:32	Email	Yes	Didn't apply	Yes	3.9	4.25	4.03	7	9	Biology	Bioeng.		USC
205
3/8/2026 17:21:48	Id	No	Didn't apply	Yes	3.89	4.63	4.24	9	7	public health	public health	didnt apply	ut austin, umich, cwru ppsp finalist (40/4400)
206
3/8/2026 17:22:01	Id	No	Yes	Yes	3.9	4.53	4.16	7	9	Chemistry (Letters and Science)	Pharmacological Chemistry	Pharmaceutical Sciences	
207
3/8/2026 17:24:14	Id	No	Yes	Yes	3.93	3.93	3.93	7	8	math	math	math	
208
3/8/2026 17:29:23	Didn't apply	Yes	Didn't apply	Yes	3.72	3.78	3.78	3	4	n/a	Astronomy & Astrophysics	n/a	NONE???? Waitlisted NYU ED1 😭😭
209
3/8/2026 17:29:24	Id	Yes	Yes	No	4	4.72	4.22	8	9	met/eecs	comp eng	cse?	uiuc cs oos
210
3/8/2026 17:38:30	Didn't apply	Yes	Didn't apply	Yes	4	4.98	4.18	9	10		Structural Engineering		MIT // 4% > 28% ; Honestly laughable joke because from what I'm understanding I'm not getting into UCSD
211
3/8/2026 17:44:44	Id	No	Yes	No	4	4.02	4.02	9	10	Economics	Economics	Economics	UCD
212
3/8/2026 17:45:51	Id	Didn't apply	Didn't apply	Yes	4	4.52	4.18	7	5	Biology!!!			Early Berkeley offer!! (committed)
213
3/8/2026 17:54:04	Didn't apply	No	No	No	3.96	4.26	4.13	7	5		aerospace	aerospace	uiuc, purdue
214
3/8/2026 17:59:49	Email	Yes	Yes	No	4	4.27	4.27	7	9	Chemistry	Chemistry	Chemistry	UIUC ChemE
215
3/8/2026 18:03:15	Id	Yes	Didn't apply	No	3.8	4.4	4.2	7	8	Mech Eng	Mech Eng	N/A	University College London
216
3/8/2026 18:06:38	Id	No	Didn't apply	Yes	3.28	4.06	3.72	10	8	Political science	Political science international relations	Didnt apply	UC Santa Cruz, cal poly slo
217
3/8/2026 18:08:06	Email	Yes	Didn't apply	No	4	4.58	4.14	7	7	engineering undeclared	electrical engineering	n/a	uiuc grainger
218
3/8/2026 18:10:35	Id	Yes	Didn't apply	Yes	4	4	4	7	8	political science	public law	NA	Yale
219
3/8/2026 18:14:56	Didn't apply	Yes	No	Yes	3.92	4.2	4	7	6	N/A	Public Health with Concentration in Climate and Environmental Sciences	Environmental Engineering	
220
3/8/2026 18:17:09	Didn't apply	No	No	Yes	3.78	4.58	4	8	7	n/a	bio	bio	
221
3/8/2026 18:26:53	Email	No	Didn't apply	No	91.447	91.447	100	7	6	Business	Math	N/A	Note: my school does NOT do weighted GPAs + GPA is out of 100
222
3/8/2026 18:29:53	Email	No	Yes	Yes	4	4.73	4.36	8	6	physics	physics	physics	UC Davis
223
3/8/2026 18:30:04	Didn't apply	No	Didn't apply	No	3.6	4.05	4	7	5	Urban Planning	Urban Planning	N/A	Penn State (for Architecture - they accept 100 people out of 1000 applicants)
224
3/8/2026 18:34:50	Id	Yes	Didn't apply	Yes	3.6	4.24	3.9	5	7	Data Science	Data Science	N/A	applied to 40 schools, most of them coming out in the following weeks
225
3/8/2026 18:36:10	Email	No	Yes	Yes	3.89	4.42	4.35?	9	7	Media Studies (changed from HAAS)	Business Psychology	Business Administration	Cal State Long Beach | UC wise: UCSC
226
3/8/2026 18:47:16	Email	No	Yes	Yes	3.89	4.1	4.1	8	7	Microbial Bio	Global Health	Public Health	UC Davis
227
3/8/2026 18:47:30	Email	Didn't apply	Didn't apply	Yes	4	4.29	4.29	9	8	Biology	DNA	DNA	UDub
228
3/8/2026 18:47:57	Id	No	Yes	Yes	4	5	4.22	9	8	Physics	Undeclared	Undeclared	Caltech
229
3/8/2026 18:50:31	Id	Yes	No	Yes	3.82	3.99	3.99	8	6	CS	CS	CS	UMichigan
230
3/8/2026 18:51:13	Email	No	Yes	Yes	3.91	4.25	4.25	5	7	materials engineering	structural engineering	aerospace engineering	davis
231
3/8/2026 18:53:05	Didn't apply	Yes	Yes	No	3.57	3.76	3.76	5	7		English	English	UC davis
232
3/8/2026 18:54:30	Didn't apply	Didn't apply	Yes	No	3.44	3.46	3.46	4	3	n/a	n/a	Economics	UT Austin
233
3/8/2026 18:56:04	Id	No	Didn't apply	Yes	3.74	4.42	4.04	9	9	Nuclear engineering	ChemE oceanography alt major	Didn’t apply	UCSC undeclared major, ucr chemE with honors invitation
234
3/8/2026 18:56:54	Id	No	Didn't apply	Yes	4	4.21	4.21	3	8	cognitive science	chemistry	i did not apply to uci	mit (early action)
235
3/8/2026 19:03:36	Id	No	Yes	Yes	3.98	4.71	4.29	7	8	Political Science	Political Science - Public Policy	Social Policy and Public Service	USC
236
3/8/2026 19:05:14	Id	No	Yes	Yes	3.9	4.7	4.3	8	7	Psych	Psych	Psych	Davis
237
3/8/2026 19:16:16	Id	No	No	No	3.87??	4.33???	4.33???	4	4	enviro	enviro	enviro	ucsc ToTTTTTTTTTTT
238
3/8/2026 19:25:23	Id	Yes	Didn't apply	No	4	4.99	4.12	8	9	Civil Engineering	Aerospace Engineering	N/A	I applied rd for all 8 ivy leagues so N/A
239
3/8/2026 19:29:18	Didn't apply	Didn't apply	Yes	Yes	3.3	3.56	3.49	10	5	Didn't apply	Didn't apply	Public Health major	UCSB reception idfk how
240
3/8/2026 19:32:47	Id	No	Yes	No	3.89	4.18	4.04	10	10	engineering	engineering	engineering	uni north carolina chapel hill
241
3/8/2026 19:38:08	Id	No	Yes	Yes	3	3	3	7	7	Biology	Human Biology	Bioengineering	San Francisco State University
242
3/8/2026 19:47:45	Id	Yes	Didn't apply	No	4	4.11??????	idk	7	8	Computer Science	Computer Science	Computer Science	Carnegie Mellon University (breaking the ED contract bc unable to afford)
243
3/8/2026 20:04:19	Id	Yes	Didn't apply	No	3.68	3.93	4.06	9	10	Nutrition and Metabolic Biology	Human Biology	N/A	Pitzer College
244
3/8/2026 20:05:32	Id	No	Yes	Yes	4	4.89	4.11	6	7	Bio	Bio	Bio	UCD
245
3/8/2026 20:06:03	Email	No	Yes	Yes	4	4.99	4.15	8	9	molecular biology	Bioengineering	CS	University of Chicago
246
3/8/2026 20:07:20	Id	Yes	Yes	Yes	3.47	3.5	3.5	9	8	History	English	Undeclared Major	University of Florida, Georgia Tech
247
3/8/2026 20:11:26	Id	No	Yes	No	3.93	4.48	4.21	8	9	HAAS— Spieker (Business Admin)	Business	Business	
248
3/8/2026 20:12:08	Email	No	Didn't apply	Yes	3.94	4.19	3.94	8	9	chemistry	mechanical major	didn't apply	case western
249
3/8/2026 20:13:33	Id	No	No	No	4	4.53	4.48	7	7	Political Science	Political Science	Political Science	
250
3/8/2026 20:13:41	Email	Yes	No	No	0.58	0.61	0.61	9	10	i thought maybe it's a poliltical science major	these one i chose economics	i want to do farmaceutical major	san diego city college
251
3/8/2026 20:33:45	Email	No	No	Yes	3.77	4.27	4.18	7	8	Economics	Business Economics	Business Administration	Pepperdine
252
3/8/2026 20:45:34	Email	Didn't apply	Didn't apply	No	3.7	4	idk	6	6	chem	no	no	WAITLSTED FOR GOERGIA TECH I HATE MY LIFE
253
3/8/2026 20:55:39	Id	Yes	No	Yes	3.8	4.39	4	9	9	Sociology	Political Science	Criminology	
254
3/8/2026 21:34:51	Id	No	Didn't apply	No	3.92	4.52	4.42	9	8	SUBP	Economics	N/A	
255
3/8/2026 21:45:20	Email	No	Yes	Yes	3.71	4.46	3.81	8	7	History	History	History	Davis
256
3/8/2026 22:07:55	Id	Yes	No	Yes	3.9	4.4	4.23	9	8	Economics	Economics	Economics	
257
3/8/2026 22:32:52	Email	Didn't apply	Didn't apply	No	3.95	4.43	4.43	7	8	Political Science	did not apply	did not apply	
258
3/9/2026 1:20:02	Email	No	Yes	Yes	4	4.23	4.23	7	7	Math	Math	Math	Davis
259
3/9/2026 2:09:16	Id	No	Yes	Yes	4	4.79	4.25	7	8	Political Science	Political Science - International Relations	Political Science	UC Davis/McGill
260
3/9/2026 6:47:47	Id	No	Yes	No	4	4.6	4.27	7	8	Sociology	Political Science	Sociology	UNC Chapel-Hill (Honors Program)
261
3/9/2026 9:29:01	Id	No	Didn't apply	No	4	4.26	4.26	8	5	statistics/math	math and economics	N/A	University of Washington
262
3/9/2026 12:19:23	Id	Yes	No	Yes	3.55	4.09	3.91	8	8	Political Science	Political Science	Political Science	UC Santa Cruz
263
3/9/2026 13:47:10	Id	Yes	Yes	No	3.9	3.9	3.9	8	7	Philosophy	Philosophy	Philosophy	USF, SFSU, SJSU (all safety)
264
3/9/2026 15:16:02	Id	Yes	Yes	Yes	4	4.67	4.33	8	7	Mechanical Engineering	Mechanical Engineering	Mechanical Engineering	Northeastern (Boston Campus)
265
3/9/2026 17:05:29	Email	No	Yes	Yes	3.7	4.1	4.1	10	8	Biology	Public health	biological sciences	UC Davis
266
3/9/2026 21:30:35	Id	No	Yes	Yes	4	4.56	4.2	8	8	Physics	Physics	Physics	Stanford
267
3/10/2026 0:23:08	Email	No	Yes	No	3.97	Na	Na	8	10	Pub health	Human bio	Pub health	
268
3/10/2026 2:29:10	Id	No	No	No	3.9	4	4	8	8	Data Science	Data Science	Data Science	UW or UIUC
269
3/10/2026 2:36:25	Email	Didn't apply	Didn't apply	No	4	4	4.0 (im int)	9	9	GMP Haas	n/a	b/a	
270
3/10/2026 5:29:49	Didn't apply	No	No	Yes	4.2	4.2	N/A	8	7	Astrophysics	N/A	N/A	N/A. Btw random tip, surveyswap.io was a lifesaver for finding respondents, and it's free. Anyway, good luck!
271
3/10/2026 21:54:37	Email	No	No	Yes	3.91	4.64	4.27	6	6	Mechanical Engineering	Mechanical Engineering	Mechanical Engineering	SJSU
272
3/10/2026 22:12:06	Id	No	Yes	Yes	3.87	4.67	4.27	7	7	Sociology	Sociology	Sociology	USC
273
3/10/2026 23:32:56	Email	No	Yes	Yes	3.86	4.18	4.08	4	3	applied math	n/a	applied math	currently all the free ucs that i applied to, i only applied to ucs
274
3/10/2026 23:33:55	Id	No	Yes	No	4	4.66	4.13	5	8	ECE	ECE	EE	Stanford, Georgia Tech
275
3/10/2026 23:44:37	Didn't apply	No	No	No	3.86	4.38	4.15	6	6	n/a	bio	bio	udub
276
3/11/2026 7:36:15	Id	No	Didn't apply	No	4	4	4	8	6	Computer Science	Computer Science	NA	University of Virginia
277
3/11/2026 16:36:15	Didn't apply	Yes	No	Yes	3.64	4.13	4.13	6	8	NA	Stats	DATA Science	
278
3/12/2026 16:44:08	Id	Yes	Didn't apply	No	3.93	4.43	4.11	7	7	Political Science	Political Science - Intl relations	N/A	

"""

# 2. 使用原始问卷问题作为表头
COLUMNS = [
    "Timestamp",
    "Berkeley id or email?",
    "Is your UCSD #3 prestige banner there?",
    "Can you log in to the UCI link?",
    "Did you apply for financial aid?",
    "GPA(UC UW)?",
    "GPA(UC W)",
    "GPA(UC W capped)",
    "Rate your piqs on a scale of 1-10",
    "Rate your ec's on a scale of 1-10",
    "UCB major?",
    "UCSD major?",
    "UCI major?",
    "Best college you've already gotten accepted to(not required)"
]


def process_and_clean_data(raw_text):
    print("正在解析粘贴的原始文本...")
    lines = raw_text.strip().split('\n')
    data = []

    # --- 第一阶段：文本解析 ---
    for line in lines:
        # 去除聊天记录或复制带来的 标签
        clean_line = re.sub(r'\\s*', '', line).strip()

        # 跳过空行、纯数字行(如表单序号)、以及表头行
        if not clean_line or clean_line.isdigit() or clean_line.startswith('Timestamp'):
            continue

        # 识别数据行：以日期开头 (如 3/8/2026 或 3/10/2026)
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}', clean_line):
            parts = clean_line.split('\t')

            # 如果有人没填最后几题，用空字符串补齐，防止列数错位
            while len(parts) < len(COLUMNS):
                parts.append('')

            data.append(parts[:len(COLUMNS)])
        else:
            # 如果不是以日期开头，说明是上一行的文字被硬换行了（比如某个同学很长的吐槽）
            if data:
                data[-1][-1] += " " + clean_line

    df = pd.DataFrame(data, columns=COLUMNS)
    print(f"解析完成！共提取出 {len(df)} 条有效数据记录。")

    # --- 第二阶段：数据清洗 ---
    print("正在清洗 GPA 和评分格式...")

    # 提取 GPA 数字的内部函数
    def extract_gpa(val):
        val = str(val).strip().lower().replace(',', '.')
        match = re.search(r'(\d+\.?\d*)', val)  # 抓取数字
        if match:
            num = float(match.group(1))
            if num > 10:  # 处理填了百分制的同学（如 97 或 91.447）
                return round((num / 100) * 4.0, 2)
            return num
        return None

    # 清洗三列 GPA
    gpa_cols = ["GPA(UC UW)?", "GPA(UC W)", "GPA(UC W capped)"]
    for col in gpa_cols:
        df[col] = df[col].apply(extract_gpa)

    # 提取评分数字 (1-10) 的内部函数
    def extract_rating(val):
        nums = re.findall(r'\d+', str(val))
        return int(nums[0]) if nums else None

    # 清洗 PIQ 和 EC 评分
    rating_cols = ["Rate your piqs on a scale of 1-10", "Rate your ec's on a scale of 1-10"]
    for col in rating_cols:
        df[col] = df[col].apply(extract_rating)

    return df


if __name__ == "__main__":
    # 运行处理函数
    cleaned_df = process_and_clean_data(RAW_DATA)

    # 导出为 CSV 文件 (utf-8-sig 确保 Excel 打开不乱码)
    output_filename = "uc_application_data_cleaned.csv"
    cleaned_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"大功告成！清洗后的数据已保存为：{output_filename}")

    # 打印前 3 行看看效果
    print("\n--- 你的数据预览 (前 3 行) ---")
    print(cleaned_df.head(3))