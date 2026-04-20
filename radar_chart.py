"""
Radar chart for the PMDF assessment — cherry/navy palette on transparent background.

The six dimensions plot in dimensions.py order, so the 'shape' of a scenario's
violations is visually consistent across runs. Data-centric cases (Cambridge
Analytica) collapse on the data-side axes; content-centric cases (deepfakes,
voice clones) collapse on the opposite side. That geometric contrast is the
visual proof of the paradigm shift.
"""

import plotly.graph_objects as go

CHERRY = "#990011"
CHERRY_FILL = "rgba(153, 0, 17, 0.18)"
CHERRY_FILL_STRONG = "rgba(153, 0, 17, 0.28)"
NAVY = "#2F3C7E"
SOFT_CHERRY = "#E8D5D5"
SLATE = "#4A5568"

# Short labels used on the radar chart so they don't get clipped.
# The dimension grid next to the radar shows the full names.
SHORT_LABELS = {
    "Informed Consent": "Consent",
    "Transparency of Intent": "Transparency",
    "Respect for Autonomy": "Autonomy",
    "Content Authenticity": "Authenticity",
    "Targeting Proportionality": "Proportionality",
    "Accountability & Oversight": "Accountability",
}


def build_radar_chart(
    dimension_scores: dict,
    dimension_names: list,
    title: str | None = None,
    height: int = 360,
    compact: bool = False,
) -> go.Figure:
    """
    dimension_scores: {dim_id: avg_score_or_None} for dimensions 1-6.
    dimension_names:  list of six dimension names, ordered by dim_id.
    compact:          smaller labels for a sidebar context.

    Unanswered dimensions are plotted at 0 so the chart still renders.
    """
    values = []
    for dim_id in range(1, 7):
        score = dimension_scores.get(dim_id)
        values.append(score if score is not None else 0)

    # Short labels: "D1 Consent" etc. — full names shown in the dimension grid.
    labels = [
        f"D{i + 1} {SHORT_LABELS.get(name, name)}"
        for i, name in enumerate(dimension_names)
    ]

    # Close the loop
    theta = labels + [labels[0]]
    r = values + [values[0]]

    fig = go.Figure()

    # Reference rings at score 1 and 2 (band boundaries)
    for ring_value in (1, 2):
        fig.add_trace(go.Scatterpolar(
            r=[ring_value] * (len(labels) + 1),
            theta=theta,
            mode="lines",
            line=dict(color=SOFT_CHERRY, width=1, dash="dot"),
            hoverinfo="skip",
            showlegend=False,
            name="",
        ))

    # Main assessment shape
    fill_color = CHERRY_FILL_STRONG if not compact else CHERRY_FILL
    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=theta,
        fill="toself",
        fillcolor=fill_color,
        line=dict(color=CHERRY, width=2.4),
        marker=dict(size=7 if not compact else 5, color=CHERRY),
        name="Assessment",
        showlegend=False,
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.2f} / 3<extra></extra>",
    ))

    label_font_size = 10 if compact else 11

    # Build layout kwargs explicitly so 'title' is only set when provided.
    # Passing title=None to update_layout can render the string 'undefined'
    # in some Plotly versions — this avoids that entirely.
    layout_kwargs = dict(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[0, 1, 2, 3],
                ticktext=["0", "1", "2", "3"],
                gridcolor=SOFT_CHERRY,
                tickfont=dict(size=9, color=SLATE),
                angle=90,
                tickangle=90,
            ),
            angularaxis=dict(
                tickfont=dict(size=label_font_size, color=NAVY, family="Georgia, serif"),
                gridcolor=SOFT_CHERRY,
                linecolor=SOFT_CHERRY,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        margin=dict(l=80, r=80, t=20, b=30),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=SLATE),
    )
    if title:
        layout_kwargs["title"] = dict(
            text=title, x=0.5, font=dict(size=13, color=NAVY)
        )
        layout_kwargs["margin"]["t"] = 40

    fig.update_layout(**layout_kwargs)

    return fig
