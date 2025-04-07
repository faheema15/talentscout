import os
import json
import logging
import anthropic
from anthropic import Anthropic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Anthropic client
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    logger.warning("Anthropic API key not found in environment variables")
    client = None
else:
    try:
        client = Anthropic(api_key=api_key)
        logger.info("Anthropic client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Anthropic client: {str(e)}")
        client = None

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

def generate_chat_response(chat_history, interview_stage, candidate_info):
    """
    Generate a response from Claude based on the chat history and current interview stage.
    
    Args:
        chat_history: List of previous message exchanges
        interview_stage: Current stage of the interview process
        candidate_info: Dictionary containing collected candidate information
        
    Returns:
        String containing the assistant's response
    """
    if not client:
        raise Exception("Anthropic client not initialized")
    
    # Format the system prompt
    system_prompt = get_system_prompt(interview_stage, candidate_info)
    
    # Format the messages for Claude
    messages = []
    for message in chat_history:
        role = "assistant" if message["role"] == "assistant" else "user"
        messages.append({"role": role, "content": message["content"]})
    
    logger.info(f"Generating Claude response for interview stage {interview_stage}")
    
    try:
        response = client.messages.create(
            model=DEFAULT_MODEL,
            system=system_prompt,
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error generating Claude response: {str(e)}")
        raise

def generate_technical_questions(tech_stack):
    """
    Generate technical questions based on the candidate's tech stack using Claude.
    
    Args:
        tech_stack: List of technologies the candidate is proficient in
        
    Returns:
        String containing technical questions
    """
    if not client:
        raise Exception("Anthropic client not initialized")
    
    tech_list = ", ".join(tech_stack)
    prompt = f"""Generate 5 technical interview questions appropriate for a candidate skilled in: {tech_list}. 
    The questions should:
    1. Be specific to the technologies mentioned
    2. Range from moderate to challenging difficulty
    3. Test both practical knowledge and theoretical understanding
    4. Each be answerable in 2-3 minutes
    5. Not require writing actual code
    
    Format each question on a separate line, numbered 1-5. Don't include answers."""
    
    logger.info(f"Generating technical questions with Claude for tech stack: {tech_list}")
    
    try:
        response = client.messages.create(
            model=DEFAULT_MODEL,
            system="You are an expert technical interviewer for a tech recruitment agency.",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error generating technical questions with Claude: {str(e)}")
        raise

def evaluate_technical_response(question, answer, tech_stack):
    """
    Evaluate the technical response provided by the candidate using Claude.
    
    Args:
        question: The technical question that was asked
        answer: The candidate's answer
        tech_stack: List of technologies the candidate is proficient in
        
    Returns:
        Dictionary containing evaluation and follow-up
    """
    if not client:
        raise Exception("Anthropic client not initialized")
    
    tech_list = ", ".join(tech_stack)
    prompt = f"""Evaluate the following technical response from a candidate with skills in {tech_list}.

QUESTION: {question}

CANDIDATE'S ANSWER: {answer}

Provide your evaluation in JSON format with these fields:
1. assessment: A brief evaluation of the technical accuracy (1-2 sentences)
2. response: A conversational response to the candidate that acknowledges their answer (1-2 sentences)
3. follow_up: A follow-up question that probes deeper into the topic or clarifies any misconceptions (1 sentence)

Be fair but thorough in your assessment. Don't be too harsh or too lenient.
Your response should be ONLY the JSON object with no other text."""
    
    logger.info(f"Evaluating technical response with Claude for question: {question[:50]}...")
    
    try:
        response = client.messages.create(
            model=DEFAULT_MODEL,
            system="You are an expert technical interviewer for a tech recruitment agency. Always respond in valid JSON format.",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.5
        )
        
        # Parse the JSON response
        try:
            # Clean the response to remove any potential markdown code block formatting
            cleaned_response = response.content[0].text
            cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(cleaned_response)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Claude response: {str(e)}")
            logger.error(f"Raw response: {response.content[0].text}")
            # Fallback response
            return {
                "assessment": "Unable to properly evaluate the response",
                "response": "Thank you for your answer. Let's move on to the next question.",
                "follow_up": "Could you tell me more about your practical experience with this technology?"
            }
            
    except Exception as e:
        logger.error(f"Error evaluating technical response with Claude: {str(e)}")
        raise

def get_system_prompt(interview_stage, candidate_info):
    """
    Generate the system prompt based on the current interview stage.
    
    Args:
        interview_stage: Current stage of the interview process
        candidate_info: Dictionary containing collected candidate information
        
    Returns:
        String containing the system prompt
    """
    base_prompt = """You are an intelligent hiring assistant for TalentScout, a recruitment agency specializing in tech placements. You are conducting a preliminary technical interview with a candidate. Be professional but conversational and friendly.

Candidate information collected so far:
"""
    # Add candidate info that we have so far
    for key, value in candidate_info.items():
        if key == "tech_stack" and isinstance(value, list):
            base_prompt += f"- {key}: {', '.join(value)}\n"
        else:
            base_prompt += f"- {key}: {value}\n"
    
    # Specific guidance based on interview stage
    stage_prompts = {
        1: """
You are at the INTRODUCTION stage of the interview.
Introduce yourself as the TalentScout interview assistant. 
The candidate has just provided their name. 
Acknowledge their name and ask for their contact information (email and phone number).
Be friendly and professional.
""",
        2: """
You are at the CONTACT INFORMATION stage of the interview.
The candidate has just provided their contact details.
Thank them and now ask about their years of experience and what position they're looking for.
Keep your response concise and professional.
""",
        3: """
You are at the EXPERIENCE & POSITION stage of the interview.
The candidate has just shared their experience level and desired position.
Acknowledge this information and now ask them to select their technical skills from a list that will be shown.
Encourage them to select all technologies they are proficient in.
""",
        4: """
You are at the TECHNICAL SKILLS stage of the interview.
The candidate has just selected their technical stack.
Acknowledge their skills and explain that you'll ask a few technical questions to assess their expertise.
Tell them you'll start with questions specific to their selected technologies.
""",
        5: """
You are at the TECHNICAL ASSESSMENT stage of the interview.
Listen carefully to the candidate's answers and provide thoughtful follow-up questions.
Evaluate their technical knowledge but maintain a supportive tone.
Focus on their problem-solving approach and depth of understanding.
""",
        6: """
You are at the CONCLUSION stage of the interview.
Thank the candidate for their time and responses.
Summarize what you've learned about their background and skills.
Explain that a TalentScout recruiter will contact them soon to discuss potential opportunities.
Provide a positive and encouraging conclusion to the interview.
"""
    }
    
    if interview_stage in stage_prompts:
        base_prompt += stage_prompts[interview_stage]
    
    return base_prompt
