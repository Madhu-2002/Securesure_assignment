from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import torch
import torchvision.models as models
import torch.optim as optim
import torch.nn as nn

def preprocess_images():
    """
    This function is used to preprocess the images before sending them across our resnet model for fine-tuning
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return transform

def load_training_data():
    """
    This function is used to load the images from our training set
    """
    training_data = ImageFolder('training_model/training_dataset',transform=preprocess_images())
    return training_data

def train_the_model():
    """
    This function is used to fine-tune the resnet18 model to classify our training set of images.
    -We get our custom classifier that can be used to classify images into a damaged/undamaged windshield
    """
    #We use resnet18 model, Adam's optimizer and Cross-Entropy Loss function for finetuning our model
    resnet = models.resnet18(pretrained=True)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(resnet.parameters(),lr=1e-4)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_of_classes = 2
    resnet.fc = nn.Linear(resnet.fc.in_features,num_of_classes)
    train_dataset = load_training_data()
    train_loader = DataLoader(train_dataset,batch_size=2,shuffle=True)
    #We the num_of_iterations we run the process of updating the weights and biases = 200 
    num_of_iterations = 200
    resnet.train()
    resnet = resnet.to(device)
    for iteration in range(num_of_iterations):
        running_loss = 0.0
        for inputs,labels in train_loader:
            inputs,labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = resnet(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(train_loader)
    #Saves our fine-tuned model which can be used for classification of the user's uplodad image
    torch.save(resnet.state_dict(), "validate_window.pth")
