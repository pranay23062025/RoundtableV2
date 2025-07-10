import streamlit as st
from core.session_manager import reset_chat_session, update_agent_status
from config.settings import MAX_AGENT_TURNS

def render_control_buttons():
    """Render chat control buttons"""
    st.markdown("### 🎮 Discussion Controls")
    
    # Create button columns
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    # Get current status - FIX: Don't override agents_paused with update_agent_status()
    chat_running = getattr(st.session_state, 'chat_running', False)
    agents_paused = getattr(st.session_state, 'agents_paused', False)  # Use session state directly
    has_student_data = st.session_state.student_data is not None
    consecutive_turns = getattr(st.session_state, 'consecutive_agent_turns', 0)
    
    # DEBUG - Add temporarily to see values
    #st.write(f"🔍 DEBUG: chat_running={chat_running}, agents_paused={agents_paused}, has_student_data={has_student_data}")
    
    # Start Discussion Button
    with col1:
        start_disabled = chat_running or not has_student_data
        start_help = _get_button_help_text("start", start_disabled, has_student_data, chat_running)
        
        if st.button(
            "🚀 Start Discussion", 
            type="primary",
            disabled=start_disabled,
            help=start_help,
            use_container_width=True
        ):
            _handle_start_discussion()
    
    # Pause Discussion Button  
    with col2:
        pause_disabled = not chat_running or agents_paused
        pause_help = _get_button_help_text("pause", pause_disabled, has_student_data, chat_running)
        
        if st.button(
            "⏸️ Pause Discussion",
            type="secondary", 
            disabled=pause_disabled,
            help=pause_help,
            use_container_width=True
        ):
            _handle_pause_discussion()

    # Resume Discussion Button
    with col3:
        # FIXED: Resume should be enabled when discussion is paused (not running but agents_paused is True)
        resume_disabled = chat_running or not has_student_data or (not agents_paused and len(st.session_state.get('chat_history', [])) == 0)
        resume_help = _get_button_help_text("resume", resume_disabled, has_student_data, chat_running)
        
        if st.button(
            "▶️ Resume Discussion",
            disabled=resume_disabled,
            help=resume_help,
            use_container_width=True
        ):
            _handle_resume_discussion()
    
    # Clear Chat Button
    with col4:
        clear_disabled = not st.session_state.get('chat_history', [])
        clear_help = _get_button_help_text("clear", clear_disabled, has_student_data, chat_running)
        
        if st.button(
            "🗑️ Clear Chat",
            disabled=clear_disabled,
            help=clear_help,
            use_container_width=True
        ):
            _handle_clear_chat()
    
    # Display control status
    _render_control_status(agents_paused, chat_running, consecutive_turns)

def _get_button_help_text(button_type, disabled, has_student_data, chat_running):
    """Get help text for buttons based on current state"""
    if button_type == "start":
        if not has_student_data:
            return "❌ Please enter student information first"
        elif chat_running:
            return "❌ Discussion is already running"
        else:
            return "✅ Start the AI mentor discussion"
    
    elif button_type == "pause":
        if not chat_running:
            return "❌ Discussion is not running"
        else:
            return "✅ Pause the discussion to interact"
    
    elif button_type == "resume":
        if not has_student_data:
            return "❌ Please enter student information first"
        elif chat_running:
            return "❌ Discussion is already running"
        else:
            return "✅ Resume the AI mentor discussion"
    
    elif button_type == "clear":
        if disabled:
            return "❌ No chat history to clear"
        else:
            return "✅ Clear all chat messages"
    
    return ""

def _handle_start_discussion():
    """Handle start discussion button click"""
    try:
        st.session_state.chat_running = True
        st.session_state.consecutive_agent_turns = 0
        st.session_state.pending_agent_message = None
        st.session_state.agent_turn_in_progress = False
        st.session_state.thinking_agent = None
        st.session_state.message_streaming = False
        
        # Ensure we have a current agent
        if not getattr(st.session_state, 'current_agent', None):
            st.session_state.current_agent = "Academic Mentor"
        
        st.success("🚀 Discussion started! The AI mentors will begin their roundtable.")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error starting discussion: {str(e)}")

def _handle_pause_discussion():
    """Handle pause discussion button click"""
    try:
        # Set states in the correct order
        st.session_state.chat_running = False
        st.session_state.agents_paused = True
        st.session_state.thinking_agent = None
        st.session_state.agent_turn_in_progress = False
        st.session_state.message_streaming = False
        
        st.info("⏸️ Discussion paused. You can now send a message or generate a report.")
        st.rerun()  # Force immediate rerun
        
    except Exception as e:
        st.error(f"❌ Error pausing discussion: {str(e)}")

def _handle_resume_discussion():
    """Handle resume discussion button click"""
    try:
        # Set states in the correct order
        st.session_state.agents_paused = False
        st.session_state.chat_running = True
        st.session_state.agent_turn_in_progress = False
        st.session_state.thinking_agent = None
        st.session_state.message_streaming = False
        st.session_state.consecutive_agent_turns = 0
        
        # Fix: Properly select next agent
        if hasattr(st.session_state, 'orchestrator') and st.session_state.orchestrator:
            if st.session_state.chat_history:
                st.session_state.current_agent = st.session_state.orchestrator.select_next_agent(
                    st.session_state.chat_history
                )
            else:
                available_agents = [agent["name"] for agent in st.session_state.get('agents_info', [])]
                if available_agents:
                    st.session_state.current_agent = available_agents[0]
                else:
                    st.session_state.current_agent = "Academic Mentor"
        else:
            st.session_state.current_agent = "Academic Mentor"
        
        st.success("▶️ Discussion resumed! The AI mentors will continue their conversation.")
        st.rerun()  # Force immediate rerun
        
    except Exception as e:
        st.error(f"❌ Error resuming discussion: {str(e)}")

def _handle_clear_chat():
    """Handle clear chat button click"""
    try:
        # Confirm before clearing
        if st.session_state.get('confirm_clear', False):
            reset_chat_session()
            st.session_state.confirm_clear = False
            st.success("🗑️ Chat cleared successfully!")
            st.rerun()
        else:
            st.session_state.confirm_clear = True
            st.warning("⚠️ Click 'Clear Chat' again to confirm. This will delete all messages.")
            
    except Exception as e:
        st.error(f"❌ Error clearing chat: {str(e)}")

def _render_control_status(agents_paused, chat_running, consecutive_turns):
    """Render current control status"""
    # Custom CSS for compact spacing
    st.markdown("""
    <style>
    .status-container {
        margin-top: 8px;
        margin-bottom: 8px;
        padding: 12px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        border: 1px solid #E5E8EC;
    }
    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0;
    }
    .status-item {
        font-size: 14px;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Determine status
    if chat_running:
        status_text = "🟢 <strong>Discussion Active</strong>"
    elif agents_paused:
        status_text = "🟡 <strong>Discussion Paused</strong>"
    else:
        status_text = "🔴 <strong>Discussion Stopped</strong>"
    
    current_agent = getattr(st.session_state, 'current_agent', 'None')
    
    # Compact status display - FIXED: Use HTML <strong> instead of markdown **
    st.markdown(f"""
    <div class="status-container">
        <div class="status-row">
            <span class="status-item">{status_text}</span>
            <span class="status-item">🎯 <strong>Current:</strong> {current_agent}</span>
            <span class="status-item">🔢 <strong>Turns:</strong> {consecutive_turns}/{MAX_AGENT_TURNS}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar for agent turns (only if needed)
    if consecutive_turns > 0:
        progress = min(consecutive_turns / MAX_AGENT_TURNS, 1.0)
        st.progress(progress, text=f"Agent turns: {consecutive_turns}/{MAX_AGENT_TURNS}")
        
        if consecutive_turns >= MAX_AGENT_TURNS:
            st.info("ℹ️ Agents have reached the turn limit. Send a message to continue or resume discussion.")

def render_advanced_controls():
    """Render advanced control options (optional)"""
    with st.expander("⚙️ Advanced Controls"):
        st.markdown("### 🔧 Advanced Options")
        
        # Agent selection
        available_agents = [agent["name"] for agent in st.session_state.get('agents_info', [])]
        if available_agents:
            selected_agents = st.multiselect(
                "Select Active Agents",
                options=available_agents,
                default=available_agents,
                help="Choose which agents participate in the discussion"
            )
            
            if st.button("Update Agent Selection"):
                st.session_state.selected_agents = selected_agents
                st.success(f"✅ Updated to {len(selected_agents)} active agents")
        
        # Discussion settings
        auto_advance = st.checkbox(
            "Auto-advance conversation",
            value=st.session_state.get('auto_advance', True),
            help="Automatically move to next agent after each message"
        )
        st.session_state.auto_advance = auto_advance
        
        # Speed control
        speed = st.select_slider(
            "Discussion Speed",
            options=["Slow", "Normal", "Fast"],
            value="Normal",
            help="Control how quickly agents respond"
        )
        
        # Speed mapping
        speed_mapping = {
            "Slow": 2.0,
            "Normal": 1.0, 
            "Fast": 0.5
        }
        st.session_state.agent_delay = speed_mapping[speed]
        
        # Emergency reset
        st.markdown("---")
        st.markdown("### 🚨 Emergency Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset Session", type="secondary"):
                # Full session reset
                for key in list(st.session_state.keys()):
                    if key not in ['student_data']:  # Preserve student data
                        del st.session_state[key]
                st.success("🔄 Session reset complete")
                st.rerun()
        
        with col2:
            if st.button("🆘 Force Stop", type="secondary"):
                # Force stop all processes
                st.session_state.chat_running = False
                st.session_state.agent_turn_in_progress = False
                st.session_state.thinking_agent = None
                st.session_state.message_streaming = False
                st.warning("🆘 All processes stopped")

def get_control_state_summary():
    """Get summary of current control state"""
    return {
        "chat_running": getattr(st.session_state, 'chat_running', False),
        "agents_paused": update_agent_status(),
        "consecutive_turns": getattr(st.session_state, 'consecutive_agent_turns', 0),
        "current_agent": getattr(st.session_state, 'current_agent', None),
        "thinking_agent": getattr(st.session_state, 'thinking_agent', None),
        "has_student_data": st.session_state.student_data is not None,
        "chat_history_length": len(st.session_state.get('chat_history', []))
    }