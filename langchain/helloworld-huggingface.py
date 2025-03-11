from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-base")
result = pipe("Translate English to French: Hello, how are you?")
print(result)

