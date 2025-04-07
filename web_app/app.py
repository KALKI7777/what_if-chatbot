
from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import knowledge_base
import rag_system
import llm_service
from llm_service import model
import tts_service

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key


@app.route("/", methods=['GET', 'POST'])
def initialize():
    # Transcribe audio and save to file
    import stt_service
    transcription = stt_service.transcribe_audio()
    with open("romeo_and_juliet.txt", "w") as f:
        f.write(transcription)
    return "Audio transcribed and saved to romeo_and_juliet.txt"

@app.route("/chatbot", methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []

    answer = None
    if request.method == 'POST':
        question = request.form['question']
        context = rag_system.retrieve_relevant_context("romeo_and_juliet", question)
        chat_history = session['chat_history']
        formatted_history = "\n".join(chat_history)

        prompt = f"""You are a helpful and creative chatbot discussing hypothetical "what if" scenarios about audiobooks.
You have access to the following information about the audiobook:
{context}

Here is the recent conversation history:
{formatted_history}

The user's latest question is: "{question}"

Based *only* on the provided Audiobook Context and Conversation History, answer the user's 'what if' question. Be creative but stay consistent with the themes and characters mentioned in the context. If the context doesn't provide enough information to answer definitively, acknowledge that and offer a plausible speculation based on the available details.
"""
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                answer = response.text.strip()
            else:
                answer = "I apologize, I encountered an issue generating a response. Could you try rephrasing?"
        except Exception as e:
            print(f"[LLM Service] ERROR calling Gemini API: {e}")
            answer = "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."

        session['chat_history'].append(f"User: {question}")
        session['chat_history'].append(f"AI: {answer}")

    return render_template("index.html", answer=answer)

@app.route("/tts")
def tts():
    text = request.args.get("text")
    tts_service.simulate_tts(text)
    return ""

if __name__ == "__main__":
    app.run(debug=True)