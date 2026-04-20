"""
PMDF Diagnostic Tool — Streamlit app.

Three screens:
  1. Landing     — hero statement + three documented cases + custom scenario CTA
  2. Questionnaire — stepped, one dimension at a time, live radar sidebar
  3. Output      — verdict hero + radar + dimension grid + regulatory coverage

Pre-loaded scenarios jump directly to the Output screen (all answers are
pre-filled). Custom scenarios walk through the Questionnaire. Copy is written
in product voice — the academic provenance shows up as citations next to each
dimension and as the attribution line at the page foot.
"""

import textwrap

import streamlit as st

from data.dimensions import DIMENSIONS, get_dimension
from data.scenarios import SCENARIOS
from components.scoring import (
    calculate_all_dimension_scores,
    calculate_total_score,
    get_verdict,
    get_verdict_color,
    get_dimension_level,
    all_dimensions_answered,
    get_answer_score,
    segment_color,
)
from components.radar_chart import build_radar_chart
from components.output import render_output


def _html(template: str) -> str:
    """
    Clean a multi-line HTML template for st.markdown.

    Streamlit's markdown parser treats lines indented by 4+ spaces as a code
    block. Passing indented Python source strings to st.markdown(..., unsafe_allow_html=True)
    therefore renders the raw HTML as text. This helper removes common leading
    whitespace and trims surrounding newlines.
    """
    return textwrap.dedent(template).strip()


# ---------------------------------------------------------------------------
# Page configuration + global styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PMDF · Persuasion or Manipulation?",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CUSTOM_CSS = """
<style>
    /* ----- Cream canvas everywhere ----- */
    .stApp { background: #FCF6F5; }

    /* ----- Layout ----- */
    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1180px;
    }

    /* ----- Hide Streamlit chrome ----- */
    #MainMenu, header, footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ----- Typography ----- */
    h1, h2, h3, h4 {
        color: #2F3C7E !important;
        font-weight: 500 !important;
    }
    h1 {
        font-family: Georgia, 'Times New Roman', serif !important;
        font-weight: 400 !important;
        letter-spacing: -0.02em !important;
    }
    .stMarkdown, .stText, p, label, li { color: #1A1A1A; }

    /* ----- Radio buttons styled as option cards ----- */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 6px !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: white !important;
        border: 0.5px solid #E8D5D5 !important;
        border-radius: 4px !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        cursor: pointer;
        transition: all 0.12s ease;
        width: 100%;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        border-color: #C8A3A8 !important;
        background: #FEFBFB !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: #F7EDED !important;
        border: 1.5px solid #990011 !important;
        padding: 11.5px 15.5px !important;
    }
    /* Hide the default radio circle indicator */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    /* Style the option text */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label p {
        color: #1A1A1A !important;
        font-size: 13px !important;
        margin: 0 !important;
        line-height: 1.45 !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* ----- Buttons ----- */
    .stButton > button {
        border-radius: 4px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: 0.5px solid #E8D5D5 !important;
        background: white !important;
        color: #4A5568 !important;
        padding: 10px 20px !important;
        transition: all 0.12s ease;
    }
    .stButton > button:hover:not([disabled]) {
        border-color: #990011 !important;
        color: #990011 !important;
    }
    .stButton > button[kind="primary"] {
        background: #990011 !important;
        color: white !important;
        border-color: #990011 !important;
    }
    .stButton > button[kind="primary"]:hover:not([disabled]) {
        background: #780009 !important;
        color: white !important;
    }
    .stButton > button[disabled] {
        opacity: 0.4;
        cursor: not-allowed;
    }

    /* ----- Text area / notes ----- */
    .stTextArea textarea {
        border: 0.5px solid #E8D5D5 !important;
        background: white !important;
        font-size: 12.5px !important;
        color: #1A1A1A !important;
    }
    .stTextArea textarea:focus {
        border-color: #990011 !important;
        box-shadow: none !important;
    }

    /* ----- Expander ----- */
    details {
        border: 0.5px solid #E8D5D5 !important;
        background: white !important;
        border-radius: 4px !important;
    }
    details > summary {
        color: #4A5568 !important;
        font-size: 12px !important;
    }

    /* ----- Sidebar permanently hidden ----- */
    section[data-testid="stSidebar"] { display: none !important; }

    /* ----- Plotly container trim ----- */
    .js-plotly-plot { background: transparent !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "screen": "landing",
        "scenario_key": None,
        "scenario_name": None,
        "current_dim": 1,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def collect_answers() -> dict:
    """(dim_id, q_id) -> selected option label, for every answered question."""
    answers = {}
    for dim in DIMENSIONS:
        for q in dim["questions"]:
            key = f"q_{dim['id']}_{q['id']}"
            val = st.session_state.get(key)
            if val is not None:
                answers[(dim["id"], q["id"])] = val
    return answers


def clear_all_answers():
    keys = [k for k in list(st.session_state.keys())
            if k.startswith("q_") or k.startswith("notes_")]
    for k in keys:
        del st.session_state[k]


def load_scenario(scenario_key: str):
    """Pre-fill all answers for a documented case, then jump straight to output."""
    clear_all_answers()
    scenario = SCENARIOS[scenario_key]
    for (dim_id, q_id), option_index in scenario["answers"].items():
        dim = get_dimension(dim_id)
        q = next(qq for qq in dim["questions"] if qq["id"] == q_id)
        st.session_state[f"q_{dim_id}_{q_id}"] = q["options"][option_index]["label"]
    st.session_state.scenario_key = scenario_key
    st.session_state.scenario_name = scenario["display_name"]
    st.session_state.current_dim = 1
    st.session_state.screen = "output"


def load_custom():
    """Empty questionnaire; user walks through all six dimensions."""
    clear_all_answers()
    st.session_state.scenario_key = None
    st.session_state.scenario_name = "Custom scenario"
    st.session_state.current_dim = 1
    st.session_state.screen = "questionnaire"


def reset_to_landing():
    clear_all_answers()
    st.session_state.scenario_key = None
    st.session_state.scenario_name = None
    st.session_state.current_dim = 1
    st.session_state.screen = "landing"


def goto_questionnaire_review():
    """From the output screen, go back to review/edit answers from dimension 1."""
    st.session_state.current_dim = 1
    st.session_state.screen = "questionnaire"


# ---------------------------------------------------------------------------
# Shared rendering helpers
# ---------------------------------------------------------------------------
def render_footer():
    st.markdown(
        _html("""
        <div style="margin-top: 60px; padding-top: 18px; border-top: 0.5px solid #E8D5D5;
             color: #4A5568; font-size: 11px; text-align: center; letter-spacing: 0.04em;">
            PMDF Diagnostic Tool &nbsp;·&nbsp; María Reiter Hernández &nbsp;·&nbsp;
            IE University &nbsp;·&nbsp; 2026
        </div>
        """),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Screen 1 — Landing
# ---------------------------------------------------------------------------
def render_landing():
    # ---- Hero
    st.markdown(
        _html("""
        <div style="color: #990011; font-size: 11px; letter-spacing: 0.22em;
             font-weight: 500; margin-bottom: 12px;">PMDF · DIAGNOSTIC TOOL</div>
        """),
        unsafe_allow_html=True,
    )

    col_title, col_sub = st.columns([1.05, 1], gap="large")
    with col_title:
        st.markdown(
            _html("""
            <h1 style="font-family: Georgia, serif; color: #2F3C7E; font-size: 56px;
                 font-weight: 400; line-height: 0.98; margin: 0; letter-spacing: -0.02em;">
                Persuasion.<br><span style="color: #990011;">Or manipulation?</span>
            </h1>
            """),
            unsafe_allow_html=True,
        )
    with col_sub:
        st.markdown(
            _html("""
            <div style="color: #1A1A1A; font-size: 15px; line-height: 1.6; padding-top: 26px;">
                Every political campaign tries to move you. The question is
                <span style="color: #990011; font-weight: 500;">how</span>. Six dimensions
                tell you whether the line has been crossed.
            </div>
            """),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # ---- Documented cases header
    st.markdown(
        _html("""
        <div style="color: #4A5568; font-size: 11px; letter-spacing: 0.14em;
             font-weight: 500; text-transform: uppercase; margin-bottom: 12px;">
            Documented cases
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ---- Three case tiles
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        render_case_tile_cambridge()
    with c2:
        render_case_tile_slovak()
    with c3:
        render_case_tile_biden()

    st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)

    # ---- Custom scenario CTA
    render_custom_cta()

    render_footer()


def _violation_strip(violated_dims: list, on_dark: bool = False) -> str:
    """Render the six-segment signature strip. violated_dims lists {1..6} that are in 'red' level."""
    cherry = "#990011"
    neutral = "#E8D5D5" if not on_dark else "#E8D5D5"
    bar_bg = "#F7EDED" if not on_dark else "#FCF6F5"

    segments = ""
    for i in range(1, 7):
        color = cherry if i in violated_dims else neutral
        segments += f'<div style="height: 4px; flex: 1; background: {color}; border-radius: 2px;"></div>'

    label = "·".join(f"D{d}" for d in violated_dims) + " violated"

    return f"""
    <div style="background: {bar_bg}; padding: 12px 18px 14px;">
        <div style="display: flex; gap: 3px; margin-bottom: 6px;">{segments}</div>
        <div style="color: #4A5568; font-size: 10.5px; letter-spacing: 0.04em;">{label}</div>
    </div>
    """


def render_case_tile_cambridge():
    tile_html = f"""
    <div style="background: #2F3C7E; color: white; display: flex; flex-direction: column;
         height: 100%;">
        <div style="padding: 22px 20px 18px;">
            <div style="font-family: Georgia, serif; font-size: 44px; line-height: 1;
                 font-weight: 400; color: white; margin-bottom: 4px;">87M</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 10px; letter-spacing: 0.08em;
                 margin-bottom: 14px;">FACEBOOK USERS PROFILED</div>
            <div style="color: white; font-size: 14px; font-weight: 500;">Cambridge Analytica</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 11px; margin-top: 2px;">
                Brexit · 2016 · data-centric</div>
        </div>
        {_violation_strip([1, 2, 3, 5, 6], on_dark=True)}
    </div>
    """
    st.markdown(tile_html, unsafe_allow_html=True)
    if st.button("ANALYZE →", key="btn_ca", use_container_width=True, type="primary"):
        load_scenario("cambridge_analytica")
        st.rerun()


def render_case_tile_slovak():
    tile_html = f"""
    <div style="background: white; border: 0.5px solid #E8D5D5; display: flex; flex-direction: column;
         height: 100%;">
        <div style="padding: 22px 20px 18px;">
            <div style="font-family: Georgia, serif; font-size: 44px; line-height: 1;
                 font-weight: 400; color: #990011; margin-bottom: 4px;">48h</div>
            <div style="color: #4A5568; font-size: 10px; letter-spacing: 0.08em;
                 margin-bottom: 14px;">OF PRE-ELECTION SILENCE</div>
            <div style="color: #2F3C7E; font-size: 14px; font-weight: 500;">Slovak Deepfake</div>
            <div style="color: #4A5568; font-size: 11px; margin-top: 2px;">
                Šimečka · 2023 · content-centric</div>
        </div>
        {_violation_strip([2, 3, 4, 6])}
    </div>
    """
    st.markdown(tile_html, unsafe_allow_html=True)
    if st.button("ANALYZE →", key="btn_sk", use_container_width=True, type="primary"):
        load_scenario("slovak_deepfake")
        st.rerun()


def render_case_tile_biden():
    tile_html = f"""
    <div style="background: white; border: 0.5px solid #E8D5D5; display: flex; flex-direction: column;
         height: 100%;">
        <div style="padding: 22px 20px 18px;">
            <div style="font-family: Georgia, serif; font-size: 44px; line-height: 1;
                 font-weight: 400; color: #990011; margin-bottom: 4px;">25K</div>
            <div style="color: #4A5568; font-size: 10px; letter-spacing: 0.08em;
                 margin-bottom: 14px;">VOTERS CALLED WITH AI VOICE</div>
            <div style="color: #2F3C7E; font-size: 14px; font-weight: 500;">Biden Robocall</div>
            <div style="color: #4A5568; font-size: 11px; margin-top: 2px;">
                New Hampshire · Jan 2024</div>
        </div>
        {_violation_strip([1, 2, 3, 4, 6])}
    </div>
    """
    st.markdown(tile_html, unsafe_allow_html=True)
    if st.button("ANALYZE →", key="btn_biden", use_container_width=True, type="primary"):
        load_scenario("biden_robocall")
        st.rerun()


def render_custom_cta():
    st.markdown(
        _html("""
        <div style="background: #2F3C7E; padding: 22px 26px; display: flex;
             justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="color: white; font-size: 15px; font-weight: 500;">
                    Build your own scenario
                </div>
                <div style="color: rgba(255,255,255,0.72); font-size: 12.5px; margin-top: 3px;">
                    Apply the framework to a case of your choosing.
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )
    if st.button("START →", key="btn_custom", type="primary", use_container_width=True):
        load_custom()
        st.rerun()


# ---------------------------------------------------------------------------
# Screen 2 — Stepped questionnaire
# ---------------------------------------------------------------------------
def render_questionnaire():
    current = st.session_state.current_dim
    dim = get_dimension(current)
    answers = collect_answers()

    # ---- Header row
    scenario_label = (st.session_state.scenario_name or "Custom scenario").upper()
    st.markdown(
        _html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;
             margin-bottom: 10px;">
            <div style="color: #4A5568; font-size: 11px; letter-spacing: 0.14em;
                 font-weight: 500;">{scenario_label}</div>
            <div style="color: #4A5568; font-size: 11px;">Dimension {current} of 6</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ---- Progress strip
    segments = ""
    for i in range(1, 7):
        dim_i = get_dimension(i)
        has_any = any((i, q["id"]) in answers for q in dim_i["questions"])
        if i == current:
            color = "#990011"     # current
        elif has_any:
            color = "#2F3C7E"     # completed
        else:
            color = "#E8D5D5"     # upcoming
        segments += f'<div style="height: 3px; flex: 1; background: {color}; border-radius: 2px;"></div>'
    st.markdown(
        f"<div style='display: flex; gap: 4px; margin-bottom: 28px;'>{segments}</div>",
        unsafe_allow_html=True,
    )

    # ---- Main: questions (left) + radar sidebar (right)
    col_q, col_r = st.columns([2.3, 1], gap="large")

    with col_q:
        st.markdown(
            _html(f"""
            <div style="color: #990011; font-size: 11px; letter-spacing: 0.22em;
                 font-weight: 500; margin-bottom: 8px;">
                D{dim['id']} · {dim['name'].upper()}
            </div>
            <h1 style="font-family: Georgia, serif; color: #2F3C7E; font-size: 26px;
                 line-height: 1.25; margin: 0 0 8px; font-weight: 400;">
                {dim['core_question']}
            </h1>
            <div style="color: #4A5568; font-size: 12px; margin-bottom: 22px;
                 font-style: italic;">{' · '.join(dim['literature'])}</div>
            """),
            unsafe_allow_html=True,
        )

        for q in dim["questions"]:
            st.markdown(
                _html(f"""
                <div style="color: #2F3C7E; font-size: 13.5px; font-weight: 500;
                     margin: 18px 0 10px;">{q['text']}</div>
                """),
                unsafe_allow_html=True,
            )
            key = f"q_{dim['id']}_{q['id']}"
            options = [opt["label"] for opt in q["options"]]
            current_val = st.session_state.get(key)
            idx = options.index(current_val) if current_val in options else None
            st.radio(
                label=f"question_{dim['id']}_{q['id']}",
                options=options,
                index=idx,
                key=key,
                label_visibility="collapsed",
            )

        with st.expander("Add notes (optional)"):
            st.text_area(
                "notes",
                key=f"notes_{dim['id']}",
                height=80,
                label_visibility="collapsed",
                placeholder="Context, assumptions, or observations…",
            )

    with col_r:
        render_live_radar_sidebar(answers)

    # ---- Bottom navigation
    st.markdown(
        "<hr style='border: none; border-top: 0.5px solid #E8D5D5; margin: 24px 0 16px;'>",
        unsafe_allow_html=True,
    )

    # Recollect answers AFTER radio widgets have rendered
    fresh_answers = collect_answers()
    current_has_answer = any((current, q["id"]) in fresh_answers for q in dim["questions"])
    all_complete = all_dimensions_answered(fresh_answers)

    nav_back, nav_spacer, nav_forward = st.columns([1, 1.2, 1])

    with nav_back:
        if current > 1:
            if st.button(f"← BACK TO D{current - 1}", key="nav_back",
                         use_container_width=True):
                st.session_state.current_dim = current - 1
                st.rerun()
        else:
            if st.button("← LANDING", key="nav_landing", use_container_width=True):
                reset_to_landing()
                st.rerun()

    with nav_spacer:
        st.markdown(
            _html(f"""
            <div style="text-align: center; color: #4A5568; font-size: 11px;
                 letter-spacing: 0.06em; padding-top: 12px;">
                {sum(1 for i in range(1, 7) if any((i, q['id']) in fresh_answers
                     for q in get_dimension(i)['questions']))} of 6 dimensions answered
            </div>
            """),
            unsafe_allow_html=True,
        )

    with nav_forward:
        if current < 6:
            if st.button(f"CONTINUE TO D{current + 1} →", key="nav_forward",
                         type="primary", use_container_width=True,
                         disabled=not current_has_answer):
                st.session_state.current_dim = current + 1
                st.rerun()
        else:
            if st.button("VIEW ASSESSMENT →", key="nav_generate",
                         type="primary", use_container_width=True,
                         disabled=not all_complete):
                st.session_state.screen = "output"
                st.rerun()

    if current == 6 and not all_complete:
        missing = [
            i for i in range(1, 7)
            if not any((i, q["id"]) in fresh_answers for q in get_dimension(i)["questions"])
        ]
        st.markdown(
            _html(f"""
            <div style="color: #990011; font-size: 11.5px; text-align: center; margin-top: 10px;">
                Answer at least one question in every dimension to generate the assessment.
                Missing: {', '.join(f'D{i}' for i in missing)}.
            </div>
            """),
            unsafe_allow_html=True,
        )


def render_live_radar_sidebar(answers: dict):
    st.markdown(
        _html("""
        <div style="color: #4A5568; font-size: 10.5px; letter-spacing: 0.12em;
             font-weight: 500; margin-bottom: 10px;">LIVE RADAR</div>
        """),
        unsafe_allow_html=True,
    )

    scores = calculate_all_dimension_scores(answers)
    dim_names = [d["name"] for d in DIMENSIONS]
    fig = build_radar_chart(scores, dim_names, height=260, compact=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    total = calculate_total_score(answers)
    verdict = get_verdict(total)
    verdict_color = get_verdict_color(verdict)
    answered_count = sum(
        1 for d in DIMENSIONS
        if any((d["id"], q["id"]) in answers for q in d["questions"])
    )

    st.markdown(
        _html(f"""
        <div style="background: white; padding: 14px 16px; border: 0.5px solid #E8D5D5;
             margin-top: 8px;">
            <div style="color: #4A5568; font-size: 10px; letter-spacing: 0.1em;
                 text-transform: uppercase; margin-bottom: 4px;">Running total</div>
            <div style="font-family: Georgia, serif; color: {verdict_color}; font-size: 22px;
                 font-weight: 400; line-height: 1;">
                {total:.1f}<span style="color: #4A5568; font-size: 12px;"> / 18</span>
            </div>
            <div style="color: #4A5568; font-size: 10.5px; margin-top: 6px;">
                {answered_count} of 6 dimensions answered
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Screen 3 — Output
# ---------------------------------------------------------------------------
def render_output_screen():
    answers = collect_answers()
    if not all_dimensions_answered(answers):
        # Defensive — should not happen unless state was tampered with
        st.session_state.screen = "questionnaire"
        st.rerun()
        return

    render_output(answers, st.session_state.scenario_name)

    st.markdown(
        "<hr style='border: none; border-top: 0.5px solid #E8D5D5; margin: 32px 0 16px;'>",
        unsafe_allow_html=True,
    )

    nav_home, nav_review, nav_new = st.columns(3)
    with nav_home:
        if st.button("← LANDING", key="out_landing", use_container_width=True):
            reset_to_landing()
            st.rerun()
    with nav_review:
        if st.button("REVIEW ANSWERS", key="out_review", use_container_width=True):
            goto_questionnaire_review()
            st.rerun()
    with nav_new:
        if st.button("NEW SCENARIO →", key="out_new", type="primary",
                     use_container_width=True):
            load_custom()
            st.rerun()

    render_footer()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
def main():
    init_state()
    screen = st.session_state.screen
    if screen == "landing":
        render_landing()
    elif screen == "questionnaire":
        render_questionnaire()
    elif screen == "output":
        render_output_screen()
    else:
        st.session_state.screen = "landing"
        st.rerun()


if __name__ == "__main__":
    main()
