# Sample Dashboard Enhancements for Additional Student Fields
# Add these functions to your data_showcase_enhanced.py

def render_enhanced_academic_section(data):
    """Enhanced academic performance visualization"""
    st.markdown("### 📊 Academic Performance Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # GPA Trend Chart
        gpa_history = data.get('gpa_history', [])
        if gpa_history:
            fig = px.line(
                x=range(len(gpa_history)), 
                y=gpa_history,
                title="GPA Trend",
                labels={'x': 'Semester', 'y': 'GPA'}
            )
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Subject Performance Radar
        subjects = data.get('current_courses', [])
        if subjects:
            subject_scores = [data.get(f'{subj.lower()}_grade', 85) for subj in subjects[:6]]
            fig = go.Figure(data=go.Scatterpolar(
                r=subject_scores,
                theta=subjects[:6],
                fill='toself',
                name='Performance'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Subject Performance",
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Study Habits Metrics
        study_hours = data.get('study_hours_per_week', 0)
        homework_rate = data.get('homework_completion_rate', 0)
        
        st.metric("Study Hours/Week", f"{study_hours}h")
        st.metric("Homework Completion", f"{homework_rate}%")
        st.metric("Learning Style", data.get('learning_style', 'Mixed'))

def render_career_readiness_section(data):
    """Career readiness and future planning visualization"""
    st.markdown("### 🎯 Career Readiness Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Career Interest Distribution
        career_interests = data.get('career_interests', [])
        if career_interests:
            fig = px.pie(
                values=[1] * len(career_interests),
                names=career_interests,
                title="Career Interest Areas"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Work Experience Timeline
        work_exp = data.get('work_experience', [])
        if work_exp:
            st.markdown("**Work Experience:**")
            for exp in work_exp:
                st.write(f"• {exp}")
    
    with col2:
        # Career Readiness Score
        readiness_score = calculate_career_readiness(data)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = readiness_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Career Readiness Score"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def render_wellbeing_dashboard(data):
    """Student wellbeing and personal development metrics"""
    st.markdown("### 🧘 Wellbeing & Personal Development")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stress_level = data.get('stress_level', 5)
        stress_color = "red" if stress_level > 7 else "yellow" if stress_level > 4 else "green"
        st.metric("Stress Level", f"{stress_level}/10", delta=None)
        st.markdown(f"<div style='width:100%; height:10px; background-color:{stress_color}; border-radius:5px;'></div>", unsafe_allow_html=True)
    
    with col2:
        sleep_hours = data.get('sleep_hours_average', 8)
        sleep_quality = "Good" if sleep_hours >= 7 else "Needs Improvement"
        st.metric("Sleep Hours", f"{sleep_hours}h", delta=None)
        st.write(sleep_quality)
    
    with col3:
        activity_level = data.get('physical_activity_level', 'Medium')
        st.metric("Activity Level", activity_level)
        
    with col4:
        balance_rating = data.get('work_life_balance_rating', 5)
        st.metric("Work-Life Balance", f"{balance_rating}/10")

def render_skills_matrix(data):
    """Technical and soft skills visualization"""
    st.markdown("### 💻 Skills & Competencies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Technical Skills**")
        tech_skills = {
            'Programming': len(data.get('programming_experience', [])) * 20,
            'Software': len(data.get('software_skills', [])) * 15,
            'Digital Literacy': {'Beginner': 25, 'Intermediate': 50, 'Advanced': 75, 'Expert': 100}.get(data.get('digital_literacy_level', 'Intermediate'), 50)
        }
        
        fig = px.bar(
            x=list(tech_skills.keys()),
            y=list(tech_skills.values()),
            title="Technical Skills Assessment"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Soft Skills**")
        soft_skills = data.get('emotional_intelligence_areas', [])
        if soft_skills:
            skills_scores = {skill: np.random.randint(60, 95) for skill in soft_skills}
            fig = px.bar(
                x=list(skills_scores.values()),
                y=list(skills_scores.keys()),
                orientation='h',
                title="Emotional Intelligence Areas"
            )
            st.plotly_chart(fig, use_container_width=True)

def calculate_career_readiness(data):
    """Calculate career readiness score based on multiple factors"""
    score = 0
    
    # Work experience (0-25 points)
    work_exp = len(data.get('work_experience', []))
    score += min(25, work_exp * 8)
    
    # Leadership experience (0-20 points)
    leadership = len(data.get('leadership_experience', []))
    score += min(20, leadership * 7)
    
    # Clear career interests (0-15 points)
    career_clarity = len(data.get('career_interests', []))
    score += min(15, career_clarity * 5)
    
    # Academic performance (0-20 points)
    gpa = float(data.get('academic_gpa', 3.0))
    score += (gpa / 4.0) * 20
    
    # Goal clarity (0-20 points)
    has_goals = bool(data.get('short_term_goals')) and bool(data.get('long_term_goals'))
    score += 20 if has_goals else 10
    
    return min(100, score)

# Enhanced Data Collection Form
def render_enhanced_data_collection():
    """Enhanced student data collection form"""
    st.markdown("### 📝 Comprehensive Student Profile")
    
    with st.form("enhanced_student_form"):
        # Basic Information
        st.markdown("#### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=12, max_value=25)
            grade_level = st.selectbox("Grade Level", ["9th", "10th", "11th", "12th", "College Freshman", "College Sophomore", "College Junior", "College Senior"])
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone (optional)")
            gvc_id = st.text_input("GVC ID")
        
        # Academic Information
        st.markdown("#### Academic Profile")
        col1, col2, col3 = st.columns(3)
        with col1:
            current_courses = st.multiselect("Current Courses", ["Math", "Science", "English", "History", "Arts", "Languages", "PE", "Technology", "Business", "Computer Science"])
            favorite_subjects = st.multiselect("Favorite Subjects (Top 3)", ["Math", "Science", "English", "History", "Arts", "Languages", "PE", "Technology"], max_selections=3)
        with col2:
            academic_gpa = st.number_input("Current GPA", min_value=0.0, max_value=4.0, step=0.1)
            study_hours = st.number_input("Study Hours per Week", min_value=0, max_value=80)
        with col3:
            learning_style = st.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic", "Reading/Writing", "Mixed"])
            grade_trend = st.selectbox("Recent Grade Trend", ["Improving", "Stable", "Declining"])
        
        # Career & Future Planning
        st.markdown("#### Career & Future Goals")
        col1, col2 = st.columns(2)
        with col1:
            career_interests = st.multiselect("Career Interest Areas", ["Technology", "Healthcare", "Education", "Business", "Arts", "Science", "Engineering", "Social Work", "Law", "Finance"])
            dream_job = st.text_input("Dream Career")
            college_plans = st.selectbox("College Plans", ["Definitely Yes", "Probably Yes", "Undecided", "Probably No", "Definitely No"])
        with col2:
            work_experience = st.multiselect("Work Experience", ["Part-time job", "Internship", "Volunteer work", "Family business", "Freelancing", "None"])
            short_term_goals = st.text_area("Short-term Goals (1-2 years)")
            long_term_goals = st.text_area("Long-term Goals (5+ years)")
        
        # Personal Development
        st.markdown("#### Personal Development")
        col1, col2, col3 = st.columns(3)
        with col1:
            personality_type = st.selectbox("Personality Type (if known)", ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP", "Unknown"])
            social_comfort = st.selectbox("Social Comfort Level", ["Very extroverted", "Somewhat extroverted", "Ambivert", "Somewhat introverted", "Very introverted"])
        with col2:
            leadership_exp = st.multiselect("Leadership Experience", ["Student government", "Club president", "Team captain", "Project leader", "Peer mentor", "None"])
            stress_level = st.slider("Current Stress Level", 1, 10, 5)
        with col3:
            teamwork_pref = st.selectbox("Teamwork Preference", ["Prefer to lead", "Happy to collaborate", "Prefer to work independently", "Depends on the task"])
            help_seeking = st.selectbox("Help-Seeking Behavior", ["Quick to ask for help", "Try independently first", "Only ask when really stuck", "Prefer to figure it out alone"])
        
        submitted = st.form_submit_button("Save Enhanced Profile")
        
        if submitted:
            # Compile all data
            enhanced_data = {
                'name': name, 'age': age, 'grade_level': grade_level, 'email': email, 
                'gvc_id': gvc_id, 'current_courses': current_courses, 
                'favorite_subjects': favorite_subjects, 'academic_gpa': academic_gpa,
                'study_hours_per_week': study_hours, 'learning_style': learning_style,
                'grade_trend': grade_trend, 'career_interests': career_interests,
                'dream_job': dream_job, 'college_plans': college_plans,
                'work_experience': work_experience, 'short_term_goals': short_term_goals,
                'long_term_goals': long_term_goals, 'personality_type': personality_type,
                'social_comfort_level': social_comfort, 'leadership_experience': leadership_exp,
                'stress_level': stress_level, 'teamwork_preference': teamwork_pref,
                'help_seeking_behavior': help_seeking
            }
            
            st.session_state.student_data = enhanced_data
            st.success("Enhanced student profile saved successfully!")
            return enhanced_data
