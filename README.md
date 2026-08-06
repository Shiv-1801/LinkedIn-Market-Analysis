# MIA — Marketing Intelligence & AI-Adoption Analysis

Analysis of 4,949 marketing/analytics job postings scraped from LinkedIn across 10 countries, examining how AI-adoption is reshaping the marketing analyst role: which tools and skills define the AI-adjacent segment of the market, how that segment differs from traditional BI/marketing roles, and where it's concentrated by seniority tier and geography.

Three independent text-analysis methods — topic modeling, TF-IDF term comparison, and skill co-occurrence network analysis — converge on the same underlying divide between AI-native and traditional marketing-analytics postings.
## Key findings

- LinkedIn matches postings by search intent, not literal title — only ~5% of postings literally contain the searched phrase.
- AI-mention rate varies substantially by country (26% France to 58% Canada), and by seniority tier: Entry/Junior is the most AI-mention-saturated segment globally, while in India specifically AI-adoption hiring skews toward Mid/Manager-Lead roles instead.
- Power BI shows up in only 43% of AI-adjacent postings — well behind Python (60%), Databricks (67%), and Snowflake (63%) — reading as legacy BI tooling rather than part of the AI stack.
- Topic modeling, TF-IDF term-frequency comparison, and skill co-occurrence network structure all independently identify the same boundary: AI-mention postings pull toward a distinct technical/analytical vocabulary (analysis, engineering, automation), while non-AI postings cluster around traditional retail/brand-marketing language.

## Pipeline

```
01_linkedin_scraper.ipynb
    Scrapes postings via the Apify LinkedIn Jobs Scraper actor
    -> data/mia_postings_raw.csv

02b_enrich_ai_flag_language_geo.ipynb
    Adds mentions_ai, is_english, country, applicationsCount fields, posting recency
    -> data/mia_postings_final.csv

02_final_cleaning.ipynb
    Collapses workType into broad categories, extracts seniority tier from title
    -> data/mia_postings_final2.csv

03b_ingestion_fixes.ipynb
    Fixes two ingestion artifacts from the raw scrape (stray quotes, whitespace)
    -> data/mia_postings_final2_fixed2.csv

03_skill_extraction.ipynb                    05_tfidf_nmf_topics.ipynb
    Regex-extracts a 42-skill vocabulary          NMF topic modeling + TF-IDF
    -> data/mia_skills_long.csv                   term comparison, AI vs non-AI

06_skill_cooccurrence_network.ipynb
    Builds and compares skill co-occurrence networks by AI-mention group
    -> network visualization + edge lists
```

## Requirements

```
pandas
numpy
scikit-learn
langdetect
networkx
matplotlib
apify-client   # only needed for 01_linkedin_scraper.ipynb
```

Each notebook expects a local `data/` folder for CSV input/output. Raw
scraped postings aren't included in this repo; running the pipeline from
scratch requires an [Apify](https://apify.com) account and API token, set as
the `APIFY_API_TOKEN` environment variable (see `01_linkedin_scraper.ipynb`).

## Notes on reconstructed steps

`02b_enrich_ai_flag_language_geo.ipynb` and `03b_ingestion_fixes.ipynb` were
reconstructed after the fact by diffing intermediate data snapshots, since
the original notebooks for those two steps weren't preserved. Every
transformation in them was verified against the actual data before being
included; two (the `mentions_ai` keyword regex and the `postedDaysAgo`
date parser) are close reconstructions rather than exact matches, and are
flagged as such inline. Full verification detail is in each notebook's
markdown cells.

## Limitations

The two TF-IDF vectorizers in `05_tfidf_nmf_topics.ipynb` are fit
independently per group (AI-mention vs. non-AI-mention), so the group-diff
comparison treats a term missing from one group's vocabulary as a score of
0 — a reasonable approximation, not a perfectly controlled comparison. See
`Inferences.md` for the specific artifact this causes on the term `tools`.

An inferential/statistical layer (e.g. logistic regression of AI-mention on
country, seniority, and work type) is planned but not yet implemented.
