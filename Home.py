import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Economic Indices Overview")
st.title("📊 Economic Indices Dashboard")
st.markdown("*Select an index below to explore its detailed trends and analysis.*")

# Color map
color_map = {
    -5: ("#800000", "Extremely Low"), -4: ("#bd0026", "Severely Low"),
    -3: ("#e31a1c", "Very Low"), -2: ("#fc4e2a", "Low"),
    -1: ("#fd8d3c", "Slightly Low"), 0: ("#fecc5c", "Neutral"),
    1: ("#c2e699", "Slightly High"), 2: ("#78c679", "High"),
    3: ("#31a354", "Very High"), 4: ("#006837", "Severely High"),
    5: ("#004529", "Extremely High")
}

# Index data
indices = {
    "Consumer Demand Index (CDI)": (
        "1_CDI_Dashboard", "#00FFF7", [1.0, 0.2, 0.74, 1.6, 1.8], "🛍️",
        "The Consumer Demand Index captures shifts in real-time consumer activity..."
    ),
    "EV Market Adoption Rate": (
        "2_EV_Market_Adoption_Rate", "#FF00D4", [2.5, 2.0, 1.1, 0.9, 1.7], "🚗",
        "The EV Market Adoption Rate tracks how quickly India is transitioning..."
    ),
    "Housing Affordability Stress Index": (
        "3_Housing_Affordability_Stress_Index", "#39FF14", [1.5, 1.3, 1.1, 1.4, 1.7], "🏠",
        "This index measures how financially stretched households are in buying homes..."
    ),
    "Renewable Transition Readiness Score": (
        "4_Renewable_Transition_Readiness_Score", "#FFD700", [1.2, 1.8, 1.1, 1.9, 1.5], "🌱",
        "Measures how prepared India is to shift from fossil fuels to clean energy..."
    ),
    "Infrastructure Activity Index (IAI)": (
        "5_Infrastructure_Activity_Index_(IAI)", "#FF3131", [1.0, 1.5, 1.2, 1.8, 2.5], "🏢",
        "Tracks and forecasts the pace of infrastructure development..."
    ),
    "IMP Index": (
        "6_IMP_Index", "#8A2BE2", [2.0, 2.5, 1.8, 2.8, 2.3], "💰",
        "India’s Macroeconomic Performance (IMP) Index measures India's overall economic well-being..."
    ),
}

# Split columns with visible vertical line simulation
col1, col_mid, col2 = st.columns([1, 0.02, 1])

with col_mid:
    # Create a tall spacer so the vertical line shows clearly
    st.markdown("""
        <div style="height: 1000px; width: 1px; background-color: lightgray; margin: auto;"></div>
    """, unsafe_allow_html=True)

# Helper function to draw index card
def render_index(col, name, data, key):
    page, color, trend, icon, overview = data
    with col:
        st.subheader(f"{icon} {name}")

        latest_real = trend[-1]
        latest_scaled = max(min(round(latest_real), 5), -5)

        fig = go.Figure()
        for val in range(-5, 6):
            fill_color, label = color_map[val]
            fig.add_shape(type="rect", x0=val - 0.5, x1=val + 0.5, y0=-0.3, y1=0.3,
                          line=dict(color="black", width=1), fillcolor=fill_color, layer="below")
            fig.add_trace(go.Scatter(x=[val], y=[0], mode='text', text=[str(val)],
                                     hovertext=[f"{label} ({val})"], showlegend=False,
                                     textfont=dict(color='white', size=14)))
        fig.add_shape(type="rect", x0=latest_scaled - 0.5, x1=latest_scaled + 0.5,
                      y0=-0.35, y1=0.35, line=dict(color="crimson", width=3, dash="dot"),
                      fillcolor="rgba(0,0,0,0)", layer="above")
        fig.add_trace(go.Scatter(x=[latest_scaled], y=[0.45], mode='text',
                                 text=[f"{latest_real:.2f}"], showlegend=False,
                                 textfont=dict(size=14, color='crimson')))
        fig.update_layout(
            xaxis=dict(range=[-5.5, 5.5], showticklabels=False, showgrid=False),
            yaxis=dict(visible=False),
            height=200, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True, key=f"scale-{key}")

        overview_text = f"<p style='color:{color}; margin-bottom: 0.5rem;'><em>{overview}</em></p>"
        st.markdown(overview_text, unsafe_allow_html=True)

        if st.button("Open detailed view of the index →", key=f"btn-{key}"):
            st.switch_page(f"pages/{page}.py")

# Assign half the indices to left, half to right
index_items = list(indices.items())
mid = len(index_items) // 2
for i, (name, data) in enumerate(index_items[:mid]):
    render_index(col1, name, data, f"left-{i}")
for i, (name, data) in enumerate(index_items[mid:]):
    render_index(col2, name, data, f"right-{i}")