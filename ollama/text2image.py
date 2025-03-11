import ollama

# Load the pre-trained model (if needed)
model_name = "stable-diffusion"
model = ollama.load_model(model_name)

# Define your text-to-image dataset
dataset = [
    {"text": "A beautiful sunny day", "image":   "/Downloads/test1/1.jpg"},
    {"text": "A dark and stormy night", "image": "/Downloads/test1/2.jpg"},
    # ...
]

# Train the model using OLLAMA
ollama.train_model(dataset, num_epochs=10, batch_size=32)

# Use the trained model for generation
prompt = "A beautiful sunny day"
image = ollama.generate_image(model, prompt)