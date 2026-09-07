import gradio as gr
import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

tfidf_diff = pd.read_csv(DATA_DIR / "mia_tfidf_group_diff.csv")
exclusive = pd.read_csv(DATA_DIR / "mia_skill_group_exclusive.csv")
topics = pd.read_csv(DATA_DIR / "mia_tfidf_nmf_topic_terms.csv")

# Build lookup structures once
ai_signal_terms = set(tfidf_diff[tfidf_diff["diff"] > 0]["term"].str.lower())
non_ai_terms = set(tfidf_diff[tfidf_diff["diff"] < 0]["term"].str.lower())
ai_exclusive_skills = set(exclusive["skill"].str.lower())

ai_topics = topics[topics["group"] == "AI-mention"][["topic", "top_terms"]].reset_index(drop=True)
non_ai_topics = topics[topics["group"] != "AI-mention"][["topic", "top_terms"]].reset_index(drop=True)


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z][a-z0-9 ]{1,30}[a-z0-9]|[a-z]+", text)
    return tokens


def score_jd(jd_text: str) -> tuple:
    if not jd_text or not jd_text.strip():
        return "Paste a job description above to get started.", "", "", ""

    tokens = tokenize(jd_text)
    token_set = set(tokens)

    ai_hits = token_set & ai_signal_terms
    non_ai_hits = token_set & non_ai_terms
    exclusive_hits = token_set & ai_exclusive_skills

    total = len(ai_hits) + len(non_ai_hits)
    raw_score = (len(ai_hits) / total * 100) if total > 0 else 50
    # Boost for exclusive AI skills (each adds up to 5 points, capped)
    exclusive_boost = min(len(exclusive_hits) * 5, 20)
    score = min(round(raw_score + exclusive_boost), 100)

    if score >= 70:
        verdict = "AI-adjacent — this posting reads like the AI-mention segment."
    elif score >= 45:
        verdict = "Mixed — elements of both AI-native and traditional marketing analytics."
    else:
        verdict = "Traditional — this posting reads like the non-AI-mention segment."

    signal_terms_out = ", ".join(sorted(ai_hits)[:20]) if ai_hits else "none detected"

    exclusive_out = ", ".join(sorted(exclusive_hits)) if exclusive_hits else "none detected"

    # Find closest AI topic by word overlap
    best_topic, best_overlap = None, -1
    for _, row in ai_topics.iterrows():
        topic_words = set(row["top_terms"].lower().replace('"', '').split(", "))
        overlap = len(token_set & topic_words)
        if overlap > best_overlap:
            best_overlap = overlap
            best_topic = row["top_terms"]

    topic_out = best_topic if best_topic and best_overlap > 0 else "no strong match"

    summary = f"**AI Signal Score: {score}/100** — {verdict}"
    details = f"**AI-signal terms found ({len(ai_hits)}):** {signal_terms_out}"
    skills_out = f"**AI-exclusive skills detected:** {exclusive_out}"
    topic_line = f"**Closest AI topic cluster:** {topic_out}"

    return summary, details, skills_out, topic_line


with gr.Blocks(title="MIA — Job Description Analyzer") as demo:
    gr.Markdown(
        """
# MIA — Marketing Intelligence & AI-Adoption Analyzer

Paste a job description. The tool scores it against vocabulary extracted from 4,949 LinkedIn postings
(TF-IDF group-difference analysis, NMF topic modeling, and a 42-skill co-occurrence network) to estimate
whether the role sits in the AI-adjacent or traditional segment of the marketing-analytics market.

**How the score works:** terms that appear more in AI-mention postings add to the score; terms that skew
toward non-AI postings subtract. Presence of AI-exclusive skills (LLMs, RAG, Prompt Engineering, etc.)
adds a further boost. 70+ = AI-adjacent, 45–69 = mixed, below 45 = traditional.

*Based on [MIA Project](https://github.com/Shiv-1801/LinkedIn-Market-Analysis) — analysis of 4,949 postings across 10 countries.*
        """
    )

    with gr.Row():
        jd_input = gr.Textbox(
            label="Job Description",
            placeholder="Paste the full job description here…",
            lines=12,
        )

    analyze_btn = gr.Button("Analyze", variant="primary")

    score_out = gr.Markdown(label="Score")
    signal_out = gr.Markdown(label="Signal terms")
    skills_out = gr.Markdown(label="AI-exclusive skills")
    topic_out = gr.Markdown(label="Closest topic cluster")

    analyze_btn.click(
        fn=score_jd,
        inputs=[jd_input],
        outputs=[score_out, signal_out, skills_out, topic_out],
    )

    gr.Examples(
        examples=[
            [
                "We are looking for a Data Scientist with experience in Python, LLM fine-tuning, RAG pipelines, "
                "and Prompt Engineering. You will build AI-native analytics workflows using Databricks and Snowflake "
                "to drive product decisions. Experience with LangChain, Generative AI, and Hugging Face preferred."
            ],
            [
                "We need a Marketing Analyst to track campaign performance across Google Ads, Meta Ads, "
                "and Marketo. You will own weekly reporting in Power BI, manage CRM data in Salesforce, "
                "and present insights to brand and retail stakeholders."
            ],
        ],
        inputs=[jd_input],
        label="Try an example",
    )

demo.launch()
