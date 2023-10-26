import numpy
import speech_recognition
import pyttsx3
import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

from PIL import Image
from diffusers import DiffusionPipeline

pipa = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipa.to("cuda")




recognizer = speech_recognition.Recognizer()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            
            recognizer.adjust_for_ambient_noise(mic, duration=2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower() # type: ignore
            text_tensor = torch.tensor("bubbles",dtype=torch.float16).to("cuda")
            pomos = [text_tensor]
            genera_samples = pipa.generate(pomos)
            image = genera_samples.images[0]

            print(f"Dijiste ={text} ")
    except speech_recognition.UnknownValueError:
        print("que dijooo? xd ??")
        
        