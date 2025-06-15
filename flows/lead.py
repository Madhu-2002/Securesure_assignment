# securesure_bot/flows/lead.py
from utils import state_manager, lead_utils

lead_fields = ["query_from_user","car_value", "car_make", "car_type", "car_model"]

async def handle(user_input, state, conversation_id):
    """
    This is the handler function called when user wants a lead on their car
    Args:
        user_input(str): The user's details about their car
        state: Gives the idea of what stage the user is in with answering the queries of their car
        conversation_id(str): The id that keeps record of the user's interaction with the assistant
    Returns:
        str: A string containing:
            -question: The next question prompted to the user
    """
    #Gets the step at which the user is at with regards to answering the required questions
    step = state["step"]

    #If user has answered all the questions, indicated the lead has been submitted... Send user a message indicating the same
    if step >= len(lead_fields):
        return "Your lead has already been submitted. Thank you!"

    current_field = lead_fields[step]
    state["data"][current_field] = user_input
    state["step"] += 1


    #When user submits the last query, update the databse and save it... Send user a message indiacting the same
    if state["step"] == len(lead_fields):
        lead_utils.save_lead_to_db(state["data"])
        state_manager.update_state(conversation_id, state)
        return "Thank you! Your quote request has been submitted. We'll contact you soon."
    
    #Gets the next step in the process
    next_field = lead_fields[state["step"]]
    questions = {
        "query_from_user":"",
        "car_value": "What is the estimated value of your car?",
        "car_make": "What is the make of the car, like Toyota, Ford?",
        "car_type": "Is it an SUV, Sedan, or Coupe?",
        "car_model": "What year was the car manufactured?"
    }

    #Updates the step at which the user is at
    state_manager.update_state(conversation_id, state)
    return questions[next_field]
