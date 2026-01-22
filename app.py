"""
Compliance Matrix - Minimal Dark UI
Clean dark mode with dotted background and Space Grotesk font
"""

import streamlit as st
import pickle
import pandas as pd
from datetime import datetime
import io
import os

# Page configuration
st.set_page_config(
    page_title="Compliance Matrix",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Minimal Dark UI with Dotted Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
    }

    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#333333 1px, transparent 1px);
        background-size: 30px 30px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Minimal Cards */
    .matrix-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: border-color 0.3s ease;
    }
    
    .matrix-card:hover {
        border-color: rgba(255, 255, 255, 0.3);
    }

    .header-container {
        padding: 4rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 3rem;
        text-align: center;
    }
    
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #ffffff;
        letter-spacing: -0.05em;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 300;
        letter-spacing: 0.05em;
    }

    /* Compliance List Items */
    .compliance-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem 0;
    }
    
    .compliance-item:last-child {
        border-bottom: none;
    }

    .compliance-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .compliance-id {
        font-family: monospace;
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .compliance-description {
        color: #94a3b8;
        line-height: 1.6;
        margin: 0.75rem 0;
        font-weight: 300;
    }
    
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .info-badge {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.3rem 0.7rem;
        font-size: 0.7rem;
        color: #ffffff;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 500;
    }
    
    .mandatory-badge {
        background: #ffffff;
        color: #000000;
        font-weight: 700;
        border: none;
    }
    
    /* Stats */
    .stat-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    /* Inputs */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border: none !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #ffffff !important;
    }

    /* Buttons */
    .stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        width: 100%;
        transition: transform 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
    }

    .stDownloadButton > button {
        background: transparent !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #ffffff !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        background: rgba(0, 0, 0, 0.5);
    }

    .footer {
        text-align: center;
        color: #475569;
        margin-top: 6rem;
        padding: 2rem;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        letter-spacing: 0.1em;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model and metadata, or train if missing"""
    try:
        required_files = ['compliance_model.pkl', 'company_metadata.pkl', 'company_types.pkl']
        if not all(os.path.exists(f) for f in required_files):
            with st.spinner("Initializing data matrix... this may take a moment."):
                from train_model import load_and_preprocess_data, create_company_compliance_mapping, save_model_artifacts
                df = load_and_preprocess_data('mop_updated.xlsx')
                mapping = create_company_compliance_mapping(df)
                save_model_artifacts(mapping, df)
        
        with open('compliance_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('company_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        with open('company_types.pkl', 'rb') as f:
            company_types = pickle.load(f)
        return model, metadata, company_types
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        st.info("Ensure 'mop_updated.xlsx' and 'train_model.py' are present in the repository.")
        st.stop()

def display_header():
    """Display the app header"""
    st.markdown("""
    <div class="header-container">
        <h1>Compliance Matrix</h1>
        <p class="subtitle">PROFESSIONAL COMPLIANCE IDENTIFICATION SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

def display_stats(total_compliances, regulation_types):
    """Display statistics cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="matrix-card">
            <div class="stat-label">Total Records</div>
            <div class="stat-number">{total_compliances}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="matrix-card">
            <div class="stat-label">Classification</div>
            <div class="stat-number">Mandatory</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        reg_types_count = len(regulation_types)
        st.markdown(f"""
        <div class="matrix-card">
            <div class="stat-label">Regulation Types</div>
            <div class="stat-number">{reg_types_count}</div>
        </div>
        """, unsafe_allow_html=True)

def display_compliance_item(compliance):
    """Display a single compliance item"""
    st.markdown(f"""
    <div class="compliance-item">
        <span class="compliance-id">{compliance['obligation_id']}</span>
        <div class="compliance-title">{compliance['title']}</div>
        <div class="compliance-description">{compliance['description']}</div>
        <div class="badge-container">
            <span class="info-badge">{compliance['regulation_name']}</span>
            <span class="info-badge">{compliance['regulation_type']}</span>
            <span class="info-badge">{compliance['authority']}</span>
            <span class="info-badge mandatory-badge">{compliance['mandatory']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_csv_buffer(df):
    """Convert dataframe to CSV buffer for download"""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def main():
    """Main application function"""
    model, metadata, company_types = load_model()
    
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<p style='font-weight: 600; color: #ffffff; margin-bottom: 1.5rem; letter-spacing: 0.05em;'>CONFIGURATION</p>", unsafe_allow_html=True)
        
        selected_company = st.selectbox(
            "Company Type",
            options=[""] + company_types,
            format_func=lambda x: "Select Type" if x == "" else x
        )
        
        if selected_company and selected_company in metadata:
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            meta = metadata[selected_company]
            
            st.markdown(f"""
            <div class="matrix-card">
                <p class="stat-label">Items Found</p>
                <p class="stat-number">{meta['total_compliances']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='color: #64748b; font-size: 0.75rem; margin-bottom: 0.5rem; font-weight: 600;'>DISTRIBUTION</p>", unsafe_allow_html=True)
            for reg_type, count in sorted(meta['regulation_types'].items(), key=lambda x: x[1], reverse=True)[:3]:
                st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem; margin: 0.2rem 0;'>{reg_type}: <span style='color: #ffffff; font-weight: 600;'>{count}</span></p>", unsafe_allow_html=True)
    
    # Main content
    if selected_company and selected_company != "":
        if selected_company in model:
            compliances = model[selected_company]
            
            display_stats(
                len(compliances),
                metadata[selected_company]['regulation_types']
            )
            
            # Search
            search_term = st.text_input("Search Matrix", placeholder="Filter by keyword...")
            
            if search_term:
                filtered_compliances = [
                    c for c in compliances 
                    if search_term.lower() in c['title'].lower() 
                    or search_term.lower() in c['description'].lower()
                ]
            else:
                filtered_compliances = compliances
            
            # Tabs
            tab1, tab2 = st.tabs(["Compliance List", "Data Export"])
            
            with tab1:
                st.markdown(f"<p style='color: #64748b; font-size: 0.8rem; margin: 1.5rem 0;'>Showing {len(filtered_compliances)} records</p>", unsafe_allow_html=True)
                
                if filtered_compliances:
                    st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
                    for compliance in filtered_compliances:
                        display_compliance_item(compliance)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No records match your search.")
            
            with tab2:
                st.markdown("<h2 style='margin: 2rem 0 1rem 0; font-weight: 600;'>Data Preview</h2>", unsafe_allow_html=True)
                
                if filtered_compliances:
                    export_df = pd.DataFrame(filtered_compliances)
                    
                    st.dataframe(
                        export_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.markdown("<div style='margin-top: 2rem; text-align: center;'>", unsafe_allow_html=True)
                    csv_data = get_csv_buffer(export_df)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"compliance_matrix_{selected_company}.csv",
                        mime="text/csv"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No data available to export.")
        else:
            st.warning(f"No data for {selected_company}")
    else:
        # Welcome screen
        st.markdown("""
        <div class="matrix-card" style="text-align: center; padding: 8rem 2rem;">
            <h2 style="font-weight: 600; margin-bottom: 1rem;">System Ready</h2>
            <p style="color: #94a3b8; max-width: 400px; margin: 0 auto; line-height: 1.6; font-weight: 300;">
                Select a company type from the sidebar to initialize the compliance matrix and access data export tools.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        COMPLIANCE MATRIX // PROFESSIONAL DATA EXPORT // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
