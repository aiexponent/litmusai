# How the cases were selected

This file was committed before any case file, expected answer or declaration was written, and before any screen was run. The git history shows the order.

## Sources

| Document | Where it was read | Read on |
|---|---|---|
| Commission Guidelines on prohibited artificial intelligence practices established by Regulation (EU) 2024/1689 (AI Act), C(2025) 5052 final, 29 July 2025, English, 134 pages | https://ec.europa.eu/newsroom/dae/redirection/document/112367 (SHA-256 `298bf8677884b333fae6d5f84aac947f45a59dff6027ca038ba08615092fd82f`, checked) | 2026-11-02 |
| Regulation (EU) 2026/1744 (Digital Omnibus on AI), Article 1 point (7) and recitals 10 to 14 | https://publications.europa.eu/resource/celex/32026R1744 (English XHTML) | 2026-11-02 |
| Regulation (EU) 2024/1689, Article 5 | https://publications.europa.eu/resource/celex/32024R1689 (English XHTML) | 2026-11-02 |

Page numbers for the guidelines are the numbers printed at the foot of each page. The PDF page number is five higher (printed page 84 is PDF page 89). Paragraph numbers are the guidelines' own numbers in brackets.

## The rule

A case is made from:

1. every worked example in chapters 3 to 9 of the guidelines (Article 5(1), points (a) to (h)) that states whether a described AI system or practice falls inside or outside a prohibition, or says the answer depends on facts the example does not give; and
2. every example in recitals 12, 13 and 14 of Regulation (EU) 2026/1744 for points (ba) and (bb).

Chapters 1, 2, 10, 11 and 12 of the guidelines are not used.

**Departure from the brief, stated up front.** The brief named recitals 13 and 14 only. In the published text the examples for point (ba) (try-on and medical applications, edits that do not increase exposure, cartoonish depictions, and the provider and deployer cases) are all in recital 12. Recital 13 holds only the two point (bb) examples, and recital 14 restates limits already given in recital 12. Using 13 and 14 alone would give no case for point (ba). The brief's own source list says "recitals 12 to 14", so recital 12 is included. Every case file and every `source_ref` names its recital, so a reader who wants the narrower rule can drop the recital 12 rows and rescore.

## What counts as a worked example and as a stated conclusion

A **worked example** is a passage that describes a particular AI system or a particular use of one: what it does, to whom, and in what setting. It is usually introduced by "for example", "for instance", "e.g." or a bulleted list of examples. A passage that only describes a place, a definition, a legal test or a general principle, without a system or use, is not a worked example.

A **stated conclusion** is an express statement in the passage about the prohibition as a whole: that the system or use is prohibited, falls within the prohibition, is likely or would normally be prohibited (red); that it is not prohibited, out of scope, permitted or covered by an exception (clear); or that it may be prohibited if, provided that, or depending on a fact the passage does not give (amber). Because the guidelines treat the conditions of each prohibition as cumulative, a statement that one required condition is **not** met (for example "is not emotion recognition") counts as a clear conclusion. A statement that one condition **is** met (for example "fulfils the condition of remoteness"), or an example given only to show what a term or a type of harm means, does not count, and is logged as "illustrates one element".

When one recital passage states the same conclusion for both non-consensual intimate material and child sexual abuse material, it gives one case for point (ba) and one for point (bb). A passage that repeats an example already counted is logged as a duplicate and does not become a second case.

## Case ids

`<point letters>-<two digits>`, numbered in the order the passages appear in the source: for example `a-01`, `f-03`, `ba-01`, `bb-02`.

## Examples considered

Every passage looked at while applying the rule, in the order of the source. "Point" is the Article 5(1) point the passage sits under. A passage that names several systems is split into rows. A passage that touches two points is counted once under each in the summary, unless it became a case. Chapter 10 of the guidelines (safeguards for point (h)) and chapter 2 (general scope) were not read for cases, as the rule covers chapters 3 to 9 only.

### Summary

| Point | Passages considered | Cases | red | amber | clear |
|---|---|---|---|---|---|
| a | 34 | 17 | 3 | 2 | 12 |
| b | 30 | 16 | 4 | 1 | 11 |
| c | 32 | 26 | 10 | 4 | 12 |
| d | 23 | 19 | 3 | 2 | 14 |
| e | 13 | 8 | 2 | 0 | 6 |
| f | 42 | 35 | 14 | 0 | 21 |
| g | 17 | 14 | 4 | 0 | 10 |
| h | 28 | 15 | 2 | 2 | 11 |
| ba | 22 | 16 | 5 | 0 | 11 |
| bb | 13 | 9 | 4 | 0 | 5 |
| all | 254 | 175 | 51 | 11 | 113 |

### Guidelines C(2025) 5052, chapters 3 to 9

| Point | Location | Passage | Case | Reason if not a case |
|---|---|---|---|---|
| a | p. 19, para. 65 | List of subliminal techniques (flashed images, masked sounds, tactile stimuli and others) | no | explains a term; the text says they are not necessarily prohibited |
| a | p. 20, para. 66 | Brain-interface game covertly extracting bank details | a-01 |  |
| a | p. 20, para. 66 | Brain-interface applications designed safely | a-02 |  |
| a | p. 21, para. 68 | Sensory manipulation with background audio; personalised persuasive messages | no | illustrates one element (the technique), no conclusion on the prohibition |
| a | p. 21, para. 69 | System learning manipulative techniques from training data or feedback | no | illustrates one element (the technique) |
| a | p. 21, para. 69 | Merely incidental manipulative behaviour with preventive measures | a-03 |  |
| a | p. 22, para. 73 | Chatbot impersonating a relative with a synthetic voice to run scams | no | given as an example of a deceptive technique; no conclusion on the prohibition |
| a | p. 22, para. 73 | System that halts bad behaviour while being evaluated | a-04 |  |
| a | p. 23, para. 73 | Generative chatbot that hallucinates, with disclosures and safeguards | a-05 |  |
| a | p. 25, para. 82 | Chatbot with subliminal cues in ads pushing harmful financial decisions | a-06 |  |
| a | p. 25-26, para. 82 | AI impersonating other persons | a-07 |  |
| a | p. 26, para. 84 | Well-being chatbot pushing excessive exercise | a-08 |  |
| a | p. 27, para. 87 | Chatbot promoting self-harm or violence | no | illustrates a type of harm, no conclusion on a system |
| a | p. 27-28, para. 88 | Companion app fostering emotional dependency | no | illustrates a type of harm |
| a | p. 28, para. 89 | Chatbot offering fraudulent products | no | illustrates a type of harm |
| a | p. 28, para. 90 | Combined harms: addictive design, harassment, deep fakes | no | illustrates combinations of harm |
| a | p. 29-30, para. 93 | Suggestions to commit crimes reach the threshold; bruises do not | no | explains the harm threshold, no system described |
| a | p. 31, para. 96 | Provider cannot foresee depression from outside causes | no | general point on causation, no system described |
| b | p. 33, para. 105 | AI toy urging risky challenges | b-01 |  |
| b | p. 33-34, para. 105 | Addictive children's game | b-02 |  |
| b | p. 34, para. 105 | Toys, games and learning apps in general | no | duplicate of the para. 121 list (b-08) |
| b | p. 34, para. 106 | Scams aimed at older people | b-03 |  |
| b | p. 34, para. 106 | Assistive robot forcing older people into activities | b-04 |  |
| b | p. 34, para. 106 | Assistants and assistive robots in general | no | duplicate of the para. 121 list (b-09) |
| b | p. 35, para. 108 | Therapeutic chatbot pushing people with mental disabilities to buy products; grooming of girls with disabilities | no | illustrates one element (exploitation), no conclusion on the prohibition |
| b | p. 35, para. 108 | Applications not designed to be accessible | b-05 |  |
| b | p. 35, para. 110 | Predatory financial ads in low-income postcodes | no | illustrates one element (exploitation), no conclusion on the prohibition |
| b | p. 35-36, para. 110 | Inadvertently biased system affecting disadvantaged people | b-06 |  |
| b | p. 36, para. 111 | Intersection of socio-economic status and ethnic origin | no | general point, no system described |
| b | p. 36, para. 111 | Targeting by phone model, city size and travel | b-07 |  |
| b | p. 36, para. 112 | Chatbot pushing migrants toward extremist views | no | illustrates one element (exploitation), no conclusion on the prohibition |
| b | p. 37-38, para. 116 | Child sexual abuse material, addictive schedules, anthropomorphic systems for children | no | illustrates types of harm |
| b | p. 38, para. 116 | Legitimate user engagement practices | no | general statement, no system described |
| b | p. 38-39, para. 117 | Expensive treatments sold to older people; differential insurance pricing | no | illustrates types of harm |
| b | p. 39, para. 118 | Emotion recognition support tool manipulating purchases | no | illustrates a type of harm |
| b | p. 39, para. 119 | Chatbot inciting disadvantaged groups to violence | no | illustrates a type of harm |
| b | p. 39-40, para. 120 | Group harms: societal costs, financial exclusion, polarisation | no | illustrates types of harm |
| b | p. 40, para. 121 | Learning and game support for children | b-08 |  |
| b | p. 40, para. 121 | Assistants and robots for older people | b-09 |  |
| b | p. 40, para. 121 | Integration support for disadvantaged people | b-10 |  |
| b | p. 40, para. 121 | Aids for visually or hearing impaired people | b-11 |  |
| b | p. 40, para. 121 | Accessibility solutions | b-12 |  |
| b | p. 40, para. 121 | AI-enabled prosthetics | b-13 |  |
| a/b | p. 41, para. 124 | Image flashes under (a); insurance offers to older people under (b) | no | explains which point applies, no conclusion on whether prohibited |
| a | p. 42, para. 128 | Transparent personalised recommendations | a-09 |  |
| a | p. 42, para. 128 | Imperceptible images steering choices | no | illustrates one element (manipulation) |
| a | p. 42, para. 129 | Transparent customer-support emotion analysis | a-10 |  |
| a | p. 42, para. 129 | Hidden emotion recognition to push higher prices | no | illustrates one element (manipulation), no conclusion on harm |
| a | p. 42, para. 130 | Language app with subliminal techniques and consent | a-11 |  |
| a | p. 42-43, para. 131 | Compliance with data protection law | no | general statement, no system described |
| a | p. 43, para. 132 | Subliminal techniques in medical treatment with consent | a-12 |  |
| a | p. 43, para. 133 | Personalised advertising on user preferences | a-13 |  |
| b | p. 43, para. 133 | Classifiers detecting child sexual abuse material | b-14 |  |
| b | p. 43, para. 133 | Banking systems using age or socio-economic inputs to protect | b-15 |  |
| b | p. 43, para. 133 | Driver drowsiness detection | b-16 |  |
| a | p. 44, para. 134 | Anthropomorphic companion app without other manipulation | a-14 |  |
| a | p. 44, para. 134 | Therapeutic chatbot with subliminal techniques to quit smoking | a-15 |  |
| a | p. 44, para. 134 | Music service recommending songs by mood | a-16 |  |
| a | p. 44, para. 134 | Phishing simulation in security training | a-17 |  |
| a | p. 45, para. 139 | Dark patterns under the Digital Services Act | no | explains a term |
| a | p. 46, para. 142 | Targeted political advertising under the political advertising regulation | no | says compliance helps; no firm conclusion on a system |
| a/b | p. 47, para. 143 | Differential pricing in insurance | no | pointer to another authority's statement; no system described |
| c | p. 50-51, para. 154 | Credit score as profiling (court case) | c-01 |  |
| c | p. 51, para. 155 | Refugee camp surveillance scoring abscond risk | c-02 |  |
| c | p. 53, para. 161 | Public trust score combined with human review | c-03 |  |
| c | p. 53, para. 162 | Authority obtains a credit score from another company | no | illustrates one element (who produces the score) |
| c | p. 53-54, para. 165 | People singled out for extra fraud inspections | no | explains a term |
| c | p. 54, para. 166 | Tax returns selected using social habits | c-04 |  |
| c | p. 54-55, para. 166 | Welfare fraud score using spouse's nationality | c-05 |  |
| c | p. 55, para. 166 | Welfare fraud score using relevant data | c-06 |  |
| c | p. 55, para. 166 | Employment agency score with health data | c-07 |  |
| c | p. 55-56, para. 167 | Family profiling for children at risk | c-08 |  |
| c | p. 56, para. 167 | Municipal trustworthiness blacklist | c-09 |  |
| c | p. 56, para. 168 | Child benefit fraud profiling | c-10 |  |
| c | p. 56, para. 168 | Student housing grant fraud indicators | c-11 |  |
| c | p. 56-57, para. 168 | Government rating of citizens across life | c-12 |  |
| c | p. 57, para. 169 | Awards or preferential treatment | no | general statement, no system described |
| c | p. 57, para. 170 | Life insurer using bank spending data | c-13 |  |
| c | p. 57, para. 170 | Credit agency using unrelated characteristics | c-14 |  |
| c | p. 57-58, para. 171-172 | Burden of proof; compliance with high-risk rules | no | general statement, no system described |
| c | p. 58, para. 173 | Scoring legal entities such as municipalities | c-15 |  |
| c | p. 58, para. 173 | Entity score aggregating employees' or students' behaviour | c-16 |  |
| c | p. 58, para. 174 | Platform ratings of drivers and hosts | c-17 |  |
| c | p. 58-59, para. 175-176 | Credit and risk scoring not prohibited as such | no | general statement; its examples are in para. 177 |
| c | p. 59, para. 177 | Credit scoring on income and expenses | c-18 |  |
| c | p. 59, para. 177 | Customer fraud evaluation | c-19 |  |
| c | p. 59, para. 177 | Telematics insurance premium | c-20 |  |
| c | p. 60, para. 177 | Health data for diagnosis | c-21 |  |
| c | p. 60, para. 177 | Platform safety profiling | c-22 |  |
| c | p. 60, para. 177 | Targeted commercial advertising | c-23 |  |
| c | p. 60, para. 177 | Refugee camp data for resettlement decisions | c-24 |  |
| c | p. 60, para. 177 | Shopping platform perks | c-25 |  |
| c | p. 60, para. 177 | Police scoring under criminal law | c-26 |  |
| c | p. 61, para. 179-183 | Interplay with consumer, data protection and credit law | no | general statement, no system described |
| d | p. 63, para. 190 | Uses of crime prediction (patrol planning, controls) | no | explains a term |
| d | p. 64-65, para. 196 | Group profile applied to an individual | no | illustrates one element (profiling) |
| d | p. 66, para. 202 | Terrorism prediction from personal traits | d-01 |  |
| d | p. 66, para. 202 | Tax offence prediction from profile | d-02 |  |
| d | p. 66, para. 202 | Children scored by their links to others | d-03 |  |
| d | p. 68, para. 208 | Private analytics firm working for police | d-04 |  |
| d | p. 68, para. 209 | Bank anti-money-laundering screening | d-05 |  |
| d | p. 68-69, para. 210-211 | Private customer profiling for business purposes | d-06 |  |
| d | p. 69, para. 212 | Area-based predictive policing | d-07 |  |
| d | p. 69, para. 212 | Customs prediction of where drugs are | d-08 |  |
| d | p. 69, para. 212 | Gunshot detection | d-09 |  |
| d | p. 69-70, para. 213 | Location score linked to a person's residence | no | says only that the system is person-based (one element); no firm conclusion |
| d | p. 70, para. 214 | Crowd behaviour classification with human review | d-10 |  |
| d | p. 70, para. 214 | Armed robbery investigation with number-plate data | d-11 |  |
| d | p. 70, para. 214 | Early release assessment | d-12 |  |
| d | p. 70-71, para. 214 | Judge's pre-trial detention tool | d-13 |  |
| d | p. 71, para. 214 | Probation risk support | d-14 |  |
| d | p. 71, para. 214 | Customs goods risk assessment | d-15 |  |
| d | p. 71, para. 215 | Company tax or customs fraud risk | d-16 |  |
| d | p. 71, para. 215 | Customs instructions to companies | d-17 |  |
| d | p. 71-72, para. 216 | Sole trader or lawyer | d-18 |  |
| d | p. 72, para. 217 | Administrative offences | d-19 |  |
| d | p. 72-73, para. 218-221 | Offence classification; interplay with other law | no | general statement, no system described |
| e | p. 74, para. 225 | Scraping tools in general | no | general statement |
| e | p. 75, para. 229 | Scraping for one criminal or a group of victims | no | general form of the para. 230 example (e-01) |
| e | p. 75, para. 230 | Crawler collecting images of trafficking victims | e-01 |  |
| e | p. 75, para. 230 | Step-by-step scraping by group | e-02 |  |
| e | p. 75, para. 231 | Targeted and untargeted searches combined | e-03 |  |
| e | p. 75, para. 232 | Face recognition company scraping social media | no | illustrates one element (internet as source); the text does not state a conclusion |
| e | p. 75, para. 233 | Reverse image search | e-04 |  |
| e | p. 76, para. 234 | Untargeted scraping of voice samples | e-05 |  |
| e | p. 76, para. 234 | Scraping without AI | e-06 |  |
| e | p. 76, para. 234 | Face database for training and testing only | e-07 |  |
| e | p. 76, para. 235 | Faces harvested to generate fictitious people | e-08 |  |
| e | p. 76, para. 236 | Databases built before the prohibition and not expanded | no | implies but does not state a conclusion; points to data protection law |
| e | p. 76, para. 237-238 | Act of identification; data protection | no | general statement |
| f | p. 76-77, para. 240 | Areas where emotion recognition is used | no | explains a term |
| f | p. 79, para. 249 | Observing a smile | f-01 |  |
| f | p. 79, para. 249 | Identifying whether a person is sick | f-02 |  |
| f | p. 79, para. 249 | Broadcaster counting presenters' smiles | f-03 |  |
| f | p. 79, para. 249 | Inferring that a person is happy, an employee is angry, a student is furious | no | says only that these are emotion recognition (one element) |
| f | p. 79, para. 249 | Pilot or driver fatigue alerts | f-04 |  |
| f | p. 80, para. 251 | Sentiment of written text | f-05 |  |
| f | p. 80, para. 251 | Emotions from keystrokes, faces or posture | no | states the biometric condition only; no setting given |
| f | p. 81, para. 254 | Call centre tracking employees' anger | f-06 |  |
| f | p. 81, para. 254 | Emotion recognition for personal training only | f-07 |  |
| f | p. 81, para. 254 | Call centre tracking customers' anger | f-08 |  |
| f | p. 81, para. 254 | Emotional tone of hybrid teams | f-09 |  |
| f | p. 81, para. 254 | Recruitment | f-10 |  |
| f | p. 81, para. 254 | Probation period | f-11 |  |
| f | p. 82, para. 254 | Supermarket tracking employees' happiness | f-12 |  |
| f | p. 82, para. 254 | Supermarket or bank spotting suspicious customers | f-13 |  |
| f | p. 82, para. 255 | Language app outside an institution | f-14 |  |
| f | p. 82, para. 255 | Language app required by an institution | f-15 |  |
| f | p. 82, para. 255 | Exam eye-tracking for gaze | f-16 |  |
| f | p. 82, para. 255 | Exam eye-tracking that also detects emotions | f-17 |  |
| f | p. 82, para. 255 | Institution inferring interest and attention | f-18 |  |
| f | p. 82, para. 255 | Role-play training for actors or teachers | f-19 |  |
| f | p. 83, para. 255 | Admission tests | f-20 |  |
| f | p. 83, para. 255 | Detecting students talking in online lectures | f-21 |  |
| f | p. 83, para. 255 | Same, also detecting emotions | f-22 |  |
| f | p. 83, para. 255 | Institution watching teachers and students | f-23 |  |
| f | p. 83, para. 257 | Burnout or depression detection | f-24 |  |
| f | p. 83, para. 258 | Safety does not include protecting property | no | explains a term |
| f | p. 84, para. 261 | Fatigue of pilots and drivers | no | duplicate of f-04 |
| f | p. 84, para. 263 | Support for autism and accessibility | f-25 |  |
| f | p. 84, para. 263 | Wellbeing, motivation, satisfaction | f-26 |  |
| f | p. 84, para. 263 | Employer measuring anxiety or boredom | f-27 |  |
| f | p. 84, para. 263 | Stress monitoring around dangerous machines | f-28 |  |
| f | p. 84, para. 264 | Member State law barring medical use at work | no | about national law, no system described |
| f | p. 85, para. 265 | Out-of-scope summary (non-biometric, physical states) | no | restates earlier examples |
| f | p. 85, para. 266 | Commercial emotion recognition on customers | f-29 |  |
| f | p. 85, para. 267 | Crowd control on overall noise and mood | f-30 |  |
| f | p. 85, para. 268 | Crowd control counting angry faces | f-31 |  |
| f | p. 85, para. 269 | Care robots | f-32 |  |
| f | p. 85, para. 269 | Doctor during an examination | f-33 |  |
| f | p. 85, para. 269 | Emergency call voice monitors | f-34 |  |
| f | p. 86, para. 270 | Stadium aggression detection catching staff | f-35 |  |
| g | p. 87, para. 276 | Advertising display choosing ads by age or gender | no | explains a term |
| g | p. 87, para. 277 | Categorising by clothes or accessories | g-01 |  |
| g | p. 87, para. 277 | Categorising by social media activity | g-02 |  |
| g | p. 88, para. 280 | Marketplace try-on filter | g-03 |  |
| g | p. 88, para. 280 | Social network photo filters | g-04 |  |
| g | p. 88, para. 280 | Political orientation from photos | g-05 |  |
| g | p. 88, para. 280 | Sexual orientation from photos | g-06 |  |
| g | p. 89, para. 282 | Whole group categorised | g-07 |  |
| g | p. 89, para. 282 | Attribute estimation; singling out by scar or tattoo | no | the text says all conditions must still be met (one element) |
| g | p. 89, para. 283 | Race from voice | g-08 |  |
| g | p. 89, para. 283 | Religion from tattoos or faces | g-09 |  |
| g | p. 89, para. 283 | Sorting by skin or eye colour | g-10 |  |
| g | p. 89, para. 283 | DNA of crime victims | g-11 |  |
| g | p. 90, para. 285 | Labelling to prevent hiring bias | g-12 |  |
| g | p. 90, para. 285 | Skin colour for cancer diagnosis | g-13 |  |
| g | p. 90, para. 286 | Police labelling an abuse material dataset | g-14 |  |
| g | p. 90-91, para. 287-288 | Interplay with other law | no | general statement |
| h | p. 91, para. 291 | Placing real-time identification systems on the market | h-01 |  |
| h | p. 91, para. 292 | Retrospective (post) identification | h-02 |  |
| h | p. 93-94, para. 302 | Following a fleeing suspect | no | explains a term |
| h | p. 94, para. 303 | Airport e-gate verification | h-03 |  |
| h | p. 94, para. 305 | Face scan to enter a power plant | h-04 |  |
| h | p. 94, para. 306 | Ceiling cameras in metro stations | no | says only that remoteness is met (one element) |
| h | p. 95, para. 306 | Biometric metro tickets | h-05 |  |
| h | p. 95, para. 307 | Voice, gait and keystroke identification | no | the text says it does not imply a prohibition (one element) |
| h | p. 95, para. 308 | Body-cams at a demonstration | no | says only that remoteness is met (one element) |
| h | p. 95, para. 309 | Schengen database as reference database | no | explains a term |
| h | p. 96, para. 311 | Live screening of all concert visitors | no | says only that it is real-time (one element) |
| h | p. 96, para. 311 | Identification on concert video after the event | h-06 |  |
| h | p. 96, para. 312 | Covert phone photo, immediate search | h-07 |  |
| h | p. 96-98, para. 314-318 | Public and non-public spaces (concert venue, gated estate, online spaces, badge-only workplace, prison, border, airport) | no | describe places, not AI systems or uses |
| h | p. 98-99, para. 319-323 | Law enforcement definitions | no | explains a term |
| h | p. 99, para. 324 | Transport firms, sports federations and banks acting for police | no | illustrates one element (law enforcement purpose) |
| h | p. 99, para. 324 | Bank acting on its own behalf | h-08 |  |
| h | p. 99, para. 326 | Use without national law | no | general statement, no system described |
| h | p. 100, para. 328 | Live identification of a shoplifter | h-09 |  |
| h | p. 101, para. 332 | Search for a kidnapped child | h-10 |  |
| h | p. 101, para. 336 | Administrative search for a missing person | h-11 |  |
| h | p. 102, para. 339 | Threat to critical infrastructure | no | explains a term |
| h | p. 103, para. 342 | Former student planning an attack | no | illustrates one element (specific threat); no use described |
| h | p. 104, para. 347 | Knife attacker in a park | h-12 |  |
| h | p. 105-106, para. 354 | Broad live facial recognition at a festival | h-13 |  |
| h | p. 106, para. 354 | Targeted search for one wanted person at a festival | h-14 |  |
| h | p. 106, para. 354 | Christmas market attacker fleeing | h-15 |  |
| h | p. 106, para. 355 | Links between the exceptions | no | general statement |

### Regulation (EU) 2026/1744, recitals 10 to 14

| Point | Location | Passage | Case | Reason if not a case |
|---|---|---|---|---|
| ba/bb | recital 10-11 | Background: nudification applications, harm of such material | no | outside the rule (recitals 12 to 14 only); no conclusion on a system |
| ba/bb | recital 12 | General image generator; developing technical capability is not prevented | ba-01, bb-01 |  |
| ba/bb | recital 12 | System intended to generate such material | ba-02, bb-02 |  |
| ba/bb | recital 12 | Foreseeable, reproducible output without adequate safeguards | ba-03, bb-03 |  |
| ba/bb | recital 12 | List of safeguards and what makes them adequate; platforms reporting misuse; corrective measures for open-source releases | no | explains what adequate safeguards are, no system with a conclusion |
| ba/bb | recital 12 | Deployer using a system lacking safeguards for such material | ba-04, bb-04 |  |
| ba/bb | recital 12 | Deployer circumventing safeguards or using a lawful system for such material | ba-05, bb-05 |  |
| ba/bb | recital 12 | Deployer using a system lacking safeguards for lawful material | ba-06, bb-06 |  |
| ba/bb | recital 12 | Accidental generation | ba-07, bb-07 |  |
| ba | recital 12 | Systems intended for intimate material must collect and demonstrate consent | no | states a requirement, not a conclusion on a described system |
| ba | recital 12 | Limited to realistic depictions of intimate parts or sexual activity; meaning of realism | no | explains a term; the excluded cartoonish case is ba-08 |
| ba | recital 12 | Cartoonish or physically impossible depictions | ba-08 |  |
| ba | recital 12 | Nude material of non-identifiable persons | ba-09 |  |
| ba | recital 12 | Realistic partial nudity | ba-10 |  |
| ba | recital 12 | Non-realistic artistic nudes | ba-11 |  |
| ba | recital 12 | Try-on applications | ba-12 |  |
| ba | recital 12 | Medical applications (anatomical simulations, mammograms) | ba-13 |  |
| ba | recital 12 | Emergency diagnosis without consent | ba-14 |  |
| ba | recital 12 | Enhancing an existing image (background, heading, contrast) | ba-15 |  |
| ba | recital 12 | Manipulation that increases exposure | ba-16 |  |
| bb | recital 13 | Authorities generating material in criminal proceedings | bb-08 |  |
| bb | recital 13 | Red-teaming and evaluation for compliance | bb-09 |  |
| ba/bb | recital 14 | Limits restated: realistic depictions, identifiable persons, more nudity, consent excluded, reasonable and adequate measures | no | restates recital 12; duplicates of ba-08 to ba-16 and ba-01/bb-01 |
| ba/bb | recital 14 | Alignment with Charter and other directives | no | no system described |

## Post-run notes

Written after the first run on litmus-screener 1.1.2 (2026-11-02). No expected label, case file or declaration was changed after seeing a verdict. These notes record declaration choices that a reader should weigh when reading the scorecard. None is a correction.

1. **Point (a) has no field for its core facts.** The template has no field for subliminal, manipulative or deceptive techniques, or for significant harm. For a-01, a-06 and a-08 these facts could only go into the free-text `other` fields and `system_description`. All three came back clear. The misses may reflect the template as much as the ruleset.
2. **Point (b) has no category for older people.** The allowed population categories (found from the schema error message, not the template) are `general_public`, `minors`, `other`, `persons_in_vulnerable_economic_situations`, `persons_with_disabilities`, `students` and `workers`. b-03 and b-04 (older people) used `other` with a note. Both came back clear.
3. **`workplace: true` where only customers or patients are analysed.** In f-08, f-13, f-33 and f-35 the system runs in a workplace but the people analysed are customers, patients or a crowd. I set `workplace: true` because the template asks where the system is deployed, and said so in a comment. These came back red. A user who reads the field as "applied to workers" would set it false.
4. **`scraped_internet_data: true` for targeted collection.** In e-01 and e-04 the collection is targeted. The template has no field for targeted versus untargeted collection, so I set the field true and said so in a comment or in `inputs.other`. Both came back red.
5. **Provider that does not use the system (h-01).** The template has no field for the actor's role beyond the `provider` and `deployer` strings. I filled `deployment_context` with the intended use by customers. It came back red; point (h) covers use only.
6. **Exceptions and human assessment.** Many expected-clear cases rest on a fact the template cannot hold as a field: human assessment based on objective facts (d-10 to d-15), a targeted search or national authorisation (h-10, h-14, h-15), medical or safety reasons (f-25, f-28), personal training only (f-07, f-19), a 'without right' defence (bb-08, bb-09), or accidental generation (ba-07, bb-07). These went into `mitigations` or `other` as free text.
7. **Recital 12.** As stated under "The rule", the (ba) and (bb) cases from recital 12 go beyond the brief's wording (recitals 13 and 14). They are ba-01 to ba-16 and bb-01 to bb-07; only bb-08 and bb-09 come from recital 13.
