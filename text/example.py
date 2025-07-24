from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("gsi-upm/llama-3b-emotion-classifier", num_labels=5)
tokenizer = AutoTokenizer.from_pretrained("gsi-upm/llama-3b-emotion-classifier")

# Input text
text = "I just got a promotion and I feel amazing!"

# Tokenize the input
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# Predict emotions
with torch.no_grad():
    logits = model(**inputs).logits
    probs = torch.sigmoid(logits)

# Display results
labels = ['anger', 'fear', 'joy', 'sadness', 'surprise']
results = {label: float(prob) for label, prob in zip(labels, probs[0])}
print(results)