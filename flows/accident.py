# securesure_bot/flows/accident.py
from utils import state_manager, ocr_utils, schema

async def handle(file, state, conversation_id):
    """
    This is the handler function called when user wants to access assistance on an accident
    Args:
        file: The specific file required for insurance claim
        state: Gives the ieda of what stage the user is in with uploading the documents required for accident assitance
        conversation_id(str): The id that keeps record of the user's interaction with the assistant
    Returns:
        str: A string giving a status of the particular document uploaded
    """
    #Get the step at which the user is at with the process of claiming insurance post an accident
    step = state["step"]
    steps = schema.ACCIDENT_STEPS

    #If all documents have been collected... Send user a message indicating the same
    if step >= len(steps):
        return "All documents have been collected and validated. Your accident claim is now under review."

    current_doc = steps[step] 

    #If user hasn't uploaded the document required... Send user a message indicating the same
    if not file:
        return f"Please upload your {current_doc.replace('_', ' ')}."

    file_bytes = await file.read()
    result = ocr_utils.validate_document(current_doc, file_bytes)

    #If user uploaded a valid document, update the step the user is at and query for the next document
    if result["is_valid"]:
        state["validated"].append(current_doc)
        state["step"] += 1
        state["data"][current_doc] = file.filename
        state_manager.update_state(conversation_id, state)
        return f"""\
{current_doc.replace('_', ' ').title()} validated. 
Please upload the next document.
1.car registration copy
2.civil id copy
3.driver license copy
4.police report copy
"""
    #If user uploaded an invalid document... Send user a message indicating the same
    else:
        return f"{result['reason']} Please re-upload a valid {current_doc.replace('_', ' ')}."
