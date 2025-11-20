import streamlit as st
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="BIET - AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 50%, #F3E8FF 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #2563EB 0%, #1E40AF 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
    }
    
    .main-header p {
        color: #DBEAFE;
        margin: 0;
        font-size: 0.9rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 1rem;
        border-radius: 20px;
        border-top-right-radius: 5px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background: white;
        color: #1F2937;
        padding: 1rem;
        border-radius: 20px;
        border-top-left-radius: 5px;
        margin: 0.5rem 0;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .info-box {
        background: linear-gradient(135deg, #2A2438 0%, #443C5C 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #2A2438 0%, #443C5C 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# College Data Repository
COLLEGE_DATA = {
    "name": "Bapuji Institute of Engineering & Technology (BIET)",
    "established_year": 1985,
    "location": "Davanagere, Karnataka",
    "accreditation": "NAAC A++ Grade, NBA Accredited",
    
    "courses": [
        {
            "name": "Bachelor of Technology (B.Tech)",
            "branches": [
                {"name": "Computer Science Engineering", "duration": "4 years", "seats": 180, "eligibility": "Min 75% in 12th with Physics, Chemistry, Math"},
                {"name": "CSE(DS)", "duration": "4 years", "seats": 120, "eligibility": "Min 70% in 12th with PCM"},
                {"name": "Mechanical Engineering", "duration": "4 years", "seats": 120, "eligibility": "Min 70% in 12th with PCM"},
                {"name": "Civil Engineering", "duration": "4 years", "seats": 90, "eligibility": "Min 65% in 12th with PCM"},
                {"name": "Artificial Intelligence & ML", "duration": "4 years", "seats": 60, "eligibility": "Min 80% in 12th with PCM"}
            ]
        },
        {
            "name": "Master of Business Administration (MBA)",
            "branches": [
                {"name": "General Management", "duration": "2 years", "seats": 120, "eligibility": "Any Graduate with 50% + CAT/MAT score"},
                {"name": "Finance", "duration": "2 years", "seats": 60, "eligibility": "Any Graduate with 50% + CAT/MAT score"},
                {"name": "Marketing", "duration": "2 years", "seats": 60, "eligibility": "Any Graduate with 50% + CAT/MAT score"}
            ]
        }
    ],
    
    "admissions": {
        "process": [
            "Fill online application form on college website",
            "Upload required documents (10th, 12th marksheets, ID proof)",
            "Pay application fee of ₹1,500",
            "Appear for entrance exam (if applicable) or based on merit",
            "Attend counseling session (online/offline)",
            "Document verification",
            "Pay admission fee to confirm seat"
        ],
        "entrance_exams": ["JEE Main", "State CET", "University Entrance Test", "CAT/MAT (for MBA)"],
        "important_dates": [
            {"event": "Application Start", "date": "March 1, 2025"},
            {"event": "Application Deadline", "date": "June 15, 2025"},
            {"event": "Entrance Exam", "date": "July 1-5, 2025"},
            {"event": "Results Announcement", "date": "July 20, 2025"},
            {"event": "Counseling Starts", "date": "July 25, 2025"},
            {"event": "Classes Begin", "date": "August 15, 2025"}
        ],
        "required_documents": [
            "10th Marksheet & Certificate",
            "12th Marksheet & Certificate",
            "Transfer Certificate",
            "Migration Certificate",
            "Entrance Exam Scorecard",
            "Aadhar Card",
            "Passport size photographs (6 copies)",
            "Caste/Category Certificate (if applicable)",
            "Income Certificate (for scholarships)"
        ]
    },
    
    "fees": {
        "btech": {"tuition": 150000, "hostel": 80000, "mess": 45000, "other": 15000, "total": 290000},
        
        "mba": {"tuition": 200000, "hostel": 80000, "mess": 45000, "other": 20000, "total": 345000}
    },
    
    "scholarships": [
        {"name": "Merit Scholarship", "eligibility": "90%+ in qualifying exam", "amount": "50% tuition fee waiver", "slots": 20},
        {"name": "Sports Quota", "eligibility": "State/National level players", "amount": "25-100% fee waiver", "slots": 15},
        {"name": "Economically Weaker Section (EWS)", "eligibility": "Family income < ₹3 lakhs", "amount": "40% tuition fee waiver", "slots": 50},
        {"name": "Girl Child Scholarship", "eligibility": "Female students with 80%+", "amount": "30% tuition fee waiver", "slots": 30},
        {"name": "Alumni Ward Scholarship", "eligibility": "Children of alumni", "amount": "20% tuition fee waiver", "slots": 25}
    ],
    
    "facilities": {
        "academic": ["Smart Classrooms", "Well-stocked Library (50,000+ books)", "Advanced Labs", "Research Centers", "Computer Centers (500+ systems)", "24/7 WiFi Campus"],
        "infrastructure": ["450-acre Green Campus", "Separate Boys & Girls Hostels", "AC Auditorium (1000 capacity)", "Sports Complex", "Gymnasium", "Medical Center", "Cafeteria & Food Courts"],
        "amenities": ["Bank & ATM", "Stationery Store", "Laundry Service", "Transportation Service", "Security 24/7", "Solar Power Backup"]
    },
    
    "placements": {
        "year2024": {
            "total_students": 850,
            "students_placed": 782,
            "placement_rate": "92%",
            "highest_package": "₹45 LPA",
            "average_package": "₹8.5 LPA",
            "median_package": "₹6.2 LPA",
            "top_recruiters": ["RedBus", "Amazon", "TCS", "Infosys", "Wipro", "Cognizant", "Accenture", "Deloitte", "ICICI Bank", "HDFC Bank", "Flipkart", "PhonePe", "Oracle", "Adobe"]
        },
        "internships": "80% students receive internship opportunities in pre-final year"
    },
    
    "events": [
        {"name": "TechFest 2025", "date": "February 14-16, 2025", "description": "Annual technical festival with coding competitions, robotics, and tech talks"},
        {"name": "Davana Fest", "date": "March 20-22, 2025", "description": "Music, dance, drama, and celebrity performances"},
        {"name": "Sports Meet", "date": "January 10-15, 2025", "description": "Inter-college sports competition"}
    ],
    
    "contact": {
        "phone": "+91 8197223456",
        "email": "admissions@biet.edu",
        "website": "www.biet.edu",
        "address": "123 Innovation Drive,Davanagere, 577530, Karnataka, India"
    }
}

def create_college_context():
    """Create a formatted context string from college data"""
    context = f"""You are an AI assistant for {COLLEGE_DATA['name']}, established in {COLLEGE_DATA['established_year']}, located in {COLLEGE_DATA['location']}.

COLLEGE DATA:

COURSES OFFERED:
"""
    for course in COLLEGE_DATA['courses']:
        context += f"\n{course['name']}:\n"
        for branch in course['branches']:
            context += f"  - {branch['name']}: {branch['duration']}, {branch['seats']} seats, Eligibility: {branch['eligibility']}\n"
    
    context += f"\nADMISSION PROCESS:\n"
    for i, step in enumerate(COLLEGE_DATA['admissions']['process'], 1):
        context += f"{i}. {step}\n"
    
    context += f"\nEntrance Exams Accepted: {', '.join(COLLEGE_DATA['admissions']['entrance_exams'])}\n"
    
    context += f"\nImportant Dates:\n"
    for date in COLLEGE_DATA['admissions']['important_dates']:
        context += f"- {date['event']}: {date['date']}\n"
    
    context += f"\nRequired Documents:\n"
    for doc in COLLEGE_DATA['admissions']['required_documents']:
        context += f"- {doc}\n"
    
    context += f"\nFEE STRUCTURE (Annual in INR):\n"
    for program, fees in COLLEGE_DATA['fees'].items():
        context += f"- {program.upper()}: ₹{fees['total']:,} (Tuition: ₹{fees['tuition']:,}, Hostel: ₹{fees['hostel']:,}, Mess: ₹{fees['mess']:,})\n"
    
    context += f"\nSCHOLARSHIPS:\n"
    for scholarship in COLLEGE_DATA['scholarships']:
        context += f"- {scholarship['name']}: {scholarship['amount']} (Eligibility: {scholarship['eligibility']}, {scholarship['slots']} slots)\n"
    
    context += f"\nCAMPUS FACILITIES:\n"
    context += f"Academic: {', '.join(COLLEGE_DATA['facilities']['academic'])}\n"
    context += f"Infrastructure: {', '.join(COLLEGE_DATA['facilities']['infrastructure'])}\n"
    context += f"Amenities: {', '.join(COLLEGE_DATA['facilities']['amenities'])}\n"
    
    placement = COLLEGE_DATA['placements']['year2024']
    context += f"\nPLACEMENT STATISTICS (2024):\n"
    context += f"- Placement Rate: {placement['placement_rate']}\n"
    context += f"- Highest Package: {placement['highest_package']}\n"
    context += f"- Average Package: {placement['average_package']}\n"
    context += f"- Median Package: {placement['median_package']}\n"
    context += f"- Top Recruiters: {', '.join(placement['top_recruiters'][:10])}\n"
    context += f"- {COLLEGE_DATA['placements']['internships']}\n"
    
    context += f"\nUPCOMING EVENTS:\n"
    for event in COLLEGE_DATA['events']:
        context += f"- {event['name']} ({event['date']}): {event['description']}\n"
    
    context += f"\nCONTACT:\n"
    context += f"Phone: {COLLEGE_DATA['contact']['phone']}\n"
    context += f"Email: {COLLEGE_DATA['contact']['email']}\n"
    context += f"Website: {COLLEGE_DATA['contact']['website']}\n"
    context += f"Address: {COLLEGE_DATA['contact']['address']}\n"
    context += f"\nAccreditation: {COLLEGE_DATA['accreditation']}"
    
    return context

def get_ai_response_openai(user_message, api_key):
    """Get response from OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        context = create_college_context()
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"{context}\n\nYou are a helpful, friendly college admission assistant. Answer questions using the college data provided. Be specific with numbers, dates, and details. Use bullet points for lists, and be concise but informative."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key or contact admissions at {COLLEGE_DATA['contact']['phone']}"

def get_ai_response_gemini(user_message, api_key):
    """Get response from Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        context = create_college_context()
        
        prompt = f"""{context}

You are a helpful, friendly college admission assistant. Answer the student's question using the college data provided above. Be specific with numbers, dates, and details.

Student Question: {user_message}

Provide a helpful, conversational response. Use bullet points for lists, and be concise but informative."""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key or contact admissions at {COLLEGE_DATA['contact']['phone']}"

def get_ai_response_anthropic(user_message, api_key):
    """Get response from Anthropic Claude API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        context = create_college_context()
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""{context}

You are a helpful, friendly college admission assistant. Answer the student's question using the college data provided above. Be specific with numbers, dates, and details.

Student Question: {user_message}

Provide a helpful, conversational response. Use bullet points for lists, and be concise but informative."""
                }
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key or contact admissions at {COLLEGE_DATA['contact']['phone']}"

def get_ai_response_groq(user_message, api_key):
    """Get response from Groq API (Fast, Free tier available)"""
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        context = create_college_context()
        
        response = client.chat.completions.create(
            model="allam-2-7b",
            messages=[
                {"role": "system", "content": f"{context}\n\nYou are a helpful, friendly college admission assistant. Answer questions using the college data provided. Be specific with numbers, dates, and details."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key or contact admissions at {COLLEGE_DATA['contact']['phone']}"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Welcome to {COLLEGE_DATA['name']}! 👋 I'm your AI assistant, here to help you with information about our courses, admissions, fees, scholarships, campus facilities, placements, and upcoming events. How can I assist you today?"
        }
    ]

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "OpenAI (GPT-4)"

# Header
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="background: white; padding: 0.5rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 2rem;">
            🎓
        </div>
        <div>
            <h1>{COLLEGE_DATA['name']}</h1>
            <p>AI Assistant • Est. {COLLEGE_DATA['established_year']} • {COLLEGE_DATA['location']}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 AI Configuration")
    
    # API Provider Selection
    api_provider = st.selectbox(
        "Select AI Provider",
        ["OpenAI (GPT-4)", "Google Gemini", "Anthropic Claude", "Groq (Fast & Free)"],
        index=["OpenAI (GPT-4)", "Google Gemini", "Anthropic Claude", "Groq (Fast & Free)"].index(st.session_state.api_provider)
    )
    st.session_state.api_provider = api_provider
    
    # API Key Input with provider-specific help
    help_text = {
        "OpenAI (GPT-4)": "Get your API key from https://platform.openai.com/api-keys",
        "Google Gemini": "Get your API key from https://makersuite.google.com/app/apikey",
        "Anthropic Claude": "Get your API key from https://console.anthropic.com/",
        "Groq (Fast & Free)": "Get your FREE API key from https://console.groq.com/"
    }
    
    api_key = st.text_input(
        f"Enter {api_provider} API Key",
        type="password",
        value=st.session_state.api_key,
        help=help_text[api_provider]
    )
    st.session_state.api_key = api_key
    
    if not api_key:
        st.warning(f"⚠️ Please enter your {api_provider} API key to start chatting!")
        st.info("💡 **Recommendation**: Try Groq for fast, free API access!")
    
    # Installation instructions
    with st.expander("📦 Installation Instructions"):
        if api_provider == "OpenAI (GPT-4)":
            st.code("pip install openai", language="bash")
        elif api_provider == "Google Gemini":
            st.code("pip install google-generativeai", language="bash")
        elif api_provider == "Anthropic Claude":
            st.code("pip install anthropic", language="bash")
        elif api_provider == "Groq (Fast & Free)":
            st.code("pip install groq", language="bash")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Access")
    
    quick_topics = [
        ("📚 Courses", "Tell me about available courses"),
        ("📝 Admissions", "What is the admission process?"),
        ("💰 Fees", "What is the fee structure?"),
        ("🏆 Scholarships", "Tell me about scholarships"),
        ("🏛️ Campus", "What facilities are available on campus?"),
        ("📊 Placements", "Show me placement statistics"),
        ("📅 Events", "What events are upcoming?"),
        ("📞 Contact", "How can I contact the college?")
    ]
    
    for icon_text, prompt in quick_topics:
        if st.button(icon_text, key=icon_text, use_container_width=True):
            if api_key:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("Getting response..."):
                    # Route to appropriate API
                    if api_provider == "OpenAI (GPT-4)":
                        response = get_ai_response_openai(prompt, api_key)
                    elif api_provider == "Google Gemini":
                        response = get_ai_response_gemini(prompt, api_key)
                    elif api_provider == "Anthropic Claude":
                        response = get_ai_response_anthropic(prompt, api_key)
                    else:  # Groq
                        response = get_ai_response_groq(prompt, api_key)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
        <h4>📞 Contact Us</h4>
        <p>📧 {email}</p>
        <p>☎️ {phone}</p>
        <p>🌐 {website}</p>
    </div>
    """.format(**COLLEGE_DATA['contact']), unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="highlight-box">
        <h4>🏆 Highlights</h4>
        <p>✓ {COLLEGE_DATA['accreditation']}</p>
        <p>✓ {COLLEGE_DATA['placements']['year2024']['placement_rate']} Placements</p>
        <p>✓ {COLLEGE_DATA['placements']['year2024']['highest_package']} Highest Package</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Welcome to {COLLEGE_DATA['name']}! 👋 I'm your AI assistant. How can I assist you today?"
            }
        ]
        st.rerun()

# Main chat area
st.markdown("### 💬 Chat with AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 You:</strong><br>{message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong>🤖 Assistant:</strong><br>{message['content']}
        </div>
        """, unsafe_allow_html=True)

# Chat input
if api_key:
    user_input = st.chat_input("Ask about courses, fees, admissions, placements...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response based on selected provider
        with st.spinner("🤔 Thinking..."):
            if api_provider == "OpenAI (GPT-4)":
                response = get_ai_response_openai(user_input, api_key)
            elif api_provider == "Google Gemini":
                response = get_ai_response_gemini(user_input, api_key)
            elif api_provider == "Anthropic Claude":
                response = get_ai_response_anthropic(user_input, api_key)
            else:  # Groq
                response = get_ai_response_groq(user_input, api_key)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update chat
        st.rerun()
else:
    st.info(f"👈 Please enter your {api_provider} API key in the sidebar to start chatting!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>Powered by {api_provider} • Available 24/7 • Instant Responses</p>
    <p style="font-size: 0.8rem;">© 2025 {COLLEGE_DATA['name']} • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)