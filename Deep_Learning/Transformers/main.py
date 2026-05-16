# pip install transformers torch
from transformers import pipeline
# Step 1: Create Transformer model
classifier = pipeline("sentiment-analysis")
# Step 2: Store multiple sentences
sentences = [
    "I love this phone",
    "This movie is terrible",
    "The food was average",
    "Python is very interesting",
    "I hate waiting in traffic"
]
# sentiment-analysis
# tokenization
# positional encoding
# word embedding
# encoder
# decoder
# output

# Step 3: Loop through sentences
for text in sentences:

    # Step 4: Predict sentiment
    result = classifier(text)

    # Step 5: Print result
    print("Sentence:", text)
    print("Prediction:", result)
    print("-------------------")