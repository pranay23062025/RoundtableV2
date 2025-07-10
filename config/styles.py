"""CSS styles for the application"""

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global theme override */
.stApp {
    background-color: #FFFAF1 !important;
    color: #14213D !important;
}

/* Global font and color reset */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    color: #14213D !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #FFFAF1 !important;
    font-family: 'Inter', sans-serif !important;
    color: #14213D !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%) !important;
    border-right: 1px solid #E5E8EC !important;
    font-family: 'Inter', sans-serif !important;
    color: #14213D !important;
}

/* Typography hierarchy */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: #14213D !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

.main .block-container h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #14213D 0%, #009CA6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem !important;
}

h2 {
    font-size: 1.8rem !important;
    color: #009CA6 !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

h3 {
    font-size: 1.4rem !important;
    color: #14213D !important;
    margin-bottom: 0.8rem !important;
}

/* Ensure all text elements have proper contrast */
p, span, div, label {
    color: #14213D !important;
}

/* Button styling - Enhanced specificity with !important */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0, 156, 166, 0.15) !important;
    cursor: pointer !important;
}

/* Primary buttons - Ocean Teal - HIGHEST PRIORITY */
button[kind="primary"],
.stButton > button[kind="primary"],
div[data-testid="column"] .stButton > button[kind="primary"],
[data-testid="stVerticalBlock"] .stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #009CA6 0%, #007882 100%) !important;
    color: white !important;
    border: 1px solid #009CA6 !important;
}

button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover,
div[data-testid="column"] .stButton > button[kind="primary"]:hover,
[data-testid="stVerticalBlock"] .stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #007882 0%, #005f66 100%) !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 156, 166, 0.25) !important;
}

/* Secondary buttons - Platinum Gray - SECOND PRIORITY */
button[kind="secondary"],
.stButton > button[kind="secondary"],
div[data-testid="column"] .stButton > button[kind="secondary"],
[data-testid="stVerticalBlock"] .stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #ffffff 0%, #E5E8EC 100%) !important;
    color: #14213D !important;
    border: 1px solid #E5E8EC !important;
}

button[kind="secondary"]:hover,
.stButton > button[kind="secondary"]:hover,
div[data-testid="column"] .stButton > button[kind="secondary"]:hover,
[data-testid="stVerticalBlock"] .stButton > button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, #E5E8EC 0%, #d1d5db 100%) !important;
    color: #14213D !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Default buttons - Warm Gold - LOWEST PRIORITY (comes last) */
.stButton > button:not([kind="primary"]):not([kind="secondary"]),
.stButton > button[kind=""],
div[data-testid="column"] .stButton > button:not([kind="primary"]):not([kind="secondary"]),
[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]):not([kind="secondary"]),
button:not([kind="primary"]):not([kind="secondary"]) {
    background: linear-gradient(135deg, #F7B801 0%, #e6a600 100%) !important;
    color: white !important;
    border: 1px solid #F7B801 !important;
}

.stButton > button:not([kind="primary"]):not([kind="secondary"]):hover,
.stButton > button[kind=""]:hover,
div[data-testid="column"] .stButton > button:not([kind="primary"]):not([kind="secondary"]):hover,
[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]):not([kind="secondary"]):hover,
button:not([kind="primary"]):not([kind="secondary"]):hover {
    background: linear-gradient(135deg, #e6a600 0%, #cc9500 100%) !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(247, 184, 1, 0.25) !important;
}

/* Force override for disabled states */
.stButton > button:disabled {
    opacity: 0.6 !important;
    cursor: not-allowed !important;
    background: #cccccc !important;
    color: #666666 !important;
}

/* Chat message styling */
.stChatMessage {
    font-family: 'Inter', sans-serif !important;
    background: #ffffff !important;
    color: #14213D !important;
    border-radius: 16px !important;
    border: 1px solid #E5E8EC !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    margin-bottom: 1rem !important;
    padding: 1rem !important;
}

/* Chat message content */
.stChatMessage p, .stChatMessage div {
    color: #14213D !important;
}

/* Enhanced chat message avatar styling */
[data-testid="chatAvatarImg"] {
    width: 60px !important;
    height: 60px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #009CA6 !important;
    box-shadow: 0 2px 8px rgba(0, 156, 166, 0.2) !important;
}

/* Mentor name styling in chat */
.mentor-name-badge {
    display: inline-block !important;
    background: linear-gradient(135deg, #009CA6, #007A83) !important;
    color: white !important;
    padding: 4px 12px !important;
    border-radius: 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 8px rgba(0, 156, 166, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-family: 'Inter', sans-serif !important;
}

.user-name-badge {
    display: inline-block !important;
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    padding: 4px 12px !important;
    border-radius: 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Info/success/warning boxes */
.stInfo, .stSuccess, .stWarning {
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    font-family: 'Inter', sans-serif !important;
}

.stInfo {
    background: linear-gradient(135deg, #e6f7ff 0%, #cceeff 100%) !important;
    color: #14213D !important;
    border: 1px solid #009CA6 !important;
}

.stInfo p, .stInfo div {
    color: #14213D !important;
}

.stSuccess {
    background: linear-gradient(135deg, #e6f7f0 0%, #ccf2e6 100%) !important;
    color: #14213D !important;
    border: 1px solid #28a745 !important;
}

.stSuccess p, .stSuccess div {
    color: #14213D !important;
}

.stWarning {
    background: linear-gradient(135deg, #fff8e6 0%, #ffefcc 100%) !important;
    color: #14213D !important;
    border: 1px solid #F7B801 !important;
}

.stWarning p, .stWarning div {
    color: #14213D !important;
}

/* Input styling - FIXED */
.stTextInput > div > div > input {
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    border: 1px solid #E5E8EC !important;
    background-color: #ffffff !important;
    color: #14213D !important;
    padding: 0.5rem 0.75rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #009CA6 !important;
    box-shadow: 0 0 0 2px rgba(0, 156, 166, 0.1) !important;
    color: #14213D !important;
    background-color: #ffffff !important;
}

.stTextInput > div > div > input::placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

/* Text area styling - FIXED */
.stTextArea > div > div > textarea {
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    border: 1px solid #E5E8EC !important;
    background-color: #ffffff !important;
    color: #14213D !important;
    padding: 0.75rem !important;
    resize: vertical !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #009CA6 !important;
    box-shadow: 0 0 0 2px rgba(0, 156, 166, 0.1) !important;
    color: #14213D !important;
    background-color: #ffffff !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

/* Number input styling - FIXED */
.stNumberInput > div > div > input {
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    border: 1px solid #E5E8EC !important;
    background-color: #ffffff !important;
    color: #14213D !important;
    padding: 0.5rem 0.75rem !important;
}

.stNumberInput > div > div > input:focus {
    border-color: #009CA6 !important;
    box-shadow: 0 0 0 2px rgba(0, 156, 166, 0.1) !important;
    color: #14213D !important;
    background-color: #ffffff !important;
}

/* Select box styling - FIXED */
.stSelectbox > div > div > div {
    font-family: 'Inter', sans-serif !important;
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
    color: #14213D !important;
}

.stSelectbox > div > div > div > div {
    background-color: #ffffff !important;
    color: #14213D !important;
}

.stSelectbox label {
    color: #14213D !important;
    font-weight: 500 !important;
}

/* Fix dropdown/select styling - COMPREHENSIVE FIX */
.stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div > div {
    background-color: #ffffff !important;
    color: #14213D !important;
    border: none !important;
}

/* Fix dropdown arrow and container */
.stSelectbox [data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Fix dropdown options list */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: none !important;
}

[data-baseweb="menu"] [role="option"] {
    background-color: #ffffff !important;
    color: #14213D !important;
    padding: 8px 12px !important;
}

[data-baseweb="menu"] [role="option"]:hover {
    background-color: #f8f9fa !important;
    color: #14213D !important;
}

[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background-color: #009CA6 !important;
    color: white !important;
}

/* Fix multi-select dropdown */
.stMultiSelect > div > div {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
}

.stMultiSelect [data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
}

.stMultiSelect [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Fix select option text color specifically */
[data-baseweb="select"] [data-baseweb="select-dropdown"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Force override for dark select elements */
select, option {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Fix placeholder text in selects */
.stSelectbox [data-baseweb="select"] [data-baseweb="select-placeholder"] {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

/* Additional specificity for stubborn dropdowns */
div[data-baseweb="select"] div[data-baseweb="select-dropdown"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

div[data-baseweb="select"] div {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Fix any remaining dark select containers */
[role="combobox"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

[role="combobox"] > div {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Emergency override for all select-related elements */
[data-testid*="select"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

[data-testid*="select"] * {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* File uploader styling - FIXED */
.stFileUploader > div {
    background-color: #ffffff !important;
    border: 2px dashed #E5E8EC !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    text-align: center !important;
}

.stFileUploader > div > div {
    font-family: 'Inter', sans-serif !important;
    background-color: transparent !important;
    color: #14213D !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"] {
    background-color: #ffffff !important;
    border: 2px dashed #E5E8EC !important;
    border-radius: 12px !important;
}

.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
    color: #14213D !important;
}

/* Fix the drag and drop area specifically */
[data-testid="stFileUploadDropzone"] {
    background-color: #ffffff !important;
    border: 2px dashed #E5E8EC !important;
    border-radius: 12px !important;
    color: #14213D !important;
}

[data-testid="stFileUploadDropzone"] > div {
    background-color: transparent !important;
    color: #14213D !important;
}

/* Browse files button */
.stFileUploader button {
    background: linear-gradient(135deg, #009CA6 0%, #007882 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    cursor: pointer !important;
}

.stFileUploader button:hover {
    background: linear-gradient(135deg, #007882 0%, #005f66 100%) !important;
    transform: translateY(-1px) !important;
}

/* Fix form labels */
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label {
    color: #14213D !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 0.5rem !important;
}

/* Fix disabled inputs */
.stTextInput > div > div > input:disabled,
.stTextArea > div > div > textarea:disabled,
.stNumberInput > div > div > input:disabled {
    background-color: #F3F4F6 !important;
    color: #6B7280 !important;
    cursor: not-allowed !important;
}

/* Fix expandable sections */
.streamlit-expanderHeader {
    background-color: #ffffff !important;
    color: #14213D !important;
    border: 1px solid #E5E8EC !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
}

.streamlit-expanderContent {
    background-color: #ffffff !important;
    border: 1px solid #E5E8EC !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 1rem !important;
}

/* Fix any remaining dark containers */
div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

div[data-testid="stHorizontalBlock"] {
    background-color: transparent !important;
}

div[data-testid="column"] {
    background-color: transparent !important;
}

/* Fix specific input containers that might be dark */
[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Emergency fix for any dark input backgrounds */
input, textarea, select {
    background-color: #ffffff !important;
    color: #14213D !important;
    border: 1px solid #E5E8EC !important;
}

/* Fix placeholder text in all browsers */
input::placeholder,
textarea::placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

input::-webkit-input-placeholder,
textarea::-webkit-input-placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

input::-moz-placeholder,
textarea::-moz-placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

input:-ms-input-placeholder,
textarea:-ms-input-placeholder {
    color: #6B7280 !important;
    opacity: 0.7 !important;
}

/* Specific fix for number input dark background */
.stNumberInput div[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #14213D !important;
}

.stNumberInput input[type="number"] {
    background-color: #ffffff !important;
    color: #14213D !important;
    border: 1px solid #E5E8EC !important;
}

/* Force override any remaining dark inputs */
[data-baseweb="input"] > div {
    background-color: #ffffff !important;
}

[data-baseweb="input"] input {
    background-color: #ffffff !important;
    color: #14213D !important;
}

/* Enhanced Agent Display Styles */
.mentor-name-badge {
    display: inline-block !important;
    background: linear-gradient(135deg, #009CA6, #007A83) !important;
    color: white !important;
    padding: 4px 12px !important;
    border-radius: 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 8px rgba(0, 156, 166, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-family: 'Inter', sans-serif !important;
}

.user-name-badge {
    display: inline-block !important;
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    padding: 4px 12px !important;
    border-radius: 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Roundtable Agent Display Enhancements */
.roundtable-container {
    position: relative !important;
    width: 320px !important;
    height: 320px !important;
    margin: 15px auto !important;
    background: radial-gradient(circle at center, #f8fbff 0%, #e8f4f8 70%, #d0e8ed 100%) !important;
    border-radius: 50% !important;
    border: 4px solid #009CA6 !important;
    box-shadow: 0 8px 25px rgba(0, 156, 166, 0.3) !important;
    overflow: visible !important;
}

.roundtable-avatar {
    position: absolute !important;
    width: 50px !important;
    height: 50px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 14px !important;
    color: #333 !important;
    cursor: pointer !important;
    z-index: 5 !important;
    transition: all 0.3s ease !important;
    overflow: hidden !important;
}

.roundtable-avatar:hover {
    transform: translate(-50%, -50%) scale(1.1) !important;
}

.roundtable-name-label {
    position: absolute !important;
    font-size: 8px !important;
    font-weight: bold !important;
    color: #444 !important;
    background: rgba(255, 255, 255, 0.95) !important;
    padding: 3px 6px !important;
    border-radius: 8px !important;
    text-align: center !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    line-height: 1.1 !important;
    max-width: 65px !important;
    z-index: 6 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Agent Status Indicators */
.agent-thinking {
    animation: pulse 2s infinite !important;
    border-color: #FFD700 !important;
    background-color: #FFF8DC !important;
    box-shadow: 0 4px 16px rgba(255, 215, 0, 0.5) !important;
}

.agent-active {
    border-color: #009CA6 !important;
    background-color: #E6F3FF !important;
    box-shadow: 0 4px 16px rgba(0, 156, 166, 0.5) !important;
}

.agent-inactive {
    border-color: #CCC !important;
    background-color: #F8F9FA !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
}

@keyframes pulse {
    0%, 100% { 
        transform: translate(-50%, -50%) scale(1) !important; 
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.5) !important;
    }
    50% { 
        transform: translate(-50%, -50%) scale(1.05) !important; 
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.7) !important;
    }
}

/* Chat Message Enhancements */
.stChatMessage {
    margin-bottom: 16px !important;
}

.stChatMessage [data-testid="chatAvatarIcon-assistant"] {
    width: 50px !important;
    height: 50px !important;
    border-radius: 50% !important;
    border: 2px solid #009CA6 !important;
}

.stChatMessage [data-testid="chatAvatarIcon-user"] {
    width: 50px !important;
    height: 50px !important;
    border-radius: 50% !important;
    border: 2px solid #6366f1 !important;
}

/* Responsive Design for Enhanced Agent Display */
@media (max-width: 768px) {
    .roundtable-container {
        width: 280px !important;
        height: 280px !important;
    }
    
    .roundtable-avatar {
        width: 40px !important;
        height: 40px !important;
        font-size: 12px !important;
    }
    
    .roundtable-name-label {
        font-size: 7px !important;
        max-width: 55px !important;
        padding: 2px 4px !important;
    }
    
    .mentor-name-badge,
    .user-name-badge {
        font-size: 11px !important;
        padding: 3px 10px !important;
    }
}
</style>
"""

ROUNDTABLE_CSS = """
<style>
.roundtable-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem 0;
    background-color: transparent !important;
}

.roundtable-header {
    text-align: center !important;
    margin-bottom: 2rem !important;
    color: #14213D !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}

.circle-table {
    position: relative;
    width: 400px;
    height: 400px;
    margin: 0 auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), inset 0 2px 8px rgba(0, 156, 166, 0.1);
    border: 2px solid #E5E8EC;
}

.avatar {
    position: absolute;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    color: #14213D !important;
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid #E5E8EC;
    cursor: pointer;
    font-family: 'Inter', sans-serif !important;
    overflow: hidden;
    transform: translate(-50%, -50%); /* Center the avatar on its position */
}

/* Avatar images should fill the entire avatar */
.avatar img {
    width: 60px !important;
    height: 60px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
}

/* When showing emoji (no image), center it */
.avatar:not(:has(img)) {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.avatar.active {
    background: linear-gradient(135deg, #009CA6 0%, #007882 100%);
    color: white !important;
    border: 2px solid #009CA6;
    box-shadow: 0 8px 24px rgba(0, 156, 166, 0.3);
    transform: translate(-50%, -50%) scale(1.15);
    z-index: 10;
}

.avatar.thinking {
    background: linear-gradient(135deg, #F7B801 0%, #e6a600 100%);
    color: white !important;
    border: 2px solid #F7B801;
    box-shadow: 0 8px 24px rgba(247, 184, 1, 0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { 
        transform: translate(-50%, -50%) scale(1);
        box-shadow: 0 8px 24px rgba(247, 184, 1, 0.3);
    }
    50% { 
        transform: translate(-50%, -50%) scale(1.08);
        box-shadow: 0 12px 32px rgba(247, 184, 1, 0.4);
    }
}

.avatar-label {
    position: absolute;
    top: 65px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    text-align: center;
    font-size: 10px;
    color: #14213D !important;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 8px;
    padding: 4px 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #E5E8EC;
}

.avatar.active .avatar-label {
    background: rgba(0, 156, 166, 0.1);
    border-color: #009CA6;
    color: #009CA6 !important;
    font-weight: 600;
}

.avatar.thinking .avatar-label {
    background: rgba(247, 184, 1, 0.1);
    border-color: #F7B801;
    color: #cc9500 !important;
    font-weight: 600;
}

/* Hover effects */
.avatar:hover:not(.active):not(.thinking) {
    transform: translate(-50%, -50%) scale(1.05);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    border-color: #009CA6;
}

/* Fix center indicator background */
.center-indicator {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%) !important;
    border: 2px solid #E5E8EC !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #14213D !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    z-index: 5;
}

/* Alternative selectors for center indicator */
.circle-table::after,
.circle-table > div:first-child,
.center,
[class*="center"] {
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%) !important;
    color: #14213D !important;
}

/* Force override any dark backgrounds in the center */
.circle-table > * {
    background-color: transparent !important;
}

.circle-table > *:first-child {
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%) !important;
    color: #14213D !important;
}
</style>
"""

MENTOR_PROFILE_CSS = """
<style>
.mentor-card {
    background: linear-gradient(135deg, #ffffff 0%, #FFFAF1 100%);
    border: 2px solid #E5E8EC;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
    color: #14213D !important;
}

.mentor-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    border-color: #009CA6;
}

.mentor-card h4 {
    color: #009CA6 !important;
    margin-bottom: 0.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

.mentor-card p {
    color: #14213D !important;
    margin-bottom: 0.5rem !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
}

.mentor-card p:last-child {
    margin-bottom: 0 !important;
}

.mentor-card strong {
    color: #14213D !important;
    font-weight: 600 !important;
}

.mentor-card em {
    color: #666 !important;
    font-style: normal !important;
}

.mentor-summary-box {
    background: linear-gradient(135deg, #009CA6 0%, #007882 100%);
    color: white !important;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 2rem;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 156, 166, 0.25);
    font-family: 'Inter', sans-serif;
}

.mentor-summary-box h3 {
    color: white !important;
    margin-bottom: 1rem !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

.mentor-summary-box p {
    color: white !important;
    margin-bottom: 0 !important;
    font-size: 1.1rem !important;
    line-height: 1.6 !important;
}
</style>
"""