import streamlit as st
import pandas as pd
from datetime import datetime

def render_data_input_page():
    """Page 1: Data Input"""
    
    # Enhanced CSS styles for minimalist academic design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main page styling */
    .main-title {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 3rem 0;
        animation: fadeInUp 0.8s ease-out;
        font-family: 'Inter', sans-serif;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(245,245,220,0.7) 100%);
        border: 2px solid rgba(220, 38, 38, 0.2);
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #dc2626;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(145deg, #dc2626, #991b1b);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #dc2626, #991b1b) !important;
        color: white !important;
        border-color: #dc2626 !important;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4) !important;
    }
    
    /* Section cards */
    .section-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(245,245,220,0.9) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid rgba(75, 85, 99, 0.15);
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        backdrop-filter: blur(10px);
        animation: slideInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .section-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #dc2626, #991b1b, #7f1d1d);
    }
    
    /* Form styling */
    .stForm {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    /* Input field enhancements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border: 2px solid rgba(75, 85, 99, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.9) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #dc2626 !important;
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dc2626, #991b1b) !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(145deg, rgba(75, 85, 99, 0.1), rgba(55, 65, 81, 0.1)) !important;
        border: 1px solid rgba(75, 85, 99, 0.2) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
    }
    
    /* Success/Error styling */
    .stSuccess {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.1), rgba(22, 163, 74, 0.1)) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 15px !important;
    }
    
    .stError {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1)) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Section headers */
    .section-header {
        color: #dc2626;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #dc2626, #991b1b);
        border-radius: 2px;
    }
    
    .subsection-header {
        color: #374151;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    }
    
    /* Download button special styling */
    .download-section {
        background: linear-gradient(145deg, rgba(245,245,220, 0.4), rgba(229,229,229, 0.3));
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(75, 85, 99, 0.2);
        margin: 2rem 0;
    }
    
    /* Code element styling fix */
    code {
        background: rgba(255,255,255,0.9) !important;
        color: #dc2626 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        border: 1px solid rgba(220, 38, 38, 0.2) !important;
    }
    
    /* Text color fixes */
    p, li, span {
        color: #374151 !important;
    }
    
    strong {
        color: #1f2937 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">📝 Student Data Input</h1>', unsafe_allow_html=True)
    
    # Enhanced tabs with better styling
    tab1, tab2 = st.tabs(["📊 Upload CSV", "✏️ Manual Entry"])
    
    with tab1:
        render_csv_upload_section()
    
    with tab2:
        render_manual_entry_section()

def render_csv_upload_section():
    """Handle CSV file upload"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 Upload Student Data</h2>', unsafe_allow_html=True)
    
    # Enhanced instructions with better formatting
    st.markdown("""
    <div style="background: linear-gradient(145deg, rgba(75, 85, 99, 0.05), rgba(55, 65, 81, 0.05)); 
                padding: 1.5rem; border-radius: 15px; border-left: 4px solid #dc2626; margin: 1.5rem 0;">
        <h4 style="color: #dc2626; margin-top: 0; font-size: 1.1rem;">📋 CSV File Requirements</h4>
        <p style="margin-bottom: 0.5rem; color: #374151;"><strong>Required columns:</strong></p>
        <ul style="margin: 0.5rem 0; color: #374151;">
            <li><code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">name</code> - Student's full name</li>
            <li><code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">age</code> - Student's current age</li>
            <li><code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">grade_level</code> - Academic level (e.g., "11th Grade")</li>
            <li><code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">interests</code> - Academic interests and subjects</li>
            <li><code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">goals</code> - Career goals and future aspirations</li>
        </ul>
        <p style="margin-bottom: 0; color: #374151;"><strong>Optional:</strong> 
        <code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">challenges</code>, 
        <code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">strengths</code>, 
        <code style="background: rgba(255,255,255,0.8); color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 500;">email</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Show preview with enhanced styling
            st.markdown('<h3 class="subsection-header">📊 Data Preview</h3>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            
            # Validate required columns
            required_columns = ['name', 'age', 'grade_level', 'interests', 'goals']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                st.info("💡 Please ensure your CSV has: name, age, grade_level, interests, goals")
            else:
                st.success(f"✅ Successfully loaded {len(df)} student record(s)!")
                
                if len(df) > 1:
                    st.info("📌 Multiple students found. Using the first student's data.")
                
                # Import button with enhanced styling
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
                    if st.button("📥 Import This Data", type="primary", use_container_width=True):
                        # Take first row as student data
                        student_data = df.iloc[0].to_dict()
                        # Clean up any NaN values
                        student_data = {k: (v if pd.notna(v) else '') for k, v in student_data.items()}
                        
                        st.session_state.student_data = student_data
                        st.success("✅ Data imported successfully! Redirecting to profile showcase...")
                        
                        # Auto-advance to showcase page
                        st.session_state.current_page = 'data_showcase'
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
            st.info("💡 Please check your CSV file format and try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download sample template
    render_csv_template_section()

def render_csv_template_section():
    """Provide sample CSV template"""
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📥 Download Template</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: #dc2626; margin-bottom: 1rem;">📄 Get Started Quickly</h4>
            <p style="margin-bottom: 1.5rem; color: #374151;">Download our sample CSV template with example data to get started immediately.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create sample data
        sample_data = {
            'name': ['Alex Johnson', 'Maya Patel'],
            'age': [16, 17],
            'grade_level': ['11th Grade', '12th Grade'],
            'interests': ['Computer Science, Mathematics', 'Biology, Chemistry'],
            'goals': ['Software Engineer', 'Medical Doctor'],
            'challenges': ['Advanced Calculus', 'Time Management']
        }
        sample_df = pd.DataFrame(sample_data)
        csv_data = sample_df.to_csv(index=False)
        
        st.download_button(
            label="📄 Download Sample CSV",
            data=csv_data,
            file_name=f"student_data_template_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.markdown('<h4 style="color: #dc2626; margin-bottom: 1rem; text-align: center;">📊 Preview</h4>', unsafe_allow_html=True)
        st.dataframe(sample_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_manual_entry_section():
    """Handle manual data entry"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">✏️ Manual Entry</h2>', unsafe_allow_html=True)
    
    with st.form("student_form", clear_on_submit=False):
        # Basic Information with enhanced styling
        st.markdown('<h3 class="subsection-header">👤 Basic Information</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name *", 
                placeholder="e.g., Alex Johnson",
                help="Enter the student's complete name"
            )
            age = st.number_input(
                "Age *", 
                min_value=10, 
                max_value=30, 
                value=16,
                help="Student's current age"
            )
        
        with col2:
            grade = st.selectbox(
                "Grade Level *", 
                [
                    "9th Grade", "10th Grade", "11th Grade", "12th Grade",
                    "College Freshman", "College Sophomore", 
                    "College Junior", "College Senior",
                    "Graduate Student"
                ],
                help="Select current academic level"
            )
            email = st.text_input(
                "Email (Optional)", 
                placeholder="student@example.com",
                help="Optional: For future communication"
            )
        
        # Academic Information with enhanced styling
        st.markdown('<h3 class="subsection-header">📚 Academic Information</h3>', unsafe_allow_html=True)
        
        interests = st.text_area(
            "Academic Interests & Subjects *",
            placeholder="e.g., Mathematics, Computer Science, Creative Writing, Biology...",
            help="List subjects or fields the student is passionate about",
            height=100
        )
        
        goals = st.text_area(
            "Career Goals & Future Aspirations *",
            placeholder="e.g., Become a software engineer, Study medicine, Start own business...",
            help="Describe what the student wants to achieve in their career",
            height=100
        )
        
        # Optional Information with enhanced styling
        st.markdown('<h3 class="subsection-header">💪 Additional Information <span style="font-size: 0.8em; color: #888;">(Optional)</span></h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            strengths = st.text_area(
                "Key Strengths & Skills",
                placeholder="e.g., Problem-solving, Leadership, Creative thinking...",
                help="What does the student excel at?",
                height=80
            )
        
        with col2:
            challenges = st.text_area(
                "Areas for Improvement",
                placeholder="e.g., Time management, Public speaking, Advanced math...",
                help="What areas need development?",
                height=80
            )
        
        additional_info = st.text_area(
            "Extra Information",
            placeholder="e.g., Extracurricular activities, hobbies, special circumstances...",
            help="Any other relevant information for the AI mentors",
            height=70  # FIXED: Changed from 60 to 70 (minimum is 68)
        )
        
        # Submit section with enhanced styling
        st.markdown("""
        <div style="border-top: 2px solid rgba(75, 85, 99, 0.1); 
                    margin: 3rem 0 2rem 0; padding-top: 2rem;">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submitted = st.form_submit_button(
                "💾 Save Student Profile", 
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            # Validation
            if not name or not interests or not goals:
                st.error("❌ **Please fill in all required fields** (marked with *)")
            else:
                # Create student data object
                student_data = {
                    'name': name.strip(),
                    'age': int(age),
                    'grade_level': grade,
                    'email': email.strip() if email else '',
                    'interests': interests.strip(),
                    'goals': goals.strip(),
                    'strengths': strengths.strip(),
                    'challenges': challenges.strip(),
                    'additional_info': additional_info.strip(),
                    'created_at': datetime.now().isoformat(),
                    'input_method': 'manual'
                }
                
                # Store in session state
                st.session_state.student_data = student_data
                st.success("✅ **Student profile saved successfully!** Redirecting to profile showcase...")
                
                # Auto-advance to showcase page
                st.session_state.current_page = 'data_showcase'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)