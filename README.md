# PMDF Diagnostic Tool

Interactive companion app to the BBA Final Thesis:

> **"Persuasion or Manipulation? A Diagnostic Framework for Ethical Assessment Across Data-Driven and AI-Enabled Political Marketing"**
> María Reiter Hernández — IE University — April 2026

This app operationalises the thesis's original contribution, the **Persuasion–Manipulation
Diagnostic Framework (PMDF)**, as a live diagnostic tool. It evaluates a political marketing
practice across six ethical dimensions and classifies it as *ethical persuasion*, *borderline*,
or *manipulation*. The tool is designed as an interactive visual aid for the thesis oral defense
and as a demonstration layer for the broader PMDF framework.

## What the app does

- Presents three pre-loaded cases from the thesis — **Cambridge Analytica / Brexit (2016)**,
  the **Slovak election deepfake (2023)**, and the **Biden robocall (2024)** — or lets the user
  build a custom scenario.
- Walks the user through the six PMDF dimensions: Informed Consent, Transparency of Intent,
  Respect for Autonomy, Content Authenticity, Targeting Proportionality, and Accountability &
  Oversight.
- Updates a radar chart live as the user answers, making the violation-clustering pattern at
  the heart of Hypothesis 2 visually immediate.
- Produces a final assessment with the verdict, color-coded dimension summary, literature-backed
  explanations, and a regulatory coverage table that operationalises Hypothesis 1 (the gap).

## Run locally

Requires Python 3.11+.

```bash
# 1. Clone or unzip the project
cd pmdf_app

# 2. (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate          # on macOS/Linux
# .venv\Scripts\activate            # on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this folder to a public GitHub repository (for example, `pmdf_app`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, choose your repo, set the main file to `app.py`, and deploy.
4. Streamlit will install from `requirements.txt` and apply the theme in `.streamlit/config.toml`
   automatically.

Community Cloud gives you a persistent public URL you can put on the first slide of the oral
defense.

## Project structure

```
pmdf_app/
├── app.py                         # Main Streamlit entry point & screen router
├── requirements.txt               # Python dependencies
├── README.md
├── .streamlit/
│   └── config.toml                # Theme (navy primary, light background)
├── data/
│   ├── __init__.py
│   ├── dimensions.py              # Six PMDF dimensions + questions + explanations
│   ├── scenarios.py               # Pre-loaded answer keys (Cambridge, Slovak, Biden)
│   └── regulations.py             # Regulatory coverage matrix (Section 7)
└── components/
    ├── __init__.py
    ├── scoring.py                 # Dimension averaging, verdicts, level colours
    ├── radar_chart.py             # Plotly radar chart builder
    └── output.py                  # Screen 3: verdict, summary, coverage table
```

## Scoring

- Each answer maps to a score from **0 (manipulation)** to **3 (ethical persuasion)**.
- **Dimension score** = average of its sub-question scores (range 0–3).
- **Total score** = sum of the six dimension averages (range 0–18).
- **Verdict:** `0–6` Manipulation · `7–12` Borderline · `13–18` Ethical Persuasion.
- Dimension-level colour: `0–1` red · `1–2` yellow · `>2` green.

## Academic integrity note

Every question, score threshold, dimension, explanation, and regulatory verdict traces
directly to the thesis and its reference list. The app is a demonstration layer — not an
independent intellectual contribution. Nothing in the app introduces concepts, scoring logic,
or claims that are not grounded in the thesis itself.

## Citations used in the app

Chesney & Citron (2019) · Cialdini (2001) · DCMS Committee (2019) · European Parliament (2024,
*EU AI Act*) · Freedom House (2024) · Goldstein et al. (2023) · Hunt & Vitell (1986) · ICO
(2020) · Kosinski et al. (2013) · Laczniak & Murphy (2006) · Mathur et al. (2019) · Regulation
(EU) 2016/679 (GDPR) · Susser et al. (2019) · Zuiderveen Borgesius et al. (2018) · AMA Code of
Ethics (2022) · Digital Services Act (2022)

Full references are in the thesis bibliography.
