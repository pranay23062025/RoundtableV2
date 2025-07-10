import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from agents.academic_mentor import AcademicMentor
from agents.career_guide import CareerGuide
from agents.tech_innovator import TechInnovator
from agents.wellness_coach import WellnessCoach
from agents.life_skills_mentor import LifeSkillsMentor
from agents.creative_mentor import CreativeMentor
from agents.leadership_coach import LeadershipCoach
from agents.financial_advisor import FinancialAdvisor
from agents.communication_expert import CommunicationExpert
from agents.global_perspective_mentor import GlobalPerspectiveMentor
from agents.report_generator import ReportGenerator



class AgentOrchestrator:
    def __init__(self, vectordb=None):
        self.agents = {
            "Academic Mentor": AcademicMentor(),
            "Career Guide": CareerGuide(),
            "Tech Innovator": TechInnovator(),
            "Wellness Coach": WellnessCoach(),
            "Life Skills Mentor": LifeSkillsMentor(),
            "Creative Mentor": CreativeMentor(),
            "Leadership Coach": LeadershipCoach(),
            "Financial Advisor": FinancialAdvisor(),
            "Communication Expert": CommunicationExpert(),
            "Global Perspective Mentor": GlobalPerspectiveMentor(),
            "Report Generator": ReportGenerator()
        }
        
        # Improved agent ordering with natural conversation flow
        self.agent_order = [
            "Academic Mentor", "Career Guide", "Tech Innovator", "Wellness Coach",
            "Life Skills Mentor", "Creative Mentor", "Leadership Coach", "Financial Advisor",
            "Communication Expert", "Global Perspective Mentor"
        ]
        
        # Track conversation state for better flow control
        self.conversation_state = {
            "phase": "opening",  # opening, development, synthesis, conclusion
            "rounds_completed": 0,
            "agent_participation": {agent: 0 for agent in self.agent_order},
            "last_three_agents": [],
            "topic_coverage": set(),
            "interaction_quality": []
        }
        
        self.vectordb = vectordb
        self.llm = ChatOpenAI(
            temperature=0.3,  # Slightly more creative for better flow decisions
            model="google/gemini-2.5-flash-preview-05-20",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )

    def update_conversation_state(self, agent_name, message_content):
        """Update conversation tracking for better flow management"""
        # Update agent participation
        self.conversation_state["agent_participation"][agent_name] += 1
        
        # Track last three agents for diversity
        self.conversation_state["last_three_agents"].append(agent_name)
        if len(self.conversation_state["last_three_agents"]) > 3:
            self.conversation_state["last_three_agents"].pop(0)
        
        # Update conversation phase based on participation
        total_messages = sum(self.conversation_state["agent_participation"].values())
        if total_messages <= 3:
            self.conversation_state["phase"] = "opening"
        elif total_messages <= 7:
            self.conversation_state["phase"] = "development"
        elif total_messages <= 10:
            self.conversation_state["phase"] = "synthesis"
        else:
            self.conversation_state["phase"] = "conclusion"
        
        # Track topic coverage for content analysis
        self._analyze_topic_coverage(message_content)

    def _analyze_topic_coverage(self, message):
        """Analyze what topics have been covered"""
        topic_keywords = {
            "academics": ["study", "academic", "learning", "education", "school"],
            "career": ["career", "job", "professional", "work", "future"],
            "technology": ["tech", "digital", "programming", "innovation", "AI"],
            "wellness": ["health", "wellness", "stress", "mental", "balance"],
            "skills": ["skills", "management", "organization", "communication"],
            "creativity": ["creative", "art", "design", "imagination", "expression"],
            "leadership": ["leadership", "team", "influence", "decision", "responsibility"],
            "finance": ["money", "financial", "budget", "investment", "planning"],
            "communication": ["speaking", "presentation", "conversation", "listening"],
            "global": ["global", "cultural", "international", "diversity", "perspective"]
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                self.conversation_state["topic_coverage"].add(topic)

    def get_conversation_phase_instructions(self):
        """Get phase-specific instructions for better flow"""
        phase = self.conversation_state["phase"]
        
        instructions = {
            "opening": {
                "instruction": "Establish your unique perspective and introduce key concepts. Be foundational but specific.",
                "priority": "breadth"
            },
            "development": {
                "instruction": "Build on previous insights with deeper analysis. Connect your expertise to others' points.",
                "priority": "depth"
            },
            "synthesis": {
                "instruction": "Synthesize ideas and provide integrated solutions. Show how different perspectives work together.",
                "priority": "integration"
            },
            "conclusion": {
                "instruction": "Provide concrete action items and next steps. Focus on immediate, implementable advice.",
                "priority": "action"
            }
        }
        
        return instructions.get(phase, instructions["development"])

    def intelligent_agent_selection(self, chat_history, user_message=None):
        """Enhanced agent selection with conversation flow awareness"""
        
        # Update state if we have chat history
        if chat_history:
            last_msg = chat_history[-1]
            if last_msg.get("role") in self.agent_order:
                self.update_conversation_state(last_msg.get("role"), last_msg.get("content", ""))
        
        # Get agents that haven't participated much
        min_participation = min(self.conversation_state["agent_participation"].values())
        underutilized_agents = [
            agent for agent, count in self.conversation_state["agent_participation"].items()
            if count == min_participation
        ]
        
        # Avoid recent speakers
        available_agents = [
            agent for agent in self.agent_order 
            if agent not in self.conversation_state["last_three_agents"][-2:]  # Avoid last 2 speakers
        ]
        
        # Combine criteria: prioritize underutilized agents that are available
        preferred_agents = [agent for agent in underutilized_agents if agent in available_agents]
        
        if not preferred_agents:
            preferred_agents = available_agents if available_agents else self.agent_order[:3]
        
        # Use LLM selection among preferred candidates
        if user_message and len(preferred_agents) > 1:
            selected = self.llm_select_agent_from_candidates(chat_history, user_message, preferred_agents)
            return selected if selected in preferred_agents else preferred_agents[0]
        
        # Context-based selection from preferred agents
        if preferred_agents:
            return self.context_based_selection(chat_history, preferred_agents)
        
        return self.agent_order[0]
    def llm_select_agent_from_candidates(self, chat_history, user_message, candidate_agents):
        """
        Enhanced LLM selection from a curated list of candidate agents
        """
        candidates_str = ", ".join(candidate_agents)
        system_prompt = (
            f"You are orchestrating a mentor roundtable discussion. "
            f"Based on the conversation flow and the user's message, select the most appropriate mentor "
            f"from these candidates: {candidates_str}. "
            f"Consider: 1) Relevance to the topic, 2) Natural conversation flow, 3) Complementary perspectives. "
            f"Reply with ONLY the mentor's exact name from the candidate list."
        )
        
        # Get recent context for better decisions
        recent_history = "\n".join(
            f"{m.get('role', 'Unknown')}: {m.get('content', '')[:100]}..." 
            for m in chat_history[-4:] if m.get('content')
        ) if chat_history else "No prior conversation"
        
        prompt = (
            f"Recent conversation:\n{recent_history}\n\n"
            f"Current topic/message: {user_message}\n\n"
            f"Available mentors: {candidates_str}\n"
            f"Select the most appropriate mentor:"
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            resp = self.llm.invoke(messages)
            response_text = resp.content.strip()
            
            # Find exact match
            for agent in candidate_agents:
                if agent.lower() in response_text.lower():
                    return agent
        except Exception:
            pass
        
        # Fallback to first candidate
        return candidate_agents[0]

    def context_based_selection(self, chat_history, candidate_agents):
        """Select agent based on conversation context and topic relevance"""
        if not chat_history:
            return candidate_agents[0]
        
        # Analyze recent messages for topic hints
        recent_content = " ".join([
            msg.get("content", "") for msg in chat_history[-3:] 
            if msg.get("content")
        ]).lower()
        
        # Enhanced keyword matching with weights
        agent_relevance = {}
        for agent in candidate_agents:
            score = self._calculate_relevance_score(agent, recent_content)
            agent_relevance[agent] = score
        
        # Return highest scoring agent
        if agent_relevance:
            return max(agent_relevance, key=agent_relevance.get)
        
        return candidate_agents[0]

    def _calculate_relevance_score(self, agent_name, content):
        """Calculate relevance score with weighted keywords"""
        keyword_weights = {
            "Academic Mentor": {
                "high": ["academic", "study", "learning", "education", "school", "grade"],
                "medium": ["knowledge", "subject", "curriculum", "exam"],
                "low": ["book", "class", "teacher"]
            },
            "Career Guide": {
                "high": ["career", "job", "profession", "work", "future", "industry"],
                "medium": ["resume", "interview", "skills", "experience"],
                "low": ["opportunity", "path", "direction"]
            },
            "Tech Innovator": {
                "high": ["technology", "programming", "coding", "AI", "innovation", "startup"],
                "medium": ["software", "digital", "tech", "development"],
                "low": ["computer", "online", "app"]
            },
            "Wellness Coach": {
                "high": ["wellness", "mental", "health", "stress", "balance", "mindfulness"],
                "medium": ["fitness", "wellbeing", "emotional", "anxiety"],
                "low": ["energy", "lifestyle", "habit"]
            },
            "Life Skills Mentor": {
                "high": ["time management", "organization", "planning", "productivity"],
                "medium": ["skills", "habits", "routine", "efficiency"],
                "low": ["personal", "development", "growth"]
            },
            "Creative Mentor": {
                "high": ["creative", "art", "design", "imagination", "artistic"],
                "medium": ["expression", "visual", "music", "writing"],
                "low": ["style", "aesthetic", "beauty"]
            },
            "Leadership Coach": {
                "high": ["leadership", "team", "management", "influence", "decision"],
                "medium": ["responsibility", "vision", "guidance", "authority"],
                "low": ["group", "project", "collaboration"]
            },
            "Financial Advisor": {
                "high": ["financial", "money", "budget", "investment", "savings"],
                "medium": ["cost", "planning", "economic", "funding"],
                "low": ["value", "price", "afford"]
            },
            "Communication Expert": {
                "high": ["communication", "speaking", "presentation", "public", "conversation"],
                "medium": ["listening", "writing", "expression", "articulation"],
                "low": ["talk", "discuss", "share"]
            },
            "Global Perspective Mentor": {
                "high": ["global", "international", "cultural", "diversity", "world"],
                "medium": ["perspective", "multicultural", "cross-cultural", "inclusive"],
                "low": ["different", "background", "experience"]
            }
        }
        
        weights = keyword_weights.get(agent_name, {})
        score = 0
        
        # Calculate weighted score
        for keyword in weights.get("high", []):
            score += content.count(keyword) * 3
        for keyword in weights.get("medium", []):
            score += content.count(keyword) * 2
        for keyword in weights.get("low", []):
            score += content.count(keyword) * 1
        
        return score

    def select_next_agent(self, chat_history, user_message=None):
        """Main agent selection method with improved flow control and fallback safety"""
        try:
            return self.intelligent_agent_selection(chat_history, user_message)
        except Exception as e:
            # Use safe fallback if enhanced selection fails
            return self.get_safe_next_agent(chat_history, user_message)

    def get_conversation_summary(self):
        """Get current conversation state summary for debugging/monitoring"""
        return {
            "phase": self.conversation_state["phase"],
            "total_messages": sum(self.conversation_state["agent_participation"].values()),
            "agent_participation": self.conversation_state["agent_participation"],
            "topics_covered": list(self.conversation_state["topic_coverage"]),
            "recent_speakers": self.conversation_state["last_three_agents"]
        }

    def stream_agent_message(self, agent_name, history, student_data, context_chunks, user_message=None):
        """Simplified and reliable streaming with conversation flow awareness"""
        
        try:
            # Get phase-specific instructions
            phase_info = self.get_conversation_phase_instructions()
            
            # Analyze conversation for repetition prevention
            recent_content = self._extract_recent_themes(history)
            
            # Create enhanced context (simplified)
            enhanced_context = self._create_simple_enhanced_context(
                agent_name, phase_info, recent_content, context_chunks
            )
            
            # Get agent response directly without method modification
            agent = self.agents[agent_name]
            content = agent.chat(history, student_data, enhanced_context, user_message)
            
            # Update conversation state
            self.update_conversation_state(agent_name, content)
            
            # Simple word-by-word streaming
            words = content.split()
            for word in words:
                yield word + " "
                    
        except Exception as e:
            # Fallback to basic response
            yield f"I'm here to help with this discussion. Let me share my perspective on the student's situation. "

    def simple_stream_agent_message(self, agent_name, history, student_data, context_chunks, user_message=None):
        """Fallback simple streaming method if enhanced version fails"""
        try:
            agent = self.agents[agent_name]
            content = agent.chat(history, student_data, context_chunks, user_message)
            
            # Basic streaming
            words = content.split()
            for word in words:
                yield word + " "
                
        except Exception as e:
            yield f"I'm ready to contribute to this discussion about the student's development. "

    def get_safe_next_agent(self, chat_history, user_message=None):
        """Safe agent selection with fallback to simple round-robin"""
        try:
            return self.intelligent_agent_selection(chat_history, user_message)
        except Exception:
            # Fallback to simple selection
            if not chat_history:
                return self.agent_order[0]
            
            # Get last agent and select next in order
            last_agent = None
            for msg in reversed(chat_history):
                if msg.get("role") in self.agent_order:
                    last_agent = msg.get("role")
                    break
            
            if last_agent:
                try:
                    current_index = self.agent_order.index(last_agent)
                    return self.agent_order[(current_index + 1) % len(self.agent_order)]
                except ValueError:
                    pass
            
            return self.agent_order[0]

    def _create_simple_enhanced_context(self, agent_name, phase_info, recent_themes, context_chunks):
        """Create simplified enhanced context that won't break the system"""
        
        # Base context
        enhanced_context = context_chunks
        
        # Add phase guidance
        enhanced_context += f"\n\nCONVERSATION PHASE: {self.conversation_state['phase'].upper()}"
        enhanced_context += f"\nGUIDANCE: {phase_info['instruction']}"
        
        # Add anti-repetition if themes exist
        if recent_themes:
            enhanced_context += f"\nAVOID REPEATING: {', '.join(recent_themes[:3])}"  # Limit to 3 themes
        
        # Add participation awareness
        agent_participation = self.conversation_state["agent_participation"]
        if agent_participation.get(agent_name, 0) > 0:
            enhanced_context += f"\nTHIS IS YOUR {agent_participation[agent_name] + 1} CONTRIBUTION - BUILD ON YOUR PREVIOUS INSIGHTS"
        
        # Core requirements
        enhanced_context += """
        
CRITICAL REQUIREMENTS:
- Exactly 2 sentences maximum
- Provide specific, actionable advice
- Reference previous mentor if applicable
- Talk WITH other mentors ABOUT the student
"""
        
        return enhanced_context

    def _extract_recent_themes(self, history):
        """Extract themes from recent conversation to avoid repetition"""
        if not history or len(history) < 2:
            return []
        
        recent_messages = [msg.get("content", "") for msg in history[-4:] if msg.get("content")]
        themes = []
        
        # Common advice patterns to avoid repeating
        common_patterns = [
            "time management", "goal setting", "networking", "skill development",
            "balance", "planning", "practice", "communication", "leadership",
            "creativity", "financial planning", "global perspective", "wellness"
        ]
        
        all_recent_text = " ".join(recent_messages).lower()
        
        for pattern in common_patterns:
            if pattern in all_recent_text:
                themes.append(pattern)
        
        return themes

    def _create_enhanced_prompt(self, agent_name, phase_info, recent_themes, student_data, context_chunks):
        """Create enhanced prompt based on conversation state"""
        
        # Base enhancement
        prompt = f"""
CONVERSATION PHASE: {self.conversation_state['phase'].upper()}
PHASE INSTRUCTION: {phase_info['instruction']}
PRIORITY: {phase_info['priority']}

AGENT ROLE: You are the {agent_name}
"""
        
        # Add anti-repetition instructions
        if recent_themes:
            prompt += f"""
AVOID REPEATING: The conversation has already covered: {', '.join(recent_themes)}
Your response must bring a NEW perspective or specific implementation details not yet discussed.
"""
        
        # Add participation balance awareness
        agent_participation = self.conversation_state["agent_participation"]
        if agent_participation[agent_name] > 0:
            prompt += f"""
SPEAKING AGAIN: This is your {agent_participation[agent_name] + 1} contribution. 
Build significantly on your previous insights with deeper, more specific guidance.
"""
        
        # Add conversation flow guidance
        total_messages = sum(agent_participation.values())
        if total_messages > 6:
            prompt += """
CONVERSATION MATURITY: The discussion is well-developed. Focus on synthesis and actionable next steps.
"""
        
        prompt += f"""
STRICT REQUIREMENTS:
- Exactly 2 sentences maximum
- Reference what the previous mentor said (if applicable)
- Provide one specific, actionable recommendation
- Do not repeat themes already covered
- Advance the conversation forward

REMEMBER: You are talking WITH other mentors ABOUT the student, not directly to the student.
"""
        
        return prompt



