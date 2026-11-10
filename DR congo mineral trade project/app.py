from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "production.csv"
TRADE_DATA_PATH = APP_DIR / "trade.csv"


st.set_page_config(
    page_title="DRC mineral trade dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 3rem; padding-bottom: 2rem; }
    .brand { font-size: 1.55rem; font-weight: 700; letter-spacing: .02em; }
    .brand span { color: #d7ad65; }
    .tagline { color: #9aadc2; margin-top: -.35rem; }
    .demo-note { color: #f2c66d; font-size: .85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🇨🇩 DRC")
    st.caption("Mineral trade & economic analysis")
    page = st.radio(
        "Dashboard section",
        ["Overview", "Minerals", "Trade & exports", "Trade routes", "Economy", "Reports"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Step 1 of 5 · Page structure")


left, right = st.columns([5, 2], vertical_alignment="center")
with left:
    st.markdown('<div class="brand"><span>DRC</span> MINERAL TRADE & ECONOMIC ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Resources · Trade · Opportunity</div>', unsafe_allow_html=True)
with right:
    st.markdown("<div style='text-align:right;color:#9aadc2'>A stronger Congo. A more connected world.</div>", unsafe_allow_html=True)

st.divider()
st.markdown(f"### {page}")
st.markdown('<div class="demo-note">Visual prototype </div>', unsafe_allow_html=True)
st.write("")

metric_specs = [
    ("Total mineral exports · 2024", "$8.4B", "+12.6% vs. 2023", True),
    ("Total trade volume · 2024", "$12.7B", "+9.8% vs. 2023", True),
    ("GDP · 2024", "$73.4B", "+6.1% vs. 2023", True),
    ("Mineral sector share of GDP", "~60%", "Estimated in reference image", False),
]

cols = st.columns(4)
for col, (label, value, note, show_delta) in zip(cols, metric_specs):
    with col:
        st.metric(label, value, note if show_delta else None, border=True)
        if not show_delta:
            st.caption(note)



with st.sidebar:
    st.markdown("### Filters")

    selected_minerals = st.multiselect(
        "Minerals",
        ["Cobalt", "Copper", "Gold", "Coltan","Diamonds"],
        default=["Cobalt", "Copper", "Gold", "Coltan", "Diamonds"],
    )
    st.image(r"C:\Users\TechCharities\Downloads\drc logo.jpg", width=120)
 
    selected_years = st.slider(
        "Trend chart years",
        min_value=2020,
        max_value=2024,
        value=(2020, 2024),
    )

   
export_values = pd.DataFrame({
    "Mineral": [
        "Cobalt ores (HS 2605)",
        "Copper ores (HS 2603)",
        "Coltan-related ores (HS 261590)",
        "Gold (HS 7108)",
        "Diamonds (HS 7102)",
    ],
    "Export value (USD billions)": [
        0.000000020,
        2.708566742,
        0.026869221,
        1.793095146,
        0.089870055,
    ],
    "Value label": ["$20", "$2.71B", "$26.87M", "$1.79B", "$89.87M"],
})

years = [2020, 2021,2022, 2023, 2024]

trend_values = pd.DataFrame({

    "Year": years * 5,
    "Mineral": (
        ["Cobalt"] * 5
        + ["Copper"] * 5
        + ["Gold"] * 5
        + ["Coltan"] * 5
        + ["Diamonds"] * 5
    ),
    "Export value (USD billions)": [
        0.013857638, 0.010627658, 2.4, 0.000000146, 0.000000020,
        0.820466037, 1.580127541, 0.000011983, 2.158079077, 2.708566742,
        0.003959114, 0.002325365, 0.002663727, 1.327514937, 1.793095146,
        0.020207194, 0.013840117, 0.005174900, 0.026207727,0.026869221,
        0.116052342, 0.150719952, 0.133354663, 0.079748784, 0.089870055,
    ],
})

chart_left, chart_right = st.columns([1, 1])
with chart_left:
    with st.container(border=True):
        st.subheader("Top minerals by export value")
        st.caption("USD billions · 2024")
        export_fig = px.bar(
            export_values.sort_values("Export value (USD billions)"),
            x="Export value (USD billions)",
            y="Mineral",
            orientation="h", 
            text="Value label",
            color="Mineral",
            color_discrete_sequence=["#1696e5", "#dd7447", "#a073dc", "#e8bd48", "#21b8b0", "#9ba8b5", "#61758a"],
        )
        
        export_fig.update_traces(texttemplate="%{text}", textposition="outside", cliponaxis=False)
        export_fig.update_layout(
            height=360,
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            xaxis=dict(showgrid=False, showticklabels=False),
            margin=dict(l=5, r=35, t=10, b=5),
        )
        st.plotly_chart(export_fig, width="stretch")

with chart_right:
    with st.container(border=True):
        st.subheader("Mineral export trends")
        st.caption("USD billions · 2020–2024")
        trend_fig = px.line(
            trend_values,
            x="Year",
            y="Export value (USD billions)",
            color="Mineral",
            markers=True,
            color_discrete_map={
                "Cobalt": "#1696e5", "Copper": "#dd7447", "Gold": "#e8bd48",
                "Coltan": "#a073dc", "Diamonds": "#21b8b0",
            },
        )
        trend_fig.update_layout(
            height=360,
            xaxis_title=None,
            yaxis_title=None,
            legend_title=None,
            margin=dict(l=5, r=5, t=10, b=5),
        )
        trend_fig.update_xaxes(dtick=1, showgrid=False)
        trend_fig.update_yaxes(rangemode="tozero", gridcolor="#1d3448")

        filtered_trends = trend_values[
            trend_values["Mineral"].isin(selected_minerals)
            & trend_values["Year"].between(selected_years[0], selected_years[1])
        ]

        trend_flig = px.line(
            filtered_trends,
            x="Year",
            y="Export value (USD billions)",
            color="Mineral",
            markers=True,
        )
        st.plotly_chart(trend_fig, width="stretch")