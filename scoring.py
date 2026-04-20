"""
Scoring logic for the PMDF assessment.

Per the brief (Section 5):
- Each answer maps to 0 (manipulation) ... 3 (ethical persuasion).
- Dimension score = AVERAGE of its sub-question scores (range 0-3).
- Total score = SUM of the six dimension averages (range 0-18).
- Verdict thresholds: 0-6 = Manipulation, 7-12 = Borderline, 13-18 = Ethical Persuasion.

Dimension-level colour coding uses the same geometry projected onto a single
dimension: avg 0-1 = red, 1-2 = yellow, >2 = green.
"""

from data.dimensions import DIMENSIONS, get_question


def get_answer_score(dim_id: int, q_id: int, selected_label: str | None) -> float | None:
    """Return the score (0-3) for the selected option label, or None if unanswered."""
    if selected_label is None:
        return None
    question = get_question(dim_id, q_id)
    for option in question["options"]:
        if option["label"] == selected_label:
            return float(option["score"])
    return None


def calculate_dimension_score(dim_id: int, answers: dict) -> float | None:
    """
    answers: dict mapping (dim_id, q_id) -> selected option label.
    Returns the AVERAGE score for this dimension across the questions that
    have been answered. Returns None if no question in the dimension is answered.
    """
    dim = next(d for d in DIMENSIONS if d["id"] == dim_id)
    scores = []
    for q in dim["questions"]:
        score = get_answer_score(dim_id, q["id"], answers.get((dim_id, q["id"])))
        if score is not None:
            scores.append(score)
    if not scores:
        return None
    return sum(scores) / len(scores)


def calculate_all_dimension_scores(answers: dict) -> dict:
    """Return {dim_id: average_score_or_None} for every dimension."""
    return {dim["id"]: calculate_dimension_score(dim["id"], answers) for dim in DIMENSIONS}


def calculate_total_score(answers: dict) -> float:
    """Total = sum of dimension averages. Unanswered dimensions count as 0."""
    dim_scores = calculate_all_dimension_scores(answers)
    return sum((s if s is not None else 0) for s in dim_scores.values())


def get_verdict(total_score: float) -> str:
    """Overall classification: Manipulation (0-6), Borderline (7-12), Ethical Persuasion (13-18)."""
    if total_score <= 6:
        return "Manipulation"
    elif total_score <= 12:
        return "Borderline"
    else:
        return "Ethical Persuasion"


def get_verdict_color(verdict: str) -> str:
    return {
        "Manipulation": "#990011",         # cherry
        "Borderline": "#4A5568",           # slate (serious neutral)
        "Ethical Persuasion": "#2F3C7E",   # navy
    }[verdict]


def get_dimension_level(score: float | None) -> str:
    """
    Map a dimension average (0-3) to a colour level.
    Returns 'red', 'yellow', 'green', or 'unanswered'.
    """
    if score is None:
        return "unanswered"
    if score <= 1:
        return "red"
    if score <= 2:
        return "yellow"
    return "green"


def get_level_color(level: str) -> str:
    return {
        "red": "#990011",          # cherry
        "yellow": "#4A5568",       # slate
        "green": "#2F3C7E",        # navy
        "unanswered": "#E8D5D5",   # soft cherry
    }[level]


def segment_color(score: float | None) -> str:
    """Colour for a single violation-bar segment (one sub-question's score)."""
    if score is None:
        return "#E8D5D5"           # soft cherry (unanswered)
    if score <= 1:
        return "#990011"           # cherry (concerning)
    if score <= 2:
        return "#C8A3A8"           # muted cherry (borderline)
    return "#2F3C7E"               # navy (not concerning)


def get_level_label(level: str) -> str:
    return {
        "red": "Manipulation",
        "yellow": "Borderline",
        "green": "Ethical Persuasion",
        "unanswered": "Not answered",
    }[level]


def all_dimensions_answered(answers: dict) -> bool:
    """Check that every dimension has at least one answered question."""
    for dim in DIMENSIONS:
        dim_scores = [
            get_answer_score(dim["id"], q["id"], answers.get((dim["id"], q["id"])))
            for q in dim["questions"]
        ]
        if all(s is None for s in dim_scores):
            return False
    return True


def count_answered(answers: dict) -> tuple[int, int]:
    """Return (answered_dimensions, total_dimensions)."""
    answered = 0
    for dim in DIMENSIONS:
        dim_scores = [
            get_answer_score(dim["id"], q["id"], answers.get((dim["id"], q["id"])))
            for q in dim["questions"]
        ]
        if any(s is not None for s in dim_scores):
            answered += 1
    return answered, len(DIMENSIONS)
