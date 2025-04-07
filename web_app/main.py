# --- main.py ---
# Main application orchestration file.
# *** Updated to call the new get_llm_response function ***

import stt_service
import tts_service
import rag_system
import llm_service # Now uses the real LLM service
import knowledge_base # To display available books

def run_chatbot():
    """Main function to run the chatbot interaction."""
    print("--- Welcome to the 'What If' Audiobook Chatbot (Gemini Powered) ---")

    # Let user choose a book (simplified)
    print("\nAvailable Audiobooks:")
    for book_id, details in knowledge_base.SIMULATED_KB.items():
        print(f"- {book_id}: {details['title']}")

    while True:
        selected_book_id = input("Enter the ID of the audiobook you finished (e.g., audiobook_123): ").strip()
        if knowledge_base.get_book_details(selected_book_id):
            print(f"Selected: {knowledge_base.get_book_details(selected_book_id)['title']}")
            break
        else:
            print("Invalid book ID. Please try again.")

    print("\nStarting 'What If' discussion...")
    tts_service.simulate_tts(f"Okay, let's discuss '{knowledge_base.get_book_details(selected_book_id)['title']}'. What hypothetical scenario are you wondering about?")

    chat_history = [] # Store conversation turns (User:, AI:)

    while True:
        # 1. Get user input (simulating STT)
        user_query = stt_service.simulate_stt()

        if user_query.lower() in ['quit', 'exit', 'bye']:
            tts_service.simulate_tts("Okay, ending our discussion. Hope you enjoyed exploring the 'what ifs'!")
            break

        # 2. Retrieve relevant context (Simulated RAG - IMPORTANT NEXT STEP)
        context = rag_system.retrieve_relevant_context(selected_book_id, user_query)

        # 3. Generate response (Using REAL LLM via Gemini API)
        #    Note: Passing chat_history to maintain conversation context
        ai_response = llm_service.get_llm_response(selected_book_id, user_query, context, chat_history)

        # 4. Output response (Simulated TTS - IMPORTANT NEXT STEP)
        tts_service.simulate_tts(ai_response)

        # 5. Update chat history
        chat_history.append(f"User: {user_query}")
        chat_history.append(f"AI: {ai_response}")
        # Limit history size to prevent overly long prompts
        if len(chat_history) > 8: # Keep last 4 turns (User + AI)
             chat_history = chat_history[-8:]

if __name__ == "__main__":
    run_chatbot()