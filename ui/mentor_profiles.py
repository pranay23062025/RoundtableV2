"""Mentor profile cards display component"""

import streamlit as st
from data.mentor_data import MENTOR_CARDS
from config.styles import MENTOR_PROFILE_CSS

def render_mentor_profiles():
    """Render mentor profile cards section"""
    # Apply mentor profile specific CSS
    st.markdown(MENTOR_PROFILE_CSS, unsafe_allow_html=True)
    
    # Section header
    st.markdown('<div class="mentor-profile-section">', unsafe_allow_html=True)
    st.markdown("## 👥 Meet Your AI Mentor Team")
    
    # Summary box
    render_mentor_summary()
    
    # Profile cards
    render_mentor_cards()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mentor_summary():
    """Render mentor team summary"""
    summary_html = """
    <div class="mentor-summary-box">
        <h3>🌟 Your Personal Advisory Board</h3>
        <p>
            Our AI mentors combine decades of real-world experience with cutting-edge expertise. 
            Each mentor brings unique perspectives from top universities, Fortune 500 companies, 
            and specialized fields to provide you with comprehensive, personalized guidance.
        </p>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

def render_mentor_cards():
    """Render mentor profile cards in a grid layout"""
    # Display in 2 columns, 5 rows
    for i in range(0, len(MENTOR_CARDS), 2):
        col1, col2 = st.columns(2)
        
        # Left column card
        with col1:
            if i < len(MENTOR_CARDS):
                render_single_mentor_card(MENTOR_CARDS[i])
        
        # Right column card
        with col2:
            if i + 1 < len(MENTOR_CARDS):
                render_single_mentor_card(MENTOR_CARDS[i + 1])

def render_single_mentor_card(mentor):
    """Render a single mentor profile card"""
    card_html = f"""
    <div class="mentor-card">
        <h4>{mentor['title']}</h4>
        <p><strong>🎓 Education:</strong><br><em>{mentor['education']}</em></p>
        <p><strong>💼 Experience:</strong><br><em>{mentor['experience']}</em></p>
        <p><strong>🎯 Specialty:</strong><br><em>{mentor['specialty']}</em></p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_mentor_statistics():
    """Render mentor team statistics (optional enhancement)"""
    stats_html = """
    <div style="
        display: flex; 
        justify-content: space-around; 
        margin: 2rem 0; 
        padding: 1rem; 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        border: 1px solid #E5E8EC;
    ">
        <div style="text-align: center;">
            <h3 style="color: #009CA6; margin-bottom: 0.5rem;">10</h3>
            <p style="margin: 0; font-weight: 500;">Expert Mentors</p>
        </div>
        <div style="text-align: center;">
            <h3 style="color: #009CA6; margin-bottom: 0.5rem;">200+</h3>
            <p style="margin: 0; font-weight: 500;">Years Combined Experience</p>
        </div>
        <div style="text-align: center;">
            <h3 style="color: #009CA6; margin-bottom: 0.5rem;">15+</h3>
            <p style="margin: 0; font-weight: 500;">Areas of Expertise</p>
        </div>
        <div style="text-align: center;">
            <h3 style="color: #009CA6; margin-bottom: 0.5rem;">10K+</h3>
            <p style="margin: 0; font-weight: 500;">Students Helped</p>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)

def render_mentor_profiles_with_stats():
    """Enhanced version with statistics (call this instead of render_mentor_profiles for enhanced view)"""
    # Apply mentor profile specific CSS
    st.markdown(MENTOR_PROFILE_CSS, unsafe_allow_html=True)
    
    # Section header
    st.markdown('<div class="mentor-profile-section">', unsafe_allow_html=True)
    st.markdown("## 👥 Meet Your AI Mentor Team")
    
    # Statistics
    render_mentor_statistics()
    
    # Summary box
    render_mentor_summary()
    
    # Profile cards
    render_mentor_cards()
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_mentor_by_name(mentor_name):
    """Get mentor data by name (utility function)"""
    for mentor in MENTOR_CARDS:
        if mentor_name.lower() in mentor['title'].lower():
            return mentor
    return None

def get_mentors_by_specialty(specialty_keyword):
    """Get mentors that match a specialty keyword"""
    matching_mentors = []
    for mentor in MENTOR_CARDS:
        if specialty_keyword.lower() in mentor['specialty'].lower():
            matching_mentors.append(mentor)
    return matching_mentors