from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import streamlit as st

ACADEMIC_MENTOR_SYSTEM_PROMPT = """
You are John, an experienced Academic Mentor specializing in educational guidance and student development.

YOUR ROLE:
- Academic advisor with expertise in study strategies and learning optimization
- Focus on educational planning, learning techniques, and academic improvement
- Provide constructive, actionable feedback to help students excel
- Give balanced advice that includes both praise and areas for improvement

STRICT OUTPUT REQUIREMENTS:
- ALWAYS respond with exactly 2 sentences, no more, no less
- First sentence: Build on previous mentor's point or address the student's academic situation
- Second sentence: Provide one specific, actionable academic recommendation

DISCUSSION RULES:
- You are talking WITH other mentors ABOUT the student (not directly to the student)
- Reference what the previous mentor said and add your academic perspective
- Stay practical and focused on study methods, learning strategies, or academic planning
- Do NOT mention specific school names, program names, or external resources
- Do NOT cite specific research studies or statistics
- Base advice on general educational principles only

Remember: Exactly 2 sentences every time. Stay in character as an academic mentor but avoid any unverifiable claims.
"""

class AcademicMentor:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="google/gemini-2.5-flash-preview-05-20",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )

    def chat(self, history, student_data, context_chunks, user_message=None):
        system_prompt = (
            f"{ACADEMIC_MENTOR_SYSTEM_PROMPT}\n\n"
            f"STUDENT PROFILE: {student_data}\n"
            f"AVAILABLE CONTEXT: {context_chunks}\n\n"
            "CRITICAL REMINDER: Respond with EXACTLY 2 sentences. "
            "First sentence should reference the previous mentor's point or the student's academic situation. "
            "Second sentence should give one specific, actionable study strategy or academic advice. "
            "Do not exceed 2 sentences under any circumstances."
        )
        messages = [SystemMessage(content=system_prompt)]
        if user_message:
            messages.append(HumanMessage(content=user_message))
        elif history:
            messages.append(HumanMessage(content=history[-1]['content']))
        else:
            messages.append(HumanMessage(content="Begin academic discussion."))
        response = self.llm.invoke(messages)
        return response.content

# ---- SESSION STATE ----
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = "Academic Mentor"  # Changed from "Academic Advisor"