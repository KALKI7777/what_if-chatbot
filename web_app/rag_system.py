def retrieve_relevant_context(book_id, user_query):
    """
    Retrieves context relevant to the user's query from the transcribed text.
    """
    print(f"[RAG System] Searching for context related to: '{user_query}' in book '{book_id}'")
    try:
        file_path = f"{book_id}.txt"  # Construct file path based on book_id
        with open(file_path, "r") as f:
            text = f.read()
        # Basic context retrieval: return the entire text
        context = f"Context: {text}"
        print(f"[RAG System] Found context: {context[:100]}...")  # Print snippet
        return context
    except FileNotFoundError:
        return "Context: Transcribed text not found. Please run the audio transcription first."
