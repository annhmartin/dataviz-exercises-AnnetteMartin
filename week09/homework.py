import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness", page_icon="🌍", layout="wide")

# ── Data ─────────────────────────────────────────────────────────────────
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'world_happiness_2023.csv'))
df.columns = ['Country', 'Region', 'Score', 'GDP', 'Social_Support',
              'Life_Expectancy', 'Freedom', 'Generosity', 'Corruption']

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N", 5, 25, 15)

filtered = df if selected_region == 'All' else df[df['Region'] == selected_region]

# ── Title + KPIs ──────────────────────────────────────────────────────────
st.title("🌍 World Happiness Dashboard")
st.caption("Source: World Happiness Report 2023 | Kaggle")

col1, col2, col3 = st.columns(3)
col1.metric("Countries", len(filtered))
col2.metric("Avg Score", f"{filtered['Score'].mean():.2f}",
            f"{filtered['Score'].mean() - df['Score'].mean():+.2f} vs global")
col3.metric("Happiest", filtered.nlargest(1, 'Score')['Country'].values[0])

st.divider()

# ── Step 4: Rankings + Scatter ────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Rankings")
    top = filtered.nlargest(top_n, 'Score').sort_values('Score')
    fig1 = px.bar(top, x='Score', y='Country', orientation='h',
                  color_discrete_sequence=['#2E75B6'],
                  labels={'Score': 'Score (0–10)', 'Country': ''})
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       xaxis=dict(range=[0, 8.5]), font=dict(family='Arial', size=12),
                       margin=dict(l=10, r=10, t=5, b=10))
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Score vs GDP")
    fig2 = px.scatter(filtered, x='GDP', y='Score', hover_name='Country',
                      color_discrete_sequence=['#E63946'])
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font=dict(family='Arial', size=12),
                       margin=dict(l=10, r=10, t=5, b=10))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Step 6: Diverging chart ───────────────────────────────────────────────
st.subheader("Distance from Global Mean")

global_mean = df['Score'].mean()
filtered2 = filtered.copy()
filtered2['Delta'] = filtered2['Score'] - global_mean
filtered_sorted = filtered2.sort_values('Delta')

fig3 = px.bar(
    filtered_sorted,
    x='Delta',
    y='Country',
    orientation='h',
    color='Delta',
    color_continuous_scale='RdBu',
    color_continuous_midpoint=0,
    labels={'Delta': 'Δ vs Global Mean', 'Country': ''},
)
fig3.add_vline(
    x=0,
    line_width=1.5,
    line_dash='dash',
    line_color='#555555',
    annotation_text=f'Global mean: {global_mean:.2f}',
    annotation_position='top right',
    annotation_font_size=11,
)
fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=11),
    coloraxis_showscale=False,
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis=dict(gridcolor='#EEEEEE', zeroline=False),
    yaxis=dict(showgrid=False),
)
fig3.update_traces(marker_line_width=0)
st.plotly_chart(fig3, use_container_width=True)

st.caption("Built with Streamlit + Plotly")
