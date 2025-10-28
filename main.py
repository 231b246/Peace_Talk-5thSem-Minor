import os
from fastapi import FastAPI
from dotenv import load_dotenv
from models import ChatRequest  
from chat_engine import get_response    
from crisis import contains_crisis_keywords, SAFETY_MESSAGE        
from logger import log_chat
from doc_engine import query_documents
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Chat Assistant")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can replace "*" with your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    """
    Main endpoint for handling chatbot conversations with memory.
    """
    session_id = request.session_id
    user_query = request.message

    try:
        # Step 1: Check for crisis-related language
        is_crisis = contains_crisis_keywords(user_query)
        if is_crisis:
            bot_response = SAFETY_MESSAGE
        else:
            # Step 2: Try document-based response
            doc_response = query_documents(user_query)
            if doc_response and "I don't know" not in doc_response:
                bot_response = doc_response
            else:
                # Step 3: Fallback to conversational memory model
                bot_response = get_response(session_id, user_query)

        # Step 4: Log the interaction
        log_chat(session_id, user_query, bot_response, is_crisis)

        return {"response": bot_response}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


@app.post("/doc-chat")
def chat_with_documents(request: ChatRequest):
    """
    Endpoint for direct document-based Q&A.
    """
    try:
        response = query_documents(request.message)
        return {"response": response}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
