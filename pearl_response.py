from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os, logging

# -------------------- ENV SETUP --------------------
load_dotenv()

# Initialize Groq client
client = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.4
)

# Memory for ongoing conversation
conversation_history = []

# -------------------- SAFETY SYSTEM PROMPT --------------------
system_prompt = """
You are Doctor Pearl — a compassionate and knowledgeable AI Health Assistant.
Your purpose is to provide general first-aid tips and early health guidance based on WHO and CDC best practices.
Only give tips on how to take care of general health problems.

Your rules:
- Avoid suggesting drug names, doses, or treatments.
- Encourage the user to visit a qualified doctor or Primary Health Care center for any serious or unclear symptoms.
- Focus on empathetic listening, summarizing what the user says, and providing safe, general health guidance.
- Keep your tone calm, warm, and supportive.
- When in doubt, say: "I recommend visiting a Primary Health Care center or consulting a certified medical professional."
"""

# -------------------- FUNCTION TO GET RESPONSE --------------------
def get_response(user_input: str, lang: str = "en") -> str:
    """
    Get a safe, conversational response from Doctor Pearl.
    """
    try:
        # Append user input to history
        conversation_history.append(("human", user_input))

        # Build full conversation context
        messages = [("system", system_prompt)] + conversation_history[-6:]

        # Query model
        response = client.invoke(messages)
        text_output = response.content if hasattr(response, "content") else str(response)

        # Append assistant's reply to memory
        conversation_history.append(("assistant", text_output))

        # Basic hallucination prevention — filter unsafe phrases
        banned_terms = []
        if any(term in text_output.lower() for term in banned_terms):
            return (
                "⚠️ I can’t recommend specific drugs or dosages. "
                "Please visit a health professional for detailed treatment."
            )
        

        return text_output

    except Exception as e:
        logging.error(f"Doctor Pearl error: {e}")
        return "⚠️ Sorry, Doctor Pearl encountered a temporary issue. Please try again."
