import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# PAGE SETUP & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="SDG 1 Dashboard - Poverty Elimination & Policy Simulator",
    page_icon="un_logo_circular.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color Scheme: United Nations Blue (#0A4F85) as primary
PRIMARY_COLOR = "#0A4F85"
SECONDARY_COLOR = "#2B6CB0" # Slate Blue
ACCENT_COLOR = "#D69E2E"    # Gold
BG_CARD_LIGHT = "rgba(15, 23, 42, 0.04)"
BG_CARD_DARK = "rgba(255, 255, 255, 0.04)"

# Inject Custom CSS for Inter font, Glassmorphism Cards, and United Nations Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        color: #0A4F85;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #64748B;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(10, 79, 133, 0.15);
        border-left: 5px solid #0A4F85;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(10, 79, 133, 0.08);
        border-color: rgba(10, 79, 133, 0.4);
    }
    
    .card-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0A4F85;
        margin: 0;
    }
    
    .card-unit {
        font-size: 0.9rem;
        color: #94A3B8;
        font-weight: 400;
    }

    .regression-eq {
        background: rgba(10, 79, 133, 0.05);
        border: 1px dashed #0A4F85;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-size: 1.1rem;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        margin: 15px 0;
        color: #0A4F85;
        word-wrap: break-word;
        white-space: pre-wrap;
    }

    .badge-sig {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    
    .badge-nonsig {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    
    /* Style active sidebar radio selections & dots */
    div[data-testid="stSidebar"] [data-baseweb="radio"] div[role="presentation"] {
        border-color: #0A4F85 !important;
    }
    div[data-testid="stSidebar"] [data-baseweb="radio"] input:checked + div {
        background-color: #0A4F85 !important;
        border-color: #0A4F85 !important;
    }
    
    /* Override active tabs style to match UN Blue */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        color: #64748B;
        transition: color 0.3s ease;
    }
    button[aria-selected="true"][data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        color: #0A4F85 !important;
        font-weight: 600;
    }
    button[aria-selected="true"][data-baseweb="tab"] {
        border-bottom-color: #0A4F85 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA LOADING & CLEANING (WITH CACHING)
# ---------------------------------------------------------
# Resolve paths outside to pass modification times to cached function
base_dir = os.path.dirname(os.path.abspath(__file__))
merged_path = os.path.join(base_dir, "dashboard_final_data.csv")
poverty_path = os.path.join(base_dir, "share-of-population-in-extreme-poverty (1)", "share-of-population-in-extreme-poverty.csv")
social_path = os.path.join(base_dir, "share-covered-by-one-social-protection-benefit", "share-covered-by-one-social-protection-benefit.csv")
basic_services_path = os.path.join(base_dir, "access-to-basic-services", "access-to-basic-services.csv")

@st.cache_data
def load_datasets(mtime_merged, mtime_pov, mtime_soc, mtime_basic):
    # Load Merged Dataset
    df_merged = pd.read_csv(merged_path) if os.path.exists(merged_path) else pd.DataFrame()
    
    # Load Raw Datasets
    df_poverty = pd.read_csv(poverty_path) if os.path.exists(poverty_path) else pd.DataFrame()
    df_social = pd.read_csv(social_path) if os.path.exists(social_path) else pd.DataFrame()
    df_basic = pd.read_csv(basic_services_path) if os.path.exists(basic_services_path) else pd.DataFrame()
    
    return df_merged, df_poverty, df_social, df_basic

# Calculate modification times to trigger auto-reload on file change
mtime_merged = os.path.getmtime(merged_path) if os.path.exists(merged_path) else 0
mtime_pov = os.path.getmtime(poverty_path) if os.path.exists(poverty_path) else 0
mtime_soc = os.path.getmtime(social_path) if os.path.exists(social_path) else 0
mtime_basic = os.path.getmtime(basic_services_path) if os.path.exists(basic_services_path) else 0

df_merged, df_poverty, df_social, df_basic = load_datasets(mtime_merged, mtime_pov, mtime_soc, mtime_basic)

# Variable mappings and descriptions
indicator_labels = {
    "Poverty_Rate_Imputed": "Extreme Poverty Rate (%)",
    "Social_Protection_Coverage": "Social Protection Coverage (%)",
    "Electricity_Access": "Electricity Access (%)",
    "Clean_Cooking_Access": "Clean Cooking Access (%)",
    "Water_Access": "Drinking Water Access (%)",
    "Sanitation_Access": "Sanitation Access (%)"
}

# ---------------------------------------------------------
# NUMPY OLS REGRESSION ENGINE
# ---------------------------------------------------------
def run_ols(df_data, x_cols, y_col):
    model_df = df_data.dropna(subset=x_cols + [y_col])
    if len(model_df) < len(x_cols) + 2:
        return None
    
    y = model_df[y_col].values
    X = model_df[x_cols].values
    
    # Design matrix (adds intercept column)
    X_design = np.column_stack((np.ones(len(X)), X))
    
    # Solve standard OLS: beta = (X^T * X)^-1 * X^T * y
    XT = X_design.T
    XTX = np.dot(XT, X_design)
    try:
        XTX_inv = np.linalg.inv(XTX)
    except np.linalg.LinAlgError:
        XTX_inv = np.linalg.pinv(XTX) # Pseudo-inverse fallback
        
    beta = np.dot(XTX_inv, np.dot(XT, y))
    
    # Predicted and residuals
    y_pred = np.dot(X_design, beta)
    residuals = y - y_pred
    
    # Degrees of freedom
    n = len(y)
    p = len(x_cols)
    df_resid = n - p - 1
    
    # Sum of squares & R-squared
    rss = np.sum(residuals ** 2)
    tss = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1.0 - (rss / tss) if tss != 0 else 0.0
    adj_r_squared = 1.0 - ((1.0 - r_squared) * (n - 1) / df_resid) if df_resid > 0 else 0.0
    
    # Standard Errors & t-statistics
    s2 = rss / df_resid if df_resid > 0 else 0.0
    vcov = s2 * XTX_inv
    se = np.sqrt(np.maximum(0, np.diagonal(vcov)))
    
    t_stats = np.zeros_like(beta)
    non_zero_se = se != 0
    t_stats[non_zero_se] = beta[non_zero_se] / se[non_zero_se]
    
    # Standard Normal CDF Approximation (two-tailed p-values)
    def norm_cdf(z):
        t = 1.0 / (1.0 + 0.2316419 * np.abs(z))
        d = 0.3989422804014327 * np.exp(-z * z / 2.0)
        p = d * t * (0.31938153 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + 1.330274429 * t))))
        cdf = 1.0 - p
        return np.where(z >= 0, cdf, 1.0 - cdf)
        
    p_values = 2 * (1.0 - norm_cdf(np.abs(t_stats)))
    
    return {
        "n": n,
        "p": p,
        "df_resid": df_resid,
        "beta": beta,
        "se": se,
        "t_stats": t_stats,
        "p_values": p_values,
        "r_squared": r_squared,
        "adj_r_squared": adj_r_squared,
        "rss": rss,
        "tss": tss,
        "y_pred": y_pred,
        "y_actual": y,
        "residuals": residuals,
        "df_model": model_df
    }

# ---------------------------------------------------------
# NORMAL INVERSE CDF APPROXIMATION FOR Q-Q PLOT
# ---------------------------------------------------------
def erfinv(x):
    # Winitzki approximation for inverse error function
    a = 0.147
    log_term = np.log(1.0 - x**2)
    term1 = 2.0 / (np.pi * a) + log_term / 2.0
    inner = term1**2 - log_term / a
    val = np.sqrt(np.maximum(0, np.sqrt(inner) - term1))
    return np.sign(x) * val

def norm_ppf(p):
    # Maps percentile probability (0,1) to standard normal quantiles (Z-score)
    p_clipped = np.clip(p, 1e-9, 1.0 - 1e-9)
    return np.sqrt(2) * erfinv(2.0 * p_clipped - 1.0)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & FILTERS
# ---------------------------------------------------------
# Circular UN Logo display (centered and minimized)
logo_path = "un_logo_circular.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2:
        st.image(logo_path, width=120)

st.sidebar.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><h2 style='color:{PRIMARY_COLOR}; font-weight:700;'>SDG 1 POLICY ENGINE</h2></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose Dashboard Section:",
    [
        "Overview Dashboard", 
        "Visual Exploratory Analysis", 
        "Regression & Policy Simulator", 
        "SDG 1 Data Center"
    ]
)

# Extract min and max years for local range filters
if not df_merged.empty:
    min_year = int(df_merged["Year"].min())
    max_year = int(df_merged["Year"].max())
else:
    min_year = 2010
    max_year = 2026

st.sidebar.markdown("---")
st.sidebar.info(
    "**Sustainable Development Goal 1:**\n"
    "End poverty in all its forms everywhere.\n\n"
    "This platform demonstrates the link between social safety nets, basic services access, and poverty reduction."
)

# ---------------------------------------------------------
# PAGE 1: OVERVIEW DASHBOARD
# ---------------------------------------------------------
if page == "Overview Dashboard":
    st.markdown("<h1 class='main-title'>SDG 1: No Poverty Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Monitoring extreme poverty, social safety nets, and access to basic services</p>", unsafe_allow_html=True)
    
    # KPI metrics row
    col1, col2, col3 = st.columns(3)
    
    avg_poverty = df_merged["Poverty_Rate_Imputed"].mean()
    avg_social = df_merged["Social_Protection_Coverage"].mean()
    avg_basic = df_merged["Electricity_Access"].mean()
    
    with col1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Average Extreme Poverty Rate</div>
            <div class="card-value">{avg_poverty:.2f}%</div>
            <div class="card-unit">living on less than $3 a day</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Avg. Social Protection Coverage</div>
            <div class="card-value">{avg_social:.2f}%</div>
            <div class="card-unit">covered by at least 1 benefit</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Avg. Electricity Access</div>
            <div class="card-value">{avg_basic:.2f}%</div>
            <div class="card-unit">proxy for access to basic services</div>
        </div>
        """, unsafe_allow_html=True)

    # Global Choropleth Map with Timeline Animation
    st.write("")
    st.markdown("### Global Distribution of SDG Indicators")
    st.write("Visualize the global footprint of extreme poverty rates and access to basic services. Enable the temporal animation to play the 17-year timeline.")

    if not df_merged.empty:
        m_col1, m_col2 = st.columns([1, 3])
        with m_col1:
            st.markdown("<br>", unsafe_allow_html=True)
            map_indicator = st.selectbox(
                "Map Indicator:",
                options=list(indicator_labels.keys()),
                format_func=lambda x: indicator_labels[x],
                key="map_indicator"
            )
            animate_map = st.checkbox("Animate Map Over Time (2010–2026)", value=True)
            
            if not animate_map:
                map_year = st.slider("Select Year for Map:", min_value=2010, max_value=2026, value=2022)
            else:
                st.info("Press 'Play' below the map to run the timeline automatically.")
                
            map_countries = st.multiselect(
                "Filter map by countries (up to 5, leave blank to show all):",
                options=sorted(df_merged["Entity"].unique().tolist()),
                max_selections=5,
                key="map_countries_filter"
            )
                
        with m_col2:
            if animate_map:
                map_df = df_merged.sort_values("Year")
            else:
                map_df = df_merged[df_merged["Year"] == map_year]
                
            if map_countries:
                map_df = map_df[map_df["Entity"].isin(map_countries)]
                
            if animate_map:
                fig_map = px.choropleth(
                    map_df,
                    locations="Code",
                    color=map_indicator,
                    hover_name="Entity",
                    animation_frame="Year",
                    color_continuous_scale=px.colors.sequential.YlOrRd if "Poverty" in indicator_labels[map_indicator] else px.colors.sequential.Viridis_r,
                    labels={map_indicator: indicator_labels[map_indicator]},
                    title=f"Global Development: {indicator_labels[map_indicator]} (2010–2026)"
                )
            else:
                fig_map = px.choropleth(
                    map_df,
                    locations="Code",
                    color=map_indicator,
                    hover_name="Entity",
                    color_continuous_scale=px.colors.sequential.YlOrRd if "Poverty" in indicator_labels[map_indicator] else px.colors.sequential.Viridis_r,
                    labels={map_indicator: indicator_labels[map_indicator]},
                    title=f"Global Status: {indicator_labels[map_indicator]} (Year {map_year})"
                )
                
            fig_map.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                height=520,
                margin=dict(l=0, r=0, t=40, b=0),
                coloraxis_colorbar=dict(title="Value %", thickness=15)
            )
            st.plotly_chart(fig_map, width='stretch')
    else:
        st.error("Dataset not loaded.")

    # Breakdown of SDGs analyzed
    st.markdown("---")
    st.markdown("### SDG Targets Covered by this Platform")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("**Target 1.1 - Eradicate Extreme Poverty**")
        st.markdown("By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $3 a day (adjusted to 2021 PPP prices).")
    with t2:
        st.markdown("**Target 1.3 - Social Protection Systems**")
        st.markdown("Implement nationally appropriate social protection systems and measures for all, and by 2030 achieve substantial coverage of the poor and the vulnerable.")
    with t3:
        st.markdown("**Target 1.4 - Equal Access to Basic Services**")
        st.markdown("Ensure that all men and women, in particular the poor and the vulnerable, have equal rights to economic resources, as well as access to basic services (such as electricity, sanitation, and drinking water).")

# ---------------------------------------------------------
# PAGE 2: EXPLORATORY DATA ANALYSIS (EDA)
# ---------------------------------------------------------
elif page == "Visual Exploratory Analysis":
    st.markdown("<h1 class='main-title'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Investigate correlations, trends, and relationships across indicators</p>", unsafe_allow_html=True)
    
    # No page-level global filters are used to ensure academic clarity and individual chart autonomy.
    df_filtered = df_merged
    
    tab1, tab2, tab3 = st.tabs(["Bivariate Correlations", "Time-Series Trajectories", "Multidimensional Scatter"])
    
    with tab1:
        st.markdown("### Correlations with Poverty Rate")
        st.write("Analyzing how social protection coverage and basic services access interact with the extreme poverty rate.")
        
        # Local country filter for correlations matrix (one country at a time)
        selected_country_corr = st.selectbox(
            "Filter correlation matrix by country (select All Countries to show global correlations):",
            options=["All Countries"] + sorted(df_filtered["Entity"].unique().tolist()),
            index=0,
            key="corr_country_filter"
        )
        if selected_country_corr != "All Countries":
            df_filtered_corr = df_filtered[df_filtered["Entity"] == selected_country_corr]
        else:
            df_filtered_corr = df_filtered
            
        c1, c2 = st.columns([3, 2])
        
        with c1:
            if not df_filtered_corr.empty:
                # Select only numerical columns for correlation
                corr_cols = [
                    'Poverty_Rate_Imputed', 
                    'Social_Protection_Coverage', 
                    'Electricity_Access', 
                    'Clean_Cooking_Access', 
                    'Water_Access', 
                    'Sanitation_Access'
                ]
                corr_df = df_filtered_corr[corr_cols].corr()
                
                fig_heat = px.imshow(
                    corr_df,
                    text_auto=".3f",
                    color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1,
                    labels=dict(color="Correlation"),
                    x=[indicator_labels[col] for col in corr_cols],
                    y=[indicator_labels[col] for col in corr_cols],
                    title="Correlation Matrix Heatmap"
                )
                fig_heat.update_layout(height=420)
                st.plotly_chart(fig_heat, width='stretch')
            else:
                st.warning("No data for correlation calculation.")
                
        with c2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"""
            **Statistical Insights:**
            - **Strong Infrastructure Associations**: Poverty rate exhibits negative correlations with all four basic services. Specifically, access to **electricity**, **clean cooking**, and **sanitation** show massive negative coefficients (often < -0.70), demonstrating that physical utility buildout is structurally linked to lower poverty.
            - **Social Safety Net Protection**: Social protection coverage shows a stable negative correlation with poverty. 
            - **Multicollinearity Indicators**: Notice the extremely high positive correlations among the basic services themselves (e.g., Clean Cooking vs. Electricity). In regression modeling, this indicates multicollinearity, highlighting why a customizable regression builder is useful.
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Trajectories Over Time")
        st.write("Track and compare progress across selected countries.")
        
        if not df_merged.empty:
            indicator_to_plot = st.selectbox(
                "Select Indicator to Plot Over Time:",
                options=list(indicator_labels.keys()),
                format_func=lambda x: indicator_labels[x]
            )
            
            # Local country comparison selector for trajectories
            selected_countries_time = st.multiselect(
                "Select up to 5 countries for comparison:",
                options=sorted(df_merged["Entity"].unique().tolist()),
                default=["Philippines", "Brazil", "India", "Kenya"],
                max_selections=5,
                key="time_series_countries_filter"
            )
            
            # 2030 projections option
            project_trends = st.checkbox("Project Trends to 2030 (SDG Target Year)", value=False)
            
            if selected_countries_time:
                time_df = df_merged[df_merged["Entity"].isin(selected_countries_time)]
                
                # Plotly go.Figure for custom solid/dashed curves
                fig_line = go.Figure()
                colors = px.colors.qualitative.Plotly
                
                # List to compile projection summaries
                proj_summaries = []
                
                for idx, country in enumerate(selected_countries_time):
                    country_data = time_df[time_df["Entity"] == country].sort_values("Year")
                    color = colors[idx % len(colors)]
                    
                    if not country_data.empty:
                        # 1. Historical trace (solid)
                        fig_line.add_trace(go.Scatter(
                            x=country_data["Year"],
                            y=country_data[indicator_to_plot],
                            mode='lines+markers',
                            name=f"{country} (Historical)",
                            line=dict(color=color, width=2.5),
                            marker=dict(size=6)
                        ))
                        
                        # 2. Projected trace if enabled
                        if project_trends:
                            x_hist = country_data["Year"].values
                            y_hist = country_data[indicator_to_plot].values
                            
                            if len(x_hist) > 1:
                                slope, intercept = np.polyfit(x_hist, y_hist, 1)
                                
                                # Extrapolate from 2026 to 2030
                                last_year = int(x_hist.max())
                                proj_years = np.array(list(range(last_year, 2031)))
                                proj_vals = slope * proj_years + intercept
                                proj_vals = np.clip(proj_vals, 0.0, 100.0) # bound percentages to 0-100%
                                
                                fig_line.add_trace(go.Scatter(
                                    x=proj_years,
                                    y=proj_vals,
                                    mode='lines',
                                    name=f"{country} (Projected)",
                                    line=dict(color=color, width=2, dash='dash'),
                                    hoverlabel=dict(namelength=-1)
                                ))
                                
                                # Save summary details
                                val_2026 = float(country_data[country_data["Year"] == 2026][indicator_to_plot].values[0]) if 2026 in x_hist else y_hist[-1]
                                val_2030 = float(proj_vals[-1])
                                
                                # SDG Progress Evaluation
                                if "Poverty_Rate_Imputed" in indicator_to_plot:
                                    if val_2030 <= 3.0:
                                        status = '<span style="color:#03543F; font-weight:bold; background-color:#DEF7EC; padding:2px 8px; border-radius:4px;">On Track</span>'
                                    elif slope < 0:
                                        status = '<span style="color:#9B1C1C; font-weight:bold; background-color:#FDE8E8; padding:2px 8px; border-radius:4px;">Insufficient Progress</span>'
                                    else:
                                        status = '<span style="color:#7F1D1D; font-weight:bold; background-color:#FEE2E2; padding:2px 8px; border-radius:4px;">Regressing / Stagnant</span>'
                                else:
                                    # For basic services and social protection, target is 100%
                                    if val_2030 >= 95.0:
                                        status = '<span style="color:#03543F; font-weight:bold; background-color:#DEF7EC; padding:2px 8px; border-radius:4px;">On Track</span>'
                                    elif slope > 0:
                                        status = '<span style="color:#9B1C1C; font-weight:bold; background-color:#FDE8E8; padding:2px 8px; border-radius:4px;">Insufficient Progress</span>'
                                    else:
                                        status = '<span style="color:#7F1D1D; font-weight:bold; background-color:#FEE2E2; padding:2px 8px; border-radius:4px;">Regressing / Stagnant</span>'
                                        
                                proj_summaries.append({
                                    "Country": country,
                                    "2026 Baseline (%)": round(val_2026, 2),
                                    "2030 Projection (%)": round(val_2030, 2),
                                    "Annual Change Rate (%/yr)": round(slope, 3),
                                    "SDG Progress Status": status
                                })
                
                fig_line.update_layout(
                    title=f"Progress Trajectory: {indicator_labels[indicator_to_plot]} (2010–2026, Projected to 2030)",
                    xaxis=dict(tickmode='linear', tick0=min_year, dtick=1),
                    xaxis_title="Year",
                    yaxis_title=indicator_labels[indicator_to_plot],
                    hovermode="x unified",
                    height=500,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_line, width='stretch')
                
                # Projections Methodology Disclaimer
                if project_trends:
                    st.info(
                        "**Methodology Note:** The 2030 projection lines are calculated directly in this dashboard using "
                        "Ordinary Least Squares (OLS) linear trend extrapolation of the country's historical data (2010–2026). "
                        "These are simple mathematical trends assuming recent trajectories remain constant, and do NOT represent "
                        "official forecasts or policy-modeled predictions from the United Nations, World Bank, or other international agencies."
                    )
                    
                    if proj_summaries:
                        st.markdown("#### 2030 SDG Target Progress Summary Table")
                        sum_df = pd.DataFrame(proj_summaries)
                        st.write(sum_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Select up to 5 countries above to compare trajectories.")
        else:
            st.error("Dataset not loaded.")

    with tab3:
        st.markdown("### Multidimensional Analysis")
        st.write("Examine relationships between all indicators concurrently using size and color coordinates.")
        
        if not df_merged.empty:
            # Dropdowns for custom scatter x and size
            sc_col1, sc_col2 = st.columns(2)
            with sc_col1:
                scatter_x = st.selectbox("Select Independent Variable (X-axis):", 
                                         [c for c in indicator_labels.keys() if c != "Poverty_Rate_Imputed"],
                                         format_func=lambda x: indicator_labels[x])
            with sc_col2:
                scatter_size = st.selectbox("Select Indicator for Bubble Size:", 
                                            [c for c in indicator_labels.keys() if c != "Poverty_Rate_Imputed" and c != scatter_x],
                                            format_func=lambda x: indicator_labels[x])

            latest_df = df_merged[df_merged["Year"] == df_merged["Year"].max()]
            
            # Local country filter for bubble scatter plot
            selected_countries_scatter = st.multiselect(
                "Filter bubble scatter plot by up to 5 countries (leave blank to show all):",
                options=sorted(latest_df["Entity"].unique().tolist()),
                max_selections=5,
                key="scatter_countries_filter"
            )
            
            if selected_countries_scatter:
                latest_df_scatter = latest_df[latest_df["Entity"].isin(selected_countries_scatter)]
            else:
                latest_df_scatter = latest_df
                
            fig_scatter = px.scatter(
                latest_df_scatter,
                x=scatter_x,
                y="Poverty_Rate_Imputed",
                size=scatter_size,
                color="Entity",
                hover_name="Entity",
                hover_data=["Year", scatter_size],
                labels={
                    scatter_x: indicator_labels[scatter_x],
                    "Poverty_Rate_Imputed": "Poverty Rate (%)",
                    scatter_size: indicator_labels[scatter_size]
                },
                title=f"Poverty Rate vs. {indicator_labels[scatter_x]} (Bubble size = {indicator_labels[scatter_size]}, Latest Year)"
            )
            fig_scatter.update_layout(height=500)
            st.plotly_chart(fig_scatter, width='stretch')
            
            # Simple trendline addition without external statsmodels package
            st.markdown("#### Bivariate Regression Trendlines")
            
            # Local country filter for trendline plot
            selected_countries_trend = st.multiselect(
                "Filter trendline plot by up to 5 countries (leave blank to show all):",
                options=sorted(latest_df["Entity"].unique().tolist()),
                max_selections=5,
                key="trend_countries_filter"
            )
            
            if selected_countries_trend:
                latest_df_trend = latest_df[latest_df["Entity"].isin(selected_countries_trend)]
            else:
                latest_df_trend = latest_df
                
            temp_df = latest_df_trend.dropna(subset=[scatter_x, "Poverty_Rate_Imputed"])
            x_data = temp_df[scatter_x].values
            y_data = temp_df["Poverty_Rate_Imputed"].values
            
            if len(x_data) > 1:
                slope, intercept = np.polyfit(x_data, y_data, 1)
                x_range = np.linspace(x_data.min(), x_data.max(), 100)
                y_range = slope * x_range + intercept
                
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=x_data, y=y_data,
                    mode='markers',
                    name='Countries',
                    text=temp_df['Entity'].values,
                    marker=dict(size=8, color='#64748B')
                ))
                fig_trend.add_trace(go.Scatter(
                    x=x_range, y=y_range,
                    mode='lines',
                    name='Linear Trendline',
                    line=dict(color='#E5243B', width=2)
                ))
                fig_trend.update_layout(
                    title=f"Trendline: Poverty Rate vs {indicator_labels[scatter_x]} (Slope: {slope:.3f})",
                    xaxis_title=indicator_labels[scatter_x],
                    yaxis_title="Poverty Rate (%)",
                    height=400
                )
                st.plotly_chart(fig_trend, width='stretch')
            else:
                st.warning("Insufficient data to compute trendline.")

# ---------------------------------------------------------
# PAGE 3: REGRESSION & POLICY SIMULATOR
# ---------------------------------------------------------
elif page == "Regression & Policy Simulator":
    st.markdown("<h1 class='main-title'>Dynamic Regression & Policy Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Select custom predictors, analyze OLS coefficients, check diagnostic Q-Q curves, and test policy sliders</p>", unsafe_allow_html=True)
    
    # 🎛️ Predictor Selection panel
    st.markdown("### Step 1: Design OLS Regression Model")
    st.write("Construct your custom multivariate OLS regression model by selecting which indicators predict the poverty rate.")
    
    regression_features = [col for col in indicator_labels.keys() if col != "Poverty_Rate_Imputed"]
    
    selected_features = st.multiselect(
        "Select Independent Variables (X Predictors):",
        options=regression_features,
        default=["Social_Protection_Coverage", "Electricity_Access", "Water_Access"],
        format_func=lambda x: indicator_labels[x],
        key="selected_regression_features"
    )
    
    # Validation
    if not selected_features:
        st.warning("Please select at least one predictor variable. Defaulting to all variables.")
        selected_features = regression_features
        
    # Fit OLS model dynamically
    model_results = run_ols(df_merged, selected_features, "Poverty_Rate_Imputed")
    
    if model_results is None:
        st.error("Unable to fit the regression model. Insufficient overlapping data points.")
    else:
        tab_reg, tab_sim = st.tabs(["Dynamic OLS Results", "Adaptive Policy Sandbox"])
        
        with tab_reg:
            st.markdown("### Dynamic OLS Regression Summary Table")
            st.write("Calculated dynamically using NumPy's OLS solver. Dependent Variable: **Poverty_Rate_Imputed**")
            
            # Show regression equation dynamically
            coefs = model_results["beta"]
            eq_parts = [f"{coefs[0]:.4f}"]
            for i, feat in enumerate(selected_features):
                sign = "+" if coefs[i+1] >= 0 else "-"
                eq_parts.append(f"{sign} ({abs(coefs[i+1]):.4f} * {feat.replace('_', ' ')})")
            equation_str = "Poverty Rate = " + " ".join(eq_parts)
            
            st.markdown(f"""
            <div class="regression-eq">
                {equation_str}
            </div>
            """, unsafe_allow_html=True)
            
            # Construct coefficient table
            terms = ["Intercept"] + [indicator_labels[feat] for feat in selected_features]
            sig_status = []
            for p in model_results["p_values"]:
                if p < 0.05:
                    sig_status.append('<span class="badge-sig">Significant</span>')
                else:
                    sig_status.append('<span class="badge-nonsig">Not Significant</span>')
                    
            reg_df = pd.DataFrame({
                "Variable Term": terms,
                "Coefficient Estimate": coefs.round(5),
                "Standard Error": model_results["se"].round(5),
                "t-statistic": model_results["t_stats"].round(4),
                "p-value": [f"{p:.5f}" if p >= 0.00001 else "< 0.00001" for p in model_results["p_values"]],
                "Statistical Significance": sig_status
            })
            
            # Output dataframe as HTML to render the significance badges
            st.write(reg_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Performance metrics row
            st.markdown("#### Model Performance Metrics")
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.metric("Observations (N)", model_results["n"])
            with r2:
                st.metric("Residual DoF", model_results["df_resid"])
            with r3:
                st.metric("R-squared (R²)", f"{model_results['r_squared']:.4f}")
            with r4:
                st.metric("Adjusted R-squared", f"{model_results['adj_r_squared']:.4f}")
                
            st.markdown("---")
            st.markdown("### Statistical Diagnostic Suite")
            st.write("Verifying linear regression assumptions (Normality of residuals, constant variance, and linearity).")
            
            # Country hover labels preparation
            model_df = model_results["df_model"]
            hover_text = model_df["Entity"] + " (" + model_df["Year"].astype(str) + ")"
            
            # Render Diagnostic Plots Sequentially (Vertically Stacked with Local Filters)
            # 1. Actual vs Predicted
            st.markdown("#### 1. Linearity & Accuracy: Actual vs. Predicted Rates")
            st.write("This plot shows the actual poverty rates against those predicted by your model. Closer alignment with the diagonal dashed line indicates stronger predictive accuracy.")
            
            diag_countries_ap = st.multiselect(
                "Filter Actual vs Predicted chart by up to 5 countries (leave blank to show all):",
                options=sorted(model_df["Entity"].unique().tolist()),
                max_selections=5,
                key="diag_countries_ap_filter"
            )
            
            if diag_countries_ap:
                mask_ap = model_df["Entity"].isin(diag_countries_ap)
                mask_ap_vals = mask_ap.values
                y_pred_ap = model_results["y_pred"][mask_ap_vals]
                y_actual_ap = model_results["y_actual"][mask_ap_vals]
                hover_text_ap = hover_text[mask_ap_vals]
            else:
                y_pred_ap = model_results["y_pred"]
                y_actual_ap = model_results["y_actual"]
                hover_text_ap = hover_text
            
            fig_act_pred = go.Figure()
            fig_act_pred.add_trace(go.Scatter(
                x=y_pred_ap,
                y=y_actual_ap,
                mode='markers',
                text=hover_text_ap,
                hovertemplate="<b>%{text}</b><br>Predicted Poverty: %{x:.2f}%<br>Actual Poverty: %{y:.2f}%<extra></extra>",
                marker=dict(color='#2B6CB0', size=6, opacity=0.6),
                name='Countries'
            ))
            
            if len(y_actual_ap) > 0 and len(y_pred_ap) > 0:
                perfect_line = np.linspace(
                    min(y_actual_ap.min(), y_pred_ap.min()), 
                    max(y_actual_ap.max(), y_pred_ap.max()), 
                    100
                )
                fig_act_pred.add_trace(go.Scatter(
                    x=perfect_line, y=perfect_line,
                    mode='lines',
                    line=dict(color='#E5243B', dash='dash'),
                    name='Perfect (y=x)'
                ))
            
            fig_act_pred.update_layout(
                xaxis_title="Predicted Poverty Rate (%)",
                yaxis_title="Actual Poverty Rate (%)",
                height=500,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_act_pred, width='stretch')
            
            # 2. Residuals vs Predicted
            st.markdown("#### 2. Homoscedasticity: Residuals vs. Fitted Values")
            st.write("This plot tests the assumption of constant variance (homoscedasticity). Ideally, residuals should be randomly and evenly distributed around the horizontal zero line without forming any distinct patterns (like a funnel shape).")
            
            diag_countries_rf = st.multiselect(
                "Filter Residuals vs Fitted chart by up to 5 countries (leave blank to show all):",
                options=sorted(model_df["Entity"].unique().tolist()),
                max_selections=5,
                key="diag_countries_rf_filter"
            )
            
            if diag_countries_rf:
                mask_rf = model_df["Entity"].isin(diag_countries_rf)
                mask_rf_vals = mask_rf.values
                y_pred_rf = model_results["y_pred"][mask_rf_vals]
                residuals_rf = model_results["residuals"][mask_rf_vals]
                hover_text_rf = hover_text[mask_rf_vals]
            else:
                y_pred_rf = model_results["y_pred"]
                residuals_rf = model_results["residuals"]
                hover_text_rf = hover_text
                
            fig_resid = go.Figure()
            fig_resid.add_trace(go.Scatter(
                x=y_pred_rf,
                y=residuals_rf,
                mode='markers',
                text=hover_text_rf,
                hovertemplate="<b>%{text}</b><br>Predicted Poverty: %{x:.2f}%<br>Residual: %{y:.2f}%<extra></extra>",
                marker=dict(color='#D69E2E', size=6, opacity=0.6),
                name='Residuals'
            ))
            
            if len(y_pred_rf) > 0:
                fig_resid.add_trace(go.Scatter(
                    x=[y_pred_rf.min(), y_pred_rf.max()],
                    y=[0, 0],
                    mode='lines',
                    line=dict(color='black', width=1),
                    name='Zero Residual'
                ))
            
            fig_resid.update_layout(
                xaxis_title="Predicted Poverty Rate (%)",
                yaxis_title="Residual (Actual - Predicted)",
                height=500,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_resid, width='stretch')
            
            # 3. Residual Q-Q Plot
            st.markdown("#### 3. Normality of Residuals: Normal Q-Q Plot")
            st.write("This quantile-quantile plot tests whether the model's residuals are normally distributed. If they are, the points should fall closely along the red reference line.")
            
            diag_countries_qq = st.multiselect(
                "Filter Normal Q-Q plot by up to 5 countries (leave blank to show all):",
                options=sorted(model_df["Entity"].unique().tolist()),
                max_selections=5,
                key="diag_countries_qq_filter"
            )
            
            if diag_countries_qq:
                mask_qq = model_df["Entity"].isin(diag_countries_qq)
                mask_qq_vals = mask_qq.values
                residuals_qq = model_results["residuals"][mask_qq_vals]
                hover_text_qq = hover_text[mask_qq_vals]
            else:
                residuals_qq = model_results["residuals"]
                hover_text_qq = hover_text
                
            if len(residuals_qq) > 0:
                std_residuals = residuals_qq / np.std(residuals_qq) if len(residuals_qq) > 1 and np.std(residuals_qq) > 0 else residuals_qq
                sort_idx = np.argsort(std_residuals)
                sorted_std_residuals = std_residuals[sort_idx]
                sorted_hover_text = hover_text_qq.iloc[sort_idx].tolist()
                
                n_points = len(sorted_std_residuals)
                ranks = np.arange(1, n_points + 1)
                p_values = (ranks - 0.5) / n_points
                theoretical_quantiles = norm_ppf(p_values)
                
                fig_qq = go.Figure()
                fig_qq.add_trace(go.Scatter(
                    x=theoretical_quantiles,
                    y=sorted_std_residuals,
                    mode='markers',
                    text=sorted_hover_text,
                    hovertemplate="<b>%{text}</b><br>Theoretical Quantile: %{x:.2f}<br>Standardized Residual: %{y:.2f}<extra></extra>",
                    marker=dict(color='#38A169', size=6, opacity=0.6),
                    name='Residuals'
                ))
                
                # Draw standard reference line (from 25th percentile to 75th percentile)
                if n_points > 1:
                    q25_x, q75_x = norm_ppf(0.25), norm_ppf(0.75)
                    q25_y = np.percentile(sorted_std_residuals, 25)
                    q75_y = np.percentile(sorted_std_residuals, 75)
                    x_diff = q75_x - q25_x
                    slope = (q75_y - q25_y) / x_diff if x_diff != 0 else 1.0
                    intercept = q25_y - slope * q25_x
                    
                    ref_x = np.linspace(theoretical_quantiles.min(), theoretical_quantiles.max(), 100)
                    ref_y = slope * ref_x + intercept
                    
                    fig_qq.add_trace(go.Scatter(
                        x=ref_x, y=ref_y,
                        mode='lines',
                        line=dict(color='#E5243B'),
                        name='Normal Line'
                    ))
                
                fig_qq.update_layout(
                    xaxis_title="Theoretical Quantiles (Normal)",
                    yaxis_title="Standardized Residuals",
                    height=500,
                    margin=dict(l=20, r=20, t=30, b=20)
                )
                st.plotly_chart(fig_qq, width='stretch')
            else:
                st.warning("Select at least one country with data.")
                
        with tab_sim:
            st.markdown("### Adaptive Policy Sandbox")
            st.write(
                "Simulate policy interventions using this model. Sliders below dynamically render for the "
                "predictors selected in **Step 1**."
            )
            
            s_col1, s_col2 = st.columns([1, 1])
            
            with s_col1:
                st.markdown("#### Policy Interventions (Inputs)")
                
                # Adaptive Sliders based on selected features
                policy_inputs = {}
                for feat in selected_features:
                    # Get baseline average of this feature for starting slider positions
                    baseline_avg = float(df_merged[feat].mean())
                    policy_inputs[feat] = st.slider(
                        f"Target: {indicator_labels[feat]}",
                        min_value=0.0,
                        max_value=100.0,
                        value=max(0.0, min(100.0, float(round(baseline_avg)))),
                        step=1.0,
                        help=f"Determine target access levels for {indicator_labels[feat]}."
                    )
                    
                # Compute predicted poverty rate using matrix OLS coefficients
                pred_poverty = coefs[0]
                for idx, feat in enumerate(selected_features):
                    pred_poverty += coefs[idx+1] * policy_inputs[feat]
                    
                # Clip output to logical range [0, 100]%
                actual_pred_val = max(0.0, min(100.0, pred_poverty))
                
                # Output narrative
                st.markdown("---")
                st.markdown("#### Scenario Interpretation")
                if actual_pred_val == 0.0:
                    st.success(
                        f"**Poverty Eradicated!** Under this policy scenario, extreme poverty is predicted to be "
                        "**completely eliminated (0.00%)**. This aligns with the United Nations SDG 1 goal."
                    )
                else:
                    st.warning(
                        f"**Poverty Rate Prediction:** The model predicts a remaining extreme poverty rate of "
                        f"**{actual_pred_val:.2f}%** under this policy framework. Look at individual indicator impacts to optimize."
                    )
                    
                # Model decomposition breakdown
                st.write("")
                st.markdown("**Scenario Math Breakdown:**")
                st.markdown(f"- **Baseline Poverty (Constant):** `{coefs[0]:.2f}%` *(Poverty if safety nets/services are 0)*")
                for idx, feat in enumerate(selected_features):
                    impact = coefs[idx+1] * policy_inputs[feat]
                    st.markdown(f"- **{indicator_labels[feat]} Impact:** `{impact:.2f}%` (target: {policy_inputs[feat]}%, slope: {coefs[idx+1]:.4f})")
                st.markdown(f"- **Net Predicted Rate:** `{pred_poverty:.2f}%` *(Clipped to 0% in visual outputs)*")
                
            with s_col2:
                st.markdown("#### Predicted SDG 1.1.1 Status (Output)")
                
                # Plotly Gauge Chart for Predicted Poverty Rate
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = actual_pred_val,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Predicted Poverty Rate (%)", 'font': {'size': 20}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#E5243B" if actual_pred_val > 15 else ("#D69E2E" if actual_pred_val > 5 else "#38A169")},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 5], 'color': 'rgba(56, 161, 105, 0.15)'},     # Low Poverty (Green)
                            {'range': [5, 15], 'color': 'rgba(214, 158, 46, 0.15)'},    # Moderate (Yellow)
                            {'range': [15, 100], 'color': 'rgba(229, 36, 89, 0.15)'}   # High Poverty (Red)
                        ],
                    }
                ))
                
                fig_gauge.update_layout(height=400, margin=dict(t=50, b=0, l=30, r=30))
                st.plotly_chart(fig_gauge, width='stretch')
                
                # Visual safety net comparison card
                status_color = "#38A169" if actual_pred_val < 5 else ("#D69E2E" if actual_pred_val < 15 else "#E5243B")
                status_text = "LOW POVERTY (SDG Target Met)" if actual_pred_val < 5 else ("MODERATE POVERTY" if actual_pred_val < 15 else "CRITICAL POVERTY ZONE")
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 2px solid {status_color}; border-radius: 8px; padding: 15px; text-align: center; margin-top: 10px;">
                    <span style="font-weight: 500; font-size: 0.9rem; color: #64748B; letter-spacing: 1px;">SIMULATED CLASSIFICATION</span>
                    <h3 style="color: {status_color}; margin: 5px 0 0 0; font-weight: 700;">{status_text}</h3>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 4: SDG 1 DATA CENTER
# ---------------------------------------------------------
elif page == "SDG 1 Data Center":
    st.markdown("<h1 class='main-title'>SDG 1 Data Center</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Inspect, search, filter, and download the datasets used for this analysis</p>", unsafe_allow_html=True)
    
    st.write(
        "Here you can explore the merged analytical dataset, along with the three original raw source files. "
        "Each dataset can be searched, filtered, and downloaded as a standard CSV file."
    )
    
    d_tab1, d_tab2, d_tab3, d_tab4 = st.tabs([
        "Merged Analytical Data", 
        "Raw Poverty Data", 
        "Raw Social Protection Data", 
        "Raw Basic Services Data"
    ])
    
    with d_tab1:
        st.markdown("### Dataset 1: Merged Final Analytical Dataset (`dashboard_final_data.csv`)")
        st.markdown(
            "This dataset represents the aligned, cleaned, and imputed values compiled across the three indicators. "
            "It forms the basis of the OLS regression analysis."
        )
        
        if not df_merged.empty:
            # Filters
            col_search, col_year = st.columns([2, 1])
            with col_search:
                q = st.text_input("Search Country or Code (Merged):", key="search_merged")
            with col_year:
                y_filter = st.multiselect("Filter Years:", sorted(df_merged["Year"].unique().tolist()), key="year_merged")
                
            # Filter logic
            m_df = df_merged.copy()
            if q:
                m_df = m_df[m_df["Entity"].str.contains(q, case=False) | m_df["Code"].str.contains(q, case=False)]
            if y_filter:
                m_df = m_df[m_df["Year"].isin(y_filter)]
                
            st.dataframe(m_df, width="stretch")
            
            # Download button
            csv_merged = m_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Merged Data (CSV)",
                data=csv_merged,
                file_name="sdg1_poverty_merged_filtered.csv",
                mime="text/csv"
            )
        else:
            st.error("Merged dataset not loaded.")

    with d_tab2:
        st.markdown("### Dataset 2: Share of Population in Extreme Poverty (`share-of-population-in-extreme-poverty.csv`)")
        st.markdown(
            "**Indicator:** Proportion of population living below the international poverty line ($3 a day at 2021 PPP prices). "
            "**Source:** World Bank Poverty and Inequality Platform (2026)."
        )
        
        if not df_poverty.empty:
            col_search_p, col_year_p = st.columns([2, 1])
            with col_search_p:
                qp = st.text_input("Search Country or Code (Poverty):", key="search_pov")
            with col_year_p:
                yp_filter = st.multiselect("Filter Years:", sorted(df_poverty["Year"].unique().tolist()), key="year_pov")
                
            p_df = df_poverty.copy()
            if qp:
                p_df = p_df[p_df["Entity"].str.contains(qp, case=False) | p_df["Code"].str.contains(qp, case=False)]
            if yp_filter:
                p_df = p_df[p_df["Year"].isin(yp_filter)]
                
            st.dataframe(p_df, width="stretch")
            
            csv_pov = p_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Poverty Data (CSV)",
                data=csv_pov,
                file_name="sdg1_raw_extreme_poverty.csv",
                mime="text/csv"
            )
        else:
            st.warning("Poverty dataset not loaded.")

    with d_tab3:
        st.markdown("### Dataset 3: Social Protection Coverage (`share-covered-by-one-social-protection-benefit.csv`)")
        st.markdown(
            "**Indicator:** SDG 1.3.1 - Proportion of population covered by at least one social protection benefit (%). "
            "**Source:** International Labour Organization (ILO)."
        )
        
        if not df_social.empty:
            col_search_s, col_year_s = st.columns([2, 1])
            with col_search_s:
                qs = st.text_input("Search Country or Code (Social):", key="search_soc")
            with col_year_s:
                ys_filter = st.multiselect("Filter Years:", sorted(df_social["Year"].unique().tolist()), key="year_soc")
                
            s_df = df_social.copy()
            if qs:
                s_df = s_df[s_df["Entity"].str.contains(qs, case=False) | s_df["Code"].str.contains(qs, case=False)]
            if ys_filter:
                s_df = s_df[s_df["Year"].isin(ys_filter)]
                
            st.dataframe(s_df, width="stretch")
            
            csv_soc = s_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Social Protection Data (CSV)",
                data=csv_soc,
                file_name="sdg1_raw_social_protection.csv",
                mime="text/csv"
            )
        else:
            st.warning("Social protection dataset not loaded.")

    with d_tab4:
        st.markdown("### Dataset 4: Access to Basic Services (`access-to-basic-services.csv`)")
        st.markdown(
            "**Indicators:** Proportion of population with access to Electricity, Clean cooking fuels, Improved water, and Improved sanitation. "
            "**Source:** World Bank, World Health Organization (WHO), and UNICEF (2026)."
        )
        
        if not df_basic.empty:
            col_search_b, col_year_b = st.columns([2, 1])
            with col_search_b:
                qb = st.text_input("Search Country or Code (Basic Services):", key="search_basic")
            with col_year_b:
                yb_filter = st.multiselect("Filter Years:", sorted(df_basic["Year"].unique().tolist()), key="year_basic")
                
            b_df = df_basic.copy()
            if qb:
                b_df = b_df[b_df["Entity"].str.contains(qb, case=False) | b_df["Code"].str.contains(qb, case=False)]
            if yb_filter:
                b_df = b_df[b_df["Year"].isin(yb_filter)]
                
            st.dataframe(b_df, width="stretch")
            
            csv_basic = b_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Basic Services Data (CSV)",
                data=csv_basic,
                file_name="sdg1_raw_basic_services.csv",
                mime="text/csv"
            )
        else:
            st.warning("Basic services dataset not loaded.")
