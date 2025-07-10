import streamlit as st
import json
from datetime import datetime
import os

def render_sidebar():
    """Render the sidebar with beautiful student information display"""
    # Display current time and user info
    st.sidebar.info(f"👤 User: {os.getenv('USER', 'Anonymous')}")
    
    # Add separator
    st.sidebar.markdown("---")
    
    with st.sidebar:
        # Display beautiful student profile if available
        if hasattr(st.session_state, 'student_data') and st.session_state.student_data:
            _render_beautiful_student_profile()
        else:
            # Show message when no student data is available
            st.info("📚 No student profile loaded. Please load student data from the main page.")
        
        # Session controls
        _render_session_controls()

def _render_beautiful_student_profile():
    """Render beautiful student profile in sidebar using Streamlit components"""
    
    # Get student data from session state
    student_data = st.session_state.student_data
    
    # Extract data with flexible field names
    name = _get_field_value(student_data, ['name', 'student_name'], 'Unknown Student')
    age = _get_field_value(student_data, ['age'], 'N/A')
    grade = _get_field_value(student_data, ['grade', 'grade_level'], 'N/A')
    gvc_id = _get_field_value(student_data, ['gvc_id', 'id'], 'N/A')
    email = _get_field_value(student_data, ['email'], 'Not provided')
    interests = _get_field_value(student_data, ['interests', 'hobbies'], '')
    goals = _get_field_value(student_data, ['goals', 'short_term_goals', 'career_interest'], '')
    strengths = _get_field_value(student_data, ['strengths'], '')
    challenges = _get_field_value(student_data, ['challenges'], '')
    
    # Handle nested data structures
    if isinstance(student_data, dict):
        personal_info = student_data.get('personal_info', {})
        if personal_info:
            name = personal_info.get('name', name)
            age = personal_info.get('age', age)
            grade = personal_info.get('grade', grade)
        
        goals_info = student_data.get('goals', {})
        if isinstance(goals_info, dict):
            career_interest = goals_info.get('career_interest', '')
            short_term = goals_info.get('short_term', '')
            if career_interest or short_term:
                goals = f"{career_interest} {short_term}".strip()
    
    # Format interests/hobbies
    if isinstance(interests, list):
        interests = ', '.join(interests)
    
    # Create beautiful profile using Streamlit components
    st.markdown("### 🎓 Student Profile")
    
    # Profile header with colored background
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 15px;
        ">
            <h3 style="margin: 0; color: white;">{name}</h3>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">ID: {gvc_id} • Age {age} • {grade}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Contact information
    with st.container():
        st.markdown("**📧 Contact**")
        st.write(email)
    
    st.markdown("---")
    
    # Interests
    with st.container():
        st.markdown("**🎯 Interests**")
        if interests:
            # Split interests and show as tags
            if isinstance(interests, str):
                interest_list = [i.strip() for i in interests.split(',') if i.strip()]
            else:
                interest_list = interests if isinstance(interests, list) else [str(interests)]
            
            if interest_list:
                # Create a simple tag display
                interest_text = " • ".join(interest_list[:3])
                if len(interest_list) > 3:
                    interest_text += f" + {len(interest_list) - 3} more"
                st.write(interest_text)
            else:
                st.write("No interests specified")
        else:
            st.write("No interests specified")
    
    st.markdown("---")
    
    # Goals
    with st.container():
        st.markdown("**🎖️ Goals**")
        if goals:
            st.write(_truncate_sidebar_text(goals, 80))
        else:
            st.write("No goals specified")
    
    st.markdown("---")
    
    # Strengths
    with st.container():
        st.markdown("**💪 Strengths**")
        if strengths:
            strengths_text = _format_simple_list(strengths)
            st.write(strengths_text)
        else:
            st.write("No strengths specified")
    
    st.markdown("---")
    
    # Challenges
    with st.container():
        st.markdown("**🔄 Challenges**")
        if challenges:
            challenges_text = _format_simple_list(challenges)
            st.write(challenges_text)
        else:
            st.write("No challenges specified")

def _get_field_value(data, field_names, default=''):
    """Get field value from data using multiple possible field names"""
    if not isinstance(data, dict):
        return default
    
    for field_name in field_names:
        if field_name in data and data[field_name]:
            return data[field_name]
    
    return default

def _format_sidebar_interests(interests):
    """Format interests as simple text for sidebar"""
    if not interests:
        return "No interests specified"
    
    if isinstance(interests, list):
        interest_list = interests
    else:
        interest_list = [i.strip() for i in str(interests).split(',') if i.strip()]
    
    if not interest_list:
        return str(interests) if interests else "No interests specified"
    
    # Simple text format for interests
    return " • ".join(interest_list[:3]) + (f" + {len(interest_list) - 3} more" if len(interest_list) > 3 else "")

def _format_simple_list(items):
    """Format items as simple text with bullet points for sidebar"""
    if not items:
        return "None specified"
    
    if isinstance(items, list):
        item_list = items
    else:
        item_list = [i.strip() for i in str(items).split(',') if i.strip()]
    
    if not item_list:
        return str(items) if items else "None specified"
    
    if len(item_list) == 1:
        return item_list[0]
    
    # Show first 2 items with "..." if more
    if len(item_list) > 2:
        return f"• {item_list[0]}\n• {item_list[1]}\n• ... and {len(item_list) - 2} more"
    else:
        return "\n".join([f"• {item}" for item in item_list])

def _format_sidebar_list(items):
    """Format comma-separated items with bullet points for sidebar"""
    if not items:
        return "None specified"
    
    if isinstance(items, list):
        item_list = items
    else:
        item_list = [i.strip() for i in str(items).split(',') if i.strip()]
    
    if not item_list:
        return str(items) if items else "None specified"
    
    if len(item_list) == 1:
        return item_list[0]
    
    # Show first 2 items with "..." if more
    if len(item_list) > 2:
        formatted = '<br>'.join([f'• {item}' for item in item_list[:2]])
        formatted += f'<br>• ... and {len(item_list) - 2} more'
    else:
        formatted = '<br>'.join([f'• {item}' for item in item_list])
    
    return formatted

def _truncate_sidebar_text(text, max_length):
    """Truncate text to specified length for sidebar"""
    if not text or len(str(text)) <= max_length:
        return str(text) if text else ""
    
    return str(text)[:max_length] + "..."

def _render_session_controls():
    """Render minimal session state controls"""
    st.markdown("---")
    
    if st.button("🔄 Reset Session", key="reset_session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    if hasattr(st.session_state, 'student_data') and st.session_state.student_data:
        if st.button("💾 Export Profile", key="export_session"):
            try:
                # Convert student data for JSON serialization
                def convert_types(obj):
                    if hasattr(obj, 'item'):  # numpy scalar
                        return obj.item()
                    elif isinstance(obj, dict):
                        return {k: convert_types(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_types(item) for item in obj]
                    else:
                        return obj
                
                clean_student_data = convert_types(st.session_state.student_data)
                student_json = json.dumps(clean_student_data, indent=2)
                
                st.download_button(
                    label="📁 Download Profile Data",
                    data=student_json,
                    file_name=f"student_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error exporting profile: {str(e)}")

def get_student_context_summary():
    """Get a formatted summary of student data for AI context"""
    if not hasattr(st.session_state, 'student_data') or not st.session_state.student_data:
        return "No student information available."
    
    data = st.session_state.student_data
    
    # Extract basic info
    name = _get_field_value(data, ['name', 'student_name'], 'Unknown')
    age = _get_field_value(data, ['age'], 'N/A')
    grade = _get_field_value(data, ['grade', 'grade_level'], 'N/A')
    
    summary = f"""
STUDENT PROFILE:
Name: {name}
Age: {age}
Grade: {grade}
"""
    
    # Add interests/hobbies
    interests = _get_field_value(data, ['interests', 'hobbies'], '')
    if interests:
        if isinstance(interests, list):
            interests = ', '.join(interests)
        summary += f"\nHOBBIES & INTERESTS: {interests}"
    
    # Add goals
    goals = _get_field_value(data, ['goals', 'career_interest', 'short_term_goals'], '')
    if goals:
        summary += f"\nGOALS: {goals}"
    
    # Add challenges and strengths
    challenges = _get_field_value(data, ['challenges'], '')
    if challenges:
        summary += f"\nCHALLENGES: {challenges}"
    
    strengths = _get_field_value(data, ['strengths'], '')
    if strengths:
        summary += f"\nSTRENGTHS: {strengths}"
    
    return summary