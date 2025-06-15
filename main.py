# securesure_bot/main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from utils import state_manager
from flows import accident, windshield, lead, faq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import uuid

def get_best_course_of_action(query):
    """
    Gets the best course of action for the user query
    Args:
        query (str): Query from the user
    Returns:
        str: A string containing:
            -best_action: The best action to take, i.e whether it is an accident, windowshield damage, lead or FAQ.

    """
    #Load the csv file
    df = pd.read_csv("test_dataset/training_user_language.csv")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    #Generate the embeddings
    df["embeddings"] = df["user_input"].apply(lambda x: model.encode(x).tolist())

    #Embed the query
    query_vec = model.encode([query])

    # Compute similarity
    embeddings_matrix = np.array(df['embeddings'].tolist())
    similarities = cosine_similarity(query_vec, embeddings_matrix)[0]

    # Get best match
    best_idx = similarities.argmax()
    best_action = df.iloc[best_idx]['action']

    return best_action

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.post("/chat")
async def chat(user_input: str = Form(None), file: UploadFile = None, conversation_id: str = Form(...)):
    """
    Defines the POST api to take input from the user
    Args:
        user_input(str): The user request, indicating if they want assitance with an accident, windowshield damage, lead or FAQ
        file: The specific file required for insurance claim
        conversation_id(str): The id that keeps record of the user's interaction with the assistant
    Returns:
        dict: A dictionary containing:
            -response: The response from the assistant
            -conversation_id: The id that keeps record of the user's interaction with the assistant
    """
    # Generate new conversation ID if not given
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        state_manager.create_new_conversation(conversation_id)

    state = state_manager.get_state(conversation_id)

    if not state["flow"]:
        # Detect flow
        state["flow"] = get_best_course_of_action(user_input)
        state_manager.update_state(conversation_id, state)

    # Dispatch to flow
    if state["flow"] == "accident":
        response = await accident.handle(file, state, conversation_id)
    elif state["flow"] == "windshield":
        response = await windshield.handle(file, state, conversation_id)
    elif state["flow"] == "lead":
        response = await lead.handle(user_input, state, conversation_id)
    else:
        response = await faq.handle(user_input, state, conversation_id)

    return {"response": response, "conversation_id": conversation_id}
