# MIA Project — Notebooks

## Pipeline

```
01_linkedin_scraper.ipynb              -> data/mia_postings_raw.csv
                                            |
                                            v
02b_enrich_ai_flag_language_geo.ipynb  -> data/mia_postings_final.csv
   (adds mentions_ai, is_english, country,
   applicationsCount_numeric/tag, postedDaysAgo)
                                            |
                                            v
02_final_cleaning.ipynb                -> data/mia_postings_final2.csv
   (adds workType_category, seniority)
                                            |
                                            v
03b_ingestion_fixes.ipynb              -> data/mia_postings_final2_fixed2.csv
   (stray-quote fix in description,
   whitespace normalization in title)
                                            |
              +-----------------------------+-----------------------------+
              |                                                           |
              v                                                           v
03_skill_extraction.ipynb                                  05_tfidf_nmf_topics.ipynb
   -> data/mia_skills_long.csv                                 -> topic terms, TF-IDF
              |                                                    group-diff scores
              v
06_skill_cooccurrence_network.ipynb
   -> skill network PNG + edge lists
```

All notebooks expect a `data/` subfolder for CSV input/output — not included
in this repo (raw scraped job postings aren't republished; the small
aggregate outputs like edge lists and term scores are fine to include and
may be added later).

Numbering has a gap where `02b` and `03b` insert between `01`/`02` and
`02`/`03` — that reflects the order these steps run in, not the order they
were reconstructed in. Renumbering everything sequentially would mean
renaming files that are already public; not worth the churn.

## Reconstructed steps — verification status

`02b_enrich_ai_flag_language_geo.ipynb` and `03b_ingestion_fixes.ipynb` were
reverse-engineered by diffing the uploaded CSV snapshots against each other
(the original notebooks for these steps weren't saved). Each transformation
was checked against the real data before being written:

- `country` = copy of `search_location_used` — **100% verified**
- `applicationsCount_numeric` / `applicationsCount_tag` parsing — **100% verified** (2,291 exact / 1,159 over_200 / 1,499 first_25, matches source exactly)
- Stray-quote fix in `description` — **100% verified** (reproduces all 405 changed rows exactly)
- Whitespace normalization in `title` — **100% verified** (reproduces all 24 changed rows exactly, including embedded newlines and non-standard Unicode spaces)
- `mentions_ai` keyword regex — **~99.1% agreement**, not exact. The original regex isn't recoverable; this is a close reconstruction, flagged in the notebook itself.
- `postedDaysAgo` relative-date parsing — **~96.7% agreement** on the sample checked, also flagged in the notebook.

The "18-row column shift" and "5 phantom TAM rows" bugs mentioned in
`Inferences.md` don't show up as a row-count difference in any of the
uploaded CSV snapshots (all consistently 4,949 rows, 0 duplicate URLs) — the
TAM figure was likely a Power BI card metric computed before these CSVs were
saved, not something reconstructable from row diffs alone. Noted here rather
than silently dropped.

## Known data caveats

- `05_tfidf_nmf_topics.ipynb`: the two TF-IDF vectorizers are fit
  independently per group, so the group-diff comparison treats a term
  missing from one group's vocabulary as 0 — an approximation, not a
  perfectly controlled comparison. See `Inferences.md` for the specific
  `tools` = 0.0 artifact this causes.

## Excluded

- `Data Cleaning.ipynb` — an earlier exploratory notebook that duplicates
  `05_tfidf_nmf_topics.ipynb`'s TF-IDF/NMF logic on an intermediate snapshot
  of the data (post-`mentions_ai`, pre-`is_english`/`country`). Superseded
  by the properly-staged version in this pipeline; left out to avoid
  reviewer confusion.
- `Hubspot Data.ipynb` — dropped entirely at Shiv's request. It listed all
  43 of his real tracked job applications (company names, titles) with a
  `seniority` column that also turned out to be an unfilled placeholder
  (defaulted every row to `"Entry/Junior (inferred)"`). The aggregate
  20/43-company-overlap finding stays in `Inferences.md` as a reported
  statistic; the underlying per-application notebook isn't published.
