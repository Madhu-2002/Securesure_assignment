# securesure_bot/utils/vision_utils.py
import cv2
import numpy as np
import io
import torch
from torchvision import models
from training_model.train_model import preprocess_images
from PIL import Image
    
def predict_image(file_bytes):
    """
    This function classifies if a windowshield is damaged or not using the pretrained model
    Args:
        file_byte: The information about the image in RAW from
    Returns:
        str: A string containing:
            -The class of the windshield
    """
    num_classes = 2
    class_set = ["damaged","undamaged"]
    model = models.resnet18(pretrained = False)
    model.fc = torch.nn.Linear(model.fc.in_features,num_classes)
    model.load_state_dict(torch.load("validate_window.pth"))
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    #Pre-process the image to send send through our pre-trained model
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    transform = preprocess_images()
    input_tensor = transform(image).unsqueeze(0)
    input_tensor = input_tensor.to(device) if torch.cuda.is_available() else input_tensor

    #Classifies the image into either damaged or undamaged windshield
    with torch.no_grad():
        output = model(input_tensor)
        predicted_idx = torch.argmax(output,1)
        print(class_set[predicted_idx])
    return class_set[predicted_idx]

def validate_damage_image(file_bytes):
    """
    This function validates if a windowshield is damaged or not
    Args:
        file_byte: The information about the image in RAW from
    Returns:
        dict: A dictionary containing:
            -is_valid: Information about whether the image is a valid
            -reason: Status of the image uploaded
    """
    #Validate if the windshield is damaged
    is_broken = predict_image(file_bytes)

    #Return the response to user letting them know if they can claim insuranace on their damaged windshield
    if is_broken == "damaged":
        return {"is_valid": True, "reason": "Windshield damage detected"}
    else:
        return {"is_valid": False, "reason": "Windshield damage is not detected"}