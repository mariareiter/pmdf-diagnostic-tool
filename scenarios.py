"""
Pre-loaded scenario answer keys — taken from Section 6 of the Streamlit App Brief.

Each answer is the option index (0-based) into the options list for that question
in dimensions.py. Index-based storage is unambiguous because Dimension 4 Question 2
has two options mapping to score 3 ('Not applicable' and 'Yes, prominently labeled'),
and we need to pre-select the correct one per scenario.

Expected verdicts (all three): MANIPULATION. The visual value of the app is not that
these classify correctly — all three historical cases do — but in where the
violations CLUSTER across the six dimensions, which demonstrates Hypothesis 2's
paradigm shift.
"""

SCENARIOS = {
    "cambridge_analytica": {
        "display_name": "Cambridge Analytica / Brexit Campaign (2016)",
        "short_name": "Cambridge Analytica",
        "description": (
            "In 2016, Cambridge Analytica harvested personal data from roughly 87 million "
            "Facebook users via Aleksandr Kogan's 'This Is Your Digital Life' app. Using the "
            "OCEAN personality model, it produced psychographically targeted 'dark posts' "
            "during the Brexit referendum campaign — messages visible only to the intended "
            "audience and invisible to journalists, regulators, and opposing campaigns. "
            "Exposed by whistleblower Christopher Wylie in 2018."
        ),
        "expected_cluster": "data-side (D1, D5, D6)",
        # (dim_id, q_id) -> option_index
        "answers": {
            (1, 1): 3,  # "Data harvested without their knowledge" -> 0
            (1, 2): 3,  # "Actively deceived about the data's use" -> 0
            (2, 1): 3,  # "Deliberately disguised as organic content" -> 0
            (2, 2): 3,  # "Invisible to anyone outside the target audience (dark posts)" -> 0
            (3, 1): 3,  # "Exploits identified psychological vulnerabilities" -> 0
            (3, 2): 2,  # "Designed for emotional response over analysis" -> 1
            (4, 1): 0,  # "Entirely human-created" -> 3
            (4, 2): 0,  # "Not applicable — no synthetic content" -> 3
            (5, 1): 3,  # "Individual-level psychographic profiling" -> 0
            (5, 2): 3,  # "Designed to exploit individual vulnerabilities" -> 0
            (6, 1): 2,  # "Source is obscured but discoverable" -> 1
            (6, 2): 2,  # "Limited recourse mechanisms" -> 1
        },
    },

    "slovak_deepfake": {
        "display_name": "Slovak Election Deepfake (September 2023)",
        "short_name": "Slovak Deepfake",
        "description": (
            "Two days before Slovakia's 2023 parliamentary elections, a fabricated audio clip "
            "circulated on social media purporting to show candidate Michal Šimečka discussing "
            "electoral fraud. The clip was AI-generated and released during Slovakia's official "
            "48-hour pre-election media silence, when fact-checks could not be broadcast to "
            "respond. The case is documented in Freedom House's 'Freedom on the Net 2024' report."
        ),
        "expected_cluster": "content-side (D2, D3, D4)",
        "answers": {
            (1, 1): 1,  # "Implicitly agreed through a visible privacy notice" -> 2
            (1, 2): 1,  # "Generally informed through standard terms" -> 2
            (2, 1): 3,  # "Deliberately disguised as organic content" -> 0
            (2, 2): 3,  # "Invisible to anyone outside the target audience" -> 0
            (3, 1): 3,  # "Exploits identified psychological vulnerabilities" -> 0
            (3, 2): 3,  # "Optimized to bypass critical thinking" -> 0
            (4, 1): 3,  # "Fully AI-generated or synthetic (deepfake)" -> 0
            (4, 2): 4,  # "Deliberately presented as authentic" -> 0
            (5, 1): 1,  # "Interest-based segmentation" -> 2
            (5, 2): 1,  # "Somewhat proportionate" -> 2
            (6, 1): 3,  # "Source is anonymous or untraceable" -> 0
            (6, 2): 3,  # "No meaningful recourse available" -> 0
        },
    },

    "biden_robocall": {
        "display_name": "Biden Robocall / AI Voice Clone (January 2024)",
        "short_name": "Biden Robocall",
        "description": (
            "Ahead of New Hampshire's Democratic presidential primary in January 2024, "
            "thousands of voters received automated phone calls featuring an AI-generated "
            "clone of President Biden's voice telling them not to vote in the primary. The "
            "FCC subsequently ruled AI voice clones illegal under the Telephone Consumer "
            "Protection Act — but the ruling came after the election."
        ),
        "expected_cluster": "content-side (D2, D3, D4)",
        "answers": {
            (1, 1): 2,  # "Targeted via inferred behavior" -> 1
            (1, 2): 2,  # "Unaware of the specific use case" -> 1
            (2, 1): 3,  # "Deliberately disguised as organic content" -> 0
            (2, 2): 3,  # "Invisible to anyone outside the target audience" -> 0
            (3, 1): 3,  # "Exploits identified psychological vulnerabilities" -> 0
            (3, 2): 3,  # "Optimized to bypass critical thinking" -> 0
            (4, 1): 3,  # "Fully AI-generated or synthetic (voice clone)" -> 0
            (4, 2): 4,  # "Deliberately presented as authentic" -> 0
            (5, 1): 1,  # "Interest-based segmentation" -> 2
            (5, 2): 1,  # "Somewhat proportionate" -> 2
            (6, 1): 2,  # "Source is obscured but discoverable" -> 1
            (6, 2): 2,  # "Limited recourse mechanisms" -> 1
        },
    },
}
