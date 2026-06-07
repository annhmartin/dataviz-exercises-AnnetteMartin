#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd


# In[2]:


df = pd.read_csv('../data/world_happiness_2023.csv')

df.head()


# In[3]:


print(dir(st))


# In[4]:


# ── STEP 1: Minimal working app ──────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard")
st.write(f"Data loaded: {len(df)} countries")


# In[5]:


# ── STEP 2: Add a chart + apply appropriate colour rule ───────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard")

top15 = df.nlargest(15, 'Score').sort_values('Score')

# The bars are ordered, not categorical — sequential blue (light→dark) is appropriate
fig = px.bar(top15, x='Score', y='Country', orientation='h',
             color='Score',
             color_continuous_scale='Blues',  
             range_color=[5.0, 8.5],
             labels={'Score': 'Happiness Score (0–10)', 'Country': ''})
fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                  font=dict(family='Arial', size=12),
                  xaxis=dict(range=[0, 8.5]),  
                  coloraxis_showscale=False,
                  margin=dict(l=10,r=20,t=10,b=10))
fig.update_traces(marker_line_width=0)
fig.show()
st.plotly_chart(fig, width='stretch')  # always use this


# In[6]:


# ── STEP 3: Sidebar filter + reactive chart ──────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard")

with st.sidebar:
    st.header("Filters")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N countries", 5, 25, 15)

filtered = df if selected_region == 'All' else df[df['Region'] == selected_region]
top = filtered.nlargest(top_n, 'Score').sort_values('Score')

fig = px.bar(top, x='Score', y='Country', orientation='h',
             color_discrete_sequence=['#2E75B6'],  
             labels={'Score': 'Happiness Score (0–10)', 'Country': ''})

fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                  xaxis=dict(range=[0,8.5], gridcolor='#EEEEEE'),
                  yaxis=dict(showgrid=False),
                  font=dict(family='Arial', size=12),
                  margin=dict(l=10,r=20,t=10,b=10))

fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, width='stretch')


# In[7]:


# ── STEP 4: Full dashboard — KPIs + columns layout + BBD colour ──────────
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness", page_icon="🌍", layout="wide")

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

with st.sidebar:
    st.header("Filters")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N", 5, 25, 15)

filtered = df if selected_region == 'All' else df[df['Region'] == selected_region]

st.title("🌍 World Happiness Dashboard")
st.caption("Source: World Happiness Report 2023 | Kaggle")

# KPI row — BBD: big numbers at the top, readable in 5 seconds
col1, col2, col3 = st.columns(3)
col1.metric("Countries", len(filtered))
col2.metric("Avg Score", f"{filtered['Score'].mean():.2f}",
            f"{filtered['Score'].mean()-df['Score'].mean():+.2f} vs global")
col3.metric("Happiest", filtered.nlargest(1,'Score')['Country'].values[0])

st.divider()

# Two-column layout
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Rankings")
    top = filtered.nlargest(top_n, 'Score').sort_values('Score')

    fig1 = px.bar(top, x='Score', y='Country', orientation='h',
                  color_discrete_sequence=['#2E75B6'],
                  labels={'Score':'Score (0–10)','Country':''})

    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       xaxis=dict(range=[0,8.5]), font=dict(family='Arial',size=12),
                       margin=dict(l=10,r=10,t=5,b=10))
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, width='stretch')

with col_right:
    st.subheader("Score vs GDP")
    fig2 = px.scatter(filtered, x='GDP', y='Score', hover_name='Country',
                      # BBD categorical colour: continent = unordered group
                      color_discrete_sequence=['#E63946'])
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font=dict(family='Arial',size=12),
                       margin=dict(l=10,r=10,t=5,b=10))
    st.plotly_chart(fig2, width='stretch')

st.divider()
st.caption("Built with Streamlit + Plotly")


# ---
# ## Class Exercise 💪 💻

# In[10]:


st.divider()
st.subheader("Distance from Global Mean")

global_mean = df['Score'].mean()
filtered = filtered.copy()
filtered['Delta'] = filtered['Score'] - global_mean
filtered_sorted = filtered.sort_values('Delta')

fig3 = px.bar(
    filtered_sorted,
    x='Delta',
    y='Country',
    orientation='h',
    color='Delta',
    color_continuous_scale='RdBu',   # diverging: red = below mean, blue = above
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

st.plotly_chart(fig3, width='stretch')

