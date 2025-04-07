# --- llm_service.py ---
# Integrates with the Gemini API for LLM interaction.
# *** Requires google-generativeai library and API key ***

import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import knowledge_base # Needed for getting book title in prompt

# Configure the Gemini API key
# IMPORTANT: Set the GEMINI_API_KEY environment variable before running.
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    print("[LLM Service] Gemini API configured.")
except Exception as e:
    print(f"[LLM Service] ERROR configuring Gemini API: {e}")
    print("Please ensure the 'google-generativeai' library is installed and")
    print("the GEMINI_API_KEY environment variable is set correctly.")
    # Exit or handle gracefully if API key is missing in a real app
    exit() # Simple exit for prototype

# Select the model
# Use a model appropriate for chat/conversation, like 'gemini-1.5-flash' or 'gemini-pro'
MODEL_NAME = "gemini-1.5-flash" # Or "gemini-pro"
model = genai.GenerativeModel(MODEL_NAME)
print(f"[LLM Service] Using model: {MODEL_NAME}")

def get_llm_response(book_id, user_query, context, chat_history):
    """
    Generates an LLM response using the Gemini API based on the query,
    context, and history.
    """
    print("\n[LLM Service] Preparing prompt for Gemini...")
    book_title = knowledge_base.get_book_details(book_id)['title']

    # Format chat history for the prompt
    formatted_history = "\n".join(chat_history)

    # Construct the prompt for the Gemini API
    # This prompt structure guides the model on its role, context, and task.
    prompt = f"""You are a helpful and creative chatbot discussing hypothetical "what if" scenarios about audiobooks.
You have access to the following information about the audiobook '{book_title}':

--- Audiobook Context ---
{context}
--- End Context ---

You are having a conversation with a user. Here is the recent history:
--- Conversation History ---
{formatted_history}
--- End History ---

The user's latest question is: "{user_query}"

Based *only* on the provided Audiobook Context and Conversation History, answer the user's 'what if' question. Be creative but stay consistent with the themes and characters mentioned in the context. If the context doesn't provide enough information to answer definitively, acknowledge that and offer a plausible speculation based on the available details.
"""
# *** FIX: Evaluate the expression before the f-string ***
    prompt_snippet = prompt[:150].replace('\n', ' ')
    print(f"[LLM Service] Sending prompt to Gemini (first 150 chars): {prompt_snippet}...")

    try:
        # Make the API call
        response = model.generate_content(prompt)

        # Extract the text response
        # Ensure response.text exists and handle potential API issues gracefully
        if response and response.text:
             ai_text = response.text.strip()
             print("[LLM Service] Received response from Gemini.")
             return ai_text
        else:
             # Handle cases where the API might return an empty or malformed response
             print("[LLM Service] Warning: Received no text content from Gemini.")
             # Check response.prompt_feedback for safety blocks if needed
             if response.prompt_feedback:
                 print(f"[LLM Service] Prompt Feedback: {response.prompt_feedback}")
             return "I apologize, I encountered an issue generating a response. Could you try rephrasing?"

    except Exception as e:
        print(f"[LLM Service] ERROR calling Gemini API: {e}")
        # Provide a fallback response in case of API errors
        return "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."
