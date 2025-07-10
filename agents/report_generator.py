from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from datetime import datetime
import pdfkit
import tempfile
import json

class ReportGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="google/gemini-2.5-flash-preview-05-20",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        self.wkhtmltopdf_path = self._find_wkhtmltopdf()

    def _find_wkhtmltopdf(self):
        custom = os.getenv("WKHTMLTOPDF_PATH")
        if custom and os.path.exists(custom):
            return custom
        common_paths = [
            r"C:/Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            "/usr/local/bin/wkhtmltopdf",
            "/usr/bin/wkhtmltopdf"
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

    def generate_report_content(self, chat_history, student_data, context_chunks):
        """Generate comprehensive report content based on roundtable discussion"""
        system_prompt = """You are a PhD in psychology, master educator, and expert mentorship analyst at Growth Valley Community. 
        
        Analyze the provided chat history, student data, and company context to create a comprehensive, professional growth-focused report.
        
        IMPORTANT GUIDELINES:
        - Write in a professional, encouraging, and honest tone
        - Focus on the student's communication style, thinking patterns, and potential from the discussion
        - DO NOT directly quote the student or transcript - analyze their personality and approach instead
        - Be factual and specific with observations
        - Provide actionable insights and recommendations
        - Include specific growth metrics and improvement areas
        - Suggest realistic skill development scores and potential scores
        
        Include these sections in your analysis:
        1. Executive Summary - Brief overview of the student's engagement and key insights
        2. Highlights - Key strengths and remarkable observations from the discussion
        3. Skill Feedback - Communication, analytical thinking, collaboration, and technical skills assessment
        4. Improvements Over Time - Specific skill areas with current and potential scores (0-100 scale)
        5. Growth Areas - 3 specific areas for improvement with actionable steps
        6. Next Goals - Concrete recommendations and development targets
        7. Action Plan - Specific next steps for the student with timelines
        8. Conclusion - Encouraging summary with future outlook
        
        For the Improvements Over Time section, provide realistic scores in this format:
        - Skill Name: Current score (X), Potential score (Y) - Brief explanation
        
        Format the response as a JSON object with these sections as keys.
        Keep the tone professional but warm, suitable for parents and mentors.
        Focus on growth potential and practical insights."""
        
        # Prepare context for analysis
        discussion_summary = self._analyze_discussion(chat_history)
        student_context = self._format_student_context(student_data)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Student Profile: {student_context}
            
            Company Context: {context_chunks}
            
            Discussion Analysis: {discussion_summary}
            
            Please generate a comprehensive report focusing on the student's potential, communication style, 
            and growth opportunities based on their interaction with AI mentors.
            """)
        ]
        
        response = self.llm.invoke(messages)
        try:
            json_report = json.loads(response.content)
        except Exception:
            # Fallback structure if JSON parsing fails
            json_report = {
                "executive_summary": response.content,
                "highlights": "Student showed strong engagement and demonstrated excellent communication skills in the roundtable discussion.",
                "skill_feedback": "The student demonstrated excellent analytical thinking and communication abilities throughout the discussion.",
                "improvements_over_time": "Leadership Initiative: Current score (35), Potential score (70) - Shows natural leadership qualities. Problem-Solving Application: Current score (40), Potential score (75) - Demonstrates strong analytical thinking. Collaborative Influence: Current score (45), Potential score (80) - Works well in team environments.",
                "growth_areas": "1. Initiative Taking: Encourage more proactive project leadership. 2. Public Speaking: Practice formal presentation skills. 3. Technical Skills: Continue developing programming and analytical capabilities.",
                "next_goals": "Focus on leadership development, enhance technical skills, and build confidence in public speaking situations.",
                "action_plan": ["Schedule regular mentor check-ins", "Join leadership activities", "Practice technical presentations", "Work on identified growth areas"],
                "conclusion": "The student shows tremendous potential for growth and success with continued mentorship and focused development in key areas."
            }
        return json_report
    
    def _analyze_discussion(self, chat_history):
        """Analyze the chat history to extract key insights"""
        if not chat_history:
            return "No discussion history available."
        
        user_messages = [msg for msg in chat_history if msg.get('role') == 'User']
        agent_messages = [msg for msg in chat_history if msg.get('role') not in ['User', 'System']]
        
        analysis = {
            "total_messages": len(chat_history),
            "user_participation": len(user_messages),
            "mentor_responses": len(agent_messages),
            "topics_discussed": self._extract_topics(user_messages),
            "engagement_level": "High" if len(user_messages) > 3 else "Moderate" if len(user_messages) > 1 else "Initial"
        }
        
        return f"""
        Discussion Statistics:
        - Total messages: {analysis['total_messages']}
        - Student messages: {analysis['user_participation']}  
        - Mentor responses: {analysis['mentor_responses']}
        - Engagement level: {analysis['engagement_level']}
        - Topics explored: {', '.join(analysis['topics_discussed'])}
        
        Recent Discussion Context:
        {self._get_recent_context(chat_history)}
        """
    
    def _extract_topics(self, user_messages):
        """Extract key topics from user messages"""
        topics = []
        for msg in user_messages:
            content = msg.get('content', '').lower()
            if any(word in content for word in ['career', 'job', 'future', 'profession']):
                topics.append('Career Planning')
            if any(word in content for word in ['study', 'academic', 'school', 'learn']):
                topics.append('Academic Development')
            if any(word in content for word in ['tech', 'technology', 'programming', 'computer']):
                topics.append('Technology')
            if any(word in content for word in ['skill', 'improve', 'develop', 'growth']):
                topics.append('Skill Development')
        return list(set(topics)) if topics else ['General Discussion']
    
    def _get_recent_context(self, chat_history):
        """Get recent conversation context for analysis"""
        recent_messages = chat_history[-6:] if len(chat_history) > 6 else chat_history
        context = []
        for msg in recent_messages:
            role = msg.get('role', 'Unknown')
            content = msg.get('content', '')[:100] + "..." if len(msg.get('content', '')) > 100 else msg.get('content', '')
            context.append(f"{role}: {content}")
        return "\n".join(context)
    
    def _format_student_context(self, student_data):
        """Format student data for context"""
        if not student_data:
            return "Student profile information not available."
        
        context_items = []
        for key, value in student_data.items():
            if value and str(value).strip():
                context_items.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(context_items) if context_items else "Basic student profile available."

    def create_html_report_with_llm(self, student_data, report_content):
        prompt = f"""
        You are a skilled academic editor at Growth Valley Community. Create a professional student report based on the provided content.
        
        CRITICAL PDF FORMATTING REQUIREMENTS:
        - DO NOT include DOCTYPE, html, head, body tags, logos, or main titles - these will be added automatically
        - Start directly with the student information box using class="info-box"
        - MANDATORY: Include these fields in the info-box: Student Name, GVC ID, Class/Grade, School, City
        - Use <h2> for section titles, <p> for paragraphs, and <ul><li> for bullet points
        - Use class="info-box" for the student information section at the top
        - Use class="highlight-text" for highlighting important scores or achievements
        - Use class="score-box" for displaying improvement scores in boxes
        - Use class="current-score" for current skill levels
        - Use class="potential-score" for potential/target skill levels
        - Use class="keep-together" for sections that should not be split across pages
        - Use class="recommendation-box" for key recommendations
        - Use class="insight-box" for important insights
        - Keep paragraphs concise (max 4-5 lines) to avoid awkward page breaks
        - Group related content in div containers where appropriate
        - Use different colors for current and potential scores to easily draw insights
        - DO NOT EVER LEAVE THE FIRST PAGE WITHOUT CONTENT
        
        STYLING GUIDELINES:
        - Only use white, black, red, blue, grey colors as specified in the CSS
        - The report will be printed on A4 pages with proper margins
        - Avoid very long paragraphs that might cause page break issues
        - Use the provided CSS classes for consistent formatting
        - All headings (h2) MUST use beautiful calligraphy fonts
        - Make it professional, encouraging, and student-focused
        - For skill scores, format as: <span class="current-score">Skill: 35</span> → <span class="potential-score">Target: 70</span>
        
        REQUIRED SECTIONS:
        1. Student Information (in info-box with all required fields)
        2. Highlights (key strengths and achievements)
        3. Skill Feedback (detailed assessment of abilities)
        4. Improvements Over Time (with score boxes showing current → potential)
        5. Growth Areas (specific areas for development)
        6. Next Goals (concrete objectives and targets)
        7. Action Plan (specific steps with timelines)
        8. Conclusion (encouraging summary)
        
        Do not include any introductory text - start directly with the HTML content.
        Do not write "Report:" or any labels - start with the info-box.
        
        Student Data: {student_data}
        Report Content: {report_content}
        """
        
        response = self.llm.invoke(prompt)
        html_body = response.content if hasattr(response, "content") else response
        
        # Clean up the response
        html_body = html_body.replace("```html", "").strip()
        html_body = html_body.replace("```", "").strip()
        if html_body.lower().startswith("report:"):
            html_body = html_body[7:].strip()
        
        # Create complete HTML document with professional styling
        complete_html = self._create_complete_html(student_data, html_body)
        return complete_html
    
    def _create_complete_html(self, student_data, html_body):
        """Create complete HTML document with professional PDF-optimized styling"""
        student_name = student_data.get('name', 'Student')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Insight Report - {student_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Playfair+Display:wght@400;700&family=Great+Vibes&family=Cormorant+Garamond:wght@400;600&family=Crimson+Text:wght@400;600&family=Libre+Baskerville:wght@400;700&family=Cambria:wght@400;700&family=Georgia:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4;
            margin: 8mm;
        }}
        
        body {{
            font-family: 'Crimson Text', 'Libre Baskerville', 'Cambria', 'Georgia', serif;
            background-color: #ffffff;
            color: #2c3e50;
            line-height: 1.7;
            margin: 0;
            padding: 0;
            font-size: 13pt;
        }}
        
        .report-container {{
            width: 100%;
            min-height: 100vh;
            background-color: #ffffff;
            padding: 25px 30px;
            box-sizing: border-box;
            margin: 0;
            position: relative;
            border: 1px solid #e0e0e0;
        }}
        
        .logo-container {{
            position: relative;
            width: 100%;
            height: 80px;
            margin-bottom: 20px;
            padding: 5px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .main-title {{
            font-family: 'Cambria', 'Georgia', serif;
            font-size: 24pt;
            text-align: center;
            margin: 20px 0 10px 0;
            color: #000000;
            font-weight: 600;
            letter-spacing: 0.5px;
            page-break-after: avoid;
            border-bottom: 2px solid #000000;
            padding-bottom: 8px;
        }}
        
        h1 {{
            font-family: 'Great Vibes', 'Dancing Script', 'Playfair Display', cursive;
            font-size: 22pt;
            text-align: center;
            margin: 15px 0 25px 0;
            color: #1976D2;
            font-weight: 400;
            border-bottom: 2px solid #1976D2;
            padding-bottom: 10px;
            page-break-after: avoid;
            text-shadow: 1px 1px 2px rgba(25, 118, 210, 0.1);
        }}
        
        h2 {{
            font-family: 'Playfair Display', 'Dancing Script', 'Great Vibes', serif;
            font-size: 17pt;
            color: #1976D2;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: 600;
            border-bottom: 2px solid #1976D2;
            padding-bottom: 6px;
            page-break-after: avoid;
            text-shadow: 1px 1px 2px rgba(25, 118, 210, 0.1);
            letter-spacing: 0.3px;
        }}
        
        h3 {{
            font-family: 'Cormorant Garamond', 'Playfair Display', serif;
            font-size: 14pt;
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: 600;
            border-left: 3px solid #1976D2;
            padding-left: 10px;
        }}
        
        p {{
            margin-bottom: 14px;
            text-align: justify;
            orphans: 2;
            widows: 2;
            font-family: 'Crimson Text', 'Libre Baskerville', 'Cambria', 'Georgia', serif;
            font-size: 13pt;
            line-height: 1.7;
            color: #2c3e50;
        }}
        
        ul {{
            list-style-type: disc;
            margin-left: 25px;
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}
        
        li {{
            margin-bottom: 8px;
            orphans: 2;
            widows: 2;
            font-family: 'Crimson Text', 'Libre Baskerville', 'Cambria', 'Georgia', serif;
            font-size: 13pt;
            line-height: 1.6;
            color: #2c3e50;
        }}
        
        .info-box {{
            background-color: #E3F2FD;
            border: 1px solid #1976D2;
            border-left: 4px solid #1976D2;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 6px;
            page-break-inside: avoid;
            font-size: 12pt;
        }}
        
        .highlight-text {{
            color: #D32F2F;
            font-weight: 600;
            background-color: #FFE5E5;
            padding: 2px 4px;
            border-radius: 3px;
            border: 1px solid #FFCDD2;
        }}
        
        .section-header {{
            background-color: #F0F4C3;
            padding: 8px 12px;
            border-radius: 5px;
            margin-top: 18px;
            margin-bottom: 12px;
            font-weight: 600;
            color: #33691E;
            font-family: 'Georgia', 'Cambria', serif;
            page-break-after: avoid;
            border-left: 3px solid #8BC34A;
        }}
        
        .score-box {{
            background: linear-gradient(135deg, #E8F5E8, #F0F8F0);
            border: 2px solid #4CAF50;
            padding: 8px 12px;
            margin: 5px 3px;
            border-radius: 6px;
            display: inline-block;
            min-width: 120px;
            text-align: center;
            font-weight: 600;
            color: #2E7D32;
            font-size: 11pt;
            box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
        }}
        
        .current-score {{
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            border: 2px solid #FF9800;
            padding: 6px 10px;
            margin: 3px 2px;
            border-radius: 6px;
            display: inline-block;
            min-width: 100px;
            text-align: center;
            font-weight: 600;
            color: #E65100;
            font-size: 11pt;
            box-shadow: 0 2px 4px rgba(255, 152, 0, 0.2);
        }}
        
        .potential-score {{
            background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
            border: 2px solid #4CAF50;
            padding: 6px 10px;
            margin: 3px 2px;
            border-radius: 6px;
            display: inline-block;
            min-width: 100px;
            text-align: center;
            font-weight: 600;
            color: #1B5E20;
            font-size: 11pt;
            box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        .keep-together {{
            page-break-inside: avoid;
        }}
        
        strong {{
            color: #1976D2;
            font-weight: 600;
        }}
        
        .elegant-border {{
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 15px;
            margin: 12px 0;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .section-divider {{
            border-top: 1px solid #e0e0e0;
            margin: 20px 0;
            padding-top: 15px;
        }}
        
        .recommendation-box {{
            background-color: #F3E5F5;
            border-left: 4px solid #9C27B0;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            page-break-inside: avoid;
        }}
        
        .insight-box {{
            background-color: #E8F5E8;
            border-left: 4px solid #4CAF50;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            page-break-inside: avoid;
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }}
        
        .skill-item {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #007bff;
        }}
        
        /* Academic spacing */
        .report-container > * {{
            margin-bottom: 14px;
        }}
        
        /* Professional table styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 11pt;
        }}
        
        th, td {{
            border: 1px solid #dee2e6;
            padding: 8px 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #1a365d;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="main-title">Growth Valley Community</div>
        <h1>AI Mentor Roundtable Report</h1>
        
        {html_body}
    </div>
</body>
</html>"""

    def generate_pdf(self, html_content):
        """Generate PDF with professional formatting options"""
        options = {
            'page-size': 'A4',
            'margin-top': '8mm',
            'margin-right': '8mm',
            'margin-bottom': '8mm',
            'margin-left': '8mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore',
            'javascript-delay': 1000,
            'no-stop-slow-scripts': None,
            'debug-javascript': None
        }
        
        config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path) if self.wkhtmltopdf_path else None
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
                html_file.write(html_content.encode('utf-8'))
                html_path = html_file.name
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
                pdf_path = pdf_file.name
            
            # Generate PDF with enhanced options
            pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
            
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            
            # Clean up temporary files
            os.unlink(html_path)
            os.unlink(pdf_path)
            
            return pdf_content
            
        except Exception as e:
            # Clean up files if they exist
            try:
                if 'html_path' in locals():
                    os.unlink(html_path)
                if 'pdf_path' in locals():
                    os.unlink(pdf_path)
            except:
                pass
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def generate_comprehensive_report(self, chat_history, student_data, context_chunks):
        """Generate a comprehensive report similar to CSV report generator with enhanced formatting"""
        
        # Enhanced system prompt for comprehensive report generation
        system_prompt = """You are a PhD in psychology, master educator, tech genius, and best entrepreneurship mentor at Growth Valley Community.
        
        Write a detailed mentor-style report that is very honest, to the point, very factual with 3 improvement suggestions for the student in GVC's tone and format.
        
        CRITICAL REQUIREMENTS:
        - DO NOT USE "-" AND "*" ANYWHERE IN THE REPORT
        - Write all headings and titles as normal text
        - DO NOT highlight anything with symbols
        - Should not look AI generated
        - Use the student's background, interests, and discussion context
        - Keep it concise, 600 words max
        - Be encouraging but honest
        - Focus on growth potential and practical insights
        
        MANDATORY SECTIONS:
        1. Highlights - Key strengths and observations from the roundtable discussion
        2. Skill Feedback - Communication, analytical thinking, collaboration assessment
        3. Improvements Over Time - 3 specific skill areas with current score (50-80) and potential score (70-95)
        4. Next Goals - 3 specific focus areas for development
        5. Closing Note - Encouraging summary about their potential
        6. Summary Insight - How this growth will benefit them, praise parents for enrolling in GVC
        7. Recommended Resources - 1 TED talk, 1 book, 1 article based on their needs
        8. Parent Feedback Prompt - One question parents should ask the student
        9. Mentor Final Thought - One inspiring quote about the student
        
        For Improvements Over Time, format as:
        Leadership Initiative: Current 65, Potential 85
        Problem Solving Application: Current 70, Potential 90
        Collaborative Influence: Current 60, Potential 82
        
        Include research facts about how GVC helps future leaders and entrepreneurs.
        Make parents feel good about their investment in their child's development.
        
        Format as JSON with section names as keys."""
        
        # Prepare enhanced context
        discussion_summary = self._analyze_discussion(chat_history)
        student_context = self._format_student_context(student_data)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Student Profile: {student_context}
            
            Company Context: {context_chunks}
            
            Discussion Analysis: {discussion_summary}
            
            Generate a comprehensive, professional report focusing on the student's potential, 
            communication style, and growth opportunities based on their AI mentor roundtable interaction.
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            json_report = json.loads(response.content)
        except Exception:
            # Enhanced fallback structure
            json_report = {
                "highlights": "Student demonstrated excellent engagement and thoughtful participation in the AI mentor roundtable discussion, showing strong analytical thinking and genuine curiosity about their future development.",
                "skill_feedback": "The student exhibited strong communication abilities, asking insightful questions and actively engaging with multiple mentors. Their responses showed depth of thinking and genuine interest in personal growth.",
                "improvements_over_time": "Leadership Initiative: Current 65, Potential 85. Problem Solving Application: Current 70, Potential 90. Collaborative Influence: Current 60, Potential 82.",
                "next_goals": "Focus on developing leadership confidence through project management opportunities. Enhance technical skills through hands-on programming projects. Build public speaking abilities through presentation practice.",
                "closing_note": "This student shows tremendous potential for growth and success with their natural curiosity and commitment to learning. Their engagement in the roundtable discussion demonstrates readiness for advanced mentorship.",
                "summary_insight": "The student's participation in GVC's AI mentor roundtable has revealed strong foundations for future success. This kind of personalized, interactive learning environment helps develop critical thinking and leadership skills that traditional classroom settings cannot provide. Research from Stanford University shows that mentorship-based learning significantly improves student outcomes and career preparation.",
                "recommended_resources": "TED Talk: 'How to Build Your Creative Confidence' by David Kelley. Book: 'Mindset: The New Psychology of Success' by Carol Dweck. Article: 'The Power of Growth Mindset in Education' from Harvard Business Review.",
                "parent_feedback_prompt": "Ask your child about their favorite insight from the mentor discussion and how they plan to apply it in their daily life.",
                "mentor_final_thought": "This student doesn't just absorb knowledge; they transform it into wisdom through thoughtful application and genuine curiosity."
            }
        
        return json_report
    
    def create_enhanced_html_report(self, student_data, comprehensive_report):
        """Create enhanced HTML report with professional formatting similar to CSV generator"""
        
        # Extract student information
        student_name = student_data.get('name', 'Student')
        gvc_id = student_data.get('gvc_id', 'GVC001')
        grade = student_data.get('grade_level', 'N/A')
        school = student_data.get('school', 'School Name')
        city = student_data.get('city', 'City')
        
        # Parse improvements over time for score boxes
        improvements_text = comprehensive_report.get('improvements_over_time', '')
        score_boxes_html = self._create_score_boxes(improvements_text)
        
        html_body = f"""
<div class="info-box">
    <p><strong>Student Name:</strong> {student_name}</p>
    <p><strong>GVC ID:</strong> {gvc_id}</p>
    <p><strong>Class:</strong> {grade}</p>
    <p><strong>School:</strong> {school}</p>
    <p><strong>City:</strong> {city}</p>
</div>

<h2>Highlights</h2>
<p>{comprehensive_report.get('highlights', 'Student showed excellent engagement in the roundtable discussion.')}</p>

<h2>Skill Feedback</h2>
<p>{comprehensive_report.get('skill_feedback', 'The student demonstrated strong communication and analytical abilities.')}</p>

<h2>Improvements Over Time</h2>
<p>The student has shown wonderful growth in key areas during the AI mentor roundtable session:</p>
{score_boxes_html}

<h2>Next Goals</h2>
<div class="recommendation-box">
    <p>{comprehensive_report.get('next_goals', 'Continue developing leadership, technical, and communication skills through structured practice and mentorship.')}</p>
</div>

<h2>Closing Note</h2>
<p>{comprehensive_report.get('closing_note', 'This student shows tremendous potential for continued growth and success.')}</p>

<h2>Summary Insight</h2>
<div class="insight-box">
    <p>{comprehensive_report.get('summary_insight', 'The student engagement with GVC AI mentor roundtable demonstrates readiness for advanced learning and leadership development.')}</p>
</div>

<h2>Recommended Resources</h2>
<p>Here are some resources to inspire continued growth:</p>
<div class="elegant-border">
    {self._format_resources(comprehensive_report.get('recommended_resources', ''))}
</div>

<h2>Parent Feedback Prompt</h2>
<div class="recommendation-box">
    <p>{comprehensive_report.get('parent_feedback_prompt', 'Please discuss with your child their key takeaways from the mentor session.')}</p>
</div>

<h2>Mentor Final Thought</h2>
<div class="insight-box">
    <p><em>"{comprehensive_report.get('mentor_final_thought', 'This student demonstrates exceptional potential for future success.')}"</em></p>
</div>
"""
        
        return self._create_complete_html(student_data, html_body)
    
    def _create_score_boxes(self, improvements_text):
        """Create HTML score boxes from improvements text"""
        if not improvements_text:
            return '<p>Skill development metrics will be available after continued engagement.</p>'
        
        score_boxes = []
        lines = improvements_text.split('.')
        
        for line in lines:
            if 'Current' in line and 'Potential' in line:
                # Parse skill name and scores
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    skill_name = parts[0].strip()
                    score_part = parts[1].strip()
                    
                    # Extract current and potential scores
                    if 'Current' in score_part and 'Potential' in score_part:
                        try:
                            current_match = score_part.split('Current')[1].split(',')[0].strip()
                            potential_match = score_part.split('Potential')[1].strip()
                            
                            current_score = ''.join(filter(str.isdigit, current_match))
                            potential_score = ''.join(filter(str.isdigit, potential_match))
                            
                            if current_score and potential_score:
                                score_boxes.append(f"""
<div class="keep-together" style="margin: 10px 0;">
    <strong>{skill_name}:</strong>
    <span class="current-score">Current: {current_score}</span>
    <span style="margin: 0 5px;">→</span>
    <span class="potential-score">Target: {potential_score}</span>
</div>""")
                        except:
                            pass
        
        if not score_boxes:
            return '<p>Leadership, problem-solving, and collaboration skills show strong potential for growth through continued mentorship.</p>'
        
        return ''.join(score_boxes)
    
    def _format_resources(self, resources_text):
        """Format recommended resources as HTML list"""
        if not resources_text:
            return """
            <ul>
                <li><strong>TED Talk:</strong> "How to Build Your Creative Confidence" by David Kelley</li>
                <li><strong>Book:</strong> "Mindset: The New Psychology of Success" by Carol Dweck</li>
                <li><strong>Article:</strong> "The Future of Learning" from Harvard Business Review</li>
            </ul>
            """
        
        # Try to parse the resources text
        resources_html = "<ul>\n"
        lines = resources_text.split('.')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['ted talk', 'book', 'article']):
                if line and not line.endswith('.'):
                    line += '.'
                resources_html += f"<li>{line}</li>\n"
        
        resources_html += "</ul>"
        
        # If no resources found, use default
        if resources_html == "<ul>\n</ul>":
            return self._format_resources("")
        
        return resources_html
    
    def generate_csv_style_report(self, chat_history, student_data, context_chunks):
        """Generate a complete report with CSV-style professional formatting and features"""
        try:
            # Generate comprehensive report content
            comprehensive_report = self.generate_comprehensive_report(chat_history, student_data, context_chunks)
            
            # Create enhanced HTML with professional styling
            html_report = self.create_enhanced_html_report(student_data, comprehensive_report)
            
            # Generate PDF
            try:
                pdf_content = self.generate_pdf(html_report)
                return {
                    'html': html_report,
                    'pdf': pdf_content,
                    'success': True,
                    'message': 'Professional report generated successfully with CSV-style formatting'
                }
            except Exception as pdf_error:
                return {
                    'html': html_report,
                    'pdf': None,
                    'success': False,
                    'message': f'HTML generated successfully, but PDF generation failed: {str(pdf_error)}'
                }
                
        except Exception as e:
            return {
                'html': None,
                'pdf': None,
                'success': False,
                'message': f'Report generation failed: {str(e)}'
            }