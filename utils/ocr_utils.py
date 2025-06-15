# securesure_bot/utils/ocr_utils.py
import pytesseract
from PIL import Image
import io

keyword_map = {
    "car_registration_copy": ["Plate", "License", "Owner", "Base Number", "Year of Manufacture"],
    "civil_id_copy": ["Name", "Civil ID No", "Expiry Date", "Nationality", "Gender", "Birth Date"],
    "driver_license_copy": ["License No", "Date of Issue", "Date of Expiry"],
    "vehicle_chassis_number_photo": ["Base Number"]
}

def validate_document(file_type, file_bytes, ref_data=None):
    """
    This function validates if a given document is valid based on OCR detection
    Args:
        file_type(str): The type of file the user has uploaded
        file_bytes: The file provided by the user
        ref_data: BY default set to None, when passed used as reference against which user data is compared
    Returns:
        dict: A dictionary containing:
            -is_valid: The confirmation of whether it is a valid document
            -reason: The status of the document submitted
    """
    #Reads the documnet submitted and parses it to get information about it
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    found_keywords = [kw for kw in keyword_map.get(file_type, []) if kw in text]

    #If a vehicle chasis number photo is uploaded compares it with a reference chasis number
    if file_type == "vehicle_chassis_number_photo":
        import re
        chassis_number = re.findall(r'[A-Z0-9]{6,}', text)
        if not chassis_number:
            return {"is_valid": False, "reason": "Chassis number not found in image."}
        if ref_data and ref_data.get("Base Number") not in chassis_number[0]:
            return {"is_valid": False, "reason": "Chassis number mismatch."}
        return {"is_valid": True, "reason": "Chassis number matches."}

    #If a police report document/windshield dealer stamp is submitted then there is no verification required, just store the information
    if file_type == "police_report_copy":
        return {"is_valid": True, "reason": "The police report was the last step, and was submitted successfully!"}
    
    if file_type == "windshield_dealer_stamp_photo":
        return {"is_valid": True, "reason": "The windshield dealer stamp was the last step, and was submitted successfully!"}

    #Checks if the document submitted has all the required information
    missing = set(keyword_map[file_type]) - set(found_keywords)
    #If there isn't enough information about the document, the documnet is considered invalid, else considered as valid
    if missing:
        return {"is_valid": False, "reason": f"Missing keywords: {', '.join(missing)}"}
    return {"is_valid": True, "reason": "All required keywords found."}
