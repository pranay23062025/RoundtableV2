import streamlit as st
from agents.agent_orchestrator import AgentOrchestrator
from agents.report_generator import ReportGenerator
from config.settings import MAX_AGENT_TURNS, AGENTS_INFO

def initialize_session_state(vectordb):
    """Initialize all session state variables with enhanced orchestrator"""
    
    # Chat state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = "Academic Mentor"
    if 'chat_running' not in st.session_state:
        st.session_state.chat_running = False
    # Don't overwrite existing student_data - only initialize if truly missing
    # This preserves the data from the data_input page
    if 'student_data' not in st.session_state or st.session_state.student_data is None:
        st.session_state.student_data = None
    
    # Enhanced Agent orchestration with improved flow control
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = AgentOrchestrator(vectordb=vectordb)
    if 'report_generator' not in st.session_state:
        st.session_state.report_generator = ReportGenerator()
    
    # Enhanced conversation state tracking
    if 'conversation_state' not in st.session_state:
        st.session_state.conversation_state = {
            "phase": "opening",
            "rounds_completed": 0,
            "agent_participation": {},
            "last_three_agents": [],
            "topic_coverage": set(),
            "interaction_quality": []
        }
    
    # Agent turn management
    if 'consecutive_agent_turns' not in st.session_state:
        st.session_state.consecutive_agent_turns = 0
    if 'pending_agent_message' not in st.session_state:
        st.session_state.pending_agent_message = None
    if 'agent_turn_in_progress' not in st.session_state:
        st.session_state.agent_turn_in_progress = False
    if 'thinking_agent' not in st.session_state:
        st.session_state.thinking_agent = None
    if 'roundtable_message' not in st.session_state:
        st.session_state.roundtable_message = ""
    if 'message_streaming' not in st.session_state:
        st.session_state.message_streaming = False
    
    # Legacy conversation tracking (keep for compatibility)
    if 'conversation_topics' not in st.session_state:
        st.session_state.conversation_topics = set()
    if 'agent_message_history' not in st.session_state:
        st.session_state.agent_message_history = {}
    if 'conversation_phase' not in st.session_state:
        st.session_state.conversation_phase = "initial"
    
    # UI state
    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = [agent["name"] for agent in AGENTS_INFO]
    if 'auto_advance' not in st.session_state:
        st.session_state.auto_advance = True
    if 'last_user_message_time' not in st.session_state:
        st.session_state.last_user_message_time = None

def reset_chat_session():
    """Reset chat session state"""
    st.session_state.chat_history = []
    st.session_state.consecutive_agent_turns = 0
    st.session_state.pending_agent_message = None
    st.session_state.agent_turn_in_progress = False
    st.session_state.thinking_agent = None
    st.session_state.conversation_topics = set()
    st.session_state.agent_message_history = {}
    st.session_state.conversation_phase = "initial"
    st.session_state.roundtable_message = ""
    st.session_state.message_streaming = False
    st.session_state.chat_running = False
    st.session_state.current_agent = "Academic Mentor"

def update_agent_status():
    """Update agent status and return if paused"""
    agents_paused = False
    
    # Check if agents should pause due to turn limit
    if st.session_state.consecutive_agent_turns >= MAX_AGENT_TURNS:
        agents_paused = True
        st.session_state.chat_running = False
        st.session_state.thinking_agent = None
        st.session_state.agent_turn_in_progress = False
        st.session_state.message_streaming = False
    else:
        agents_paused = not st.session_state.chat_running
    
    return agents_paused

def get_session_summary():
    """Get a summary of the current session state"""
    return {
        "chat_messages": len(st.session_state.chat_history),
        "current_agent": st.session_state.current_agent,
        "chat_running": st.session_state.chat_running,
        "consecutive_turns": st.session_state.consecutive_agent_turns,
        "conversation_phase": st.session_state.conversation_phase,
        "topics_covered": list(st.session_state.conversation_topics),
        "agents_with_history": list(st.session_state.agent_message_history.keys())
    }

def validate_session_state():
    """Validate and fix any corrupted session state"""
    try:
        # Ensure required attributes exist
        required_attrs = [
            'chat_history', 'current_agent', 'chat_running', 'student_data',
            'consecutive_agent_turns', 'agent_turn_in_progress', 'thinking_agent'
        ]
        
        for attr in required_attrs:
            if attr not in st.session_state:
                if attr == 'chat_history':
                    st.session_state.chat_history = []
                elif attr == 'current_agent':
                    st.session_state.current_agent = "Academic Mentor"
                elif attr in ['chat_running', 'agent_turn_in_progress']:
                    setattr(st.session_state, attr, False)
                elif attr == 'consecutive_agent_turns':
                    st.session_state.consecutive_agent_turns = 0
                else:
                    setattr(st.session_state, attr, None)
        
        # Validate current agent
        valid_agents = [agent["name"] for agent in AGENTS_INFO]
        if st.session_state.current_agent not in valid_agents:
            st.session_state.current_agent = valid_agents[0]
        
        # Validate consecutive turns
        if st.session_state.consecutive_agent_turns < 0:
            st.session_state.consecutive_agent_turns = 0
        elif st.session_state.consecutive_agent_turns > MAX_AGENT_TURNS:
            st.session_state.consecutive_agent_turns = MAX_AGENT_TURNS
            st.session_state.chat_running = False
        
        return True
        
    except Exception as e:
        st.error(f"Session state validation error: {e}")
        return False

def cleanup_session_state():
    """Clean up session state to prevent memory issues"""
    # Limit chat history size
    max_history = 100
    if len(st.session_state.chat_history) > max_history:
        st.session_state.chat_history = st.session_state.chat_history[-max_history:]
    
    # Limit agent message history
    max_agent_history = 5
    for agent_name in st.session_state.agent_message_history:
        if len(st.session_state.agent_message_history[agent_name]) > max_agent_history:
            st.session_state.agent_message_history[agent_name] = \
                st.session_state.agent_message_history[agent_name][-max_agent_history:]

def export_session_data():
    """Export session data for debugging or backup"""
    import json
    from datetime import datetime
    
    session_data = {
        "timestamp": datetime.now().isoformat(),
        "chat_history": st.session_state.chat_history,
        "student_data": st.session_state.student_data,
        "session_summary": get_session_summary(),
        "conversation_topics": list(st.session_state.conversation_topics),
        "agent_message_history": st.session_state.agent_message_history
    }
    
    return json.dumps(session_data, indent=2, default=str)