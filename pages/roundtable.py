import streamlit as st
import logging
import math
import time
import traceback
from datetime import datetime
import json
import tempfile
import os
try:
    import streamlit.components.v1 as components
except ImportError:
    components = None

# Mock imports and fallback implementations
try:
    from config.settings import AGENTS_INFO, MAX_AGENT_TURNS, ROUNDTABLE_CENTER, ROUNDTABLE_RADIUS
except ImportError:
    AGENTS_INFO = [
        {"name": "Academic Mentor", "avatar": "📚", "image": "avatars/academic_mentor.png", "expertise": "Academic guidance"},
        {"name": "Career Guide", "avatar": "💼", "image": "avatars/career_guide.png", "expertise": "Career planning"},
        {"name": "Tech Innovator", "avatar": "💻", "image": "avatars/tech_innovator.png", "expertise": "Technology"},
        {"name": "Wellness Coach", "avatar": "🧘", "image": "avatars/wellness_coach.png", "expertise": "Health & wellness"},
        {"name": "Life Skills Mentor", "avatar": "🎯", "image": "avatars/life_skills_mentor.png", "expertise": "Life skills"},
        {"name": "Creative Mentor", "avatar": "🎨", "image": "avatars/creative_mentor.png", "expertise": "Creative development"},
        {"name": "Leadership Coach", "avatar": "👑", "image": "avatars/leadership_coach.png", "expertise": "Leadership skills"},
        {"name": "Financial Advisor", "avatar": "💰", "image": "avatars/financial_advisor.png", "expertise": "Financial literacy"},
        {"name": "Communication Expert", "avatar": "🗣️", "image": "avatars/communication_expert.png", "expertise": "Communication skills"},
        {"name": "Global Perspective Mentor", "avatar": "🌍", "image": "avatars/global_mentor.png", "expertise": "Global awareness"},
    ]
    MAX_AGENT_TURNS = 5
    ROUNDTABLE_CENTER = (50, 50)
    ROUNDTABLE_RADIUS = 40

try:
    from config.styles import ROUNDTABLE_CSS
except ImportError:
    ROUNDTABLE_CSS = """
    <style>
    .main-content {
        max-width: 100%;
        padding: 20px;
    }
    .full-width-mentor-profiles {
        width: 100%;
        margin-top: 30px;
    }
    </style>
    """

try:
    from core.session_manager import initialize_session_state
except ImportError:
    def initialize_session_state(vectordb=None):
        """Mock session state initialization"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'chat_running' not in st.session_state:
            st.session_state.chat_running = False
        if 'current_agent' not in st.session_state:
            st.session_state.current_agent = None
        if 'thinking_agent' not in st.session_state:
            st.session_state.thinking_agent = None
        if 'consecutive_agent_turns' not in st.session_state:
            st.session_state.consecutive_agent_turns = 0
        if 'agent_turn_in_progress' not in st.session_state:
            st.session_state.agent_turn_in_progress = False

try:
    from core.avatar_manager import create_role_to_image_mapping
except ImportError:
    def create_role_to_image_mapping():
        """Mock role to image mapping"""
        return {agent["name"]: agent["avatar"] for agent in AGENTS_INFO}

try:
    from ui.sidebar import render_sidebar
except ImportError:
    def render_sidebar():
        """Enhanced sidebar rendering with student information"""
        st.markdown("### 🎯 AI Mentor Roundtable")
        st.markdown("*Collaborative Learning Experience*")
        
        # Add student profile section
        student_data = st.session_state.get('student_data', {})
        if student_data:
            st.markdown("---")
            render_sidebar_student_profile(student_data)
        else:
            st.markdown("---")
            st.info("👤 **No student profile loaded**\n\nPlease complete the student profile to personalize your experience.")

def render_sidebar_student_profile(student_data):
    """Render student profile in main sidebar"""
    st.markdown("""
    <style>
    .sidebar-student-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .sidebar-profile-header {
        text-align: center;
        margin-bottom: 12px;
    }
    .sidebar-profile-name {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 3px;
    }
    .sidebar-profile-details {
        font-size: 11px;
        opacity: 0.9;
    }
    .sidebar-info-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 8px;
        backdrop-filter: blur(10px);
    }
    .sidebar-info-label {
        font-size: 10px;
        font-weight: bold;
        color: #FFD700;
        margin-bottom: 3px;
    }
    .sidebar-info-value {
        font-size: 11px;
        line-height: 1.3;
    }
    .sidebar-interest-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 9px;
        margin: 1px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get student data
    name = student_data.get('name', 'Unknown Student')
    age = student_data.get('age', 'N/A')
    grade = student_data.get('grade_level', 'N/A')
    gvc_id = student_data.get('gvc_id', 'N/A')
    email = student_data.get('email', 'Not provided')
    interests = student_data.get('interests', '')
    goals = student_data.get('goals', '')
    strengths = student_data.get('strengths', '')
    challenges = student_data.get('challenges', '')
    
    # Render compact student profile card
    st.markdown(f"""
    <div class="sidebar-student-card">
        <div class="sidebar-profile-header">
            <div style="font-size: 30px; margin-bottom: 8px;">🎓</div>
            <div class="sidebar-profile-name">{name}</div>
            <div class="sidebar-profile-details">ID: {gvc_id} • Age {age} • {grade}</div>
        </div>
        
        <div class="sidebar-info-item">
            <div class="sidebar-info-label">📧 CONTACT</div>
            <div class="sidebar-info-value">{email}</div>
        </div>
        
        <div class="sidebar-info-item">
            <div class="sidebar-info-label">🎯 INTERESTS</div>
            <div class="sidebar-info-value">
                {_format_sidebar_interests(interests) if interests else 'No interests specified'}
            </div>
        </div>
        
        <div class="sidebar-info-item">
            <div class="sidebar-info-label">🎖️ GOALS</div>
            <div class="sidebar-info-value">
                {_truncate_sidebar_text(goals, 80) if goals else 'No goals specified'}
            </div>
        </div>
        
        <div class="sidebar-info-item">
            <div class="sidebar-info-label">💪 STRENGTHS</div>
            <div class="sidebar-info-value">
                {_format_sidebar_list(strengths) if strengths else 'No strengths specified'}
            </div>
        </div>
        
        <div class="sidebar-info-item">
            <div class="sidebar-info-label">🔄 CHALLENGES</div>
            <div class="sidebar-info-value">
                {_format_sidebar_list(challenges) if challenges else 'No challenges specified'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def _format_sidebar_interests(interests):
    """Format interests as small tags for sidebar"""
    if not interests:
        return "No interests specified"
    
    interest_list = [i.strip() for i in interests.split(',') if i.strip()]
    if not interest_list:
        return interests
    
    tags = ''.join([f'<span class="sidebar-interest-tag">{interest}</span>' for interest in interest_list])
    return tags

def _format_sidebar_list(items):
    """Format comma-separated items with bullet points for sidebar"""
    if not items:
        return "None specified"
    
    item_list = [i.strip() for i in items.split(',') if i.strip()]
    if not item_list:
        return items
    
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
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

try:
    from ui.control_buttons import render_control_buttons
except ImportError:
    def render_control_buttons():
        """Mock control buttons"""
        pass

try:
    from ui.chat_interface import (
        render_user_input, render_chat_history, render_status_display,
        handle_agent_logic, handle_user_message
    )
except ImportError:
    def render_user_input():
        """Mock user input"""
        message = st.text_area("Ask the mentors:", placeholder="Type your question here...")
        send_button = st.button("Send", type="primary")
        return send_button and message.strip(), message.strip()
    
    def render_chat_history(role_to_image=None):
        """Mock chat history"""
        if not st.session_state.get('chat_history'):
            st.info("💡 Start the discussion or ask a question to begin!")
            return
        
        for message in st.session_state.chat_history[-10:]:
            role = message.get("role", "Unknown")
            content = message.get("content", "")
            timestamp = message.get("timestamp", "")
            
            if role == "User":
                st.markdown(f"""
                <div style="background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <strong>🎓 You</strong> <span style="color: #666; font-size: 12px; float: right;">{timestamp}</span>
                    <div style="color: #333; margin-top: 5px;">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                agent_info = next((agent for agent in AGENTS_INFO if agent["name"] == role), None)
                avatar = agent_info["avatar"] if agent_info else "🤖"
                st.markdown(f"""
                <div style="background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <strong>{avatar} {role}</strong> <span style="color: #666; font-size: 12px; float: right;">{timestamp}</span>
                    <div style="color: #333; margin-top: 5px;">{content}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def render_status_display():
        """Mock status display"""
        current_agent = st.session_state.get('current_agent', 'None')
        thinking_agent = st.session_state.get('thinking_agent', 'None')
        chat_running = st.session_state.get('chat_running', False)
        
        if thinking_agent and thinking_agent != 'None':
            st.info(f"🧠 {thinking_agent} is thinking...")
        elif current_agent and current_agent != 'None':
            st.success(f"🎤 Current speaker: {current_agent}")
        elif chat_running:
            st.warning("⏳ Discussion is active...")
        else:
            st.error("⏸️ Discussion is paused")
    
    def handle_agent_logic(get_context_chunks, role_to_image):
        """Mock agent logic"""
        pass
    
    def handle_user_message(message):
        """Mock user message handling"""
        add_user_message(message)

try:
    from ui.mentor_profiles import render_mentor_profiles
except ImportError:
    def render_mentor_profiles():
        """Mock mentor profiles"""
        st.markdown("### 👥 Meet Your AI Mentors")
        
        cols = st.columns(len(AGENTS_INFO))
        for i, agent in enumerate(AGENTS_INFO):
            with cols[i]:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 15px; background: #f8f9fa;'>
                    <div style='font-size: 40px; margin-bottom: 10px;'>{agent.get('avatar', '🤖')}</div>
                    <h4>{agent['name']}</h4>
                    <p style='color: #666; font-size: 14px;'>{agent.get('expertise', 'Expert guidance')}</p>
                </div>
                """, unsafe_allow_html=True)

try:
    from utils.vector_store import load_vectorstore, get_context_chunks
except ImportError:
    def load_vectorstore():
        """Mock vector store loading"""
        return None, None
    
    def get_context_chunks():
        """Mock context chunks"""
        return ["Context chunk 1", "Context chunk 2"]

# Configure logging
logger = logging.getLogger(__name__)

# Mock additional required functions
def reset_chat_session():
    """Reset chat session"""
    st.session_state.chat_history = []
    st.session_state.consecutive_agent_turns = 0
    st.session_state.chat_running = False
    st.session_state.current_agent = None
    st.session_state.thinking_agent = None
    st.session_state.agent_turn_in_progress = False

def add_message_to_history(content, agent_name):
    """Mock message tracking"""
    pass

def reset_agent_state_if_stuck():
    """Mock stuck state reset"""
    return False

def process_agent_turn(get_context_chunks):
    """Mock agent turn processing"""
    return False

def render_roundtable():
    """Render the roundtable visualization - FIXED VERSION"""
    
    # Roundtable header
    st.markdown('<h3 style="text-align: center; color: #009CA6; margin-bottom: 20px;">🎯 AI Mentor Roundtable</h3>', unsafe_allow_html=True)
    
    # Add logo status debugging
    logo_status = "🎯 emoji fallback"
    try:
        import os
        if os.path.exists("gvc_logo.png"):
            logo_status = "✅ GVC logo file found"
            # Test if we can load it
            test_logo = _create_center_logo_with_image()
            if '<img' in test_logo:
                logo_status = "✅ GVC logo loaded successfully"
        else:
            logo_status = "❌ GVC logo file not found"
    except Exception as e:
        logo_status = f"⚠️ Logo test error: {str(e)[:50]}"
    
    # Generate and display roundtable HTML
    try:
        roundtable_html = _generate_roundtable_html()
        
        # Debug: Check HTML size and logo presence
        html_size = len(roundtable_html)
        has_logo_image = '<img' in roundtable_html and 'logo' in roundtable_html.lower()
        
        if html_size > 100000:  # 100KB limit
            st.error(f"⚠️ HTML too large ({html_size} chars). Using fallback.")
            _render_simple_roundtable()
        else:
            # Use components.html for better rendering
            try:
                import streamlit.components.v1 as components
                components.html(roundtable_html, height=350, scrolling=False)
#                st.caption(f"✅ Roundtable loaded with {len(AGENTS_INFO)} mentors | {logo_status}")
            except ImportError:
                # Fallback to st.markdown
                st.markdown(roundtable_html, unsafe_allow_html=True)
#                st.caption(f"✅ Roundtable loaded with {len(AGENTS_INFO)} mentors (basic mode) | {logo_status}")
        
    except Exception as e:
        st.error(f"❌ Error generating roundtable: {e}")
        logging.error(f"Roundtable error: {traceback.format_exc()}")
        _render_simple_roundtable()
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Optional legend
    if st.checkbox("Show Legend", value=False):
        st.markdown("""
        **Avatar States:**
        - 🔵 **Blue**: Active speaker
        - 🟡 **Gold**: Thinking (animated)
        - ⚪ **Gray**: Available
        """)

def _render_simple_roundtable():
    """Fallback simple roundtable rendering"""
    n = len(AGENTS_INFO)
    if n == 0:
        st.info("🎯 No mentors configured for the roundtable.")
        return
    
    # Simple grid layout
    cols = st.columns(min(n, 4))
    for i, agent in enumerate(AGENTS_INFO):
        with cols[i % len(cols)]:
            # Get agent state
            is_thinking = agent["name"] == st.session_state.get('thinking_agent', None)
            is_active = agent["name"] == st.session_state.get('current_agent', None) and not is_thinking
            
            # Color based on state
            if is_thinking:
                color = "🟡"
                status = "Thinking..."
            elif is_active:
                color = "🔵"
                status = "Active"
            else:
                color = "⚪"
                status = "Available"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin: 5px;'>
                <div style='font-size: 24px;'>{agent.get('avatar', '🤖')}</div>
                <div style='font-size: 12px; font-weight: bold;'>{agent['name'][:8]}</div>
                <div style='font-size: 10px; color: #666;'>{color} {status}</div>
            </div>
            """, unsafe_allow_html=True)

def render_student_info_sidebar(student_data):
    """Render comprehensive student information in sidebar with beautiful formatting"""
    st.markdown("""
    <style>
    .student-profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .profile-header {
        text-align: center;
        margin-bottom: 15px;
    }
    .profile-avatar {
        font-size: 40px;
        margin-bottom: 10px;
    }
    .profile-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .profile-details {
        font-size: 12px;
        opacity: 0.9;
    }
    .info-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .info-label {
        font-size: 11px;
        font-weight: bold;
        color: #FFD700;
        margin-bottom: 5px;
    }
    .info-value {
        font-size: 12px;
        line-height: 1.4;
    }
    .interest-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 10px;
        margin: 2px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get student data
    name = student_data.get('name', 'Unknown Student')
    age = student_data.get('age', 'N/A')
    grade = student_data.get('grade_level', 'N/A')
    gvc_id = student_data.get('gvc_id', 'N/A')
    email = student_data.get('email', 'Not provided')
    interests = student_data.get('interests', '')
    goals = student_data.get('goals', '')
    strengths = student_data.get('strengths', '')
    challenges = student_data.get('challenges', '')
    
    # Render beautiful student profile card
    st.markdown(f"""
    <div class="student-profile-card">
        <div class="profile-header">
            <div class="profile-avatar">🎓</div>
            <div class="profile-name">{name}</div>
            <div class="profile-details">GVC ID: {gvc_id} • Age {age} • Grade {grade}</div>
        </div>
        
        <div class="info-section">
            <div class="info-label">📧 CONTACT</div>
            <div class="info-value">{email}</div>
        </div>
        
        <div class="info-section">
            <div class="info-label">🎯 INTERESTS</div>
            <div class="info-value">
                {_format_interests_as_tags(interests) if interests else 'No interests specified'}
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-label">🎖️ GOALS</div>
            <div class="info-value">
                {_truncate_text(goals, 100) if goals else 'No goals specified'}
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-label">💪 STRENGTHS</div>
            <div class="info-value">
                {_format_list_items(strengths) if strengths else 'No strengths specified'}
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-label">🔄 CHALLENGES</div>
            <div class="info-value">
                {_format_list_items(challenges) if challenges else 'No challenges specified'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def _format_interests_as_tags(interests):
    """Format interests as small tags"""
    if not interests:
        return "No interests specified"
    
    interest_list = [i.strip() for i in interests.split(',') if i.strip()]
    if not interest_list:
        return interests
    
    tags = ''.join([f'<span class="interest-tag">{interest}</span>' for interest in interest_list])
    return tags

def _format_list_items(items):
    """Format comma-separated items with bullet points"""
    if not items:
        return "None specified"
    
    item_list = [i.strip() for i in items.split(',') if i.strip()]
    if not item_list:
        return items
    
    if len(item_list) == 1:
        return item_list[0]
    
    formatted = '<br>'.join([f'• {item}' for item in item_list])
    return formatted

def _truncate_text(text, max_length):
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def render_roundtable_controls():
    """Render roundtable control buttons in sidebar"""
    st.markdown("### 🎮 Discussion Controls")
    
    # Get current state
    chat_running = st.session_state.get('chat_running', False)
    current_agent = st.session_state.get('current_agent', 'None')
    thinking_agent = st.session_state.get('thinking_agent', 'None')
    consecutive_turns = st.session_state.get('consecutive_agent_turns', 0)
    has_chat_history = bool(st.session_state.get('chat_history', []))
    
    # Main control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        # Start/Stop/Resume button
        if not chat_running and not has_chat_history:
            if st.button("🚀 Start Discussion", use_container_width=True, type="primary"):
                start_roundtable_discussion()
                st.rerun()
        elif not chat_running and has_chat_history:
            if st.button("▶️ Resume Discussion", use_container_width=True, type="primary"):
                resume_roundtable_discussion()
                st.rerun()
        else:
            if st.button("⏸️ Pause Discussion", use_container_width=True, type="secondary"):
                pause_roundtable_discussion()
                st.rerun()
    
    with col2:
        # Advanced controls
        if chat_running:
            if st.button("⏭️ Next Agent", use_container_width=True):
                advance_to_next_agent()
                st.rerun()
        else:
            if st.button("🔄 Reset Chat", use_container_width=True):
                reset_roundtable_completely()
                st.rerun()
    
    # Status display
    st.markdown("---")
    st.markdown("### 📊 Current Status")
    
    # Current agent status
    if thinking_agent and thinking_agent != 'None':
        st.success(f"🧠 **Thinking:** {thinking_agent}")
    elif current_agent and current_agent != 'None':
        st.info(f"🎤 **Current Speaker:** {current_agent}")
    else:
        st.warning("⏸️ **No Active Agent**")
    
    # Turn counter and discussion status in metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Turn Count", f"{consecutive_turns}/{MAX_AGENT_TURNS}")
    with col2:
        if chat_running:
            st.metric("Status", "🟢 Active")
        else:
            st.metric("Status", "⏸️ Paused")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("📝 Clear All Messages", use_container_width=True):
        clear_chat_history()
        st.rerun()
    
    if st.button("🎯 Focus on Academic", use_container_width=True):
        st.session_state.current_agent = "Academic Mentor"
        st.rerun()
    
    if st.button("💼 Focus on Career", use_container_width=True):
        st.session_state.current_agent = "Career Guide"
        st.rerun()

def render_visual_roundtable():
    """Render the visual roundtable with agent avatars"""
    st.markdown("### 🎭 Mentor Roundtable")
    
    # Apply CSS
    st.markdown(ROUNDTABLE_CSS, unsafe_allow_html=True)
    
    # Generate roundtable HTML
    roundtable_html = generate_roundtable_html()
    st.markdown(roundtable_html, unsafe_allow_html=True)
    
    # Legend
    if st.checkbox("Show Avatar Legend"):
        render_roundtable_legend()

def generate_roundtable_html():
    """Generate the complete HTML for the roundtable visualization"""
    n = len(AGENTS_INFO)
    if n == 0:
        return "<div style='text-align: center; color: #666;'>No agents configured</div>"
    
    avatar_divs = []
    
    # Generate avatar positions in a circle
    for i, agent in enumerate(AGENTS_INFO):
        angle = (360 / n) * i - 90  # Start from top
        radius = 47  # Percentage radius from center
        x = 50 + radius * math.cos(math.radians(angle))
        y = 50 + radius * math.sin(math.radians(angle))
        
        # Determine avatar state
        is_thinking = agent["name"] == st.session_state.get('thinking_agent', None)
        is_active = (
            agent["name"] == st.session_state.get('current_agent', None) 
            and not is_thinking
        )
        
        avatar_html = create_avatar_html(agent, (x, y), is_active, is_thinking)
        avatar_divs.append(avatar_html)
    
    all_avatars = "".join(avatar_divs)
    center_indicator = create_center_indicator()
    
    return f'''
    <div class="roundtable-container">
        <div class="circle-table">
            {all_avatars}
            {center_indicator}
        </div>
    </div>
    '''

def create_avatar_html(agent, position, is_active=False, is_thinking=False):
    """Create HTML for a single avatar using existing avatar manager"""
    classes = ["avatar"]
    if is_thinking:
        classes.append("thinking")
    elif is_active:
        classes.append("active")
    
    # Use avatar manager to get image or fallback
    avatar_content = agent["avatar"]  # Default emoji
    
    if "image" in agent and agent["image"]:
        try:
            import os
            if os.path.exists(agent["image"]):
                image_base64 = get_image_base64(agent["image"])
                if image_base64:
                    avatar_content = f'<img src="data:image/png;base64,{image_base64}" alt="{agent["name"]}" />'
        except Exception as e:
            logger.warning(f"Could not load image for {agent['name']}: {e}")
    
    status = get_agent_status(agent["name"], is_active, is_thinking)
    short_name = shorten_agent_name(agent["name"])
    
    return f'''
    <div class="{" ".join(classes)}" 
         style="left: {position[0]:.1f}%; top: {position[1]:.1f}%;" 
         title="{agent['name']} - {status}">
        {avatar_content}
        <div class="avatar-label">{short_name}</div>
    </div>
    '''

def get_logo_base64(logo_path):
    """Convert PNG logo to base64 string without quality loss"""
    try:
        import base64
        from PIL import Image
        import io
        import os
        
        if not os.path.exists(logo_path):
            return None
            
        # Open and process logo
        with Image.open(logo_path) as img:
            # Convert to RGBA to preserve transparency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Only resize if it's too large
            original_size = img.size
            target_size = (90, 90)  # Match display size
            
            if original_size[0] > target_size[0] or original_size[1] > target_size[1]:
                # Use LANCZOS for high-quality downscaling
                img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Convert to base64 with high quality
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', optimize=False, quality=100)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
    except Exception as e:
        logger.warning(f"Error converting logo {logo_path}: {e}")
        return None

def create_center_indicator():
    """Create center indicator with logo"""
    logo_path = "gvc_logo.png"
    
    try:
        logo_base64 = get_logo_base64(logo_path)
        if logo_base64:
            logo_content = f'<img src="data:image/png;base64,{logo_base64}" alt="GVC Logo" style="width: 90px; height: 90px; object-fit: contain;" />'
        else:
            logo_content = '🎓'
    except:
        logo_content = '🎓'
    
    return f'''
    <div class="center-indicator" 
         style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); 
                width: 120px; height: 120px; border-radius: 50%; background: #FFFFFF; 
                display: flex; align-items: center; justify-content: center; 
                color: white; font-size: 24px; font-weight: bold; 
                box-shadow: 0 4px 16px rgba(0, 156, 166, 0.3); z-index: 5; 
                font-family: 'Inter', sans-serif;" 
         title="GVC AI Mentor Roundtable">
        {logo_content}
    </div>
    '''

def get_agent_status(agent_name, is_active, is_thinking):
    """Get status text for agent tooltip"""
    if is_thinking:
        return "Currently thinking..."
    elif is_active:
        return "Active speaker"
    else:
        return "Listening"

def shorten_agent_name(name):
    """Shorten agent names for display"""
    name_mappings = {
        "Academic Mentor": "Academic",
        "Career Guide": "Career",
        "Tech Innovator": "Tech",
        "Wellness Coach": "Wellness",
        "Life Skills Mentor": "Life Skills",
        "Creative Mentor": "Creative",
        "Leadership Coach": "Leadership",
        "Financial Advisor": "Financial",
        "Communication Expert": "Communication",
        "Global Perspective Mentor": "Global"
    }
    return name_mappings.get(name, name)

def render_roundtable_legend():
    """Render legend explaining roundtable states"""
    st.markdown("""
    ### 🔍 Avatar States Legend
    
    - 🔵 **Active (Blue)**: Currently speaking
    - 🟡 **Thinking (Gold)**: Agent is preparing response
    - ⚪ **Listening (White)**: Waiting for turn
    
    **Instructions:**
    - Hover over avatars to see their current status
    - Agents are arranged in a circle around the GVC logo
    - Discussion flows naturally between mentors
    """)

def render_chat_interface():
    """Render the chat interface with message history"""
    st.markdown("### 💬 Live Discussion")
    
    # Message input
    user_input = st.text_area(
        "Ask the mentors a question:",
        height=100,
        placeholder="Type your question here...",
        key="user_message_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send Message", use_container_width=True):
            if user_input.strip():
                add_user_message(user_input.strip())
                st.session_state.user_message_input = ""  # Clear input
                st.rerun()
    
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            clear_chat_history()
            st.rerun()
    
    # Display chat history
    st.markdown("---")
    display_chat_history()

def display_chat_history():
    """Display the chat message history"""
    if not st.session_state.get('chat_history'):
        st.info("💡 Start the discussion or ask a question to begin!")
        return
    
    # Show recent messages (limit to last 10 for performance)
    recent_messages = st.session_state.chat_history[-10:]
    
    for message in recent_messages:
        render_chat_message(message)
    
    if len(st.session_state.chat_history) > 10:
        st.caption(f"Showing last 10 of {len(st.session_state.chat_history)} messages")

def render_chat_message(message):
    """Render a single chat message"""
    role = message.get("role", "Unknown")
    content = message.get("content", "")
    timestamp = message.get("timestamp", "")
    
    if role == "User":
        # User message
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
                    border-left: 4px solid #2196f3; border-radius: 12px; 
                    padding: 15px; margin: 10px 0;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 8px;">🎓</span>
                <strong style="color: #2196f3;">You</strong>
                <span style="color: #666; font-size: 12px; margin-left: auto;">{timestamp}</span>
            </div>
            <div style="color: #333;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Agent message
        agent_info = next((agent for agent in AGENTS_INFO if agent["name"] == role), None)
        avatar = agent_info["avatar"] if agent_info else "🤖"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                    border-left: 4px solid #007bff; border-radius: 12px; 
                    padding: 15px; margin: 10px 0;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 8px;">{avatar}</span>
                <strong style="color: #007bff;">{role}</strong>
                <span style="color: #666; font-size: 12px; margin-left: auto;">{timestamp}</span>
            </div>
            <div style="color: #333; line-height: 1.5;">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def start_roundtable_discussion():
    """Start the roundtable discussion using existing chat logic"""
    # Initialize discussion state
    st.session_state.chat_running = True
    st.session_state.consecutive_agent_turns = 0
    st.session_state.agent_turn_in_progress = False
    
    # Get student name for personalized welcome - check multiple possible locations
    student_name = "Student"
    student_data = st.session_state.get('student_data', {})
    if not student_data:
        student_data = st.session_state.get('user_profile', {})
    
    if student_data:
        student_name = student_data.get('name', student_data.get('student_name', 'Student'))
    
    # Add welcome message
    opening_message = f"🎯 Welcome to the AI Mentor Roundtable, {student_name}! Our expert mentors are here to guide you on your learning journey. Feel free to ask any questions about academics, career, technology, wellness, and more!"
    
    add_system_message(opening_message)
    
    # Set first agent (Academic Mentor as default)
    if AGENTS_INFO:
        st.session_state.current_agent = AGENTS_INFO[0]["name"]
        st.session_state.thinking_agent = None
        
        # Add initial agent introduction
        first_agent = AGENTS_INFO[0]["name"]
        intro_message = f"Hello {student_name}! I'm your {first_agent}. I'm excited to help you explore your academic potential and learning goals. What would you like to discuss today?"
        
        add_agent_message(first_agent, intro_message)
    
    st.success(f"🚀 Discussion started! Welcome {student_name}!")
    st.balloons()  # Fun celebration effect

def resume_roundtable_discussion():
    """Resume a paused roundtable discussion"""
    st.session_state.chat_running = True
    st.session_state.agent_turn_in_progress = False
    
    # Get student name - check multiple possible locations
    student_name = "Student"
    student_data = st.session_state.get('student_data', {})
    if not student_data:
        student_data = st.session_state.get('user_profile', {})
    
    if student_data:
        student_name = student_data.get('name', student_data.get('student_name', 'Student'))
    
    # Add resume message
    resume_message = f"🔄 Discussion resumed! The mentors are ready to continue helping you, {student_name}."
    add_system_message(resume_message)
    
    st.success("▶️ Discussion resumed!")

def pause_roundtable_discussion():
    """Pause the roundtable discussion"""
    st.session_state.chat_running = False
    st.session_state.thinking_agent = None
    st.session_state.agent_turn_in_progress = False
    
    # Add pause message
    pause_message = "⏸️ Discussion paused. You can resume anytime or ask questions directly."
    add_system_message(pause_message)
    
    st.info("⏸️ Discussion paused")

def stop_roundtable_discussion():
    """Stop the roundtable discussion"""
    st.session_state.chat_running = False
    st.session_state.thinking_agent = None
    st.session_state.current_agent = None

def reset_roundtable_completely():
    """Reset the entire roundtable state"""
    reset_chat_session()
    st.session_state.chat_history = []

def advance_to_next_agent():
    """Advance to the next agent in the roundtable"""
    if not AGENTS_INFO:
        return
    
    current_agent = st.session_state.get('current_agent')
    current_index = 0
    
    # Find current agent index
    for i, agent in enumerate(AGENTS_INFO):
        if agent["name"] == current_agent:
            current_index = i
            break
    
    # Move to next agent
    next_index = (current_index + 1) % len(AGENTS_INFO)
    next_agent = AGENTS_INFO[next_index]["name"]
    
    # Set thinking state first
    st.session_state.thinking_agent = next_agent
    st.session_state.current_agent = None
    
    # Brief delay for visual effect
    time.sleep(0.5)
    
    # Set as active
    st.session_state.current_agent = next_agent
    st.session_state.thinking_agent = None

def add_user_message(content):
    """Add a user message to chat history"""
    message = {
        "role": "User",
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append(message)
    
    # Reset consecutive agent turns when user speaks
    st.session_state.consecutive_agent_turns = 0

def add_system_message(content):
    """Add a system message to chat history"""
    message = {
        "role": "System",
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append(message)

def add_agent_message(agent_name, content):
    """Add an agent message to chat history"""
    message = {
        "role": agent_name,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append(message)
    
    # Track for similarity checking
    add_message_to_history(content, agent_name)

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []
    st.session_state.consecutive_agent_turns = 0

def process_agent_interactions():
    """Process agent interactions using existing code logic"""
    try:
        # Check if we should continue
        if st.session_state.consecutive_agent_turns >= MAX_AGENT_TURNS:
            st.session_state.chat_running = False
            st.warning(f"⏸️ Agents have paused after {MAX_AGENT_TURNS} consecutive turns. Ask a question to continue!")
            return
        
        # Reset if stuck
        if reset_agent_state_if_stuck():
            st.info("🔄 Reset stuck agent state")
        
        # Process agent turn if applicable
        if st.session_state.get('chat_running') and not st.session_state.get('agent_turn_in_progress'):
            # Mock get_context_chunks function for now
            def mock_get_context_chunks():
                return ["Context chunk 1", "Context chunk 2"]
            
            result = process_agent_turn(mock_get_context_chunks)
            if result:
                st.rerun()
    
    except Exception as e:
        logger.error(f"Error in process_agent_interactions: {e}")
        st.error(f"Error processing agent interactions: {e}")

# Helper functions for roundtable functionality
def _generate_roundtable_html():
    """Generate the complete HTML for the roundtable - WITH AVATAR IMAGES"""
    n = len(AGENTS_INFO)
    if n == 0:
        return """
        <div style='text-align: center; padding: 40px; color: #666;'>
            <h4>🎯 No Agents Configured</h4>
            <p>Please configure your AI mentors to display the roundtable.</p>
        </div>
        """
    
    # Create a clean, working roundtable with avatar images
    avatars_html = ""
    
    # Generate avatar positions in a perfect circle
    for i, agent in enumerate(AGENTS_INFO):
        # Calculate position (perfect circle)
        angle = (360 / n) * i - 90  # Start from top (12 o'clock)
        radius = 40  # Percentage from center
        x = 50 + radius * math.cos(math.radians(angle))
        y = 50 + radius * math.sin(math.radians(angle))
        
        # Get agent state
        is_thinking = agent["name"] == st.session_state.get('thinking_agent', None)
        is_active = agent["name"] == st.session_state.get('current_agent', None) and not is_thinking
        
        # Determine style based on state
        if is_thinking:
            border_color = "#FFD700"
            bg_color = "#FFF8DC"
            animation = "animation: pulse 2s infinite;"
            box_shadow = "0 4px 16px rgba(255, 215, 0, 0.5)"
        elif is_active:
            border_color = "#009CA6" 
            bg_color = "#E6F3FF"
            animation = ""
            box_shadow = "0 4px 16px rgba(0, 156, 166, 0.5)"
        else:
            border_color = "#CCC"
            bg_color = "#F8F9FA"
            animation = ""
            box_shadow = "0 2px 8px rgba(0,0,0,0.15)"
        
        # Try to use avatar image, fallback to emoji
        avatar_content = agent.get('avatar', '🤖')  # Default emoji fallback
        
        if 'image' in agent and agent['image']:
            try:
                import os
                image_path = agent['image']
                if os.path.exists(image_path):
                    # Get base64 image with aggressive size optimization
                    image_base64 = get_optimized_image_base64(image_path)
                    if image_base64:
                        avatar_content = f'<img src="data:image/jpeg;base64,{image_base64}" alt="{agent["name"]}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; -ms-interpolation-mode: bicubic;" />'
            except Exception as e:
                logger.warning(f"Could not load image for {agent['name']}: {e}")
                # Keep emoji fallback
        
        # Create avatar name label with person names
        # Get the actual person name for this agent
        person_name = _get_agent_person_name(agent["name"])
        name_display = _format_person_name_for_display(person_name)
        
        avatars_html += f"""
        <div style="position: absolute; 
                    left: {x:.1f}%; top: {y:.1f}%; 
                    transform: translate(-50%, -50%);
                    width: 50px; height: 50px;
                    border-radius: 50%;
                    background: {bg_color};
                    border: 3px solid {border_color};
                    display: flex; align-items: center; justify-content: center;
                    font-size: 14px; color: #333;
                    box-shadow: {box_shadow};
                    cursor: pointer; z-index: 5; {animation}
                    transition: all 0.3s ease;
                    overflow: hidden;"
             title="{agent['name']} - {'Thinking...' if is_thinking else 'Active' if is_active else 'Available'}"
             onmouseover="this.style.transform='translate(-50%, -50%) scale(1.1)'"
             onmouseout="this.style.transform='translate(-50%, -50%) scale(1)'">
            {avatar_content}
        </div>
        <div style="position: absolute; 
                    left: {x:.1f}%; top: {y + 10:.1f}%; 
                    transform: translateX(-50%);
                    font-size: 8px; font-weight: bold; color: #444;
                    background: rgba(255,255,255,0.95); padding: 3px 6px;
                    border-radius: 8px; white-space: nowrap; z-index: 6;
                    text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    line-height: 1.1; max-width: 65px;">
            {name_display}
        </div>
        """
    
    # Create center logo with GVC logo
    center_html = _create_center_logo_with_image()
    
    # Combine everything with enhanced CSS
    complete_html = f"""
    <style>
    @keyframes pulse {{
        0%, 100% {{ 
            transform: translate(-50%, -50%) scale(1); 
            box-shadow: 0 4px 16px rgba(255, 215, 0, 0.5);
        }}
        50% {{ 
            transform: translate(-50%, -50%) scale(1.05); 
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.7);
        }}
    }}
    .roundtable-container {{
        position: relative;
        width: 320px;
        height: 320px;
        margin: 15px auto;
        background: radial-gradient(circle at center, #f8fbff 0%, #e8f4f8 70%, #d0e8ed 100%);
        border-radius: 50%;
        border: 4px solid #009CA6;
        box-shadow: 0 8px 25px rgba(0, 156, 166, 0.3);
        overflow: visible;
    }}
    </style>
    <div class="roundtable-container">
        {avatars_html}
        {center_html}
    </div>
    """
    
    return complete_html

def _create_center_logo():
    """Create the center logo/indicator"""
    return '''
    <div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); 
                width: 80px; height: 80px; border-radius: 50%; 
                background: linear-gradient(135deg, #009CA6, #007A83); 
                display: flex; align-items: center; justify-content: center; 
                color: white; font-size: 28px; font-weight: bold; 
                box-shadow: 0 4px 16px rgba(0, 156, 166, 0.4); 
                z-index: 10; border: 3px solid white;" 
         title="GVC AI Mentor Roundtable">
        🎯
    </div>
    '''

def _create_avatar_html(agent, position, is_active=False, is_thinking=False):
    """Create HTML for a single avatar - using original working style"""
    # Determine CSS classes (original style)
    classes = ["avatar"]
    if is_thinking:
        classes.append("thinking")
    elif is_active:
        classes.append("active")
    
    # Try to use image if available, otherwise use emoji (original style)
    avatar_content = agent["avatar"]  # Start with emoji fallback
    
    if "image" in agent and agent["image"]:
        try:
            import os
            if os.path.exists(agent["image"]):
                image_base64 = get_image_base64(agent["image"])
                # Safety check: ensure image base64 is reasonable size (< 1MB)
                if image_base64 and len(image_base64) < 1000000:
                    avatar_content = f'<img src="data:image/png;base64,{image_base64}" alt="{agent["name"]}" />'
        except:
            pass  # Keep emoji fallback silently
    
    # Create the avatar HTML (original style)
    avatar_html = f'''<div class="{" ".join(classes)}" style="left: {position[0]:.1f}%; top: {position[1]:.1f}%;" title="{agent['name']} - {_get_agent_status(agent['name'], is_active, is_thinking)}">
    {avatar_content}
    <div class="avatar-label">{_shorten_name(agent['name'])}</div>
</div>'''
    
    return avatar_html

def _get_agent_status(agent_name, is_active, is_thinking):
    """Get status text for agent tooltip (original style)"""
    if is_thinking:
        return "Currently thinking..."
    elif is_active:
        return "Active speaker"
    else:
        return "Listening"

def _get_agent_person_name(agent_role):
    """Get the actual person name for each agent role"""
    person_names = {
        "Academic Mentor": "John Doe",
        "Career Guide": "Angela Smith", 
        "Tech Innovator": " Gregory Brown",
        "Wellness Coach": "Ana Maria",
        "Life Skills Mentor": "Sarah Chen",
        "Creative Mentor": "David Kim",
        "Leadership Coach": "Maria Garcia",
        "Financial Advisor": "Robert Johnson",
        "Communication Expert": "Lisa White",
        "Global Perspective Mentor": "Alex Martinez"
    }
    return person_names.get(agent_role, agent_role)

def _format_person_name_for_display(person_name):
    """Format person name for roundtable display"""
    # Split name and show first name + last initial for space
    name_parts = person_name.split()
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        if first_name.startswith("Dr."):
            # Handle titles like "Dr. Sarah"
            if len(name_parts) >= 3:
                first_name = name_parts[1]  # Get "Sarah" from "Dr. Sarah Chen"
                last_initial = name_parts[2][0] if name_parts[2] else ""
            else:
                first_name = name_parts[0]
                last_initial = name_parts[1][0] if len(name_parts) > 1 else ""
        else:
            last_initial = name_parts[-1][0] if name_parts[-1] else ""
        
        return f"{first_name}<br>{last_initial}."
    else:
        return person_name

def _shorten_name(name):
    """Format agent names for display in roundtable - now shows person names"""
    # Get the actual person name instead of role
    person_name = _get_agent_person_name(name)
    return _format_person_name_for_display(person_name)

def _render_roundtable_legend():
    """Render the roundtable legend"""
    st.markdown("### 🎯 Roundtable Legend")
    st.markdown("""
    - **🟢 Active**: Currently speaking agent
    - **🟡 Thinking**: Agent is preparing response
    - **⚪ Inactive**: Available agents
    """)

def get_image_base64(image_path):
    """Get base64 encoded image - safe fallback implementation"""
    try:
        import base64
        import os
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img_str = base64.b64encode(img_file.read()).decode()
                # Safety check for size
                if len(img_str) < 1000000:  # < 1MB
                    return img_str
        return None
    except Exception as e:
        logger.warning(f"Error loading image {image_path}: {e}")
        return None

def get_optimized_image_base64(image_path, target_size=(100, 100)):
    """Get optimized base64 encoded image for avatars - HIGH QUALITY"""
    try:
        import base64
        import os
        from PIL import Image
        import io
        import logging
        
        if not os.path.exists(image_path):
            logging.warning(f"Image not found: {image_path}")
            return None
        
        # Open and optimize image with better quality
        with Image.open(image_path) as img:
            # Preserve transparency for PNG logos if they have it
            if img.mode in ('RGBA', 'LA') and 'logo' in image_path.lower():
                # For logos, keep transparency and high quality
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                img_resized.save(buffer, format='PNG', optimize=True, compress_level=6)
                img_str = base64.b64encode(buffer.getvalue()).decode()
                
                # If PNG is too large, try WebP or high-quality JPEG
                if len(img_str) > 200000:  # 200KB limit for logos (increased)
                    rgb_img = img.convert('RGB')
                    rgb_resized = rgb_img.resize(target_size, Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    rgb_resized.save(buffer, format='JPEG', optimize=True, quality=92)
                    img_str = base64.b64encode(buffer.getvalue()).decode()
            else:
                # Convert to RGB with high quality
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to larger target size for better quality
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Convert to high-quality JPEG
                buffer = io.BytesIO()
                img_resized.save(buffer, format='JPEG', optimize=True, quality=92)
                img_str = base64.b64encode(buffer.getvalue()).decode()
            
            # Only reduce quality if absolutely necessary
            if len(img_str) > 300000:  # 300KB (increased from 100KB)
                logging.warning(f"Image {image_path} large after optimization: {len(img_str)} chars")
                # Try with slightly smaller size but maintain quality
                smaller_size = (80, 80)
                img_smaller = img.resize(smaller_size, Image.Resampling.LANCZOS)
                if img_smaller.mode != 'RGB':
                    img_smaller = img_smaller.convert('RGB')
                buffer_smaller = io.BytesIO()
                img_smaller.save(buffer_smaller, format='JPEG', optimize=True, quality=88)
                img_str = base64.b64encode(buffer_smaller.getvalue()).decode()
            
            logging.info(f"Optimized {image_path}: {len(img_str)} chars")
            return img_str
            
    except Exception as e:
        logging.warning(f"Error optimizing image {image_path}: {e}")
        return None

def _create_center_logo_with_image():
    """Create center logo with GVC logo image"""
    import os
    import base64
    import logging
    
    logo_path = "gvc_logo.png"
    
    # Try to load GVC logo
    logo_content = "🎯"  # Default fallback
    
    try:
        if os.path.exists(logo_path):
            # Try to get optimized image with PNG preservation for transparency
            logo_base64 = get_optimized_image_base64(logo_path, target_size=(50, 50))
            if logo_base64:
                # Check if we got PNG (for transparency) or JPEG
                if 'logo' in logo_path.lower():
                    # For logos with potential transparency, try PNG first
                    logo_content = f'<img src="data:image/png;base64,{logo_base64}" alt="GVC Logo" style="width: 50px; height: 50px; object-fit: contain;" />'
                else:
                    logo_content = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="GVC Logo" style="width: 50px; height: 50px; object-fit: contain;" />'
                logging.info("✅ GVC logo loaded successfully for roundtable center")
            else:
                # Fallback: try basic base64 encoding
                with open(logo_path, "rb") as img_file:
                    basic_base64 = base64.b64encode(img_file.read()).decode()
                    if len(basic_base64) < 500000:  # Under 500KB
                        logo_content = f'<img src="data:image/png;base64,{basic_base64}" alt="GVC Logo" style="width: 50px; height: 50px; object-fit: contain;" />'
                        logging.info("✅ GVC logo loaded with basic encoding")
        else:
            logging.warning(f"❌ GVC logo file not found at: {logo_path}")
    except Exception as e:
        logging.warning(f"❌ Could not load GVC logo: {e}")
    
    return f"""
    <div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
                width: 70px; height: 70px; border-radius: 50%;
                background: linear-gradient(135deg, #009CA6, #007A83);
                display: flex; align-items: center; justify-content: center;
                color: white; font-size: 18px; font-weight: bold;
                box-shadow: 0 6px 18px rgba(0, 156, 166, 0.5);
                z-index: 10; border: 3px solid white;
                overflow: hidden;"
         title="GVC AI Mentor Roundtable">
        {logo_content}
    </div>
    """

def render_report_generation_section():
    """Render the report generation section at the end of the roundtable page"""
    # Add custom CSS for report section
    st.markdown("""
    <style>
    .report-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .report-section h3 {
        margin: 0;
        display: flex;
        align-items: center;
        font-size: 26px;
        font-weight: bold;
    }
    .report-section p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 16px;
    }
    .report-info-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .report-warning {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #ff6b6b;
    }
    .report-info {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #17a2b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="report-section">
        <h3>📊 Generate Discussion Report</h3>
        <p>Create a comprehensive report based on your roundtable discussion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have required data
    chat_history = st.session_state.get('chat_history', [])
    student_data = st.session_state.get('student_data', {})
    
    if not chat_history:
        st.markdown("""
        <div class="report-warning">
            <h4>📝 No Discussion History Found</h4>
            <p>Please start a discussion with the mentors first to generate a meaningful report.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not student_data:
        st.markdown("""
        <div class="report-warning">
            <h4>👤 No Student Profile Found</h4>
            <p>Please complete your profile first to generate a personalized report.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Report generation controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 📋 Report Options")
        include_full_chat = st.checkbox("Include full chat transcript", value=False)
        report_format = st.selectbox(
            "Report format:",
            ["HTML Preview", "PDF Download", "Both"],
            help="Choose how you want to receive your report"
        )
    
    with col2:
        st.markdown("### 📈 Discussion Stats")
        st.metric("Total Messages", len(chat_history))
        unique_agents = len(set(msg.get('role', '') for msg in chat_history if msg.get('role', '') not in ['User', 'System']))
        st.metric("Active Mentors", unique_agents)
    
    with col3:
        st.markdown("### 🎯 Student Profile")
        student_name = student_data.get('name', 'Unknown')
        st.write(f"**Name:** {student_name}")
        st.write(f"**Grade:** {student_data.get('grade_level', 'N/A')}")
        st.write(f"**ID:** {student_data.get('gvc_id', 'N/A')}")
    
    # Generate report button
    st.markdown("---")
    
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        with st.spinner("🔄 Generating your personalized report..."):
            try:
                # Import ReportGenerator and vector store utilities
                from agents.report_generator import ReportGenerator
                from utils.vector_store import get_context_chunks
                
                # Initialize report generator
                report_generator = ReportGenerator()
                
                # Get context chunks from vector store
                try:
                    # Use student data and chat history to generate relevant context query
                    context_query = f"student development education mentoring {student_data.get('interests', '')} {student_data.get('goals', '')}"
                    context_chunks = get_context_chunks(context_query, k=5)
                except Exception as context_error:
                    st.warning(f"Could not load context from vector store: {context_error}")
                    context_chunks = "GVC AI Mentor Roundtable Discussion Context"
                
                # Generate enhanced report with professional CSV-style formatting
                report_result = report_generator.generate_csv_style_report(
                    chat_history, student_data, context_chunks
                )
                
                if report_result['success']:
                    # Display based on format selection
                    if report_format in ["HTML Preview", "Both"]:
                        st.success("✅ Report generated successfully!")
                        st.markdown("### 📖 Professional Report Preview")
                        
                        # Use components if available, otherwise show download option
                        if components:
                            components.html(report_result['html'], height=700, scrolling=True)
                        else:
                            st.info("📄 HTML preview not available. Please download the report to view.")
                            st.download_button(
                                label="📥 Download HTML Report",
                                data=report_result['html'],
                                file_name=f"GVC_Report_{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                mime="text/html",
                                use_container_width=True
                            )
                    
                    if report_format in ["PDF Download", "Both"] and report_result['pdf']:
                        # Create download button for PDF
                        st.download_button(
                            label="📥 Download Professional PDF Report",
                            data=report_result['pdf'],
                            file_name=f"GVC_Roundtable_Report_{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    elif report_format in ["PDF Download", "Both"] and not report_result['pdf']:
                        st.warning("⚠️ PDF generation encountered issues. HTML preview is available.")
                        if report_format == "PDF Download":
                            st.markdown("### 📖 Report Preview (HTML)")
                            if components:
                                components.html(report_result['html'], height=700, scrolling=True)
                            else:
                                st.download_button(
                                    label="📥 Download HTML Report",
                                    data=report_result['html'],
                                    file_name=f"GVC_Report_{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                    mime="text/html",
                                    use_container_width=True
                                )
                
                else:
                    st.error(f"❌ {report_result['message']}")
                
                # Additional options
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Regenerate Report", type="secondary", use_container_width=True):
                        st.rerun()
                with col2:
                    if st.button("📧 Email Report", type="secondary", use_container_width=True):
                        st.info("📧 Email functionality coming soon!")
                    
            except Exception as e:
                st.error(f"❌ Error generating report: {e}")
                st.info("Please ensure all required dependencies are installed and try again.")
                
                # Show debug info in expander
                with st.expander("🔍 Debug Information"):
                    st.write(f"**Error:** {str(e)}")
                    st.write(f"**Chat History Length:** {len(chat_history)}")
                    st.write(f"**Student Data Keys:** {list(student_data.keys())}")
                    st.code(traceback.format_exc())
    
    # Additional info
    st.markdown("---")
    st.markdown("""
    <div class="report-info">
        <h4 style="color: #007bff; margin: 0 0 10px 0;">ℹ️ About Report Generation</h4>
        <p style="margin: 0; color: #555; line-height: 1.6;">
            The report analyzes your discussion with AI mentors to provide personalized insights, 
            recommendations, and action items for your educational and career development. 
            The report includes academic performance analysis, personal development insights, 
            and concrete next steps based on your conversation.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_roundtable_page():
    """Main function to render the complete roundtable page with avatar images"""
    try:
        # Load vectorstore
        vectordb, _ = load_vectorstore()
        
        # Initialize session state with vectordb
        initialize_session_state(vectordb)
        
        # Create role to image mapping
        role_to_image = create_role_to_image_mapping()
        
        # Load student data from session state if available
        student_data = st.session_state.get('student_data', {})
        if not student_data:
            # Try to load from other possible session state keys
            student_data = st.session_state.get('user_profile', {})
        
        # Apply global CSS
        st.markdown(ROUNDTABLE_CSS, unsafe_allow_html=True)
        
        # Main layout with sidebar and content
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Sidebar content
            render_sidebar()
            
            # Roundtable controls
            render_roundtable_controls()
        
        with col2:
            # Main content area - START WITH ROUNDTABLE AT TOP
            st.markdown('<div class="main-content">', unsafe_allow_html=True)
            
            # Roundtable visualization - PROMINENT AT TOP WITH AVATAR IMAGES
            render_roundtable()
            
            # Discussion status
            render_status_display()
            
            # Chat history display
            render_chat_history(role_to_image)
            
            # Handle agent logic
            handle_agent_logic(get_context_chunks, role_to_image)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate Report section - MOVED BEFORE MENTOR PROFILES
        st.markdown("---")
        render_report_generation_section()
        
        # Full-width mentor profiles section at bottom
        st.markdown("---")
        st.markdown('<div class="full-width-mentor-profiles">', unsafe_allow_html=True)
        
        # Mentor profiles (full width)
        render_mentor_profiles()
        
        st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error rendering roundtable page: {e}")
        logging.error(f"Error in render_roundtable_page: {e}")
        import traceback
        st.code(traceback.format_exc())

# Main function call for compatibility
if __name__ == "__main__":
    render_roundtable_page()

def test_logo_loading():
    """Test function to debug logo loading"""
    import os
    import logging
    
    logo_path = "gvc_logo.png"
    logging.info(f"🔍 Testing logo loading from: {logo_path}")
    
    # Check if file exists
    if os.path.exists(logo_path):
        logging.info(f"✅ Logo file found at: {os.path.abspath(logo_path)}")
        file_size = os.path.getsize(logo_path)
        logging.info(f"📏 Logo file size: {file_size} bytes")
        
        # Test image loading
        try:
            logo_base64 = get_optimized_image_base64(logo_path, target_size=(50, 50))
            if logo_base64:
                logging.info(f"✅ Logo successfully converted to base64: {len(logo_base64)} chars")
                return True
            else:
                logging.warning(f"❌ Failed to convert logo to base64")
                return False
        except Exception as e:
            logging.error(f"❌ Error processing logo: {e}")
            return False
    else:
        logging.error(f"❌ Logo file not found at: {os.path.abspath(logo_path)}")
        return False
