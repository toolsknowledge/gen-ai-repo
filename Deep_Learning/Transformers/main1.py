from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch

# Step 1: Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Step 2: Load Transformer model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# Step 3: Input sentence
text = "I love Deep Learning"

# Step 4: Convert text into tokens
inputs = tokenizer(text, return_tensors="pt")

# Step 5: Send tokens into model
outputs = model(**inputs)

# Step 6: Get prediction scores
scores = outputs.logits

# Step 7: Convert scores to probabilities
probabilities = torch.softmax(scores, dim=1)

# Step 8: Get highest probability index
prediction = torch.argmax(probabilities)

# Step 9: Print result
if prediction == 1:
    print("Positive Sentiment")
else:
    print("Negative Sentiment")