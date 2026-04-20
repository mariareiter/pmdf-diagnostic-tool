"""
Regulatory coverage matrix — Section 7 of the Streamlit App Brief.

This table operationalises Hypothesis 1 of the thesis. Each PMDF dimension is
mapped to the four major current instruments and given an overall verdict:
COVERED (at least one instrument addresses it substantively), PARTIAL (addressed
but with known enforcement gaps), or GAP (no current instrument meaningfully
addresses it). The single GAP verdict — Dimension 3, Respect for Autonomy — is
the thesis's central regulatory finding.
"""

# Per-instrument coverage labels: "FULL", "PARTIAL", or "" (empty = no coverage)
REGULATORY_COVERAGE = {
    1: {
        "name": "Informed Consent",
        "GDPR": "FULL",
        "EU AI Act": "",
        "DSA": "",
        "AMA Code": "PARTIAL",
        "verdict": "COVERED",
        "notes": (
            "GDPR Articles 5, 6 and 9 directly address unauthorised data collection and "
            "non-consensual profiling. This is the dimension most fully addressed by the "
            "post-2018 regulatory response."
        ),
    },
    2: {
        "name": "Transparency of Intent",
        "GDPR": "",
        "EU AI Act": "PARTIAL",
        "DSA": "PARTIAL",
        "AMA Code": "PARTIAL",
        "verdict": "PARTIAL",
        "notes": (
            "The Digital Services Act imposes transparency on large platforms' political "
            "advertising, but enforcement varies by jurisdiction. Dark posts and platform-"
            "private distribution remain partially unaddressed."
        ),
    },
    3: {
        "name": "Respect for Autonomy",
        "GDPR": "",
        "EU AI Act": "",
        "DSA": "",
        "AMA Code": "PARTIAL",
        "verdict": "GAP",
        "notes": (
            "No current instrument substantively regulates emotional exploitation or "
            "manipulation of cognitive vulnerabilities in political marketing. The AMA "
            "Code references autonomy in general terms; no binding law operationalises it. "
            "This is the thesis's central regulatory finding."
        ),
    },
    4: {
        "name": "Content Authenticity",
        "GDPR": "",
        "EU AI Act": "PARTIAL",
        "DSA": "",
        "AMA Code": "",
        "verdict": "PARTIAL",
        "notes": (
            "The EU AI Act (2024) introduces labeling requirements for synthetic content, "
            "but relies on generator compliance, platform detection, and pre-distribution "
            "identification — all of which remain immature as of 2026."
        ),
    },
    5: {
        "name": "Targeting Proportionality",
        "GDPR": "PARTIAL",
        "EU AI Act": "",
        "DSA": "PARTIAL",
        "AMA Code": "",
        "verdict": "PARTIAL",
        "notes": (
            "GDPR's data minimisation and purpose limitation principles address some aspects "
            "of targeting granularity. The DSA imposes risk assessments on very large platforms. "
            "Neither addresses the inferential granularity generative AI enables without "
            "access to personal data."
        ),
    },
    6: {
        "name": "Accountability & Oversight",
        "GDPR": "PARTIAL",
        "EU AI Act": "PARTIAL",
        "DSA": "PARTIAL",
        "AMA Code": "PARTIAL",
        "verdict": "PARTIAL",
        "notes": (
            "Accountability is partially addressed across all four instruments, but shell "
            "companies, cross-jurisdictional transfers, and anonymous cross-platform "
            "distribution continue to evade meaningful enforcement."
        ),
    },
}


VERDICT_COLORS = {
    "COVERED": "#2E7D32",   # green
    "PARTIAL": "#F9A825",   # yellow / amber
    "GAP": "#C62828",        # red
}


VERDICT_LABELS = {
    "COVERED": "Covered",
    "PARTIAL": "Partial",
    "GAP": "Gap",
}
