# GVC AI Mentor Roundtable

A sophisticated AI-powered mentoring platform featuring 10 specialized AI mentors that provide comprehensive guidance across academic, career, personal development, and life skills domains.

## 🌟 Features

- **10 Specialized AI Mentors**: Each with unique expertise areas
  - 📚 Academic Mentor
  - 💼 Career Guide  
  - 💻 Tech Innovator
  - 🧘 Wellness Coach
  - 🌟 Life Skills Mentor
  - 🎨 Creative Mentor
  - 👑 Leadership Coach
  - 💰 Financial Advisor
  - 🗣️ Communication Expert
  - 🌍 Global Perspective Mentor

- **Interactive Roundtable Experience**: Mentors collaborate in real-time discussions
- **Student Data Integration**: Personalized guidance based on student profiles
- **Smart Report Generation**: Comprehensive summaries and recommendations
- **Modern UI**: Built with Streamlit for an intuitive user experience

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gvc-ai-mentor-roundtable.git
cd gvc-ai-mentor-roundtable
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenRouter API key to `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run main.py
```

## 📁 Project Structure

```
├── main.py                 # Main application entry point
├── agents/                 # AI mentor implementations
├── avatars/               # Avatar images for mentors
├── backend/               # Data management
├── config/                # Configuration and settings
├── core/                  # Core functionality
├── data/                  # Student data and mentor profiles
├── pages/                 # Streamlit page components
├── ui/                    # User interface components
└── utils/                 # Utility functions
```

## 🛠️ Usage

1. **Data Input**: Enter or select student information
2. **Data Review** (Optional): Review student profiles and data
3. **AI Roundtable**: Engage with AI mentors for personalized guidance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

- Never commit your `.env` file with actual API keys
- Keep your OpenRouter API key secure
- Review and sanitize any user input data

## 📞 Support

For support, please open an issue on GitHub or contact the development team.
