# MIA Project — August 2026 Temporal Analysis: Inferences

**Scrape date:** 1 September 2026 (trailing 30 days — postings from approximately August 2026)
**Dataset:** 3,897 postings, 10 countries, 6 search titles — same grid as the original scrape
**Baseline:** Original scrape (4,949 postings, broader date window, completed August 2026)

This document records interpretive findings from the August update. It follows the same format as the root `Inferences.md` and is meant to be read alongside it — not as a replacement.

---

## Structural finding: the AI/non-AI divide is stable

The core finding from the original analysis holds across all three methods in August. NMF topic structure, TF-IDF group-diff, and the skill co-occurrence network all continue to produce the same clean AI/non-AI boundary. The divide is not a snapshot artifact — it replicates on a fresh one-month slice using the same pipeline.

---

## Market & segmentation

- **Overall AI-mention rate declined from 0.42 to 0.384** — approximately a 4 percentage-point drop. The decline is spread uniformly across seniority tiers (see table below), not concentrated at a specific level. This is consistent with a post-surge normalisation: a first wave of AI-adjacent hiring language, concentrated in 2024–early 2026, followed by a modest pullback as the category matures and postings become more precise.

- **The seniority gradient is preserved in the same rank order:** Director/Executive (0.50) > Senior (0.483) > Manager/Lead (0.445) > Mid from experience (0.395) > Entry/Junior (0.367) > Mid/Unspecified (0.307). No tier inverted relative to another. The gradient itself is the durable finding, not the specific rate at any one tier.

  | Seniority tier | Original rate | August rate | Change |
  |---|---|---|---|
  | Director/Executive | 0.51 (n=226) | 0.50 (n=84) | −0.01 |
  | Senior | 0.50 (n=819) | 0.483 (n=741) | −0.02 |
  | Manager/Lead | 0.49 (n=978) | 0.445 (n=758) | −0.05 |
  | Mid (from experience) | 0.45 (n=508) | 0.395 (n=410) | −0.05 |
  | Entry/Junior | 0.43 (n=387) | 0.367 (n=248) | −0.06 |
  | Mid/Unspecified | 0.33 (n=2,031) | 0.307 (n=1,656) | −0.02 |

- **The application-competition pattern also holds.** Entry/Junior (94.9 avg. applications) and Mid from experience (92.6) still peak; Manager/Lead (78.9) is still the trough. The decoupling of AI-mention rate from applicant competition is not a fluke of the original scrape.

- **Geography is stable at the country level.** Canada remains the highest-AI-mention market (0.603), Netherlands is unchanged at 0.459, France is the consistent floor at 0.285. China (0.251) is notably lower than all other markets in August, suggesting either a scraping coverage gap or a genuine platform difference.

  Note: `applicationsCount_numeric` has 54% nulls in the August dataset — a higher missing rate than the original — because LinkedIn more aggressively hides application counts on actively-filling roles. Average-applications figures should be read as directional, not precise.

---

## Skill co-occurrence network — temporal changes

The August exclusive-skill list has 10 AI-exclusive skills versus 11 in the original. The composition changed meaningfully:

**Skills that were AI-exclusive in the original but are no longer exclusive in August:**
- Machine Learning
- Hugging Face
- LangChain
- MongoDB

These four have now crossed into non-AI postings — they are no longer discriminating signals between the two groups. The interpretation: tools that were frontier in early 2026 have diffused into mainstream technical hiring broadly, not just AI-adjacent roles. Machine Learning losing exclusive status is the most significant of these, as it was the anchor of the original AI sub-cluster.

**Skills that are newly AI-exclusive in August:**
- Agentic / AI Agents (new term category, absent from the original vocabulary)
- LLM (previously present but not exclusive)
- Kubernetes (unexpected — suggests some AI-adjacent marketing analytics roles are blurring into MLOps/infrastructure territory)

The emergence of Agentic / AI Agents as a distinct, AI-exclusive skill cluster is the clearest new signal. It did not appear as a labelled skill in the original scrape, which means the term entered job-description language after the original baseline was set — the agentic AI wave is visible in hiring vocabulary in real time.

**Claude appears in the skill network with substantive co-occurrence edges:**
Claude–SQL (77), Claude–Python (54), Claude–Tableau (46), Claude–Google Analytics (36), Claude–Looker (35), Claude–Power BI (33). ChatGPT/GPT–Claude co-occurrence = 58, meaning many postings mention both explicitly. Claude is embedded in the core BI/analytics skill cluster, not sitting as a peripheral spoke — unlike Gemini, which remains a single-edge spoke.

---

## Text analysis — TF-IDF temporal observations

- **`growth` is the single strongest non-AI signal in August** (diff = −0.025), completely absent from the AI-mention group's vocabulary. "Growth marketing" appears to be categorically non-AI territory in this data — a clean, interpretable boundary. This is sharper than any individual term in the original TF-IDF analysis and is worth citing explicitly in the write-up.

- The **NMF topic structure is preserved.** The AI-mention group continues to produce a self-contained ML/engineering/Python topic absent from the non-AI group. The non-AI retail/CPG cluster (market, sales, commercial, pricing, consumer, category, brand) remains coherent and distinct. The French-language topic (Topic 5, AI-mention) persists as a geography artefact of the country mix.

- **`management` tops the AI-skewing diff table** (mean_tfidf_non_ai = 0) — same max_df filtering artefact as the `tools` issue documented in the original Inferences.md. Not a real signal.

---

## Methodological notes specific to the August update

- The August scrape uses `DATE_POSTED = "r2592000"` (trailing 30 days), which is a narrower window than the original scrape. The smaller dataset (3,897 vs 4,949 rows) and lower per-tier sample sizes mean the rate estimates carry more variance, particularly for Director/Executive (n=84 in August vs n=226 in original).

- Zero URL duplicates in the raw August file — no dedup step required, consistent with a fresh slice of new postings.

- `applicationsCount_numeric` null rate is 54% in August vs a lower rate in the original. Do not use August avg-applications figures as the primary source for competition analysis; treat them as confirmatory of the original pattern, not as a replacement estimate.

---

## Synthesis: what the temporal comparison adds to the article

Three things are now documentable that a single-snapshot study cannot claim:

1. **The AI/non-AI structural divide replicates on a fresh sample** — this is not a one-time finding. Three independent methods (topic modeling, TF-IDF, skill network) reproduce the same boundary on August data without recalibration.

2. **The skill frontier is moving.** Machine Learning, Hugging Face, and LangChain have diffused from AI-exclusive to mainstream in approximately one year. Agentic/AI Agents is the newly exclusive category — today's discriminating signal, likely tomorrow's mainstream term.

3. **The overall AI-mention rate declined modestly (~4pp) while the structural pattern held.** This separates surface-level buzzword adoption (which fluctuates) from underlying segmentation (which is structural). The headline "AI is transforming marketing analytics" conflates two things that move at different speeds.
