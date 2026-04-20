"""
PMDF Dimensions — María Reiter Hernández BBA Thesis, IE University, April 2026.

The six dimensions, core questions, sub-questions, and answer-score mappings are
taken verbatim from the Streamlit App Brief (Section 5). Literature citations
trace back to the thesis reference list. Nothing in this file is new content —
the app is a demonstration layer for the thesis, not an independent contribution.
"""

DIMENSIONS = [
    {
        "id": 1,
        "name": "Informed Consent",
        "core_question": "Has the targeted individual knowingly agreed to receive this content and to the use of their data for targeting?",
        "explanation": (
            "Assesses whether the audience consented — explicitly or implicitly — to "
            "being targeted and to the use of their personal data for that targeting."
        ),
        "literature": ["GDPR (Regulation 2016/679)", "ICO (2020)", "DCMS Committee (2019)"],
        "questions": [
            {
                "id": 1,
                "text": "How did the audience become part of this campaign's targeting pool?",
                "options": [
                    {"label": "They actively opted in (e.g., newsletter signup)", "score": 3},
                    {"label": "They implicitly agreed through a visible privacy notice", "score": 2},
                    {"label": "They were targeted via inferred behavior (platform algorithm)", "score": 1},
                    {"label": "Their data was harvested without their knowledge", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "Is the audience aware that their personal data is being used for this specific targeting?",
                "options": [
                    {"label": "Fully informed with specific disclosure", "score": 3},
                    {"label": "Generally informed through standard terms", "score": 2},
                    {"label": "Unaware of the specific use case", "score": 1},
                    {"label": "Actively deceived about the data's use", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "This scenario lacks meaningful informed consent — the audience was targeted "
                "without adequate knowledge of how their data would be used. GDPR Articles 5, 6 "
                "and 9 were enacted to address precisely this violation in the wake of "
                "Cambridge Analytica (DCMS Committee, 2019; ICO, 2020). Consent must be "
                "explicit, informed, and purpose-specific to be valid."
            ),
            "yellow": (
                "Consent mechanisms exist but are not fully explicit or purpose-specific. "
                "The GDPR requires consent to be freely given, specific, informed and "
                "unambiguous; partial compliance leaves the audience unaware of the specific "
                "targeting logic applied to them (ICO, 2020)."
            ),
        },
    },
    {
        "id": 2,
        "name": "Transparency of Intent",
        "core_question": "Is the persuasive purpose of the communication disclosed to its recipient?",
        "explanation": (
            "Assesses whether the audience can recognise the content as political persuasion — "
            "who funded it, who sent it, and whether a third party can see what is being shown."
        ),
        "literature": ["Zuiderveen Borgesius et al. (2018)", "Digital Services Act (2022)"],
        "questions": [
            {
                "id": 1,
                "text": "Is the content clearly labeled as political advertising or persuasion?",
                "options": [
                    {"label": "Fully labeled with source and sponsor", "score": 3},
                    {"label": "Labeled as political but source is vague", "score": 2},
                    {"label": "Ambiguous — could appear organic", "score": 1},
                    {"label": "Deliberately disguised as organic content", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "Can a third party (journalist, regulator, opposing campaign) see what's being shown?",
                "options": [
                    {"label": "Yes, fully public through ad libraries or records", "score": 3},
                    {"label": "Partially visible through platform archives", "score": 2},
                    {"label": "Limited visibility", "score": 1},
                    {"label": "Invisible to anyone outside the target audience (dark posts)", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "The persuasive intent of this communication is not disclosed to its audience. "
                "Political messaging presented as organic content — including 'dark posts' "
                "visible only to the targeted audience — produces what Zuiderveen Borgesius et "
                "al. (2018) call a 'splintered and personalized information environment' in "
                "which each citizen receives their own version of reality. The EU Digital "
                "Services Act addresses part of this gap through transparency requirements, "
                "but enforcement across jurisdictions remains uneven."
            ),
            "yellow": (
                "Some disclosure exists, but the persuasive intent is not fully transparent. "
                "Platform ad archives provide partial visibility, yet the audience may still "
                "receive the content as if it were organic (Zuiderveen Borgesius et al., 2018)."
            ),
        },
    },
    {
        "id": 3,
        "name": "Respect for Autonomy",
        "core_question": "Does the practice preserve or undermine the individual's capacity for rational, independent decision-making?",
        "explanation": (
            "Assesses whether the message engages the audience as a rational agent or bypasses "
            "their critical thinking through emotional exploitation or identified vulnerabilities."
        ),
        "literature": [
            "Susser et al. (2019)",
            "Hunt & Vitell (1986)",
            "Laczniak & Murphy (2006)",
        ],
        "questions": [
            {
                "id": 1,
                "text": "Does the message rely on rational arguments or emotional exploitation?",
                "options": [
                    {"label": "Primarily factual, policy-focused", "score": 3},
                    {"label": "Mixed — emotional appeals with factual grounding", "score": 2},
                    {"label": "Primarily emotional, minimal factual content", "score": 1},
                    {"label": "Exploits identified psychological vulnerabilities (fear, identity, anger)", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "Is the content designed to be evaluated and challenged, or to bypass critical thinking?",
                "options": [
                    {"label": "Invites deliberation", "score": 3},
                    {"label": "Neutral", "score": 2},
                    {"label": "Designed for emotional response over analysis", "score": 1},
                    {"label": "Optimized to bypass critical thinking (urgency, shock)", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "This scenario bypasses rather than engages the audience's rational agency. "
                "Susser et al. (2019) define manipulation as hidden influence that exploits "
                "the subject's vulnerabilities in ways they cannot recognise or resist. This "
                "dimension is the thesis's central regulatory finding: no current instrument "
                "substantively addresses autonomy-based manipulation, regardless of whether "
                "the underlying data was legally collected or the content correctly labeled."
            ),
            "yellow": (
                "The message leans heavily on emotional appeal. Emotional appeals are not "
                "manipulation by themselves (Cialdini, 2001; Hunt & Vitell, 1986), but the "
                "balance here tips toward bypassing deliberation rather than engaging it "
                "(Susser et al., 2019)."
            ),
        },
    },
    {
        "id": 4,
        "name": "Content Authenticity",
        "core_question": "Is the marketing content genuine or synthetically fabricated (deepfakes, voice clones, AI-generated text)?",
        "explanation": (
            "Assesses whether the audience can trust what they see and hear as corresponding "
            "to reality. A pre-AI dimension in name only — decisive for AI-era political marketing."
        ),
        "literature": [
            "Chesney & Citron (2019)",
            "EU AI Act (2024)",
            "Goldstein et al. (2023)",
        ],
        "questions": [
            {
                "id": 1,
                "text": "How was the content produced?",
                "options": [
                    {"label": "Entirely human-created", "score": 3},
                    {"label": "Human-created with AI editing assistance", "score": 2},
                    {"label": "AI-assisted with clear human oversight", "score": 1},
                    {"label": "Fully AI-generated or synthetic (deepfake, voice clone)", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "Is any synthetic content clearly labeled as AI-generated?",
                "options": [
                    {"label": "Not applicable — no synthetic content", "score": 3},
                    {"label": "Yes, prominently labeled", "score": 3},
                    {"label": "Labeled but not prominently", "score": 2},
                    {"label": "Not labeled (but detectable)", "score": 1},
                    {"label": "Deliberately presented as authentic", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "The content is synthetic — generated or cloned by AI — and presented without "
                "adequate disclosure of its artificial origin. Chesney & Citron (2019) warn "
                "of a 'liar's dividend' in which synthetic media erodes the baseline assumption "
                "that recorded audio and video correspond to real events. The EU AI Act (2024) "
                "introduces labeling requirements, but relies on generator compliance and "
                "downstream detection — both of which Goldstein et al. (2023) note remain immature."
            ),
            "yellow": (
                "Synthetic elements are present but partially labeled. The EU AI Act's "
                "disclosure framework is designed for exactly this zone, though labeling alone "
                "does not solve the verification problems downstream of distribution "
                "(Chesney & Citron, 2019)."
            ),
        },
    },
    {
        "id": 5,
        "name": "Targeting Proportionality",
        "core_question": "Is the granularity of audience targeting proportionate to the marketing objective?",
        "explanation": (
            "Assesses whether the targeting precision matches the stated purpose or whether "
            "it crosses into individual-level psychographic profiling designed to exploit vulnerabilities."
        ),
        "literature": ["Kosinski et al. (2013)", "Mathur et al. (2019)"],
        "questions": [
            {
                "id": 1,
                "text": "What level of targeting is applied?",
                "options": [
                    {"label": "Broad demographic (age, location)", "score": 3},
                    {"label": "Interest-based segmentation", "score": 2},
                    {"label": "Behavioral targeting based on activity", "score": 1},
                    {"label": "Individual-level psychographic profiling", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "Is the targeting granularity proportionate to the marketing objective?",
                "options": [
                    {"label": "Yes, clearly proportionate", "score": 3},
                    {"label": "Somewhat proportionate", "score": 2},
                    {"label": "Excessive for the stated purpose", "score": 1},
                    {"label": "Designed to exploit individual vulnerabilities", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "Targeting granularity is disproportionate to the marketing objective. Kosinski "
                "et al. (2013) demonstrated that a small number of digital signals is enough "
                "to infer personality, political orientation and vulnerabilities — the capability "
                "Cambridge Analytica later operationalised. Proportionality is only partially "
                "regulated: GDPR addresses data collection, but not the inferential granularity "
                "that generative AI now enables from publicly available information."
            ),
            "yellow": (
                "Targeting is tighter than the marketing objective requires. Mathur et al. "
                "(2019) documented how such patterns normalise into industry-standard design, "
                "drifting from persuasion toward manipulation."
            ),
        },
    },
    {
        "id": 6,
        "name": "Accountability & Oversight",
        "core_question": "Are there functioning mechanisms for tracing source, holding parties accountable, and providing recourse?",
        "explanation": (
            "Assesses whether the source of the content can be identified and whether affected "
            "individuals have meaningful recourse when ethical violations occur."
        ),
        "literature": [
            "DCMS Committee (2019)",
            "AMA Code of Ethics (2022)",
            "Chesney & Citron (2019)",
        ],
        "questions": [
            {
                "id": 1,
                "text": "Can the source of the content be identified by the recipient?",
                "options": [
                    {"label": "Source is fully disclosed", "score": 3},
                    {"label": "Source is traceable through standard means", "score": 2},
                    {"label": "Source is obscured but discoverable", "score": 1},
                    {"label": "Source is anonymous or untraceable", "score": 0},
                ],
            },
            {
                "id": 2,
                "text": "If ethical violations occurred, is there a clear recourse pathway?",
                "options": [
                    {"label": "Clear regulatory recourse and enforcement", "score": 3},
                    {"label": "Recourse exists but enforcement is inconsistent", "score": 2},
                    {"label": "Limited recourse mechanisms", "score": 1},
                    {"label": "No meaningful recourse available", "score": 0},
                ],
            },
        ],
        "explanations": {
            "red": (
                "Accountability pathways are weak — the source is obscured and meaningful "
                "recourse is limited or absent. Cambridge Analytica used shell companies and "
                "cross-jurisdictional data transfers to evade oversight (DCMS Committee, 2019); "
                "AI-generated content introduces analogous traceability problems at scale "
                "(Chesney & Citron, 2019). Enforcement lags the speed of the manipulation."
            ),
            "yellow": (
                "Source identification and recourse exist but face enforcement gaps. The DCMS "
                "Committee (2019) noted that partial accountability is functionally similar to "
                "none when enforcement timelines exceed electoral cycles."
            ),
        },
    },
]


# Convenience lookups
def get_dimension(dim_id: int) -> dict:
    return next(d for d in DIMENSIONS if d["id"] == dim_id)


def get_question(dim_id: int, q_id: int) -> dict:
    dim = get_dimension(dim_id)
    return next(q for q in dim["questions"] if q["id"] == q_id)
