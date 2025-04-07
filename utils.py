import streamlit as st
import base64
from ai_bridge import generate_technical_questions, evaluate_technical_response

def initialize_session_state():
    """Initialize all required session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "interview_stage" not in st.session_state:
        st.session_state.interview_stage = 0
    
    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = {}
    
    if "technical_questions" not in st.session_state:
        st.session_state.technical_questions = []
    
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    
    if "evaluation_in_progress" not in st.session_state:
        st.session_state.evaluation_in_progress = False

def display_header():
    st.title("TalentScout Interview Assistant")
    st.markdown("*Intelligent technical screening for top tech talent*")
    st.divider()


def update_chat_history(role, content):
    """
    Add a new message to the chat history
    
    Args:
        role: Either 'user' or 'assistant'
        content: The message content
    """
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })

def create_message_container(role, content):
    """
    Create a styled container for chat messages
    
    Args:
        role: Either 'user' or 'assistant'
        content: The message content
    """
    is_user = role == "user"
    
    # Use different colors and alignment for user vs assistant
    if is_user:
        avatar = "👤"
        container_style = "background-color: #E3F2FD; border-radius: 10px; padding: 10px; margin-bottom: 10px; color: #000000;"
    else:
        avatar = "🤖"
        container_style = "background-color: #F5F5F5; border-radius: 10px; padding: 10px; margin-bottom: 10px; color: #000000;"
    
    cols = st.columns([1, 9])
    with cols[0]:
        st.markdown(f"<div style='font-size: 24px; text-align: center;'>{avatar}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<div style='{container_style}'>{content}</div>", unsafe_allow_html=True)

def get_tech_stack_options():
    """Return a comprehensive list of tech stack options"""
    return [
        "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Go", 
        "Ruby", "PHP", "Swift", "Kotlin", "Rust", "Scala",
        "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "Spring Boot", "ASP.NET", "Ruby on Rails", "Laravel",
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
        "SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
        "Git", "Jenkins", "CircleCI", "GitHub Actions", "Travis CI",
        "GraphQL", "REST API", "gRPC", "WebSockets"
    ]

def handle_user_response(user_input):
    """
    Process user input based on the current interview stage
    
    Args:
        user_input: Text input from the user
    """
    # If we're already in the chat history, add the new message
    update_chat_history("user", user_input)
    
    # Process based on interview stage
    if st.session_state.interview_stage == 1:
        # Collecting name
        st.session_state.candidate_info["name"] = user_input
        from ai_bridge import generate_chat_response
        
        assistant_response = generate_chat_response(
            st.session_state.chat_history,
            st.session_state.interview_stage,
            st.session_state.candidate_info
        )
        update_chat_history("assistant", assistant_response)
        
        # Move to next stage - collecting contact info
        st.session_state.interview_stage = 2
        
    elif st.session_state.interview_stage == 5:
        # During technical assessment
        if not st.session_state.technical_questions:
            # If we haven't generated questions yet, do so now
            questions = generate_technical_questions(st.session_state.candidate_info["tech_stack"])
            st.session_state.technical_questions = questions.split("\n")
            st.session_state.technical_questions = [q for q in st.session_state.technical_questions if q.strip()]
            st.session_state.current_question_index = 0
            
            # Display the first question
            if st.session_state.technical_questions:
                first_question = st.session_state.technical_questions[0]
                update_chat_history("assistant", first_question)
            else:
                # Fallback if question generation failed
                update_chat_history("assistant", "Let's discuss your technical experience. What projects have you worked on recently?")
        else:
            # Evaluating response to current question
            current_question = st.session_state.technical_questions[st.session_state.current_question_index]
            
            # Evaluate the response
            evaluation = evaluate_technical_response(
                current_question,
                user_input,
                st.session_state.candidate_info["tech_stack"]
            )
            
            # Prepare assistant response based on evaluation
            assistant_response = evaluation["response"] + " " + evaluation["follow_up"]
            update_chat_history("assistant", assistant_response)
            
            # Increment question index
            st.session_state.current_question_index += 1
            
            # If we've gone through all questions, conclude the interview
            if st.session_state.current_question_index >= len(st.session_state.technical_questions) or st.session_state.current_question_index >= 5:
                from ai_bridge import generate_chat_response
                
                # Generate concluding message
                st.session_state.interview_stage = 6
                conclusion = generate_chat_response(
                    st.session_state.chat_history,
                    st.session_state.interview_stage,
                    st.session_state.candidate_info
                )
                update_chat_history("assistant", conclusion)
                
    else:
        # For other stages, generate response based on current stage
        from ai_bridge import generate_chat_response
        
        assistant_response = generate_chat_response(
            st.session_state.chat_history,
            st.session_state.interview_stage,
            st.session_state.candidate_info
        )
        update_chat_history("assistant", assistant_response)
