# securesure_bot/flows/windshield.py
from utils import state_manager, ocr_utils, vision_utils, schema

async def handle(file, state, conversation_id):
    """
    This is the handler function called when user wants to report a broken windshield
    Args:
        file: The specific file required for insurance claim
        state: Gives the ieda of what stage the user is in with uploading the documents required for reporting a broken windshield
        conversation_id(str): The id that keeps record of the user's interaction with the assistant
    Returns:
        str: A string giving a status of the particular document uploaded
    """
    #Get the step at which the user is at with the process of reporting a broken windshield
    step = state["step"]
    steps = schema.WINDSHIELD_STEPS

    #If all documents have been collected... Send user a message indicating the same
    if step >= len(steps):
        return "All documents have been validated. Your windshield claim is now under review."

    current_doc = steps[step]

    #If user hasn't uploaded the document required... Send user a message indicating the same
    if not file:
        return f"Please upload your {current_doc.replace('_', ' ')}."

    file_bytes = await file.read()

    #Checking if the windshield is damaged
    if current_doc == "damage_windshield_photo":
        result = vision_utils.validate_damage_image(file_bytes)
    #Checking if the Chasis number matches the refernce Chasis number
    elif current_doc == "vehicle_chassis_number_photo":
        base_number_doc = state["data"].get("car_registration_copy")
        base_number = {"Base Number": "ABC12345XYZ"} if base_number_doc else {}
        result = ocr_utils.validate_document(current_doc, file_bytes, ref_data=base_number)
    #Checking if the uploaded document is valid based on OCR detection
    else:
        result = ocr_utils.validate_document(current_doc, file_bytes)

    #If the uploaded document is valid updates the step at which the user is at and asks for the next document
    if result["is_valid"]:
        state["validated"].append(current_doc)
        state["step"] += 1
        state["data"][current_doc] = file.filename
        state_manager.update_state(conversation_id, state)
        return f"""\
{current_doc.replace('_', ' ').title()} validated.
Please upload the next document.
1.car_registration_copy
2.civil_id_copy
3.driver_license_copy
4.damage_windshield_photo
5.vehicle_chassis_number_photo
6.windshield_dealer_stamp_photo
"""
    #If user uploaded an invalid document... Send user a message indicating the same
    else:
        return f"{result['reason']} Please re-upload a valid {current_doc.replace('_', ' ')}."
