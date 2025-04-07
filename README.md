# TalentScout - AI Hiring Assistant Chatbot  

## Project Overview  
TalentScout is an intelligent AI-powered Hiring Assistant chatbot designed to streamline the recruitment process. It interacts with candidates, gathers essential information, and asks technical questions based on the interview stage. The system dynamically uses OpenAI or Anthropic language models to generate human-like responses, ensuring a smooth and engaging candidate experience.

---

## Live Demo  

Live working demo:
[TalentScout on Streamlit](https://talentscout-l8u6jzorscte2ezubc64om.streamlit.app/)

---
## Installation Instructions  

### 1. Clone the Repository:
```bash
git clone https://github.com/faheema15/talentscout.git
cd talentscout
```

### 2. Create and Activate Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3. Install Required Packages:
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 5. Run the Application:
```bash
streamlit run app.py
```

---

## Usage Guide  

Once the application is running:

- The chatbot will interact with the candidate.
- It will ask for details like name, education, skills, and project experience.
- It dynamically generates technical questions based on the interview stage.
- If OpenAI API fails, it automatically falls back to Anthropic API for response generation.

---

## Technical Details  

### Libraries Used:
- `openai` — OpenAI API integration.
- `anthropic` — Anthropic API integration.
- `python-dotenv` — Loading environment variables.
- `logging` — For structured logs.

### Architecture:

```
app.py              → Entry point of the application
ai_bridge.py        → Handles routing between OpenAI & Anthropic APIs
openai_helper.py      → OpenAI response generation logic
anthropic_helper.py   → Anthropic response generation logic
utils.py            → Utility functions
.env                → API Keys (not shared publicly)
requirements.txt    → Dependencies
```

---

## Prompt Design Strategy  

- The prompt templates were carefully crafted to:
  - Be conversational and friendly.
  - Extract structured information from candidates.
  - Ask technical questions based on the interview stage.
  - Handle fallback gracefully if one provider fails.

---

## Challenges & Solutions  

| Challenge | Solution |
|-----------|----------|
| Handling API Failures | Implemented fallback strategy in `ai_bridge.py` to switch between OpenAI and Anthropic dynamically. |
| Structuring Prompts for Multiple Stages | Designed stage-specific prompts in helper modules for clarity and adaptability. |
| Managing Sensitive API Keys | Used `.env` files and `python-dotenv` to securely load environment variables. |
| Modular Design | Split the logic into `helpers/` and `ai_bridge.py` for maintainability and scalability. |

---

This project demonstrates the power of AI-driven chatbots in the recruitment domain. TalentScout ensures efficiency, professionalism, and adaptability while interacting with candidates.

---
