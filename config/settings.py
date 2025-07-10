APP_TITLE = "GVC AI Mentor Roundtable - 10 Expert Mentors"
PAGE_ICON = "🎓"
MAX_AGENT_TURNS = 5

# Agent information with avatars and images
AGENTS_INFO = [
    {
        "name": "Academic Mentor",
        "avatar": "📚",
        "image": "avatars/academic_mentor.png"  # Fix path
    },
    {
        "name": "Career Guide",
        "avatar": "💼",
        "image": "avatars/career_guide.png"  # Fix path
    },
    {"name": "Tech Innovator", "avatar": "💻", "image": "avatars/tech_innovator.png"},
    {"name": "Wellness Coach", "avatar": "🧘", "image": "avatars/wellness_coach.png"},
    {"name": "Life Skills Mentor", "avatar": "🌟", "image": "avatars/life_skills_mentor.png"},
    {"name": "Creative Mentor", "avatar": "🎨", "image": "avatars/creative_mentor.png"},
    {"name": "Leadership Coach", "avatar": "👑", "image": "avatars/leadership_coach.png"},
    {"name": "Financial Advisor", "avatar": "💰", "image": "avatars/financial_advisor.png"},
    {"name": "Communication Expert", "avatar": "🗣️", "image": "avatars/communication_expert.png"},
    {"name": "Global Perspective Mentor", "avatar": "🌍", "image": "avatars/global_mentor.png"}
]

# Create mappings for easy access
AGENT_NAME_SET = set(agent["name"] for agent in AGENTS_INFO)
ROLE_TO_AVATAR = {agent["name"]: agent["avatar"] for agent in AGENTS_INFO}
ROLE_TO_AVATAR["User"] = "🧑"

# UI Configuration
ROUNDTABLE_RADIUS = 150
ROUNDTABLE_CENTER = (150, 150)
AVATAR_SIZE_ROUNDTABLE = (40, 40)
AVATAR_SIZE_CHAT = (60, 60)

# File paths and data settings
VECTOR_STORE_PATH = "company_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chat configuration
SIMILARITY_THRESHOLD = 0.7
MAX_MESSAGE_ATTEMPTS = 3
STREAMING_DELAY = 0.05  # seconds between words during streaming
AGENT_TURN_DELAY = 1.0  # seconds between agent turns

# Report settings
DEFAULT_REPORT_CHUNKS = 5
MAX_CHAT_HISTORY_FOR_REPORT = 50

# Student data default values
DEFAULT_STUDENT_NAME = "Ajay"
DEFAULT_STUDENT_AGE = 15
DEFAULT_STUDENT_GRADE = "10th"

# Available options for student form
GRADE_OPTIONS = ["F", "D", "C", "B", "A"]
HOBBY_OPTIONS = [
    "Reading", "Music", "Sports", "Art", "Gaming", 
    "Coding", "Travel", "Photography", "Dancing", "Cooking"
]
EXTRACURRICULAR_OPTIONS = [
    "Debate Club", "Science Club", "Drama", "Sports Team", 
    "Student Council", "Music Band", "Volunteer Work", "Robotics", "Art Club"
]

# Conversation phases
CONVERSATION_PHASES = {
    "initial": {
        "threshold": 2,
        "description": "Beginning of discussion - introduce fresh perspectives"
    },
    "development": {
        "threshold": 4,
        "description": "Build on conversation with deeper insights"
    },
    "synthesis": {
        "threshold": float('inf'),
        "description": "Provide concrete next steps and actionable recommendations"
    }
}

# Topic keywords for conversation tracking
TOPIC_KEYWORDS = {
    "academics": ["study", "academic", "school", "grade", "homework", "exam"],
    "career": ["career", "job", "work", "profession", "internship", "employment"],
    "wellness": ["stress", "wellness", "mental", "health", "anxiety", "mindfulness"],
    "life_skills": ["skill", "time", "organization", "planning", "management"],
    "creativity": ["creative", "art", "design", "innovation", "imagination"]
}