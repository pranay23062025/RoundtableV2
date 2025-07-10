"""Mentor profile data"""

MENTOR_CARDS = [
    {
        "title": "🎓 Academic Mentor - John",
        "education": "Ph.D. Educational Psychology (Stanford), M.Ed. (Harvard)",
        "experience": "15+ years, Former MIT Dean, 500+ institutions use his methods",
        "specialty": "Study techniques, cognitive learning, academic excellence"
    },
    {
        "title": "💼 Career Guide - Angela", 
        "education": "MBA (Wharton), B.S. Industrial Engineering (Berkeley)",
        "experience": "20+ years Fortune 500, Former Google VP, 1000+ professionals coached",
        "specialty": "Career pathways, industry trends, professional networking"
    },
    {
        "title": "💻 Tech Innovator - Greg",
        "education": "Ph.D. Computer Science (MIT), M.S. AI/ML (Carnegie Mellon)",
        "experience": "12+ years Microsoft/Amazon, CTO of 2 startups, 15 AI patents",
        "specialty": "Emerging tech, programming, AI/ML, tech entrepreneurship"
    },
    {
        "title": "🧘 Wellness Coach - Ana",
        "education": "Ph.D. Clinical Psychology (UCLA), Licensed Mental Health Counselor",
        "experience": "18+ years adolescent psychology, Former Yale wellness head",
        "specialty": "Stress management, mindfulness, emotional regulation"
    },
    {
        "title": "🌟 Life Skills Mentor - Sarah",
        "education": "M.Ed. Student Development (Columbia), Certified Life Coach",
        "experience": "25+ years youth development, Former Princeton Director, 5000+ students",
        "specialty": "Time management, organization, decision-making frameworks"
    },
    {
        "title": "🎨 Creative Mentor - David",
        "education": "MFA Fine Arts (RISD), B.A. Art History (Yale)",
        "experience": "15+ years creative director, Former head of arts education",
        "specialty": "Creative problem-solving, artistic development, design thinking"
    },
    {
        "title": "👑 Leadership Coach - Maria",
        "education": "MBA Leadership (Kellogg), Executive Leadership Certification",
        "experience": "20+ years executive leadership, Former McKinsey VP",
        "specialty": "Leadership development, team dynamics, influence strategies"
    },
    {
        "title": "💰 Financial Advisor - Robert",
        "education": "CFA, MBA Finance (Chicago Booth), Certified Financial Planner",
        "experience": "18+ years top investment firms, $500M+ assets managed",
        "specialty": "Personal finance, investment strategies, financial planning"
    },
    {
        "title": "🗣️ Communication Expert - Lisa",
        "education": "Ph.D. Communication Studies (Northwestern), M.A. Public Speaking",
        "experience": "16+ years communication coach, Former Ivy League debate head",
        "specialty": "Public speaking, interpersonal communication, presentation skills"
    },
    {
        "title": "🌍 Global Perspective Mentor - Alex",
        "education": "Ph.D. International Relations (Oxford), M.A. Cultural Anthropology",
        "experience": "22+ years international education, Former UN cultural attaché",
        "specialty": "Cultural intelligence, global citizenship, diversity appreciation"
    }
]

# Additional mentor metadata (optional enhancement)
MENTOR_METADATA = {
    "Academic Mentor - John": {
        "primary_focus": "academic_excellence",
        "target_grades": ["9th", "10th", "11th", "12th"],
        "specializations": ["study_methods", "test_prep", "learning_disabilities"],
        "approach": "evidence_based"
    },
    "Career Guide - Angela": {
        "primary_focus": "career_development",
        "industries": ["tech", "finance", "consulting", "healthcare"],
        "specializations": ["resume_building", "interview_prep", "networking"],
        "approach": "practical_experience"
    },
    "Tech Innovator - Greg": {
        "primary_focus": "technology",
        "programming_languages": ["Python", "Java", "JavaScript", "C++"],
        "specializations": ["ai_ml", "web_development", "mobile_apps", "startup"],
        "approach": "hands_on_learning"
    },
    "Wellness Coach - Ana": {
        "primary_focus": "mental_health",
        "age_groups": ["teenagers", "young_adults"],
        "specializations": ["anxiety", "depression", "stress", "mindfulness"],
        "approach": "therapeutic"
    },
    "Life Skills Mentor - Sarah": {
        "primary_focus": "life_skills",
        "skill_areas": ["time_management", "organization", "goal_setting"],
        "specializations": ["productivity", "decision_making", "habit_formation"],
        "approach": "systematic"
    },
    "Creative Mentor - David": {
        "primary_focus": "creativity",
        "creative_fields": ["visual_arts", "design", "writing", "music"],
        "specializations": ["portfolio_development", "creative_blocks", "art_career"],
        "approach": "inspiration_focused"
    },
    "Leadership Coach - Maria": {
        "primary_focus": "leadership",
        "leadership_styles": ["transformational", "servant", "authentic"],
        "specializations": ["team_building", "conflict_resolution", "influence"],
        "approach": "executive_coaching"
    },
    "Financial Advisor - Robert": {
        "primary_focus": "financial_literacy",
        "topics": ["budgeting", "investing", "college_funding", "career_finance"],
        "specializations": ["student_loans", "early_investing", "financial_planning"],
        "approach": "practical_education"
    },
    "Communication Expert - Lisa": {
        "primary_focus": "communication",
        "skill_areas": ["public_speaking", "writing", "interpersonal"],
        "specializations": ["presentation_skills", "debate", "social_confidence"],
        "approach": "practice_based"
    },
    "Global Perspective Mentor - Alex": {
        "primary_focus": "global_awareness",
        "cultural_expertise": ["cross_cultural", "international_education", "diversity"],
        "specializations": ["cultural_intelligence", "global_citizenship", "empathy"],
        "approach": "experiential"
    }
}

# Mentor groupings for different student needs
MENTOR_GROUPS = {
    "academic_support": [
        "Academic Mentor - John",
        "Life Skills Mentor - Sarah",
        "Wellness Coach - Ana"
    ],
    "career_preparation": [
        "Career Guide - Angela",
        "Tech Innovator - Greg",
        "Communication Expert - Lisa"
    ],
    "personal_development": [
        "Wellness Coach - Ana",
        "Life Skills Mentor - Sarah",
        "Leadership Coach - Maria"
    ],
    "creative_development": [
        "Creative Mentor - David",
        "Communication Expert - Lisa",
        "Global Perspective Mentor - Alex"
    ],
    "financial_planning": [
        "Financial Advisor - Robert",
        "Career Guide - Angela",
        "Life Skills Mentor - Sarah"
    ]
}

# Mentor expertise keywords for smart matching
MENTOR_KEYWORDS = {
    "Academic Mentor - John": [
        "study", "homework", "exam", "grade", "test", "learning", "school",
        "academic", "education", "memory", "focus", "concentration"
    ],
    "Career Guide - Angela": [
        "career", "job", "work", "internship", "resume", "interview", "networking",
        "professional", "industry", "employment", "workplace", "business"
    ],
    "Tech Innovator - Greg": [
        "technology", "programming", "coding", "computer", "software", "app",
        "AI", "machine learning", "startup", "innovation", "digital", "tech"
    ],
    "Wellness Coach - Ana": [
        "stress", "anxiety", "mental health", "wellness", "mindfulness", "meditation",
        "emotional", "psychology", "counseling", "therapy", "self-care", "balance"
    ],
    "Life Skills Mentor - Sarah": [
        "time management", "organization", "planning", "goals", "productivity",
        "habits", "decision making", "life skills", "personal development"
    ],
    "Creative Mentor - David": [
        "creative", "art", "design", "artistic", "imagination", "innovation",
        "portfolio", "visual", "creative thinking", "expression", "aesthetic"
    ],
    "Leadership Coach - Maria": [
        "leadership", "team", "management", "influence", "communication",
        "collaboration", "conflict", "negotiation", "executive", "strategy"
    ],
    "Financial Advisor - Robert": [
        "money", "finance", "budget", "investing", "financial", "savings",
        "college fund", "student loan", "economics", "financial planning"
    ],
    "Communication Expert - Lisa": [
        "communication", "speaking", "presentation", "public speaking", "writing",
        "interpersonal", "social", "confidence", "debate", "rhetoric"
    ],
    "Global Perspective Mentor - Alex": [
        "global", "international", "cultural", "diversity", "world", "perspective",
        "multicultural", "citizenship", "empathy", "understanding", "awareness"
    ]
}

def get_mentor_by_expertise(topic_keywords):
    """Get mentors that match given topic keywords"""
    matching_mentors = []
    topic_keywords_lower = [kw.lower() for kw in topic_keywords]
    
    for mentor_name, keywords in MENTOR_KEYWORDS.items():
        match_score = 0
        for keyword in keywords:
            if any(topic_kw in keyword.lower() or keyword.lower() in topic_kw 
                   for topic_kw in topic_keywords_lower):
                match_score += 1
        
        if match_score > 0:
            matching_mentors.append({
                "name": mentor_name,
                "score": match_score,
                "keywords_matched": match_score
            })
    
    # Sort by match score
    matching_mentors.sort(key=lambda x: x["score"], reverse=True)
    return matching_mentors

def get_mentor_card_by_name(mentor_name):
    """Get full mentor card data by name"""
    for card in MENTOR_CARDS:
        if mentor_name.lower() in card["title"].lower():
            return card
    return None

def get_mentors_for_student_profile(student_interests, academic_struggles=None):
    """Get recommended mentors based on student profile"""
    recommended = []
    
    # Map interests to mentor groups
    interest_mapping = {
        "academics": "academic_support",
        "career": "career_preparation", 
        "personal_growth": "personal_development",
        "creativity": "creative_development",
        "money": "financial_planning"
    }
    
    for interest in student_interests:
        if interest.lower() in interest_mapping:
            group = interest_mapping[interest.lower()]
            if group in MENTOR_GROUPS:
                recommended.extend(MENTOR_GROUPS[group])
    
    # Remove duplicates while preserving order
    unique_recommended = []
    for mentor in recommended:
        if mentor not in unique_recommended:
            unique_recommended.append(mentor)
    
    return unique_recommended[:5]  # Limit to top 5

def validate_mentor_data():
    """Validate mentor data integrity"""
    errors = []
    
    # Check for required fields
    required_fields = ["title", "education", "experience", "specialty"]
    
    for i, mentor in enumerate(MENTOR_CARDS):
        for field in required_fields:
            if field not in mentor or not mentor[field]:
                errors.append(f"Mentor {i}: Missing or empty field '{field}'")
    
    # Check for unique titles
    titles = [mentor["title"] for mentor in MENTOR_CARDS]
    if len(titles) != len(set(titles)):
        errors.append("Duplicate mentor titles found")
    
    # Check metadata consistency
    for mentor_name in MENTOR_METADATA:
        if not any(mentor_name in card["title"] for card in MENTOR_CARDS):
            errors.append(f"Metadata exists for non-existent mentor: {mentor_name}")
    
    return errors if errors else ["Data validation passed"]

# Student data templates (for testing/demo purposes)
SAMPLE_STUDENT_PROFILES = {
    "academic_focused": {
        "name": "Alex",
        "grade": "11th",
        "interests": ["academics", "science"],
        "challenges": ["time management", "test anxiety"],
        "goals": ["improve grades", "college prep"]
    },
    "career_oriented": {
        "name": "Jordan",
        "grade": "12th", 
        "interests": ["technology", "career"],
        "challenges": ["career uncertainty", "networking"],
        "goals": ["internship", "college major decision"]
    },
    "well_rounded": {
        "name": "Sam",
        "grade": "10th",
        "interests": ["creativity", "leadership", "academics"],
        "challenges": ["stress management", "organization"],
        "goals": ["personal growth", "skill development"]
    }
}