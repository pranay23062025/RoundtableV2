import streamlit as st
import pandas as pd
from backend.data_manager import data_manager

def add_red_theme_styling():
    """Add targeted red theme styling ONLY for the dropdown menu"""
    st.markdown("""
    <style>
    /* ONLY target the selectbox dropdown - no other text changes */
    /* Make sure we don't override any global text colors */
    
    /* SELECTBOX DROPDOWN STYLING - RED THEME */
    div[data-testid="stSelectbox"] > div > div > div[data-baseweb="select"] {
        border: 2px solid rgba(220, 38, 38, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stSelectbox"] > div > div > div[data-baseweb="select"]:hover {
        border-color: rgba(220, 38, 38, 0.5) !important;
    }
    
    div[data-testid="stSelectbox"] > div > div > div[data-baseweb="select"]:focus-within {
        border-color: #dc2626 !important;
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
    }
    
    /* Dropdown menu styling - more specific targeting */
    div[data-testid="stSelectbox"] div[data-baseweb="popover"] {
        border: 1px solid rgba(220, 38, 38, 0.2) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.15) !important;
    }
    
    /* Dropdown options - only change hover and selected states, be very specific */
    div[data-testid="stSelectbox"] div[role="option"]:hover {
        background: rgba(220, 38, 38, 0.08) !important;
        color: #dc2626 !important;
    }
    
    div[data-testid="stSelectbox"] div[role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #dc2626, #991b1b) !important;
        color: white !important;
    }
    
    /* Keep search input subtle - target only the search input */
    div[data-testid="stTextInput"] input[placeholder*="search" i] {
        border: 1px solid rgba(220, 38, 38, 0.2) !important;
        border-radius: 6px !important;
    }
    
    div[data-testid="stTextInput"] input[placeholder*="search" i]:focus {
        border-color: #dc2626 !important;
        box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1) !important;
    }
    
    /* Ensure no global text color changes - explicitly preserve default colors */
    .stMarkdown, .stText, p, span, div:not([data-testid="stSelectbox"] div[role="option"]) {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_backend_stats():
    """Show backend statistics"""
    try:
        stats = data_manager.get_students_summary()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Students", stats['total_students'])
        
        with col2:
            avg_age = stats['avg_age']
            st.metric("Average Age", f"{avg_age:.1f}" if avg_age else "N/A")
        
        with col3:
            grade_dist = stats['grade_distribution']
            most_common = max(grade_dist.items(), key=lambda x: x[1]) if grade_dist else ("N/A", 0)
            st.metric("Most Common Grade", most_common[0])
        
        # Show recent students
        if stats['recent_students']:
            with st.expander("📋 Recent Students", expanded=False):
                for name in stats['recent_students']:
                    st.write(f"• {name}")
    
    except Exception as e:
        st.warning(f"Could not load backend statistics: {str(e)}")

def render_student_selector():
    """Main student selection interface"""
    
    st.markdown("### 🎯 Select Student")
    
    try:
        # Get all GVC IDs
        gvc_ids = data_manager.get_all_gvc_ids()
        
        if not gvc_ids:
            st.error("No students found in the database.")
            st.info("Please check that the CSV file exists and contains valid data.")
            return
        
        # Search functionality
        search_query = st.text_input("🔍 Search by name or GVC ID", placeholder="Type to search...")
        
        if search_query:
            # Filter students based on search
            filtered_students = data_manager.search_students(search_query)
            if not filtered_students.empty:
                display_options = []
                gvc_options = []
                
                for _, row in filtered_students.iterrows():
                    display_name = f"{row['gvc_id']} - {row['name']} (Age {row['age']}, {row['grade_level']})"
                    display_options.append(display_name)
                    gvc_options.append(row['gvc_id'])
                
                if display_options:
                    selected_index = st.selectbox(
                        "Select from search results:",
                        range(len(display_options)),
                        format_func=lambda x: display_options[x],
                        key="search_select"
                    )
                    selected_gvc_id = gvc_options[selected_index]
                else:
                    st.warning("No students found matching your search.")
                    return
            else:
                st.warning("No students found matching your search.")
                return
        else:
            # Show all students
            students_df = data_manager.load_students_data()
            
            if students_df.empty:
                st.error("No student data available.")
                return
            
            # Create display options
            display_options = []
            for _, row in students_df.iterrows():
                display_name = f"{row['gvc_id']} - {row['name']} (Age {row['age']}, {row['grade_level']})"
                display_options.append(display_name)
            
            selected_index = st.selectbox(
                "Choose a student:",
                range(len(display_options)),
                format_func=lambda x: display_options[x],
                help="Select a student to load their profile data"
            )
            
            selected_gvc_id = students_df.iloc[selected_index]['gvc_id']
        
        # Load and display selected student
        if st.button("📥 Load Student Data", type="primary", use_container_width=True):
            load_student_data(selected_gvc_id)
    
    except Exception as e:
        st.error(f"Error loading student data: {str(e)}")
        st.info("Please check your data file and try again.")
    
    # Show navigation buttons if student data is loaded (outside the try-except to always show)
    if st.session_state.get('student_data'):
        st.markdown("---")
        st.markdown("### 🚀 Student Loaded - Choose Next Step")
        
        data = st.session_state.student_data
        st.info(f"**Currently Selected:** {data['name']} ({data.get('gvc_id', 'Unknown ID')})")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Review Profile", type="secondary", use_container_width=True, key="persistent_review_profile"):
                st.session_state.current_page = 'data_showcase'
                st.rerun()
        
        with col2:
            if st.button("🚀 Start AI Roundtable", type="primary", use_container_width=True, key="persistent_start_roundtable"):
                st.session_state.current_page = 'roundtable'
                st.rerun()

def load_student_data(gvc_id: str):
    """Load student data from backend"""
    try:
        student_data = data_manager.get_student_by_gvc_id(gvc_id)
        
        if student_data:
            # Store in session state
            st.session_state.student_data = student_data
            st.session_state.selected_gvc_id = gvc_id
            
            # Show success message
            st.success(f"✅ Successfully loaded data for {student_data['name']} ({gvc_id})")
            
            # Show preview
            with st.expander("📋 Data Preview", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {student_data['name']}")
                    st.write(f"**Age:** {student_data['age']}")
                    st.write(f"**Grade:** {student_data['grade_level']}")
                
                with col2:
                    st.write(f"**GVC ID:** {student_data['gvc_id']}")
                    st.write(f"**Email:** {student_data.get('email', 'N/A')}")
                
                interests = student_data.get('interests', '')
                if interests:
                    st.write(f"**Interests:** {interests[:100]}{'...' if len(interests) > 100 else ''}")
                
        else:
            st.error(f"Student with GVC ID {gvc_id} not found.")
    
    except Exception as e:
        st.error(f"Error loading student {gvc_id}: {str(e)}")

def render_quick_actions():
    """Quick actions sidebar"""
    
    st.markdown("### ⚡ Quick Actions")
    
    # Refresh data
    if st.button("🔄 Refresh Data", use_container_width=True):
        data_manager.load_students_data.clear()
        st.success("Data refreshed!")
        st.rerun()
    
    # Clear current selection
    if st.session_state.get('student_data'):
        if st.button("🗑️ Clear Selection", use_container_width=True):
            if 'student_data' in st.session_state:
                del st.session_state.student_data
            if 'selected_gvc_id' in st.session_state:
                del st.session_state.selected_gvc_id
            st.success("Selection cleared!")
            st.rerun()
    
    # Show current selection
    if st.session_state.get('student_data'):
        st.markdown("### 👤 Current Selection")
        data = st.session_state.student_data
        st.info(f"**{data['name']}**\\n{data['gvc_id']} • {data['grade_level']}")
    
    # Data management
    with st.expander("🛠️ Data Management", expanded=False):
        st.markdown("#### Add New Student")
        if st.button("➕ Add Student", use_container_width=True):
            st.info("Add new student functionality can be implemented here")
        
        st.markdown("#### Export Data")
        if st.button("📤 Export CSV", use_container_width=True):
            try:
                df = data_manager.load_students_data()
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "students_export.csv",
                    "text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    # Database info
    with st.expander("ℹ️ Database Info", expanded=False):
        st.write(f"**Data Source:** {data_manager.csv_path}")
        
        try:
            df = data_manager.load_students_data()
            st.write(f"**Records:** {len(df)}")
            st.write(f"**Columns:** {len(df.columns)}")
            
            if not df.empty:
                st.write("**Available Fields:**")
                for col in df.columns:
                    st.write(f"• {col}")
        except Exception as e:
            st.write(f"Error reading database: {str(e)}")

def render_manual_input_option():
    """Option to manually input data (legacy functionality)"""
    
    st.markdown("---")
    st.markdown("### 📝 Manual Data Entry")
    st.info("You can also manually enter student data if they're not in the database.")
    
    if st.button("✏️ Switch to Manual Entry", use_container_width=True):
        st.session_state.manual_entry_mode = True
        st.rerun()
    
    # Manual entry form (if enabled)
    if st.session_state.get('manual_entry_mode'):
        render_manual_entry_form()

def render_manual_entry_form():
    """Manual entry form for new students"""
    
    st.markdown("#### Manual Student Data Entry")
    
    with st.form("manual_student_entry"):
        col1, col2 = st.columns(2)
        
        with col1:
            gvc_id = st.text_input("GVC ID*", placeholder="GVC###", help="Format: GVC001")
            name = st.text_input("Full Name*", placeholder="Enter student's full name")
            age = st.number_input("Age*", min_value=5, max_value=25, value=16)
            grade_level = st.selectbox("Grade Level*", 
                ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"])
        
        with col2:
            email = st.text_input("Email", placeholder="student@school.edu")
            interests = st.text_area("Interests", placeholder="List the student's interests...")
            goals = st.text_area("Goals", placeholder="What are the student's goals?")
        
        strengths = st.text_area("Strengths", placeholder="What are the student's strengths?")
        challenges = st.text_area("Challenges", placeholder="What challenges does the student face?")
        additional_info = st.text_area("Additional Information", placeholder="Any other relevant information...")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("💾 Save Student", type="primary")
        
        with col2:
            if st.form_submit_button("📋 Use This Data"):
                # Use the manually entered data
                manual_data = {
                    'gvc_id': gvc_id,
                    'name': name,
                    'age': age,
                    'grade_level': grade_level,
                    'email': email,
                    'interests': interests,
                    'goals': goals,
                    'strengths': strengths,
                    'challenges': challenges,
                    'additional_info': additional_info
                }
                
                st.session_state.student_data = manual_data
                st.session_state.manual_entry_mode = False
                st.success(f"Using manual data for {name}")
                
                # Provide options for next step
                st.markdown("**Choose next step:**")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📊 Review Profile", key="manual_review"):
                        st.session_state.current_page = 'data_showcase'
                        st.rerun()
                with col_b:
                    if st.button("🚀 Start Roundtable", key="manual_roundtable"):
                        st.session_state.current_page = 'roundtable'
                        st.rerun()
        
        with col3:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.manual_entry_mode = False
                st.rerun()
        
        if submitted:
            # Save to database
            manual_data = {
                'gvc_id': gvc_id,
                'name': name,
                'age': age,
                'grade_level': grade_level,
                'email': email,
                'interests': interests,
                'goals': goals,
                'strengths': strengths,
                'challenges': challenges,
                'additional_info': additional_info
            }
            
            if data_manager.add_student(manual_data):
                st.session_state.student_data = manual_data
                st.session_state.manual_entry_mode = False
                st.rerun()

# Add manual input option to the main page
def render_data_input_page_with_options():
    """Enhanced data input page with both backend and manual options"""
    
    # Apply red theme styling first
    add_red_theme_styling()
    
    st.markdown('<h1 class="main-title">📝 Student Selection</h1>', unsafe_allow_html=True)
    st.info("💡 **New Streamlined Flow**: After selecting a student, you can go directly to the AI Roundtable or optionally review the profile first.")
    st.markdown("Select a student by their GVC ID to load their profile data.")
    
    # Backend statistics
    render_backend_stats()
    
    # Main selection area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_student_selector()
    
    with col2:
        render_quick_actions()
    
    # Manual entry option
    render_manual_input_option()

# Export the enhanced function
render_data_input_page = render_data_input_page_with_options
