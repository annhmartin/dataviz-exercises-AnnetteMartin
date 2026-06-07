# ── STEP 6: Third chart using a DIVERGING colour scale ───────────────────
# Values go above and below a meaningful midpoint: the global mean score.
# Each bar shows how far a country deviates from the world average.

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
