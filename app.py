import streamlit as st
from ai_bridge import generate_chat_response
from utils import (
    initialize_session_state,
    display_header,
    update_chat_history,
    create_message_container,
    get_tech_stack_options,
    handle_user_response
)

# Initialize page config
st.set_page_config(
    page_title="TalentScout Interview Assistant",
    page_icon="👨‍💼",
    layout="wide"
)

# Add global styling
st.markdown("""
<style>
/* Make sure all text inputs have black text on white background */
input[type="text"], input[type="number"], input[type="email"], textarea {
    color: black !important;
    background-color: white !important;
}
/* Style buttons consistently */
.stButton button {
    background-color: #2E86C1 !important;
    color: white !important;
    font-weight: bold !important;
}
/* Style form submit buttons */
.stFormSubmit button {
    background-color: #2E86C1 !important;
    color: white !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Display header
display_header()

# Sidebar for application information
with st.sidebar:
    st.markdown("## About TalentScout")
    st.markdown("TalentScout is a specialized recruitment agency focusing on tech placements.")
    st.markdown("This interview assistant helps us gather initial information and conduct preliminary technical assessments.")
    
    # Display current progress in the interview process
    st.markdown("## Interview Progress")
    
    # Show checkboxes based on interview progress
    st.checkbox("Introduction", value=True, disabled=True)
    st.checkbox("Personal Information", 
                value=st.session_state.interview_stage > 1, 
                disabled=True)
    st.checkbox("Experience & Position", 
                value=st.session_state.interview_stage > 2, 
                disabled=True)
    st.checkbox("Technical Skills Assessment", 
                value=st.session_state.interview_stage > 3, 
                disabled=True)
    st.checkbox("Interview Conclusion", 
                value=st.session_state.interview_stage > 4, 
                disabled=True)

# Main chat container
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.chat_history:
        create_message_container(message["role"], message["content"])
    
    # If this is the start of the conversation, initiate it
    if len(st.session_state.chat_history) == 0:
        initial_message = "Hello! I'm the TalentScout interview assistant. I'm here to learn about your skills and experience for potential tech positions. Let's start with your name."
        update_chat_history("assistant", initial_message)
        st.session_state.interview_stage = 1
        st.rerun()

# Handle user input
user_input_container = st.container()

with user_input_container:
    # Conditional form based on interview stage
    if st.session_state.interview_stage == 2:  # Collecting contact info
        with st.form(key="contact_form"):
            contact_email = st.text_input("Email address:")
            contact_phone = st.text_input("Phone number:")
            submit_contact = st.form_submit_button("Submit")
            
            if submit_contact:
                contact_info = f"Email: {contact_email}, Phone: {contact_phone}"
                update_chat_history("user", contact_info)
                st.session_state.candidate_info["contact"] = contact_info
                
                # Generate next assistant response
                assistant_response = generate_chat_response(
                    st.session_state.chat_history,
                    st.session_state.interview_stage,
                    st.session_state.candidate_info
                )
                update_chat_history("assistant", assistant_response)
                
                # Move to next stage
                st.session_state.interview_stage = 3
                st.rerun()
                
    elif st.session_state.interview_stage == 3:  # Collecting experience and position
        with st.form(key="experience_form"):
            years_experience = st.number_input("Years of experience:", min_value=0, max_value=50)
            desired_position = st.text_input("Desired position:")
            submit_exp = st.form_submit_button("Submit")
            
            if submit_exp:
                exp_info = f"Experience: {years_experience} years, Desired position: {desired_position}"
                update_chat_history("user", exp_info)
                st.session_state.candidate_info["experience"] = years_experience
                st.session_state.candidate_info["position"] = desired_position
                
                # Generate next assistant response
                assistant_response = generate_chat_response(
                    st.session_state.chat_history,
                    st.session_state.interview_stage,
                    st.session_state.candidate_info
                )
                update_chat_history("assistant", assistant_response)
                
                # Move to next stage
                st.session_state.interview_stage = 4
                st.rerun()
                
    elif st.session_state.interview_stage == 4:  # Collecting tech stack
        with st.form(key="tech_stack_form"):
            tech_options = get_tech_stack_options()
            selected_techs = st.multiselect(
                "Select your tech stack:", 
                options=tech_options,
                help="Choose all technologies you're proficient in"
            )
            
            submit_tech = st.form_submit_button("Submit")
            
            if submit_tech and selected_techs:
                tech_info = f"Tech skills: {', '.join(selected_techs)}"
                update_chat_history("user", tech_info)
                st.session_state.candidate_info["tech_stack"] = selected_techs
                
                # Generate next assistant response with technical questions
                assistant_response = generate_chat_response(
                    st.session_state.chat_history,
                    st.session_state.interview_stage,
                    st.session_state.candidate_info
                )
                update_chat_history("assistant", assistant_response)
                
                # Move to next stage - technical Q&A
                st.session_state.interview_stage = 5
                st.rerun()
    
    else:  # Regular text input for other stages
        user_input = st.text_input("Your response:", key="user_message")
        
        if st.button("Send") and user_input:
            # Handle user's message based on the current stage
            handle_user_response(user_input)
            st.rerun()
