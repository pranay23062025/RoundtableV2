import streamlit as st
import time
from config.settings import MAX_AGENT_TURNS, ROLE_TO_AVATAR, STREAMING_DELAY
from core.avatar_manager import get_avatar_for_role
from core.chat_logic import process_agent_turn, handle_message_completion
from utils.chat_utils import format_message

def render_user_input():
    """Render user input section"""
    st.markdown("### 💬 Join the Discussion")
    
    # Check if user can send messages
    agents_paused = (
        not st.session_state.get('chat_running', False) or
        st.session_state.get('consecutive_agent_turns', 0) >= MAX_AGENT_TURNS
    )
    
    # User input area
    if agents_paused:
        st.markdown("✅ **You can now send a message to the mentors**")
    else:
        st.markdown("⏳ **Agents are discussing - please wait for them to pause**")
    
    # Input field
    user_message = st.text_area(
        "Your message:",
        key="user_input",
        disabled=not agents_paused,
        placeholder="Type your question or comment here..." if agents_paused else "Please wait for agents to pause...",
        height=100,
        help="Enter your message to join the discussion" if agents_paused else "You can only send messages when agents are paused"
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_button = st.button(
            "📤 Send Message",
            disabled=not agents_paused or not user_message.strip(),
            help="Send your message to the AI mentors" if agents_paused else "Wait for agents to pause",
            use_container_width=True,
            type="primary"
        )
    
    # Character counter
    if user_message:
        char_count = len(user_message)
        max_chars = 1000
        
        if char_count > max_chars:
            st.error(f"❌ Message too long ({char_count}/{max_chars} characters)")
        else:
            color = "green" if char_count < max_chars * 0.8 else "orange"
            st.markdown(f"<span style='color: {color}; font-size: 0.8em;'>Characters: {char_count}/{max_chars}</span>", unsafe_allow_html=True)
    
    return send_button and user_message.strip() and agents_paused, user_message

def render_chat_history(role_to_image):
    """Render chat message history"""
    if not st.session_state.get('chat_history', []):
        st.markdown("### 💭 Discussion Will Appear Here")
        st.info("👋 Welcome! Start the discussion to see the AI mentors' conversation.")
        return
    
    st.markdown("### 💬 Live Discussion")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for i, msg in enumerate(st.session_state.chat_history):
            _render_single_message(msg, role_to_image, i)
    
    # Auto-scroll indicator
    if st.session_state.get('chat_running', False):
        st.markdown("📡 *Live discussion in progress...*")

def _render_single_message(msg, role_to_image, message_index):
    """Render a single chat message"""
    role = msg.get("role", "Unknown")
    content = msg.get("content", "")
    timestamp = msg.get("timestamp", "")
    
    # Get avatar for role
    avatar = get_avatar_for_role(role, role_to_image)
    
    # Create message container
    with st.chat_message(name=role, avatar=avatar):
        # Message header with role badge
        if role != "User":
            # Extract agent name and position for better display
            person_name = _get_agent_person_name(role)
            agent_position = _extract_agent_position(role)
            display_name = f"{person_name} - {agent_position}"
            st.markdown(
                f'<div class="mentor-name-badge">{_get_role_emoji(role)} {display_name}</div>', 
                unsafe_allow_html=True
            )
        else:
            student_name = _get_student_name()
            st.markdown(
                f'<div class="user-name-badge">👤 {student_name}</div>', 
                unsafe_allow_html=True
            )
        
        # Message content
        if role == st.session_state.get('thinking_agent') and message_index == len(st.session_state.chat_history) - 1:
            # Show streaming effect for current message
            _render_streaming_message(content)
        else:
            # Show complete message
            st.markdown(content)
        
        # Message metadata (optional)
        if st.session_state.get('show_timestamps', False) and timestamp:
            st.caption(f"⏰ {timestamp}")

def _render_streaming_message(content):
    """Render message with streaming effect"""
    placeholder = st.empty()
    
    # Get current streaming progress
    streaming_progress = st.session_state.get('roundtable_message', '')
    
    if streaming_progress:
        placeholder.markdown(streaming_progress)
    else:
        placeholder.markdown(content)

def render_status_display():
    """Render current discussion status"""
    from core.session_manager import update_agent_status
    
    # Get current status
    agents_paused = update_agent_status()
    chat_running = st.session_state.get('chat_running', False)
    current_agent = st.session_state.get('current_agent')
    thinking_agent = st.session_state.get('thinking_agent')
    consecutive_turns = st.session_state.get('consecutive_agent_turns', 0)
    
    # Status container
    status_container = st.container()
    
    with status_container:
        if chat_running and thinking_agent:
            agent_avatar = ROLE_TO_AVATAR.get(thinking_agent, "❓")
            st.success(f"🟢 **Agents are actively discussing** | {agent_avatar} **{thinking_agent}** is thinking...")
            
        elif chat_running and current_agent and st.session_state.get('agent_turn_in_progress'):
            agent_avatar = ROLE_TO_AVATAR.get(current_agent, "❓")
            st.success(f"🟢 **Agents are actively discussing** | {agent_avatar} **{current_agent}** is preparing to speak...")
            
        elif chat_running and current_agent:
            agent_avatar = ROLE_TO_AVATAR.get(current_agent, "❓")
            st.success(f"🟢 **Agents are actively discussing** | Next up: {agent_avatar} **{current_agent}**")
            
        elif agents_paused and st.session_state.get('chat_history'):
            if current_agent:
                agent_avatar = ROLE_TO_AVATAR.get(current_agent, "❓")
                st.warning(f"⏸️ **Agents paused after {consecutive_turns} messages** | Next: {agent_avatar} **{current_agent}** | Enter message or resume discussion")
            else:
                st.warning(f"⏸️ **Agents paused after {consecutive_turns} messages** | Enter message or resume discussion")
                
        else:
            if current_agent:
                agent_avatar = ROLE_TO_AVATAR.get(current_agent, "❓")
                st.info(f"⏹️ **Ready to start discussion** | First speaker: {agent_avatar} **{current_agent}**")
            else:
                st.info("⏹️ **Ready to start discussion**")

def handle_agent_logic(get_context_chunks, role_to_image):
    """Handle agent conversation logic"""
    if not st.session_state.get('chat_running', False) or not st.session_state.get('student_data'):
        return
    
    try:
        # Process agent turn
        message_content = process_agent_turn(get_context_chunks)
        
        if message_content:
            # Clear thinking state
            st.session_state.thinking_agent = None
            
            # Get avatar for current agent
            current_agent = st.session_state.get('current_agent')
            avatar = get_avatar_for_role(current_agent, role_to_image)
            
            # Display message with streaming effect
            with st.chat_message(name=current_agent, avatar=avatar):
                # Agent name badge with position
                person_name = _get_agent_person_name(current_agent)
                agent_position = _extract_agent_position(current_agent)
                display_name = f"{person_name} - {agent_position}"
                st.markdown(
                    f'<div class="mentor-name-badge">{_get_role_emoji(current_agent)} {display_name}</div>', 
                    unsafe_allow_html=True
                )
                
                # Stream the message
                chat_placeholder = st.empty()
                _stream_message_content(message_content, chat_placeholder)
            
            # Handle message completion
            handle_message_completion(message_content)
            
    except Exception as e:
        st.error(f"❌ Error in agent logic: {str(e)}")
        # Reset states on error
        st.session_state.chat_running = False
        st.session_state.thinking_agent = None
        st.session_state.agent_turn_in_progress = False

def _stream_message_content(message_content, placeholder):
    """Stream message content word by word"""
    displayed_content = ""
    words = message_content.split()
    
    for i, word in enumerate(words):
        displayed_content += word + " "
        placeholder.markdown(displayed_content)
        
        # Update roundtable message for streaming effect
        st.session_state.roundtable_message = displayed_content
        
        # Small delay between words
        time.sleep(STREAMING_DELAY)
    
    # Clear streaming state
    st.session_state.roundtable_message = ""

def handle_user_message(user_interrupted, user_message):
    """Handle user message input with enhanced orchestrator integration"""
    if user_interrupted and user_message and user_message.strip():
        try:
            # Add user message to chat history
            from utils.chat_utils import format_message
            from datetime import datetime
            
            user_msg = format_message("User", user_message.strip())
            st.session_state.chat_history.append(user_msg)
            
            # Reset agent conversation state for user input
            st.session_state.consecutive_agent_turns = 0
            st.session_state.chat_running = True
            st.session_state.agent_turn_in_progress = False
            st.session_state.thinking_agent = None
            st.session_state.message_streaming = False
            
            # Use enhanced orchestrator to select responding agent based on user message
            if hasattr(st.session_state.orchestrator, 'intelligent_agent_selection'):
                responding_agent = st.session_state.orchestrator.intelligent_agent_selection(
                    st.session_state.chat_history, 
                    user_message
                )
            else:
                # Fallback to regular selection
                responding_agent = st.session_state.orchestrator.select_next_agent(
                    st.session_state.chat_history, 
                    user_message
                )
            
            st.session_state.current_agent = responding_agent
            
            # Update orchestrator conversation state if available
            if hasattr(st.session_state.orchestrator, 'update_conversation_state'):
                st.session_state.orchestrator.update_conversation_state("User", user_message)
            
            # Clear input and restart
            st.session_state.user_input = ""
            st.success(f"✅ Message sent! **{responding_agent}** will respond to your question.")
            
            # Brief pause then rerun
            import time
            time.sleep(0.5)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing your message: {str(e)}")
            
def _get_role_emoji(role):
    """Get emoji for a role"""
    return ROLE_TO_AVATAR.get(role, "❓")

def _extract_agent_position(role):
    """Extract position/title from agent role name"""
    position_mappings = {
        "Academic Mentor": "Academic Guidance Specialist",
        "Career Guide": "Career Planning Expert", 
        "Tech Innovator": "Technology Innovation Advisor",
        "Wellness Coach": "Health & Wellness Specialist",
        "Life Skills Mentor": "Life Skills Development Coach",
        "Creative Mentor": "Creative Development Specialist",
        "Leadership Coach": "Leadership Development Expert",
        "Financial Advisor": "Financial Planning Specialist",
        "Communication Expert": "Communication Skills Coach",
        "Global Perspective Mentor": "Global Awareness Advisor"
    }
    return position_mappings.get(role, "AI Mentor")

def _get_agent_person_name(role):
    """Get the actual person name for each agent role"""
    person_names = {
        "Academic Mentor": "John Doe",
        "Career Guide": "Angela Smith", 
        "Tech Innovator": "Gregory Brown",
        "Wellness Coach": "Ana Maria",
        "Life Skills Mentor": "Sarah Chen",
        "Creative Mentor": "David Kim",
        "Leadership Coach": "Maria Garcia",
        "Financial Advisor": "Robert Johnson",
        "Communication Expert": "Lisa White",
        "Global Perspective Mentor": "Alex Martinez"
    }
    return person_names.get(role, role)

def _get_student_name():
    """Get student name for display"""
    if st.session_state.get('student_data'):
        personal_info = st.session_state.student_data.get('personal_info', {})
        return personal_info.get('name', 'Student')
    return 'Student'

def render_chat_statistics():
    """Render chat statistics (optional)"""
    if not st.session_state.get('chat_history'):
        return
    
    with st.expander("📊 Discussion Statistics"):
        chat_history = st.session_state.chat_history
        
        # Basic stats
        total_messages = len(chat_history)
        agent_messages = [msg for msg in chat_history if msg["role"] != "User"]
        user_messages = [msg for msg in chat_history if msg["role"] == "User"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Messages", total_messages)
        
        with col2:
            st.metric("Agent Messages", len(agent_messages))
        
        with col3:
            st.metric("Your Messages", len(user_messages))
        
        # Agent participation
        if agent_messages:
            st.markdown("**Agent Participation:**")
            agent_counts = {}
            for msg in agent_messages:
                agent = msg["role"]
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
            
            for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {ROLE_TO_AVATAR.get(agent, '❓')} {agent}: {count} messages")
        
        # Word counts
        if chat_history:
            total_words = sum(len(msg["content"].split()) for msg in chat_history)
            avg_words = total_words / len(chat_history) if chat_history else 0
            
            st.markdown("**Content Analysis:**")
            st.write(f"- Total words: {total_words}")
            st.write(f"- Average words per message: {avg_words:.1f}")

def export_chat_history():
    """Export chat history in various formats"""
    if not st.session_state.get('chat_history'):
        return
    
    from utils.chat_utils import format_chat_for_export
    import json
    from datetime import datetime
    
    # Format options
    export_format = st.selectbox(
        "Export Format",
        ["JSON", "Text", "HTML"],
        help="Choose format for exporting chat history"
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    student_name = _get_student_name().replace(" ", "_")
    
    if export_format == "JSON":
        data = json.dumps(st.session_state.chat_history, indent=2)
        filename = f"mentor_chat_{student_name}_{timestamp}.json"
        mime_type = "application/json"
        
    elif export_format == "Text":
        data = format_chat_for_export(st.session_state.chat_history)
        filename = f"mentor_chat_{student_name}_{timestamp}.txt"
        mime_type = "text/plain"
        
    else:  # HTML
        data = _format_chat_as_html(st.session_state.chat_history)
        filename = f"mentor_chat_{student_name}_{timestamp}.html"
        mime_type = "text/html"
    
    st.download_button(
        f"📥 Download as {export_format}",
        data=data,
        file_name=filename,
        mime=mime_type,
        help=f"Download chat history as {export_format} file"
    )

def _format_chat_as_html(chat_history):
    """Format chat history as HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Mentor Chat History</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
            .user { background-color: #e6f3ff; }
            .agent { background-color: #f0f8f0; }
            .role { font-weight: bold; color: #009CA6; }
            .timestamp { font-size: 0.8em; color: #666; }
        </style>
    </head>
    <body>
        <h1>AI Mentor Roundtable - Chat History</h1>
    """
    
    for msg in chat_history:
        role = msg.get("role", "Unknown")
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        
        css_class = "user" if role == "User" else "agent"
        
        html += f"""
        <div class="message {css_class}">
            <div class="role">{role}</div>
            <div class="content">{content}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html