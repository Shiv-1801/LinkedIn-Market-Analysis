---
title: MIA Job Analyzer
emoji: 📊
colorFrom: yellow
colorTo: orange
sdk: static
pinned: false
short_description: Score any job description against AI-vs-traditional marketing analytics vocabulary
---

# MIA — Marketing Intelligence & AI-Adoption Analyzer

Paste a job description. The tool scores it against vocabulary learned from 4,949 LinkedIn postings
(TF-IDF group-difference analysis, NMF topic clusters, and a 10-skill AI-exclusive vocabulary) to
estimate whether the role sits in the AI-adjacent or traditional segment of the marketing-analytics market.

**Score 70+** — AI-adjacent posting (analytical toolchain, LLM/automation language)  
**Score 45–69** — Mixed signal  
**Score below 45** — Traditional posting (brand, campaign, retail-marketing language)

No ML inference. All scoring is string-matching against pre-computed group differences from the MIA dataset.

Source: [Shiv-1801/LinkedIn-Market-Analysis](https://github.com/Shiv-1801/LinkedIn-Market-Analysis)
