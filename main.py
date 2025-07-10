import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config.settings import APP_TITLE, PAGE_ICON
from config.styles import MAIN_CSS

# Import page components
from pages.data_input_backend import render_data_input_page
from pages.data_showcase_enhanced import render_data_showcase_page
from pages.roundtable import render_roundtable_page

def main():
    """Main application function with streamlined 2-step flow + optional review"""
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    
    # Apply CSS styles
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'data_input'
    
    # Simple navigation
    render_simple_navigation()
    
    # Route to pages
    if st.session_state.current_page == 'data_input':
        render_data_input_page()
    elif st.session_state.current_page == 'data_showcase':
        render_data_showcase_page()
    elif st.session_state.current_page == 'roundtable':
        # Ensure student data is available before rendering roundtable
        if st.session_state.get('student_data'):
            render_roundtable_page()
        else:
            st.error("❌ No student data found. Please complete the previous steps first.")
            st.info("👉 Please go back to the Data Input page and enter student information.")

def render_simple_navigation():
    """Simple page navigation"""
    st.title(f"🤖 {APP_TITLE}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    has_data = st.session_state.get('student_data') is not None
    current_page = st.session_state.current_page
    
    with col1:
        button_type = "primary" if current_page == 'data_input' else "secondary"
        if st.button("📝 1. Data Input", type=button_type, use_container_width=True):
            st.session_state.current_page = 'data_input'
            st.rerun()
    
    with col2:
        disabled = not has_data
        button_type = "primary" if current_page == 'data_showcase' else "secondary"
        if st.button("📊 2. Data Review (Optional)", disabled=disabled, type=button_type, use_container_width=True):
            if has_data:
                st.session_state.current_page = 'data_showcase'
                st.rerun()
    
    with col3:
        disabled = not has_data
        button_type = "primary" if current_page == 'roundtable' else "secondary"
        if st.button("🤖 3. AI Roundtable", disabled=disabled, type=button_type, use_container_width=True):
            if has_data:
                st.session_state.current_page = 'roundtable'
                st.rerun()
    
    # Progress indicator
    if has_data:
        if current_page == 'data_input':
            st.progress(0.5, text="Step 1 of 2: Student Selection Complete")
        elif current_page == 'data_showcase':
            st.progress(0.75, text="Optional: Data Review")
        elif current_page == 'roundtable':
            st.progress(1.0, text="Step 2 of 2: AI Roundtable Active")
    else:
        st.progress(0.5, text="Step 1 of 2: Select Student Data")
    
    st.markdown("---")

if __name__ == "__main__":
    main()