import streamlit as st
import streamlit.components.v1 as components
import json
import html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

def render_data_showcase_page():
    """Page 2: Modern Dashboard-style Student Profile"""
    
    if not st.session_state.get('student_data'):
        st.error("❌ No student data found. Please go back to Data Input and select a student.")
        if st.button("← Back to Data Input"):
            st.session_state.current_page = 'data_input'
            st.rerun()
        return
    
    data = st.session_state.student_data
    gvc_id = st.session_state.get('selected_gvc_id', data.get('gvc_id', 'Unknown'))
    
    # Add custom CSS for dashboard styling
    add_dashboard_css()
    
    # Header Section
    render_dashboard_header(data, gvc_id)
    
    # Main Dashboard Grid
    render_dashboard_grid(data)
    
    # Action Buttons
    render_action_buttons(data)

def add_dashboard_css():
    """Add beautiful modern dashboard CSS styling"""
    st.markdown("""
    <style>
    /* Import beautiful fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global dashboard styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Beautiful dashboard cards with glassmorphism */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 4px 16px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 10px 20px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    .dashboard-card:hover::before {
        opacity: 1;
    }
    
    /* Beautiful card headers */
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.1);
        position: relative;
    }
    
    .card-icon {
        font-size: 28px;
        margin-right: 16px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 4px rgba(102, 126, 234, 0.3));
    }
    
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        font-weight: 600;
        background: linear-gradient(135deg, #2d3748, #4a5568);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* Stunning metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 
            0 10px 25px rgba(102, 126, 234, 0.3),
            0 5px 15px rgba(118, 75, 162, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: rotate 4s linear infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 15px 35px rgba(102, 126, 234, 0.4),
            0 8px 20px rgba(118, 75, 162, 0.3);
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 8px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        opacity: 0.95;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced progress bars */
    .progress-bar {
        background: rgba(229, 231, 235, 0.3);
        border-radius: 12px;
        height: 12px;
        margin: 12px 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 12px;
        transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        animation: shimmer 2s infinite;
    }
    
    /* Beautiful tags */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        color: #667eea;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 6px 6px 6px 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .tag:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    /* Spectacular profile header */
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 48px 32px;
        border-radius: 24px;
        margin-bottom: 32px;
        text-align: center;
        box-shadow: 
            0 20px 40px rgba(102, 126, 234, 0.3),
            0 10px 20px rgba(118, 75, 162, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .profile-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.05"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.05"/><circle cx="50" cy="10" r="1" fill="white" opacity="0.03"/><circle cx="10" cy="50" r="1" fill="white" opacity="0.03"/><circle cx="90" cy="30" r="1" fill="white" opacity="0.03"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.6;
    }
    
    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        margin: 0 auto 20px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }
    
    .profile-avatar:hover {
        transform: scale(1.1);
        box-shadow: 
            0 12px 35px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }
    
    .profile-name {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 12px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }
    
    .profile-details {
        font-family: 'Inter', sans-serif;
        opacity: 0.95;
        font-size: 1.2rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Animations */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Enhanced spacing and typography */
    .stMarkdown h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Beautiful info display */
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .info-label {
        font-weight: 600;
        color: #4a5568;
    }
    
    .info-value {
        color: #2d3748;
        font-weight: 500;
    }
    
    /* Add hover effects for buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transform: scale(1.05);
    }

    /* Add animations for cards */
    .dashboard-card {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Add animations and hover effects to the FIFA card */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .metric-card:hover {
        animation: float 3s ease-in-out infinite;
    }

    /* Footer styling */
    .footer {
        margin-top: 50px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

def render_dashboard_header(data, gvc_id):
    """Render the beautiful profile header section"""
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-avatar">🎓</div>
        <div class="profile-name">{data.get('name', 'Unknown Student')}</div>
        <div class="profile-details">
            {data.get('gvc_id', 'N/A')} • Age {data.get('age', 'N/A')} • {data.get('grade_level', 'N/A')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Beautiful info banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
    ">
        <div style="
            color: #667eea;
            font-weight: 600;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
        ">
            📊 Data Source: Loaded from backend database using GVC ID: <strong>{gvc_id}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard_grid(data):
    """Render the main modular dashboard with beautiful organization"""
    
    # Row 1: Key Metrics with Visual Integration
    st.markdown("""
    <div style="margin: 20px 0;">
        <h3 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.6rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
        ">📊 Analytics Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
        render_metric_card("🎯", "Interest Areas", interests_count, "#667eea")
    
    with col2:
        goals_words = len(data.get('goals', '').split())
        render_metric_card("📝", "Goal Words", goals_words, "#764ba2")
    
    with col3:
        strengths_count = len([s.strip() for s in data.get('strengths', '').split(',') if s.strip()])
        render_metric_card("💪", "Strengths", strengths_count, "#f093fb")
    
    with col4:
        email_status = "Available" if data.get('email') else "Missing"
        render_metric_card("📧", "Contact", email_status, "#4ecdc4")
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Row 2: Mixed Layout - Chart + Info Cards
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Large chart area - Interest Distribution
        interests_chart = create_interests_chart(data)
        if interests_chart:
            render_chart_container("🎯 Interest Distribution", interests_chart)
        else:
            render_fallback_chart("🎯 Interest Distribution", 
                                 "Add more interests to see distribution chart", 
                                 "info")
    
    with col2:
        # Stacked info cards
        render_compact_basic_info_card(data)
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        render_compact_stats_card(data)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Row 3: Dual Charts Layout
    col1, col2 = st.columns(2)
    
    with col1:
        radar_chart = create_skills_radar_chart(data)
        if radar_chart:
            render_chart_container("🕸️ Skills Assessment", radar_chart)
        else:
            render_fallback_chart("🕸️ Skills Assessment", 
                                 "Skills profile based on your data", 
                                 "info")
    
    with col2:
        gauge_chart = create_performance_gauge(data)
        if gauge_chart:
            render_chart_container("📊 Profile Completeness", gauge_chart)
        else:
            render_fallback_chart("📊 Profile Completeness", 
                                 "Overall profile score gauge", 
                                 "success")
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Row 4: Full Width Content Cards
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_interests_goals_combined_card(data)
    
    with col2:
        render_timeline_card(data)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Row 5: Visual Analysis Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Strengths vs Challenges Chart
        strengths_chart = create_strengths_challenges_chart(data)
        if strengths_chart:
            render_chart_container("⚖️ Strengths vs Growth Areas", strengths_chart)
        else:
            render_fallback_chart("⚖️ Strengths vs Growth Areas", 
                                 "Add strengths and challenges to see comparison", 
                                 "info")
    
    with col2:
        # Word Cloud
        word_cloud_img = create_word_cloud(data)
        if word_cloud_img:
            render_wordcloud_container(word_cloud_img)
        else:
            render_fallback_chart("☁️ Word Cloud", 
                                 "Add more detailed goals to see word cloud", 
                                 "warning")
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Row 6: FIFA Card (Centered and Featured)
    render_featured_fifa_card(data)

def render_metric_card(icon, label, value, color="#667eea"):
    """Render a metric card with custom color"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color} 0%, {color}dd 50%, {color}bb 100%);
        color: white;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 
            0 10px 25px {color}44,
            0 5px 15px {color}33;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid {color}33;
    ">
        <div style="
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 8px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        ">{value}</div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 500;
            opacity: 0.95;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
            position: relative;
            z-index: 1;
        ">{icon} {label}</div>
    </div>
    """, unsafe_allow_html=True)

def render_chart_container(title, chart):
    """Render a chart in a beautiful container"""
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 4px 16px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    ">
        <h4 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        ">{title}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the chart outside the HTML container
    st.plotly_chart(chart, use_container_width=True)

def render_fallback_chart(title, message, chart_type="info"):
    """Render a fallback chart placeholder"""
    colors = {
        "info": {"bg": "#667eea", "text": "#ffffff"},
        "warning": {"bg": "#f093fb", "text": "#ffffff"},
        "success": {"bg": "#4ecdc4", "text": "#ffffff"}
    }
    
    color = colors.get(chart_type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color['bg']}22, {color['bg']}11);
        border: 2px dashed {color['bg']}44;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    ">
        <h4 style="
            font-family: 'Poppins', sans-serif;
            color: {color['bg']};
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
        ">{title}</h4>
        <p style="
            color: {color['bg']}aa;
            font-size: 0.9rem;
            margin: 0;
        ">{message}</p>
        <div style="
            font-size: 3rem;
            color: {color['bg']}44;
            margin-top: 15px;
        ">📊</div>
    </div>
    """, unsafe_allow_html=True)

def render_compact_basic_info_card(data):
    """Render a compact basic information card"""
    # Escape any special characters in data
    name = str(data.get('name', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    age = str(data.get('age', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    grade = str(data.get('grade_level', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    gvc_id = str(data.get('gvc_id', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    gpa = str(data.get('academic_gpa', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    contact_pref = str(data.get('contact_preference', 'N/A')).replace('"', '&quot;').replace("'", "&#39;")
    
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        ">
            <span style="
                font-size: 1.5rem;
                margin-right: 10px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">👤</span>
            <h4 style="
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 1rem;
                font-weight: 600;
                margin: 0;
            ">Profile Info</h4>
        </div>
        <div style="
            display: grid;
            gap: 8px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
        ">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">Name:</span>
                <span style="color: #374151; font-weight: 600;">{name}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">Age:</span>
                <span style="color: #374151; font-weight: 600;">{age}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">Grade:</span>
                <span style="color: #374151; font-weight: 600;">{grade}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">GPA:</span>
                <span style="color: #374151; font-weight: 600;">{gpa}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">Contact:</span>
                <span style="color: #374151; font-weight: 600;">{contact_pref}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-weight: 500;">ID:</span>
                <span style="color: #374151; font-weight: 600;">{gvc_id}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_compact_stats_card(data):
    """Render a compact statistics card with mini progress bars"""
    # Calculate stats with enhanced logic using new fields
    interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
    
    # Enhanced calculation using GPA and extracurricular data if available
    gpa = float(data.get('academic_gpa', 3.5)) if data.get('academic_gpa') else 3.5
    extracurricular = int(data.get('extracurricular_score', 80)) if data.get('extracurricular_score') else 80
    
    # Improved performance calculations
    motivation = min(100, int(60 + len(data.get('goals', '').split()) * 1.5 + (gpa - 3.0) * 10))
    potential = min(100, int(65 + (15 if data.get('strengths') else 0) + interests_count * 5 + (gpa - 3.0) * 8))
    engagement = min(100, int(50 + interests_count * 6 + (20 if data.get('challenges') else 0) + extracurricular * 0.3))
    
    # Header
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 15px;
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        ">
            <span style="
                font-size: 1.5rem;
                margin-right: 10px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">📈</span>
            <h4 style="
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 1rem;
                font-weight: 600;
                margin: 0;
            ">Performance</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bars using Streamlit components
    st.markdown("**Motivation**")
    st.progress(motivation / 100)
    st.markdown(f"<div style='text-align: right; margin-top: -20px; color: #667eea; font-weight: 600;'>{motivation}%</div>", unsafe_allow_html=True)
    
    st.markdown("**Potential**")
    st.progress(potential / 100)
    st.markdown(f"<div style='text-align: right; margin-top: -20px; color: #4ecdc4; font-weight: 600;'>{potential}%</div>", unsafe_allow_html=True)
    
    st.markdown("**Engagement**")
    st.progress(engagement / 100)
    st.markdown(f"<div style='text-align: right; margin-top: -20px; color: #f093fb; font-weight: 600;'>{engagement}%</div>", unsafe_allow_html=True)

def render_interests_goals_combined_card(data):
    """Render a combined interests and goals card"""
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        ">
            <span style="
                font-size: 1.8rem;
                margin-right: 12px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">🎯</span>
            <h4 style="
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0;
            ">Interests & Goals</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interests section using Streamlit components
    interests = data.get('interests', '')
    if interests:
        interest_list = [i.strip() for i in interests.split(',') if i.strip()]
        if interest_list:
            st.markdown("**🎨 Interests:**")
            
            # Display interests as columns of text with better formatting
            num_cols = min(len(interest_list), 3)
            cols = st.columns(num_cols)
            
            for i, interest in enumerate(interest_list):
                with cols[i % num_cols]:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
                        color: #667eea;
                        padding: 8px 12px;
                        border-radius: 20px;
                        font-size: 0.85rem;
                        font-weight: 500;
                        margin: 4px 0;
                        border: 1px solid rgba(102, 126, 234, 0.3);
                        font-family: 'Inter', sans-serif;
                        text-align: center;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    ">{interest}</div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Goals section
    goals = data.get('goals', '')
    if goals:
        st.markdown("**🎖️ Goals:**")
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            color: #374151;
            font-size: 0.9rem;
        ">
            {goals[:300]}{'...' if len(goals) > 300 else ''}
        </div>
        """, unsafe_allow_html=True)

def render_timeline_card(data):
    """Render a timeline-style card"""
    timeline_chart = create_goals_timeline(data)
    if timeline_chart:
        render_chart_container("📅 Goals Timeline", timeline_chart)
    else:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
            ">
                <span style="
                    font-size: 1.8rem;
                    margin-right: 12px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                ">📅</span>
                <h4 style="
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin: 0;
                ">Timeline Preview</h4>
            </div>
            
            <div style="
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
            ">
                <div style="
                    font-size: 2.5rem;
                    color: #667eea;
                    margin-bottom: 10px;
                ">📈</div>
                <p style="
                    color: #6b7280;
                    font-size: 0.9rem;
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                ">Add more detailed goals to see interactive timeline</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_wordcloud_container(word_cloud_img):
    """Render word cloud in a beautiful container"""
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    ">
        <h4 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
        ">☁️ Word Cloud Analysis</h4>
        <img src="data:image/png;base64,{word_cloud_img}" 
             style="width: 100%; max-width: 400px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
    </div>
    """, unsafe_allow_html=True)

def render_featured_fifa_card(data):
    """Render the FIFA card as a featured element"""
    st.markdown("""
    <div style="
        margin: 40px 0;
        text-align: center;
    ">
        <h3 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 25px;
        ">🎴 Student Profile Card</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the FIFA card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_compact_fifa_card(data)

def render_basic_info_card(data):
    """Render beautiful basic information card"""
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-header">
            <span class="card-icon">📋</span>
            <h3 class="card-title">Basic Information</h3>
        </div>
        <div style="margin-top: 20px;">
            <div class="info-row">
                <span class="info-label">Full Name</span>
                <span class="info-value">{data.get('name', 'N/A')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Age</span>
                <span class="info-value">{data.get('age', 'N/A')} years old</span>
            </div>
            <div class="info-row">
                <span class="info-label">Grade Level</span>
                <span class="info-value">{data.get('grade_level', 'N/A')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">GVC ID</span>
                <span class="info-value">{data.get('gvc_id', 'N/A')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Email</span>
                <span class="info-value">{data.get('email', 'Not provided')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_interests_card(data):
    """Render interests card with tags"""
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-header">
            <span class="card-icon">🎯</span>
            <h3 class="card-title">Interests & Passions</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    interests = data.get('interests', '')
    if interests:
        interest_list = [i.strip() for i in interests.split(',') if i.strip()]
        if interest_list:
            tags_html = "".join([f'<span class="tag">{interest}</span>' for interest in interest_list])
            st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(interests)
    else:
        st.info("No interests specified")

def render_goals_card(data):
    """Render beautiful goals card"""
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-header">
            <span class="card-icon">🎖️</span>
            <h3 class="card-title">Goals & Aspirations</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    goals = data.get('goals', '')
    if goals:
        # Display goals in a beautiful format
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #2d3748;
            margin-bottom: 16px;
        ">
            {goals}
        </div>
        """, unsafe_allow_html=True)
        
        words = len(goals.split())
        reading_time = max(1, words // 200)
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 0.9rem;
            color: #667eea;
            font-weight: 500;
        ">
            <span>📖 {words} words</span>
            <span>⏱️ ~{reading_time} min read</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No goals specified")

def render_stats_card(data):
    """Render statistics card with progress bars"""
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-header">
            <span class="card-icon">📊</span>
            <h3 class="card-title">Performance Stats</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate stats
    interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
    motivation = min(100, 60 + len(data.get('goals', '').split()) * 2)
    potential = min(100, 65 + (15 if data.get('strengths') else 0) + interests_count * 5)
    engagement = min(100, 50 + interests_count * 8 + (20 if data.get('challenges') else 0))
    
    # Render progress bars
    render_progress_bar("Motivation", motivation, "#dc2626")
    render_progress_bar("Potential", potential, "#059669")
    render_progress_bar("Engagement", engagement, "#7c3aed")

def render_progress_bar(label, value, color):
    """Render a progress bar"""
    st.markdown(f"""
    <div style="margin: 16px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-weight: 600;">{label}</span>
            <span style="color: {color}; font-weight: 600;">{value}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {value}%; background: {color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_compact_fifa_card(data):
    """Render a beautiful compact FIFA-style card - Simplified for reliability"""
    
    # Calculate rating
    def calculate_rating(data):
        base_score = 60
        if data.get('interests'):
            interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
            base_score += min(interests_count * 3, 15)
        goals = data.get('goals', '')
        if goals:
            words = len(goals.split())
            base_score += min(words // 2, 15)
        if data.get('strengths'):
            base_score += 10
        return min(base_score, 99)
    
    def get_position_title(data):
        interests = data.get('interests', '').lower()
        if any(word in interests for word in ['computer', 'programming', 'tech', 'software']):
            return 'TECH INNOVATOR'
        elif any(word in interests for word in ['science', 'research', 'physics', 'chemistry']):
            return 'RESEARCHER'
        elif any(word in interests for word in ['art', 'design', 'creative', 'music']):
            return 'CREATIVE'
        elif any(word in interests for word in ['business', 'entrepreneur', 'management']):
            return 'LEADER'
        elif any(word in interests for word in ['medicine', 'health', 'doctor']):
            return 'HEALER'
        else:
            return 'ALL-ROUNDER'
    
    overall_rating = calculate_rating(data)
    position = get_position_title(data)
    name = data.get('name', 'Student')
    age = data.get('age', 'N/A')
    grade = data.get('grade_level', 'N/A')
    
    # Beautiful FIFA Card with reliable rendering
    st.markdown("### 🎴 Student FIFA Card")
    
    # Create the FIFA card HTML with enhanced design
    card_html = f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            border-radius: 25px;
            padding: 35px 30px;
            text-align: center;
            margin: 20px auto;
            box-shadow: 
                0 25px 50px rgba(102, 126, 234, 0.4),
                0 8px 16px rgba(0, 0, 0, 0.2);
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            position: relative;
            max-width: 340px;
            height: 600px; /* Increased height */
            border: 2px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        ">
            <!-- Student Badge -->
            <div style="
                position: absolute;
                top: 18px;
                right: 18px;
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #333;
                padding: 8px 14px;
                border-radius: 20px;
                font-size: 10px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
            ">✨ STUDENT</div>
            
            <!-- Overall Rating -->
            <div style="
                font-size: 52px;
                font-weight: 900;
                color: #FFD700;
                margin: 20px 0 15px 0;
                text-shadow: 
                    0 4px 12px rgba(0, 0, 0, 0.5),
                    0 0 20px rgba(255, 215, 0, 0.3);
                filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
            ">{overall_rating}</div>
            
            <!-- Position Badge -->
            <div style="
                background: linear-gradient(45deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9));
                color: #FFD700;
                padding: 10px 18px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 25px;
                display: inline-block;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                box-shadow: inset 0 1px 3px rgba(255, 215, 0, 0.2);
            ">{position}</div>
            
            <!-- Avatar/Icon -->
            <div style="
                font-size: 55px;
                margin: 25px 0;
                filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.4));
                animation: float 3s ease-in-out infinite;
            ">🎓</div>
            
            <!-- Student Name -->
            <div style="
                font-size: 22px;
                font-weight: bold;
                margin: 20px 0 15px 0;
                text-shadow: 0 3px 8px rgba(0, 0, 0, 0.5);
                letter-spacing: 0.5px;
            ">{name}</div>
            
            <!-- Age and Grade Info -->
            <div style="
                font-size: 14px;
                opacity: 0.95;
                margin: 15px 0 25px 0;
                background: linear-gradient(45deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.1));
                padding: 8px 16px;
                border-radius: 15px;
                display: inline-block;
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(5px);
            ">📅 Age {age} • 🎯 Grade {grade}</div>
            
            <!-- Stats Section -->
            <div style="
                display: flex;
                justify-content: space-around;
                margin-top: 25px;
                padding-top: 20px;
                border-top: 2px solid rgba(255, 215, 0, 0.4);
                background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
            ">
                <div style="text-align: center; flex: 1;">
                    <div style="
                        font-size: 11px; 
                        color: #FFD700; 
                        font-weight: bold; 
                        margin-bottom: 6px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">INTERESTS</div>
                    <div style="
                        font-size: 20px; 
                        font-weight: bold;
                        color: #fff;
                        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    ">{len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])}</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="
                        font-size: 11px; 
                        color: #FFD700; 
                        font-weight: bold; 
                        margin-bottom: 6px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">POTENTIAL</div>
                    <div style="
                        font-size: 20px; 
                        font-weight: bold;
                        color: #fff;
                        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    ">{min(95, 75 + len(data.get('goals', '').split()) // 5)}</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="
                        font-size: 11px; 
                        color: #FFD700; 
                        font-weight: bold; 
                        margin-bottom: 6px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">GOALS</div>
                    <div style="
                        font-size: 20px; 
                        font-weight: bold;
                        color: #fff;
                        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    ">{len(data.get('goals', '').split())}</div>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-8px); }}
            }}
        </style>
        """
    
    # Create centered layout and render the card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Use streamlit components for reliable HTML rendering
        st.components.v1.html(card_html, height=750)  # Ensure height matches the card

def render_action_buttons(data):
    """Render beautiful action buttons section"""
    st.markdown("""
    <div style="
        margin: 48px 0 32px 0;
        text-align: center;
    ">
        <h3 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 32px;
        ">⚡ Next Steps</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start AI Roundtable", type="primary", use_container_width=True):
            st.session_state.current_page = 'roundtable'
            st.rerun()
    
    with col2:
        if st.button("← Back to Selection", use_container_width=True):
            st.session_state.current_page = 'data_input'
            st.rerun()
    
    with col3:
        # Export functionality
        export_data = {
            "student_profile": data,
            "export_timestamp": str(st.session_state.get('timestamp', 'unknown')),
            "gvc_id": st.session_state.get('selected_gvc_id', data.get('gvc_id', 'unknown'))
        }
        
        st.download_button(
            "📄 Export Profile",
            data=json.dumps(export_data, indent=2),
            file_name=f"profile_{data.get('gvc_id', 'student')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Enhanced additional sections
    render_enhanced_additional_sections(data)

def render_enhanced_additional_sections(data):
    """Render enhanced additional information in beautiful expandable sections"""
    
    st.markdown("""
    <div style="margin-top: 40px;">
        <h3 style="
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 24px;
            text-align: center;
        ">📂 Additional Details</h3>
    </div>
    """, unsafe_allow_html=True)

    
    # Strengths & Talents
    with st.expander("💪 Strengths & Talents", expanded=False):
        strengths = data.get('strengths', '')
        if strengths:
            strength_list = [s.strip() for s in strengths.split(',') if s.strip()]
            if strength_list:
                st.markdown("""
                <div style="
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 12px;
                    margin: 16px 0;
                ">
                """, unsafe_allow_html=True)
                
                for strength in strength_list:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(21, 128, 61, 0.1));
                        border: 1px solid rgba(34, 197, 94, 0.2);
                        border-radius: 12px;
                        padding: 12px 16px;
                        text-align: center;
                        color: #065f46;
                        font-weight: 600;
                        transition: all 0.3s ease;
                    ">
                        💪 {strength.title()}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(strengths)
        else:
            st.info("No strengths specified")
    
    # Challenges & Growth Areas
    with st.expander("🔄 Challenges & Growth Areas", expanded=False):
        challenges = data.get('challenges', '')
        if challenges:
            challenge_list = [c.strip() for c in challenges.split(',') if c.strip()]
            if challenge_list:
                for challenge in challenge_list:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(251, 146, 60, 0.1), rgba(234, 88, 12, 0.1));
                        border-left: 4px solid #ea580c;
                        padding: 12px 16px;
                        margin: 8px 0;
                        border-radius: 8px;
                        color: #9a3412;
                        font-weight: 500;
                    ">
                        🎯 {challenge}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(challenges)
        else:
            st.info("No challenges specified")
    
    # Additional Information
    additional_info = data.get('additional_info', '')
    if additional_info:
        with st.expander("📝 Additional Information", expanded=False):
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 20px;
                color: #3730a3;
                line-height: 1.6;
                font-family: 'Inter', sans-serif;
            ">
                {additional_info}
            </div>
            """, unsafe_allow_html=True)
    
    # Data Quality Check
    with st.expander("✅ Data Quality", expanded=False):
        required_fields = ['name', 'age', 'grade_level', 'interests', 'goals']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if missing_fields:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(185, 28, 28, 0.1));
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 12px;
                    padding: 16px;
                    color: #991b1b;
                ">
                    <strong>⚠️ Missing data:</strong><br>
                    {', '.join(missing_fields)}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(21, 128, 61, 0.1));
                    border: 1px solid rgba(34, 197, 94, 0.3);
                    border-radius: 12px;
                    padding: 16px;
                    color: #065f46;
                ">
                    <strong>✅ All required data present!</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            total_chars = sum(len(str(data.get(field, ''))) for field in data.keys())
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px;
                padding: 16px;
                color: #1e40af;
                text-align: center;
            ">
                <strong>📊 Profile completeness</strong><br>
                {total_chars} characters total
            </div>
            """, unsafe_allow_html=True)

def render_student_header(data):
    """Render student header with key information"""
    
    # Create header banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
    ">
        <h2 style="margin: 0; color: white;">👤 {data.get('name', 'Unknown Student')}</h2>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">
            {data.get('gvc_id', 'N/A')} • Age {data.get('age', 'N/A')} • {data.get('grade_level', 'N/A')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
        st.metric("Interest Areas", interests_count)
    
    with col2:
        goals_words = len(data.get('goals', '').split())
        st.metric("Goals Detail", f"{goals_words} words")
    
    with col3:
        strengths_count = len([s.strip() for s in data.get('strengths', '').split(',') if s.strip()])
        st.metric("Key Strengths", strengths_count)
    
    with col4:
        email_status = "✓ Available" if data.get('email') else "✗ Missing"
        st.metric("Contact Info", email_status)

def render_detailed_profile(data):
    """Render detailed student profile information"""
    
    # Basic Information
    with st.expander("📋 Basic Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Full Name:** {data.get('name', 'N/A')}")
            st.markdown(f"**Age:** {data.get('age', 'N/A')} years old")
            st.markdown(f"**Grade Level:** {data.get('grade_level', 'N/A')}")
        
        with col2:
            st.markdown(f"**GVC ID:** {data.get('gvc_id', 'N/A')}")
            st.markdown(f"**Email:** {data.get('email', 'Not provided')}")
    
    # Interests & Passions
    with st.expander("🎯 Interests & Passions", expanded=True):
        interests = data.get('interests', '')
        if interests:
            # Split and display as tags
            interest_list = [i.strip() for i in interests.split(',') if i.strip()]
            if interest_list:
                interest_tags = " ".join([f"`{interest}`" for interest in interest_list])
                st.markdown(f"**Interest Areas:** {interest_tags}")
            else:
                st.markdown(interests)
        else:
            st.info("No interests specified")
    
    # Goals & Aspirations
    with st.expander("🎖️ Goals & Aspirations", expanded=True):
        goals = data.get('goals', '')
        if goals:
            st.markdown(goals)
            
            # Word count and reading time
            words = len(goals.split())
            reading_time = max(1, words // 200)  # Assume 200 words per minute
            st.caption(f"📖 {words} words • ~{reading_time} min read")
        else:
            st.info("No goals specified")
    
    # Strengths & Talents
    with st.expander("💪 Strengths & Talents", expanded=True):
        strengths = data.get('strengths', '')
        if strengths:
            # Split and display as points
            strength_list = [s.strip() for s in strengths.split(',') if s.strip()]
            if strength_list:
                for strength in strength_list:
                    st.markdown(f"• **{strength.title()}**")
            else:
                st.markdown(strengths)
        else:
            st.info("No strengths specified")
    
    # Challenges & Growth Areas
    with st.expander("🔄 Challenges & Growth Areas", expanded=True):
        challenges = data.get('challenges', '')
        if challenges:
            # Split and display as points
            challenge_list = [c.strip() for c in challenges.split(',') if c.strip()]
            if challenge_list:
                for challenge in challenge_list:
                    st.markdown(f"• {challenge}")
            else:
                st.markdown(challenges)
        else:
            st.info("No challenges specified")
    
    # Additional Information
    additional_info = data.get('additional_info', '')
    if additional_info:
        with st.expander("📝 Additional Information", expanded=False):
            st.markdown(additional_info)

def render_fifa_card(data):
    """Render FIFA-style student card"""
    
    st.markdown("### 🎴 Student Card")
    
    # Calculate rating based on data completeness and content
    def calculate_rating(data):
        base_score = 60
        
        # Add points for interests
        if data.get('interests'):
            interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
            base_score += min(interests_count * 3, 15)
        
        # Add points for detailed goals
        goals = data.get('goals', '')
        if goals:
            words = len(goals.split())
            base_score += min(words // 2, 15)  # Up to 15 points for detailed goals
        
        # Add points for strengths
        if data.get('strengths'):
            base_score += 10
        
        return min(base_score, 99)
    
    # Calculate individual stats
    def get_position_title(data):
        interests = data.get('interests', '').lower()
        if any(word in interests for word in ['computer', 'programming', 'tech', 'software']):
            return 'TECH INNOVATOR'
        elif any(word in interests for word in ['science', 'research', 'physics', 'chemistry']):
            return 'RESEARCHER'
        elif any(word in interests for word in ['art', 'design', 'creative', 'music']):
            return 'CREATIVE'
        elif any(word in interests for word in ['business', 'entrepreneur', 'management']):
            return 'LEADER'
        elif any(word in interests for word in ['medicine', 'health', 'doctor']):
            return 'HEALER'
        else:
            return 'ALL-ROUNDER'
    
    # Get calculated values
    overall_rating = calculate_rating(data)
    position = get_position_title(data)
    
    interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
    motivation = min(90, 70 + len(data.get('goals', '').split()) * 2)
    potential = min(95, 75 + (10 if data.get('strengths') else 0) + interests_count * 3)
    
    # Escape HTML
    name = html.escape(str(data.get('name', 'Student')))
    age = html.escape(str(data.get('age', 'N/A')))
    grade = html.escape(str(data.get('grade_level', 'N/A')))
    
    # FIFA Card HTML
    fifa_card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                background: transparent;
                font-family: 'Arial', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 400px;
                padding: 20px;
            }}
            
            .fifa-card {{
                width: 300px;
                height: 450px;
                background: linear-gradient(145deg, #FFFFFF 0%, #FFFFFF 25%, #C0C0C0 50%, #808080 75%, #000000 100%);
                border-radius: 20px;
                position: relative;
                box-shadow: 
                    0 0 30px rgba(255, 215, 0, 0.6),
                    0 0 60px rgba(255, 140, 0, 0.4),
                    inset 0 0 30px rgba(255, 255, 255, 0.2);
                overflow: hidden;
                transition: all 0.4s ease;
                animation: glow 3s ease-in-out infinite alternate;
            }}
            
            .fifa-card:hover {{
                transform: scale(1.05);
                box-shadow: 
                    0 0 40px rgba(255, 215, 0, 0.8),
                    0 0 80px rgba(255, 140, 0, 0.6),
                    inset 0 0 40px rgba(255, 255, 255, 0.3);
            }}
            
            .card-header {{
                text-align: center;
                padding: 20px 15px 10px;
                position: relative;
                z-index: 2;
            }}
            
            .rating {{
                font-family: 'Orbitron', monospace;
                font-size: 3rem;
                font-weight: 900;
                color: #000000;
                text-shadow: 
                    0 4px 12px rgba(0, 0, 0, 0.5),
                    0 0 20px rgba(255, 215, 0, 0.3);
                margin: 0;
                line-height: 1;
            }}
            
            .position {{
                background: linear-gradient(135deg, #000000, #1a1a1a);
                color: #FFD700;
                padding: 6px 12px;
                border-radius: 15px;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 1px;
                margin-top: 8px;
                border: 2px solid #FFD700;
                text-transform: uppercase;
                display: inline-block;
            }}
            
            .photo {{
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: linear-gradient(135deg, #4A90E2, #7B68EE, #9370DB);
                margin: 15px auto;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                border: 3px solid rgba(255, 255, 255, 0.9);
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
                position: relative;
                z-index: 2;
                transition: all 0.3s ease;
            }}
            
            .photo:hover {{
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(255, 255, 255, 0.6);
            }}
            
            .name {{
                font-family: 'Orbitron', monospace;
                font-size: 1.1rem;
                font-weight: 700;
                color: #FFFFFF;
                text-align: center;
                margin: 10px 0 5px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                letter-spacing: 1px;
                text-transform: uppercase;
                line-height: 1.2;
            }}
            
            .details {{
                text-align: center;
                color: rgba(255, 255, 255, 0.95);
                font-size: 0.8rem;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .stats {{
                padding: 0 20px;
                position: relative;
                z-index: 2;
            }}
            
            .stat-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
                background: rgba(0, 0, 0, 0.4);
                padding: 8px 12px;
                border-radius: 6px;
                border-left: 3px solid #FFD700;
            }}
            
            .stat-label {{
                font-size: 0.7rem;
                font-weight: 700;
                color: #FFD700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .stat-value {{
                font-family: 'Orbitron', monospace;
                font-size: 0.9rem;
                font-weight: 700;
                color: #FFFFFF;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.6);
            }}
            
            .badge {{
                position: absolute;
                top: 15px;
                right: 15px;
                background: linear-gradient(135deg, #FF1493, #FF69B4);
                color: white;
                padding: 6px 10px;
                border-radius: 12px;
                font-size: 0.6rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                z-index: 3;
            }}
            
            .bottom {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 25px;
                background: linear-gradient(90deg, 
                    rgba(0, 0, 0, 0.9) 0%, 
                    rgba(255, 215, 0, 0.3) 50%, 
                    rgba(0, 0, 0, 0.9) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Orbitron', monospace;
                font-size: 0.6rem;
                color: #FFD700;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            
            @keyframes glow {{
                0% {{ 
                    box-shadow: 
                        0 0 30px rgba(255, 215, 0, 0.6),
                        0 0 60px rgba(255, 140, 0, 0.4),
                        inset 0 0 30px rgba(255, 255, 255, 0.2);
                }}
                100% {{ 
                    box-shadow: 
                        0 0 40px rgba(255, 215, 0, 0.8),
                        0 0 80px rgba(255, 140, 0, 0.6),
                        inset 0 0 40px rgba(255, 255, 255, 0.3);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="fifa-card">
            <div class="badge">STUDENT</div>
            
            <div class="card-header">
                <div class="rating">{overall_rating}</div>
                <div class="position">{position}</div>
            </div>
            
            <div class="photo">🎓</div>
            
            <div class="name">{name}</div>
            <div class="details">{age} years • {grade}</div>
            
            <div class="stats">
                <div class="stat-row">
                    <span class="stat-label">Motivation</span>
                    <span class="stat-value">{motivation}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Potential</span>
                    <span class="stat-value">{potential}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Interests</span>
                    <span class="stat-value">{interests_count}</span>
                </div>
            </div>
            
            <div class="bottom">ELITE EDITION</div>
        </div>
    </body>
    </html>
    """
    
    # Render the FIFA card
    components.html(fifa_card_html, height=500)

def render_profile_actions(data):
    """Render action buttons for the profile"""
    
    st.markdown("### ⚡ Actions")
    
    # Continue to roundtable
    if st.button("🚀 Start AI Roundtable", type="primary", use_container_width=True):
        st.session_state.current_page = 'roundtable'
        st.rerun()
    
    # Edit data (future functionality)
    if st.button("✏️ Edit Profile", use_container_width=True):
        st.info("Edit functionality coming soon!")
    
    # Export profile
    if st.button("📄 Export Profile", use_container_width=True):
        # Create downloadable JSON
        export_data = {
            "student_profile": data,
            "export_timestamp": st.session_state.get('timestamp', 'unknown'),
            "gvc_id": st.session_state.get('selected_gvc_id', data.get('gvc_id', 'unknown'))
        }
        
        st.download_button(
            "📥 Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"profile_{data.get('gvc_id', 'student')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Back to selection
    if st.button("← Back to Student Selection", use_container_width=True):
        st.session_state.current_page = 'data_input'
        st.rerun()
    
    # Data validation
    st.markdown("### ✅ Data Quality")
    
    # Check data completeness
    required_fields = ['name', 'age', 'grade_level', 'interests', 'goals']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        st.warning(f"Missing data: {', '.join(missing_fields)}")
    else:
        st.success("All required data present!")
    
    # Data stats
    total_chars = sum(len(str(data.get(field, ''))) for field in data.keys())
    st.info(f"Profile completeness: {total_chars} characters total")

# Complete visualization functions with improved color schemes
def create_interests_chart(data):
    """Create an interactive interests distribution chart with beautiful colors"""
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        
        interests = data.get('interests', '')
        if not interests:
            return None
            
        interest_list = [i.strip() for i in interests.split(',') if i.strip()]
        if len(interest_list) < 2:
            return None
        
        # Create a beautiful color palette
        colors = ['#667eea', '#764ba2', '#f093fb', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=interest_list,
            values=[1] * len(interest_list),  # Equal distribution
            hole=0.5,
            marker=dict(
                colors=colors[:len(interest_list)],
                line=dict(color='#ffffff', width=3)
            ),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=12, family='Inter', color='#374151'),
            hovertemplate='<b>%{label}</b><br>Interest Area<extra></extra>',
        )])
        
        fig.update_layout(
            title=dict(
                text='Interest Distribution',
                font=dict(size=16, family='Poppins', color='#374151'),
                x=0.5
            ),
            showlegend=False,
            margin=dict(t=60, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        
        return fig
        
    except ImportError:
        return None

def create_skills_radar_chart(data):
    """Create a skills radar chart with beautiful styling"""
    try:
        import plotly.graph_objects as go
        
        # Define skill categories based on interests and data
        interests = data.get('interests', '').lower()
        goals = data.get('goals', '').lower()
        strengths = data.get('strengths', '').lower()
        
        # Calculate skill scores based on content
        skills = {
            'Technical': 70 if any(word in interests + goals + strengths for word in ['tech', 'computer', 'programming', 'software']) else 45,
            'Creative': 80 if any(word in interests + goals + strengths for word in ['art', 'design', 'creative', 'music']) else 50,
            'Leadership': 65 if any(word in interests + goals + strengths for word in ['lead', 'manage', 'team', 'business']) else 40,
            'Communication': 75 if any(word in interests + goals + strengths for word in ['speak', 'present', 'write', 'communicate']) else 55,
            'Analytical': 60 if any(word in interests + goals + strengths for word in ['math', 'science', 'research', 'analyze']) else 50,
            'Social': 85 if any(word in interests + goals + strengths for word in ['social', 'help', 'volunteer', 'community']) else 60
        }
        
        categories = list(skills.keys())
        values = list(skills.values())
        
        fig = go.Figure()
        
        # Add the radar chart
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=3),
            marker=dict(color='#667eea', size=8),
            name='Skills Profile',
            hovertemplate='<b>%{theta}</b><br>Score: %{r}/100<extra></extra>'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10, color='#6b7280'),
                    gridcolor='rgba(102, 126, 234, 0.2)',
                    linecolor='rgba(102, 126, 234, 0.3)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, family='Inter', color='#374151'),
                    gridcolor='rgba(102, 126, 234, 0.2)',
                    linecolor='rgba(102, 126, 234, 0.3)'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            margin=dict(t=40, b=40, l=40, r=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        
        return fig
        
    except ImportError:
        return None

def create_performance_gauge(data):
    """Create a performance gauge chart"""
    try:
        import plotly.graph_objects as go
        
        # Calculate overall score
        score = 60  # Base score
        
        # Add points for various factors
        if data.get('interests'):
            interests_count = len([i.strip() for i in data.get('interests', '').split(',') if i.strip()])
            score += min(interests_count * 5, 20)
        
        if data.get('goals'):
            goals_words = len(data.get('goals', '').split())
            score += min(goals_words // 10, 15)
        
        if data.get('strengths'):
            score += 10
            
        if data.get('email'):
            score += 5
            
        score = min(score, 100)
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Profile Completeness Score", 'font': {'size': 16, 'family': 'Poppins', 'color': '#374151'}},
            delta = {'reference': 80, 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [None, 100], 'tickfont': {'size': 12, 'color': '#6b7280'}},
                'bar': {'color': "#667eea", 'thickness': 0.3},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(255, 107, 107, 0.3)"},
                    {'range': [50, 80], 'color': "rgba(255, 193, 7, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(76, 175, 80, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "#764ba2", 'width': 4},
                    'thickness': 0.8,
                    'value': 85
                }
            }
        ))
        
        fig.update_layout(
            margin=dict(t=60, b=20, l=40, r=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            font={'color': '#374151', 'family': 'Inter'}
        )
        
        return fig
        
    except ImportError:
        return None

def create_goals_timeline(data):
    """Create a goals timeline chart"""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        goals = data.get('goals', '')
        if not goals or len(goals.split()) < 10:
            return None
        
        # Extract timeline-related keywords
        timeline_keywords = {
            'Short-term (0-1 year)': ['immediate', 'soon', 'next year', 'this year', 'short', 'quickly'],
            'Medium-term (1-3 years)': ['college', 'university', 'degree', 'graduate', 'study'],
            'Long-term (3+ years)': ['career', 'future', 'eventually', 'long', 'lifetime', 'dream']
        }
        
        timeline_scores = {}
        goals_lower = goals.lower()
        
        for period, keywords in timeline_keywords.items():
            score = sum(1 for keyword in keywords if keyword in goals_lower)
            timeline_scores[period] = max(score, 1)  # Minimum 1 for visualization
        
        periods = list(timeline_scores.keys())
        scores = list(timeline_scores.values())
        colors = ['#667eea', '#764ba2', '#f093fb']
        
        fig = go.Figure()
        
        # Add timeline bars
        fig.add_trace(go.Bar(
            x=periods,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f'{score} goals' for score in scores],
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter'),
            hovertemplate='<b>%{x}</b><br>Focus Level: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text='Goals Timeline Focus',
                font=dict(size=16, family='Poppins', color='#374151'),
                x=0.5
            ),
            xaxis=dict(
                title=dict(
                    text='Time Period',
                    font=dict(size=12, family='Inter', color='#6b7280')
                ),
                tickfont=dict(size=11, color='#374151')
            ),
            yaxis=dict(
                title=dict(
                    text='Focus Level',
                    font=dict(size=12, family='Inter', color='#6b7280')
                ),
                tickfont=dict(size=11, color='#374151')
            ),
            margin=dict(t=60, b=60, l=60, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        
        return fig
        
    except ImportError:
        return None

def create_strengths_challenges_chart(data):
    """Create a strengths vs challenges comparison chart"""
    try:
        import plotly.graph_objects as go
        
        strengths = data.get('strengths', '')
        challenges = data.get('challenges', '')
        
        if not strengths and not challenges:
            return None
        
        # Count items
        strengths_list = [s.strip() for s in strengths.split(',') if s.strip()] if strengths else []
        challenges_list = [c.strip() for c in challenges.split(',') if c.strip()] if challenges else []
        
        if not strengths_list and not challenges_list:
            return None
        
        categories = ['Strengths', 'Growth Areas']
        values = [len(strengths_list), len(challenges_list)]
        colors = ['#4ecdc4', '#f093fb']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=values,
            textposition='auto',
            textfont=dict(color='white', size=14, family='Inter', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text='Personal Development Balance',
                font=dict(size=16, family='Poppins', color='#374151'),
                x=0.5
            ),
            xaxis=dict(
                tickfont=dict(size=12, color='#374151')
            ),
            yaxis=dict(
                title=dict(
                    text='Number of Items',
                    font=dict(size=12, family='Inter', color='#6b7280')
                ),
                tickfont=dict(size=11, color='#374151')
            ),
            margin=dict(t=60, b=40, l=60, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        
        return fig
        
    except ImportError:
        return None

def create_word_cloud(data):
    """Create a word cloud from goals and interests"""
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        import io
        import base64
        
        # Combine text from various fields
        text_parts = []
        if data.get('interests'):
            text_parts.append(data['interests'])
        if data.get('goals'):
            text_parts.append(data['goals'])
        if data.get('strengths'):
            text_parts.append(data['strengths'])
        
        text = ' '.join(text_parts)
        
        if len(text.split()) < 10:
            return None
        
        # Create word cloud with beautiful colors
        wordcloud = WordCloud(
            width=600,
            height=300,
            background_color='white',
            colormap='viridis',
            max_words=50,
            relative_scaling=0.5,
            font_path=None,
            prefer_horizontal=0.7
        ).generate(text)
        
        # Convert to image
        plt.figure(figsize=(10, 5), facecolor='white')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', 
                   facecolor='white', edgecolor='none', dpi=150)
        img_buffer.seek(0)
        
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
        
    except ImportError:
        return None
