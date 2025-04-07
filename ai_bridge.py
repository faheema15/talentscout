import os
import json
import logging
import streamlit as st  # for Streamlit secrets

#To load API Keys locally
# from dotenv import load_dotenv
# load_dotenv()

# Load API Keys in streamlit
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check which AI providers are available
has_openai = bool(openai_api_key)
has_anthropic = bool(anthropic_api_key)

logger.info(f"AI providers available - OpenAI: {has_openai}, Anthropic: {has_anthropic}")

# Import the appropriate modules based on available API keys
openai_helper = None
anthropic_helper = None

if has_openai:
    try:
        import openai_helper
        logger.info("Successfully imported OpenAI helper")
    except Exception as e:
        logger.error(f"Failed to import OpenAI helper: {str(e)}")
        has_openai = False

if has_anthropic:
    try:
        import anthropic_helper
        logger.info("Successfully imported Anthropic helper")
    except Exception as e:
        logger.error(f"Failed to import Anthropic helper: {str(e)}")
        has_anthropic = False

def generate_chat_response(chat_history, interview_stage, candidate_info):
    """
    Generate a response using the available LLM provider.
    Tries OpenAI first, falls back to Anthropic if OpenAI fails.
    
    Args:
        chat_history: List of previous message exchanges
        interview_stage: Current stage of the interview process
        candidate_info: Dictionary containing collected candidate information
        
    Returns:
        String containing the assistant's response
    """
    # Try OpenAI first if available
    if has_openai:
        try:
            logger.info("Attempting to generate response using OpenAI")
            return openai_helper.generate_chat_response(chat_history, interview_stage, candidate_info)
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}. Falling back to Anthropic if available.")
            if not has_anthropic:
                return f"I apologize, but I'm having trouble connecting to our AI systems. Please try again later or contact TalentScout directly. Error: {str(e)}"
    
    # Fall back to Anthropic or use it directly if OpenAI is not available
    if has_anthropic:
        try:
            logger.info("Generating response using Anthropic")
            return anthropic_helper.generate_chat_response(chat_history, interview_stage, candidate_info)
        except Exception as e:
            logger.error(f"Anthropic error: {str(e)}")
            return f"I apologize, but I'm having trouble connecting to our AI systems. Please try again later or contact TalentScout directly. Error: {str(e)}"
    
    # If neither is available
    logger.error("No AI providers available")
    return "I apologize, but I'm unable to connect to our AI systems. Please contact TalentScout directly for assistance."

def generate_technical_questions(tech_stack):
    """
    Generate technical questions based on the candidate's tech stack.
    Tries OpenAI first, falls back to Anthropic if OpenAI fails.
    
    Args:
        tech_stack: List of technologies the candidate is proficient in
        
    Returns:
        String containing technical questions
    """
    # Try OpenAI first if available
    if has_openai:
        try:
            logger.info("Attempting to generate technical questions using OpenAI")
            return openai_helper.generate_technical_questions(tech_stack)
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}. Falling back to Anthropic if available.")
            if not has_anthropic:
                return f"I apologize, but I'm having trouble generating technical questions. Please provide more details about your experience with these technologies instead. Error: {str(e)}"
    
    # Fall back to Anthropic or use it directly if OpenAI is not available
    if has_anthropic:
        try:
            logger.info("Generating technical questions using Anthropic")
            return anthropic_helper.generate_technical_questions(tech_stack)
        except Exception as e:
            logger.error(f"Anthropic error: {str(e)}")
            return f"I apologize, but I'm having trouble generating technical questions. Please provide more details about your experience with these technologies instead. Error: {str(e)}"
    
    # If neither is available
    logger.error("No AI providers available for generating technical questions")
    return "I apologize, but I'm unable to generate technical questions at this time. Please describe your experience with these technologies in your own words."

def evaluate_technical_response(question, answer, tech_stack):
    """
    Evaluate the technical response provided by the candidate.
    Tries OpenAI first, falls back to Anthropic if OpenAI fails.
    
    Args:
        question: The technical question that was asked
        answer: The candidate's answer
        tech_stack: List of technologies the candidate is proficient in
        
    Returns:
        JSON string containing evaluation and follow-up
    """
    # Try OpenAI first if available
    if has_openai:
        try:
            logger.info("Attempting to evaluate technical response using OpenAI")
            return openai_helper.evaluate_technical_response(question, answer, tech_stack)
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}. Falling back to Anthropic if available.")
            if not has_anthropic:
                error_response = {
                    "assessment": "Unable to evaluate response",
                    "response": f"Thank you for your answer. I'm having some technical difficulties with my evaluation system.",
                    "follow_up": "Can you tell me more about your experience with this technology?"
                }
                return error_response
    
    # Fall back to Anthropic or use it directly if OpenAI is not available
    if has_anthropic:
        try:
            logger.info("Evaluating technical response using Anthropic")
            return anthropic_helper.evaluate_technical_response(question, answer, tech_stack)
        except Exception as e:
            logger.error(f"Anthropic error: {str(e)}")
            error_response = {
                "assessment": "Unable to evaluate response",
                "response": f"Thank you for your answer. I'm having some technical difficulties with my evaluation system.",
                "follow_up": "Can you tell me more about your experience with this technology?"
            }
            return error_response
    
    # If neither is available
    logger.error("No AI providers available for evaluating technical response")
    error_response = {
        "assessment": "Unable to evaluate response",
        "response": "Thank you for your answer. I'm currently unable to access our evaluation system.",
        "follow_up": "Can you tell me more about your experience with this technology?"
    }
    return error_response

def get_system_prompt(interview_stage, candidate_info):
    """
    Get the system prompt for the current interview stage.
    Uses OpenAI's prompt if available, otherwise Anthropic's.
    
    Args:
        interview_stage: Current stage of the interview process
        candidate_info: Dictionary containing collected candidate information
        
    Returns:
        String containing the system prompt
    """
    if has_openai:
        return openai_helper.get_system_prompt(interview_stage, candidate_info)
    elif has_anthropic:
        return anthropic_helper.get_system_prompt(interview_stage, candidate_info)
    else:
        # Basic fallback prompt if neither is available
        return "You are an intelligent hiring assistant for TalentScout. Conduct a technical interview in a friendly manner."
