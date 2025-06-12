import streamlit as st
import plotly.graph_objects as go

# Set dark theme layout and page title
st.set_page_config(layout="wide", page_title="Economic Indices Overview")
st.title("📊 Economic Indices Dashboard")

st.markdown("*Select an index below to explore its detailed trends and analysis.*")

# Index info: filename, neon-style color, mock latest real value, icon, and overview
indices = {
    "Consumer Demand Index (CDI)": (
        "1_CDI_Dashboard", "#00FFF7", 1.6, "🛍️",
        "The Consumer Demand Index captures shifts in real-time consumer activity, helping forecast economic momentum through trends in spending, mobility, and energy use."
    ),
    "EV Market Adoption Rate": (
        "2_EV_Market_Adoption_Rate", "#FF00D4", 0.9, "🚗",
        "The EV Market Adoption Rate tracks how quickly India is transitioning to electric vehicles, revealing the impact of crude prices, government policies, and market trends on EV uptake."
    ),
    "Housing Affordability Stress Index": (
        "3_Housing_Affordability_Stress_Index", "#39FF14", 1.4, "🏠",
        "The Housing Affordability Stress Index measures how financially stretched urban households are in buying homes, combining income, loan limits, and property prices to guide policy and planning."
    ),
    "Renewable Transition Readiness Score": (
        "4_Renewable_Transition_Readiness_Score", "#FFD700", 1.9, "🌱",
        "The Renewable Transition Readiness Score measures how prepared India is to shift from fossil fuels to clean energy, reflecting progress in capacity and investment to support a sustainable future."
    ),
    "Infrastructure Activity Index (IAI)": (
        "5_Infrastructure_Activity_Index_(IAI)", "#FF3131", 2.5, "🏢",
        "The Infrastructure Activity Index tracks and forecasts the pace of India’s infrastructure development by combining key construction and investment trends to inform industry and policy decisions."
    ),
    "IMP Index": (
        "6_IMP_Index", "#8A2BE2", 2.3, "💰",
        "India’s Macroeconomic Performance (IMP) Index measures India's overall economic well-being, taking into consideration significant economic parameters such as inflation rate, unemployment rate, etc."
    ),
}

# Color scale mapping
color_map = {
    -5: ("#800000", "Extremely Low"), -4: ("#bd0026", "Severely Low"),
    -3: ("#e31a1c", "Very Low"), -2: ("#fc4e2a", "Low"),
    -1: ("#fd8d3c", "Slightly Low"), 0: ("#fecc5c", "Neutral"),
    1: ("#c2e699", "Slightly High"), 2: ("#78c679", "High"),
    3: ("#31a354", "Very High"), 4: ("#006837", "Severely High"),
    5: ("#004529", "Extremely High")
}

# Convert real value to scale (-5 to 5) as an example
def get_scaled_value(real):
    return max(min(round(real), 5), -5)

# Create 2-column layout
cols = st.columns(2)
for i, (name, (page, color, latest_real, icon, overview)) in enumerate(indices.items()):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div style='border:1px solid #444; padding:1.2rem; border-radius:12px; margin-bottom:2rem;'>
                <h4 style='margin-bottom:0.5rem'>{icon} {name}</h4>
            """,
            unsafe_allow_html=True
        )

        # Create scale bar chart
        latest_scaled = get_scaled_value(latest_real)
        fig = go.Figure()

        for val in range(-5, 6):
            c, label = color_map[val]
            fig.add_shape(
                type="rect", x0=val - 0.5, x1=val + 0.5, y0=-0.3, y1=0.3,
                line=dict(color="black", width=1), fillcolor=c
            )
            fig.add_trace(go.Scatter(
                x=[val], y=[0], mode="text", text=[str(val)],
                hovertext=[f"{label} ({val})"], showlegend=False,
                textfont=dict(color="white", size=14)
            ))

        # Highlight latest
        fig.add_shape(
            type="rect", x0=latest_scaled - 0.5, x1=latest_scaled + 0.5,
            y0=-0.35, y1=0.35, line=dict(color="crimson", width=3, dash="dot"),
            fillcolor="rgba(0,0,0,0)"
        )
        fig.add_trace(go.Scatter(
            x=[latest_scaled], y=[0.45], mode='text',
            text=[f"{latest_real:.2f}"], showlegend=False,
            textfont=dict(size=16, color='crimson')
        ))

        fig.update_layout(
            height=180, margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(range=[-5.5, 5.5], showticklabels=False, showgrid=False),
            yaxis=dict(visible=False), showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Overview text
        st.markdown(
            f"<p style='color:{color}; margin-bottom:1rem;'><em>{overview}</em></p>",
            unsafe_allow_html=True
        )

        # Navigation button
        if st.button("Open detailed view of the index →", key=f"btn-{i}"):
            st.switch_page(f"pages/{page}.py")

        st.markdown("</div>", unsafe_allow_html=True)  # Close styled card box