"""
Screen 3 — the assessment output.

Huge serif verdict statement, radar chart, compact six-dimension grid with
two-segment violation bars, regulatory coverage matrix as a heatmap table.
Language is product-voice throughout — no references to the research context
beyond the literature citations that appear next to each dimension.
"""

import textwrap

import streamlit as st

from data.dimensions import DIMENSIONS
from data.regulations import REGULATORY_COVERAGE
from components.scoring import (
    calculate_all_dimension_scores,
    calculate_total_score,
    get_verdict,
    get_verdict_color,
    get_dimension_level,
    get_answer_score,
    segment_color,
)
from components.radar_chart import build_radar_chart


def _html(template: str) -> str:
    """
    Clean a multi-line HTML template for st.markdown.

    Streamlit's markdown parser (CommonMark) treats lines indented by 4+ spaces
    as a code block. If we pass template strings with Python-source indentation,
    the HTML renders as raw text. This helper removes common leading whitespace
    and trims surrounding newlines so every multi-line HTML template is safe.
    """
    return textwrap.dedent(template).strip()


# ---------------------------------------------------------------------------
# Hero verdict
# ---------------------------------------------------------------------------
def _hero_headline(verdict: str) -> str:
    """Big serif statement — ends with a full stop, reads like a pronouncement."""
    return {
        "Manipulation": "Manipulation.",
        "Borderline": "Borderline.",
        "Ethical Persuasion": "Ethical persuasion.",
    }[verdict]


def _hero_subline(verdict: str, violated_count: int) -> str:
    if verdict == "Manipulation":
        return f"{violated_count} of 6 dimensions compromised"
    if verdict == "Borderline":
        return "Mixed signals — {} dimension{} flagged".format(
            violated_count, "s" if violated_count != 1 else ""
        )
    return "All six dimensions within ethical range"


def render_verdict_header(verdict: str, total_score: float, scenario_name: str, dim_scores: dict):
    color = get_verdict_color(verdict)
    headline = _hero_headline(verdict)
    violated = sum(1 for s in dim_scores.values() if s is not None and s <= 1)
    subline = _hero_subline(verdict, violated)

    st.markdown(
        _html(f"""
        <div style="color: #4A5568; font-size: 11px; letter-spacing: 0.14em;
             font-weight: 500; text-transform: uppercase; margin-bottom: 6px;">
            Assessment · {scenario_name}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;
             padding-bottom: 18px; border-bottom: 1px solid #E8D5D5; margin-bottom: 28px;
             gap: 24px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 280px;">
                <div style="font-family: Georgia, 'Times New Roman', serif; color: {color};
                     font-size: 54px; font-weight: 400; line-height: 1;
                     letter-spacing: -0.02em;">{headline}</div>
                <div style="color: #4A5568; font-size: 13px; margin-top: 10px;">{subline}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-family: Georgia, serif; color: #2F3C7E; font-size: 42px;
                     line-height: 1; font-weight: 400;">
                    {total_score:.1f}<span style="color: #4A5568; font-size: 22px;"> / 18</span>
                </div>
                <div style="color: #4A5568; font-size: 10.5px; letter-spacing: 0.1em;
                     text-transform: uppercase; margin-top: 4px;">Total score</div>
                <div style="color: #4A5568; font-size: 10.5px; margin-top: 6px;
                     font-style: italic;">
                    0–6 Manipulation · 7–12 Borderline · 13–18 Ethical
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Pattern diagnosis (next to radar chart)
# ---------------------------------------------------------------------------
def _diagnose_pattern(dim_scores: dict) -> tuple[str, str]:
    """Classify which side of the hexagon the violation shape collapses on."""
    data_side = [dim_scores.get(i) for i in (1, 5, 6)]
    content_side = [dim_scores.get(i) for i in (2, 3, 4)]

    def avg(lst):
        vals = [s for s in lst if s is not None]
        return sum(vals) / len(vals) if vals else None

    data_avg = avg(data_side)
    content_avg = avg(content_side)

    if data_avg is None or content_avg is None:
        return ("Pattern forming", "Complete all dimensions to see the full shape.")

    diff = data_avg - content_avg
    if diff < -0.5:
        return (
            "Data-side collapse",
            "Consent, proportionality, and accountability dimensions dominate the violation "
            "pattern. Signature of data-harvesting manipulation.",
        )
    if diff > 0.5:
        return (
            "Content-side collapse",
            "Transparency, autonomy, and authenticity dimensions dominate the violation "
            "pattern. Signature of AI-generated content manipulation.",
        )
    return (
        "Distributed pattern",
        "Violations span both data-side and content-side dimensions without a clear "
        "asymmetry.",
    )


# ---------------------------------------------------------------------------
# Six-dimension grid with violation bars
# ---------------------------------------------------------------------------
def render_dimension_grid(dim_scores: dict, answers: dict):
    """2x3 grid of compact dimension cards with two-segment violation bars."""
    # Helper to build one card's HTML
    def card_html(dim):
        score = dim_scores.get(dim["id"])
        level = get_dimension_level(score)
        level_color = {"red": "#990011", "yellow": "#C8A3A8",
                       "green": "#2F3C7E", "unanswered": "#E8D5D5"}[level]
        score_text = f"{score:.1f}" if score is not None else "—"

        # Two-segment bar, one per sub-question
        bar_segments = ""
        for q in dim["questions"]:
            q_score = get_answer_score(dim["id"], q["id"], answers.get((dim["id"], q["id"])))
            seg_color = segment_color(q_score)
            bar_segments += (
                f'<div style="height: 4px; flex: 1; background: {seg_color};"></div>'
            )

        return _html(f"""
        <div style="background: white; padding: 12px 14px; border-left: 3px solid {level_color};
             min-height: 78px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <div style="color: #2F3C7E; font-size: 12.5px; font-weight: 500;">
                    D{dim['id']} · {dim['name']}
                </div>
                <div style="color: {level_color}; font-size: 12px; font-weight: 500;
                     font-family: Georgia, serif;">{score_text}</div>
            </div>
            <div style="color: #4A5568; font-size: 11px; margin-top: 3px; line-height: 1.35;">
                {dim['core_question'][:72]}{'…' if len(dim['core_question']) > 72 else ''}
            </div>
            <div style="display: flex; gap: 3px; margin-top: 10px;">{bar_segments}</div>
        </div>
        """)

    st.markdown(
        '<div style="color: #2F3C7E; font-size: 12px; font-weight: 500; letter-spacing: 0.08em; '
        'text-transform: uppercase; margin-bottom: 10px;">Six-dimension breakdown</div>',
        unsafe_allow_html=True,
    )

    # Two-column grid, three rows
    col1, col2 = st.columns(2, gap="small")
    for idx, dim in enumerate(DIMENSIONS):
        target = col1 if idx % 2 == 0 else col2
        with target:
            st.markdown(card_html(dim), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Why-it-failed explanations (red and yellow dimensions only)
# ---------------------------------------------------------------------------
def render_explanations(dim_scores: dict, answers: dict):
    red_or_yellow = [
        d for d in DIMENSIONS
        if get_dimension_level(dim_scores.get(d["id"])) in ("red", "yellow")
    ]
    if not red_or_yellow:
        return

    st.markdown(
        '<div style="color: #2F3C7E; font-size: 12px; font-weight: 500; letter-spacing: 0.08em; '
        'text-transform: uppercase; margin-bottom: 4px;">Why these dimensions were flagged</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color: #4A5568; font-size: 12px; margin-bottom: 14px;">'
        'Each citation points to the source behind the threshold used.'
        '</div>',
        unsafe_allow_html=True,
    )

    for dim in red_or_yellow:
        level = get_dimension_level(dim_scores.get(dim["id"]))
        explanation = dim["explanations"][level]
        citations = " · ".join(dim["literature"])
        border_color = "#990011" if level == "red" else "#C8A3A8"

        # Collect the user's actual answers for this dimension
        answer_lines = []
        for q in dim["questions"]:
            selected = answers.get((dim["id"], q["id"]))
            if selected:
                answer_lines.append(
                    f'<div style="color: #4A5568; font-size: 11.5px; line-height: 1.5; '
                    f'margin-top: 4px;">› {selected}</div>'
                )
        answers_html = "".join(answer_lines)

        st.markdown(
            _html(f"""
            <div style="background: white; padding: 14px 16px; border-left: 3px solid {border_color};
                 margin-bottom: 10px;">
                <div style="color: #2F3C7E; font-size: 13px; font-weight: 500;
                     margin-bottom: 6px;">D{dim['id']} · {dim['name']}</div>
                <div style="color: #1A1A1A; font-size: 12.5px; line-height: 1.55;">
                    {explanation}
                </div>
                <div style="color: #4A5568; font-size: 11px; font-style: italic;
                     margin-top: 8px;">{citations}</div>
                <div style="margin-top: 8px; padding-top: 8px; border-top: 0.5px solid #F7EDED;">
                    <div style="color: #4A5568; font-size: 10.5px; letter-spacing: 0.08em;
                         text-transform: uppercase;">Answers</div>
                    {answers_html}
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Regulatory coverage matrix
# ---------------------------------------------------------------------------
def _cell(value: str) -> str:
    if value == "FULL":
        return ('<div style="background: #2F3C7E; color: white; padding: 5px 0; text-align: center;'
                ' font-size: 10px; letter-spacing: 0.06em; font-weight: 500;">FULL</div>')
    if value == "PARTIAL":
        return ('<div style="background: #F7EDED; color: #990011; padding: 5px 0; text-align: center;'
                ' font-size: 10px; letter-spacing: 0.06em; font-weight: 500;">PARTIAL</div>')
    return '<div style="color: #C8A3A8; text-align: center; padding: 5px 0; font-size: 11px;">—</div>'


def _verdict_pill(verdict: str) -> str:
    bg = {"COVERED": "#2F3C7E", "PARTIAL": "#F7EDED", "GAP": "#990011"}[verdict]
    color = {"COVERED": "white", "PARTIAL": "#990011", "GAP": "white"}[verdict]
    return (f'<div style="background: {bg}; color: {color}; padding: 5px 0; text-align: center; '
            f'font-size: 10px; letter-spacing: 0.06em; font-weight: 500;">{verdict}</div>')


def render_regulatory_coverage(dim_scores: dict):
    st.markdown(
        '<div style="color: #2F3C7E; font-size: 12px; font-weight: 500; letter-spacing: 0.08em; '
        'text-transform: uppercase; margin-bottom: 4px;">Regulatory coverage</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color: #4A5568; font-size: 12px; margin-bottom: 12px; max-width: 640px;">'
        'Which current instruments address each dimension. Rows where this scenario scored low '
        'are highlighted.'
        '</div>',
        unsafe_allow_html=True,
    )

    low_scoring = {
        dim_id for dim_id in range(1, 7)
        if get_dimension_level(dim_scores.get(dim_id)) in ("red", "yellow")
    }

    # Build the table as a single contiguous HTML string — no leading whitespace,
    # no blank lines. Streamlit's markdown parser otherwise treats indented multi-line
    # HTML as a code block, which is why the raw tags showed up as text before.
    parts = ['<div style="border: 0.5px solid #E8D5D5;">']

    # Header row
    parts.append(
        '<div style="display: grid; grid-template-columns: 1.8fr 1fr 1fr 1fr 1fr 1fr;'
        ' background: #2F3C7E; color: white; font-size: 10.5px; letter-spacing: 0.06em;'
        ' font-weight: 500; text-transform: uppercase;">'
        '<div style="padding: 9px 12px;">Dimension</div>'
        '<div style="padding: 9px 10px; text-align: center;">GDPR</div>'
        '<div style="padding: 9px 10px; text-align: center;">AI Act</div>'
        '<div style="padding: 9px 10px; text-align: center;">DSA</div>'
        '<div style="padding: 9px 10px; text-align: center;">AMA</div>'
        '<div style="padding: 9px 10px; text-align: center;">Verdict</div>'
        '</div>'
    )

    # Data rows
    for dim_id in range(1, 7):
        row = REGULATORY_COVERAGE[dim_id]
        highlight = "background: #FEFBFB;" if dim_id in low_scoring else "background: white;"
        parts.append(
            f'<div style="display: grid; grid-template-columns: 1.8fr 1fr 1fr 1fr 1fr 1fr;'
            f' border-top: 0.5px solid #F7EDED; {highlight} align-items: stretch;">'
            f'<div style="padding: 4px 12px; color: #1A1A1A; font-size: 12px; font-weight: 500;'
            f' display: flex; align-items: center;">D{dim_id} · {row["name"]}</div>'
            f'<div style="padding: 4px 6px;">{_cell(row["GDPR"])}</div>'
            f'<div style="padding: 4px 6px;">{_cell(row["EU AI Act"])}</div>'
            f'<div style="padding: 4px 6px;">{_cell(row["DSA"])}</div>'
            f'<div style="padding: 4px 6px;">{_cell(row["AMA Code"])}</div>'
            f'<div style="padding: 4px 6px;">{_verdict_pill(row["verdict"])}</div>'
            f'</div>'
        )

    parts.append('</div>')

    st.markdown(''.join(parts), unsafe_allow_html=True)

    # Acronym legend — spells out the column headers once
    st.markdown(
        '<div style="color: #4A5568; font-size: 11px; line-height: 1.6;'
        ' margin-top: 10px; font-style: italic;">'
        'GDPR: General Data Protection Regulation &nbsp;·&nbsp; '
        'AI Act: EU Artificial Intelligence Act &nbsp;·&nbsp; '
        'DSA: Digital Services Act &nbsp;·&nbsp; '
        'AMA: American Marketing Association Code of Ethics'
        '</div>',
        unsafe_allow_html=True,
    )

    # GAP callout if D3 (Autonomy) is flagged — same single-line pattern
    d3_flagged = 3 in low_scoring
    if d3_flagged:
        st.markdown(
            '<div style="background: #F7EDED; border-left: 3px solid #990011;'
            ' padding: 12px 16px; margin-top: 16px;">'
            '<div style="color: #990011; font-size: 12px; font-weight: 500;'
            ' letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px;">'
            'Regulatory gap</div>'
            '<div style="color: #1A1A1A; font-size: 12.5px; line-height: 1.55;">'
            'D3 Autonomy falls outside the coverage of every current instrument. Emotional '
            'exploitation of cognitive vulnerabilities is not regulated, regardless of whether '
            'the underlying data was legally collected or the content correctly labeled.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Top-level render
# ---------------------------------------------------------------------------
def render_output(answers: dict, scenario_name: str | None):
    dim_scores = calculate_all_dimension_scores(answers)
    total = calculate_total_score(answers)
    verdict = get_verdict(total)
    display_name = scenario_name or "Custom scenario"

    render_verdict_header(verdict, total, display_name, dim_scores)

    # Two columns: radar (left) + dimension grid (right)
    col_radar, col_grid = st.columns([1, 1.4], gap="large")

    with col_radar:
        dim_names = [d["name"] for d in DIMENSIONS]
        fig = build_radar_chart(dim_scores, dim_names, height=360)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        pattern_title, pattern_desc = _diagnose_pattern(dim_scores)
        st.markdown(
            _html(f"""
            <div style="text-align: center; color: #4A5568; font-size: 10.5px;
                 letter-spacing: 0.08em; text-transform: uppercase; margin-top: -8px;">
                {pattern_title}
            </div>
            <div style="text-align: center; color: #4A5568; font-size: 12px;
                 line-height: 1.5; margin-top: 6px; padding: 0 8px;">
                {pattern_desc}
            </div>
            """),
            unsafe_allow_html=True,
        )

    with col_grid:
        render_dimension_grid(dim_scores, answers)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    render_explanations(dim_scores, answers)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    render_regulatory_coverage(dim_scores)
