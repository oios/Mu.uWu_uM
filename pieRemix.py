from diffusers import DiffusionPipeline
import torch

# Load the pretrained model
pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# Move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if (device == "cpu"):
    print("cpiu")

pipeline.to(device)

# Define your prompt
prompt = "microscopic view of moss and droplets hd"

# Convert the prompt to a tensor and move it to the same device as the model
prompt_tensor = torch.tensor([prompt]).to(device)

# Generate an image
generated_images = pipeline.generate(prompt_tensor)

# The generated_images variable now contains your generated images!
