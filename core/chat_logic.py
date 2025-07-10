import streamlit as st
import time
from datetime import datetime
from config.settings import (
    MAX_AGENT_TURNS, 
    SIMILARITY_THRESHOLD, 
    MAX_MESSAGE_ATTEMPTS,
    STREAMING_DELAY,
    AGENT_TURN_DELAY,
    CONVERSATION_PHASES,
    TOPIC_KEYWORDS
)
import logging

logger = logging.getLogger(__name__)

def check_message_similarity(new_message, agent_name, threshold=SIMILARITY_THRESHOLD):
    """Check if a message is too similar to previous messages from the same agent"""
    if agent_name not in st.session_state.agent_message_history:
        st.session_state.agent_message_history[agent_name] = []
    
    new_words = set(new_message.lower().split())
    
    for prev_message in st.session_state.agent_message_history[agent_name]:
        prev_words = set(prev_message.lower().split())
        
        if len(new_words) > 0 and len(prev_words) > 0:
            # Calculate Jaccard similarity
            intersection = len(new_words.intersection(prev_words))
            union = len(new_words.union(prev_words))
            
            if union > 0:
                similarity = intersection / union
                if similarity > threshold:
                    return True, prev_message
    
    return False, None

def add_message_to_history(message, agent_name):
    """Add message to agent's history for similarity tracking"""
    if agent_name not in st.session_state.agent_message_history:
        st.session_state.agent_message_history[agent_name] = []
    
    st.session_state.agent_message_history[agent_name].append(message)
    
    # Keep only recent messages to prevent memory issues
    max_history = 3
    if len(st.session_state.agent_message_history[agent_name]) > max_history:
        st.session_state.agent_message_history[agent_name] = \
            st.session_state.agent_message_history[agent_name][-max_history:]

def get_conversation_progression():
    """Determine what phase the conversation should be in"""
    message_count = len(st.session_state.chat_history)
    
    for phase, config in CONVERSATION_PHASES.items():
        if message_count <= config["threshold"]:
            return phase
    
    return "synthesis"  # Default to final phase

def extract_topics_from_message(message_content):
    """Extract topics mentioned in a message"""
    message_lower = message_content.lower()
    topics_found = set()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            topics_found.add(topic)
    
    return topics_found

def get_progressive_context(agent_name):
    """Get context that encourages conversation progression"""
    phase = get_conversation_progression()
    
    # Analyze covered topics
    covered_topics = set()
    for msg in st.session_state.chat_history:
        if msg["role"] != "User":
            topics = extract_topics_from_message(msg["content"])
            covered_topics.update(topics)
    
    # Update session state
    st.session_state.conversation_topics.update(covered_topics)
    st.session_state.conversation_phase = phase
    
    # Generate context based on phase
    phase_prompts = {
        "initial": f"""
This is the beginning of the discussion. Introduce a fresh perspective on the student's situation. 
Current agent: {agent_name}
Student: {st.session_state.student_data.get('personal_info', {}).get('name', 'the student')}
Avoid repeating what others have said. Focus on your unique expertise.
""",
        "development": f"""
Build on the conversation by diving deeper into specifics. 
Topics already covered: {', '.join(covered_topics) if covered_topics else 'none yet'}
As {agent_name}, introduce NEW actionable strategies or insights that haven't been discussed.
Provide specific, practical advice based on your expertise.
""",
        "synthesis": f"""
We're in the final phase. Provide concrete next steps or synthesize the discussion into actionable recommendations.
Covered topics: {', '.join(covered_topics)}
As {agent_name}, avoid repeating earlier advice. Focus on SPECIFIC, MEASURABLE actions the student can take immediately.
Consider how your expertise connects with what others have shared.
"""
    }
    
    return phase_prompts.get(phase, phase_prompts["initial"])

def validate_agent_message(message, agent_name):
    """Validate that an agent message meets quality standards"""
    if not message or len(message.strip()) < 20:
        return False, "Message too short"
    
    if len(message) > 2000:
        return False, "Message too long"
    
    # Check for generic responses
    generic_phrases = [
        "as an ai", "i'm an ai", "i cannot", "i don't have access",
        "let me help you", "i understand", "that's a great question"
    ]
    
    message_lower = message.lower()
    if any(phrase in message_lower for phrase in generic_phrases):
        return False, "Generic AI response detected"
    
    return True, "Valid"

def process_agent_turn(get_context_chunks):
    """Process a single agent turn using enhanced orchestrator with safety measures"""
    try:
        # Initialize agent turn
        if not st.session_state.agent_turn_in_progress and st.session_state.consecutive_agent_turns < MAX_AGENT_TURNS:
            # Use safe agent selection from enhanced orchestrator
            try:
                st.session_state.current_agent = st.session_state.orchestrator.select_next_agent(
                    st.session_state.chat_history, 
                    user_message=None
                )
            except Exception as e:
                logger.warning(f"Enhanced agent selection failed: {e}, using fallback")
                # Fallback to simple selection
                st.session_state.current_agent = st.session_state.orchestrator.get_safe_next_agent(
                    st.session_state.chat_history,
                    user_message=None
                )
            
            st.session_state.thinking_agent = st.session_state.current_agent
            st.session_state.agent_turn_in_progress = True
            st.session_state.roundtable_message = ""
            
            logger.info(f"Starting turn for {st.session_state.current_agent}")
            time.sleep(0.5)
            st.rerun()
        
        # Generate message with enhanced orchestrator
        elif st.session_state.agent_turn_in_progress and not st.session_state.get('message_streaming', False):
            st.session_state.message_streaming = True
            time.sleep(AGENT_TURN_DELAY)
            
            # Ensure we have a current agent
            if not st.session_state.current_agent:
                st.session_state.current_agent = "Academic Mentor"
            
            logger.info(f"Generating message for {st.session_state.current_agent}")
            
            # Get context for message generation
            query = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
            context_chunks = get_context_chunks(query, k=3)
            
            # Generate message using enhanced orchestrator
            message_content = generate_enhanced_agent_message(context_chunks)
            return message_content
        
        return None
        
    except Exception as e:
        logger.error(f"Error in process_agent_turn: {e}")
        st.error(f"Error processing agent turn: {e}")
        
        # Reset state to prevent infinite loop
        st.session_state.agent_turn_in_progress = False
        st.session_state.thinking_agent = None
        st.session_state.message_streaming = False
        
        return None

def generate_enhanced_agent_message(context_chunks):
    """Generate agent message using enhanced orchestrator with retry and debugging"""
    attempts = 0
    
    while attempts < MAX_MESSAGE_ATTEMPTS:
        try:
            # Debug info
            logger.info(f"Attempting to generate message for {st.session_state.current_agent}, attempt {attempts + 1}")
            
            # Try enhanced orchestrator streaming first
            try:
                agent_stream = st.session_state.orchestrator.stream_agent_message(
                    st.session_state.current_agent,
                    st.session_state.chat_history,
                    st.session_state.student_data,
                    context_chunks,
                    user_message=None
                )
            except Exception as e:
                logger.warning(f"Enhanced streaming failed: {e}, falling back to simple method")
                # Fallback to simple streaming
                agent_stream = st.session_state.orchestrator.simple_stream_agent_message(
                    st.session_state.current_agent,
                    st.session_state.chat_history,
                    st.session_state.student_data,
                    context_chunks,
                    user_message=None
                )
            
            # Collect streaming content with timeout protection
            temp_message = ""
            word_count = 0
            max_words = 100  # Prevent infinite streaming
            
            for token in agent_stream:
                temp_message += token
                word_count += 1
                if word_count > max_words:
                    logger.warning(f"Message generation exceeded {max_words} words, stopping")
                    break
            
            # Ensure we have a message
            if not temp_message.strip():
                temp_message = f"As the {st.session_state.current_agent}, I believe the student should focus on developing their core strengths. This will provide a solid foundation for future growth and success."
            
            # Validate message quality
            is_valid, validation_msg = validate_agent_message(temp_message, st.session_state.current_agent)
            if not is_valid:
                logger.warning(f"Invalid message from {st.session_state.current_agent}: {validation_msg}")
                attempts += 1
                continue
            
            # Check for similarity with legacy system (for backward compatibility)
            is_similar, similar_message = check_message_similarity(temp_message, st.session_state.current_agent)
            
            if not is_similar or attempts == MAX_MESSAGE_ATTEMPTS - 1:
                logger.info(f"Generated valid message for {st.session_state.current_agent} after {attempts + 1} attempts")
                return temp_message
            else:
                logger.info(f"Similar message detected for {st.session_state.current_agent}, retrying...")
                attempts += 1
                # Add similarity context for next attempt
                context_chunks += f"\n\nIMPORTANT: Do NOT repeat or paraphrase this previous message: '{similar_message[:100]}...' Provide a completely different perspective or approach."
                
        except Exception as e:
            logger.error(f"Error generating message (attempt {attempts + 1}): {e}")
            attempts += 1
            if attempts >= MAX_MESSAGE_ATTEMPTS:
                return f"I apologize, but I'm having trouble generating a response right now. Let me try to help in a different way."
    
    return None

def handle_message_completion(message_content):
    """Handle completion of agent message with enhanced orchestrator integration"""
    try:
        # Add message to chat history
        from utils.chat_utils import format_message
        st.session_state.chat_history.append(
            format_message(st.session_state.current_agent, message_content)
        )
        
        # Add to agent message history for similarity tracking (legacy compatibility)
        add_message_to_history(message_content, st.session_state.current_agent)
        
        # Update enhanced orchestrator conversation state
        if hasattr(st.session_state.orchestrator, 'update_conversation_state'):
            st.session_state.orchestrator.update_conversation_state(
                st.session_state.current_agent, 
                message_content
            )
        
        # Update turn counter
        st.session_state.consecutive_agent_turns += 1
        
        # Check if we should pause
        if st.session_state.consecutive_agent_turns >= MAX_AGENT_TURNS:
            st.session_state.chat_running = False
            st.session_state.thinking_agent = None
            st.session_state.agent_turn_in_progress = False
            st.session_state.message_streaming = False
            
            # Show enhanced conversation summary if available
            if hasattr(st.session_state.orchestrator, 'get_conversation_summary'):
                summary = st.session_state.orchestrator.get_conversation_summary()
                phase = summary.get('phase', 'development')
                topics_covered = len(summary.get('topics_covered', []))
                st.info(f"🛑 Agents have paused after {MAX_AGENT_TURNS} messages. "
                       f"Discussion phase: {phase.title()} • Topics covered: {topics_covered} • "
                       f"Please enter your message, resume, or generate a report.")
            else:
                st.info("🛑 Agents have paused after 5 messages. Please enter your message, resume, or generate a report.")
            st.rerun()
        else:
            # Use enhanced orchestrator for next agent selection
            next_agent = st.session_state.orchestrator.select_next_agent(st.session_state.chat_history)
            st.session_state.current_agent = next_agent
            st.session_state.agent_turn_in_progress = False
            st.session_state.thinking_agent = None
            st.session_state.message_streaming = False
            
            # Brief pause before next agent
            time.sleep(AGENT_TURN_DELAY)
            st.rerun()
            
    except Exception as e:
        logger.error(f"Error in handle_message_completion: {e}")
        st.error(f"Error completing message: {e}")

def reset_conversation_state():
    """Reset conversation-specific state while preserving session"""
    st.session_state.conversation_topics = set()
    st.session_state.agent_message_history = {}
    st.session_state.conversation_phase = "initial"
    st.session_state.consecutive_agent_turns = 0
    st.session_state.thinking_agent = None
    st.session_state.agent_turn_in_progress = False
    st.session_state.message_streaming = False

def reset_agent_state_if_stuck():
    """Reset agent state if the system appears to be stuck"""
    # Check if we've been stuck for too long
    if (st.session_state.get('agent_turn_in_progress') and 
        st.session_state.get('thinking_agent') and
        not st.session_state.get('message_streaming')):
        
        # Reset the state
        st.session_state.agent_turn_in_progress = False
        st.session_state.thinking_agent = None
        st.session_state.message_streaming = False
        st.session_state.chat_running = True
        
        logger.info("Reset stuck agent state")
        return True
    return False

def get_conversation_analytics():
    """Get analytics about the current conversation"""
    total_messages = len(st.session_state.chat_history)
    agent_messages = [msg for msg in st.session_state.chat_history if msg["role"] != "User"]
    user_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "User"]
    
    # Agent participation
    agent_participation = {}
    for msg in agent_messages:
        agent = msg["role"]
        agent_participation[agent] = agent_participation.get(agent, 0) + 1
    
    # Topic coverage
    covered_topics = len(st.session_state.conversation_topics)
    
    return {
        "total_messages": total_messages,
        "agent_messages": len(agent_messages),
        "user_messages": len(user_messages),
        "agent_participation": agent_participation,
        "covered_topics": covered_topics,
        "conversation_phase": st.session_state.conversation_phase,
        "topics_list": list(st.session_state.conversation_topics)
    }

def should_continue_conversation():
    """Determine if the conversation should continue based on various factors"""
    # Check turn limits
    if st.session_state.consecutive_agent_turns >= MAX_AGENT_TURNS:
        return False, "Turn limit reached"
    
    # Check if chat is running
    if not st.session_state.chat_running:
        return False, "Chat not running"
    
    # Check if we have student data
    if not st.session_state.student_data:
        return False, "No student data"
    
    # Check for errors
    if st.session_state.agent_turn_in_progress and st.session_state.message_streaming:
        # Check if we're stuck
        if hasattr(st.session_state, 'last_agent_start_time'):
            if time.time() - st.session_state.last_agent_start_time > 30:  # 30 second timeout
                return False, "Agent timeout"
    
    return True, "Continue"