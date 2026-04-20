# Persuasion or Manipulation?

### The PMDF Diagnostic Tool

An interactive implementation of the **Persuasion–Manipulation Diagnostic Framework (PMDF)** — a six-dimension instrument for assessing whether a political marketing practice is ethical persuasion, borderline, or manipulation.

> **Live tool** → [https://YOUR-APP.streamlit.app](https://YOUR-APP.streamlit.app)
>
> *Replace this link with your actual Streamlit Community Cloud URL after deployment.*

---

## Why this tool exists

The regulatory response to the Cambridge Analytica scandal focused on one side of the problem: personal data. GDPR, platform-level audit requirements, and post-hoc investigations all target the *collection* of personal information used to target voters. But the most effective manipulation of the AI era often doesn't need personal data at all.

A deepfake of a candidate, a cloned voice used in a robocall, an LLM producing emotionally targeted messaging at scale — these operate on a different layer, and the instruments built in response to 2016 don't reach them.

The PMDF applies the same six-dimension assessment to any practice regardless of its technology, and maps each dimension against the regulatory instruments that currently cover it — making visible where today's frameworks still fall short.

## The six dimensions

| # | Dimension | Core question |
|---|-----------|---------------|
| 1 | Informed Consent | Did the person consent to being targeted and to the use of their data? |
| 2 | Transparency of Intent | Is the persuasive purpose disclosed? |
| 3 | Respect for Autonomy | Does the practice engage or bypass critical thinking? |
| 4 | Content Authenticity | Is the content genuine or synthetically produced? |
| 5 | Targeting Proportionality | Is the targeting granularity proportionate to the goal? |
| 6 | Accountability & Oversight | Can the source be traced and recourse obtained? |

Each dimension is scored 0–3 from its sub-questions (0 = manipulation, 3 = ethical persuasion). The six dimension averages sum to a total between 0 and 18:

- **0–6** Manipulation
- **7–12** Borderline
- **13–18** Ethical persuasion

## Documented cases included

| Case | Year | Paradigm |
|------|------|----------|
| Cambridge Analytica / Brexit | 2016 | Data-centric |
| Slovak election deepfake | 2023 | Content-centric |
| Biden voice-clone robocall | 2024 | Content-centric |

The tool also lets you build a custom scenario and run it through the framework.

## Regulatory coverage

Every dimension is mapped against the four instruments currently in force:

- **GDPR** — General Data Protection Regulation (EU, 2016)
- **AI Act** — EU Artificial Intelligence Act (2024)
- **DSA** — Digital Services Act (EU, 2022)
- **AMA Code** — American Marketing Association Code of Ethics (2022)

The matrix explicitly highlights **D3 Respect for Autonomy** — a dimension where no current instrument provides meaningful coverage.

## Run locally

Requires Python 3.11 or later.

```bash
git clone https://github.com/YOUR-USERNAME/pmdf-diagnostic-tool.git
cd pmdf-diagnostic-tool
pip install -r requirements.txt
python3 -m streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Stack

Python 3.11 · Streamlit · Plotly · pandas. Session-based (no database, no authentication). The design system uses a cherry–navy–cream palette; all UI copy is written in product voice.

## Project structure

```
pmdf-diagnostic-tool/
├── app.py                      # Main Streamlit entry point
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml             # Theme configuration
├── data/
│   ├── dimensions.py           # Six PMDF dimensions + questions + explanations
│   ├── scenarios.py            # Pre-loaded case answer keys
│   └── regulations.py          # Regulatory coverage matrix
└── components/
    ├── scoring.py              # Dimension averaging, verdict logic
    ├── radar_chart.py          # Plotly radar chart builder
    └── output.py               # Assessment output rendering
```

## Academic context

The PMDF was developed as the original contribution of:

> Reiter Hernández, M. (2026). *Persuasion or Manipulation? A Diagnostic Framework for Ethical Assessment Across Data-Driven and AI-Enabled Political Marketing.* Bachelor in Business Administration, IE University, Madrid.

The framework synthesises three bodies of literature: marketing ethics (Hunt & Vitell, 1986; Susser et al., 2019; Laczniak & Murphy, 2006); the Cambridge Analytica documentary record (DCMS Committee, 2019; ICO, 2020; Wylie, 2019; Kosinski et al., 2013); and emerging AI-manipulation research (Chesney & Citron, 2019; Goldstein et al., 2023; Freedom House, 2024).

Every threshold, citation, and explanation in this tool traces back to the thesis reference list. The tool is a demonstration layer over the framework — it introduces no theoretical content of its own.

## License and use

Made available for educational and research use.

---

**Author** · María Reiter Hernández
**Institution** · IE University, Madrid
**Year** · 2026
