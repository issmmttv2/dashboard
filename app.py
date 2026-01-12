import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION & PAGE STYLE ---
st.set_page_config(page_title="Product Zero | Sales Strategy", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e1e4e8; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = 'Mock-productzero-sheet 2.xlsx'
    # Reading tabs from the Excel file
    overview = pd.read_excel(file_path, sheet_name='Executive_Overview')
    actions = pd.read_excel(file_path, sheet_name='Account_Action_List')
    logic = pd.read_excel(file_path, sheet_name='ROI_Logic_Explained')
    summary = pd.read_excel(file_path, sheet_name='Phase_Summary')
    return overview, actions, logic, summary

try:
    overview_df, action_df, logic_df, summary_df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🛠 Navigation")
page = st.sidebar.radio("Go to", ["Executive Summary", "Top 10 Hit List", "Phase Deep-Dives", "Strategy & ROI Logic"])

# --- PAGE 1: EXECUTIVE SUMMARY ---
if page == "Executive Summary":
    st.title("🚀 Product Zero: Revenue Recovery")
    st.markdown("#### *Data-Driven Sales Prioritization Engine*")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Portfolio Value", overview_df.iloc[1]['Value'])
    m2.metric("Target Opps", overview_df.iloc[2]['Value'])
    m3.metric("Avg ROI Score", round(action_df['roi_speed_score'].mean(), 1))
    m4.metric("Active Accounts", overview_df.iloc[0]['Value'])
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue Potential by Phase")
        fig_rev = px.bar(summary_df, x='recommended_phase', y='total_revenue', 
                         color='recommended_phase', text_auto='.2s',
                         color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with c2:
        st.subheader("Account Distribution")
        fig_pie = px.pie(action_df, names='recommended_phase', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PAGE 2: TOP 10 HIT LIST ---
elif page == "Top 10 Hit List":
    st.title("🏆 High-Velocity Top 10")
    st.info("These accounts represent the highest recovery potential. Focus resources here for immediate impact.")
    
    top_10 = action_df.sort_values(by='roi_speed_score', ascending=False).head(10)
    
    # Highlight Table
    st.dataframe(top_10[['account_name', 'roi_speed_score', 'recommended_phase', 'recommended_action', 'primary_reason']], 
                 use_container_width=True, hide_index=True)
    
    # Speed Score Chart
    fig_top = px.bar(top_10, x='roi_speed_score', y='account_name', orientation='h',
                     color='roi_speed_score', color_continuous_scale='Greens',
                     title="Top 10 Speed Scores (0-100)")
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

# --- PAGE 3: PHASE DEEP-DIVES ---
elif page == "Phase Deep-Dives":
    st.title("📂 Execution Lists by Phase")
    
    selected_phase = st.selectbox("Select Strategy Phase", ['Phase 1A', 'Phase 1B', 'Phase 2', 'Phase 3'])
    
    phase_data = action_df[action_df['recommended_phase'] == selected_phase].sort_values('roi_speed_score', ascending=False)
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader(f"Target Accounts: {selected_phase}")
        st.dataframe(phase_data[['account_name', 'account_status', 'roi_speed_score', 'assigned_rep']], use_container_width=True)
    
    with col_b:
        st.metric("Phase Account Count", len(phase_data))
        st.markdown(f"**Strategy:** {phase_data['recommended_action'].iloc[0] if not phase_data.empty else 'N/A'}")
        
        csv = phase_data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export List to CSV", data=csv, file_name=f"{selected_phase}_list.csv")

# --- PAGE 4: STRATEGY & ROI LOGIC ---
elif page == "Strategy & ROI Logic":
    st.title("🎯 The 'How' and 'Why'")
    
    st.subheader("Scoring Weights (The How)")
    st.table(logic_df)
    
    st.subheader("Priority Clustering (The Why)")
    st.write("We map ROI Scores against Priority Labels to identify 'Low Hanging Fruit'.")
    fig_scatter = px.scatter(action_df, x='roi_speed_score', y='priority_label', 
                             color='recommended_phase', size='roi_speed_score',
                             hover_name='account_name', title="Opportunity Heatmap")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Product Zero Dashboard v1.0 | Built for Sales Excellence")
