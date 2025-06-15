# securesure_bot/utils/state_manager.py
import os
import json

CONV_DIR = "conversations"
os.makedirs(CONV_DIR, exist_ok=True)

def get_state_file_path(conversation_id):
    """
    This function returns the file path where the particular conversation is stored
    Args:
        conversation_id(str): The conversation_id that we want to continue with
    Returns:
        file path: The path of the file where the state if the conversation is stored
    """
    return os.path.join(CONV_DIR, f"{conversation_id}.json")

def create_new_conversation(conversation_id):
    """
    This function creates a new conversation with the specified conversation_id
    Args:
        conversation_id(str): The conversation_id of the newly created conversation
    """
    path = get_state_file_path(conversation_id)
    state = {"flow": None, "step": 0, "data": {}, "validated": []}
    #Writes a JSON string to the newly created conversation
    with open(path, "w") as f:
        json.dump(state, f)

def get_state(conversation_id):
    """
    This function returns the state of the particular conversation
    Args:
        conversation_id(str): The conversation_id that we want to continue with
    Returns:
        The JSON string that has the current state of the conversation
    """
    path = get_state_file_path(conversation_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    #If the path doesn't exist then returns the default JSON string
    return {"flow": None, "step": 0, "data": {}, "validated": []}

def update_state(conversation_id, state):
    """
    This function returns the state of the particular conversation
    Args:
        conversation_id(str): The conversation_id whose state needs to updated
        state: The state we need to update our conversation to
    Returns:
        The JSON string that the state of the conversation was updated to
    """
    path = get_state_file_path(conversation_id)
    with open(path, "w") as f:
        json.dump(state, f)
