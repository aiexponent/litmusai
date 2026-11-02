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
