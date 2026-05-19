# ============================================
# English → Telugu Translator using RNN
# Beginner Friendly Full Code
# ============================================

# Step 1: Import Libraries
# numpy - numerical python
# used to handle the arrays operations
import numpy as np

# Sequential - used to build layers
from tensorflow.keras.models import Sequential

# Embedding - used to convert words to numbers
# SimpleRNN - used to build RNN network
# Dense, used to produce the result
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

# used to convert statements to words (tokens)
from tensorflow.keras.preprocessing.text import Tokenizer

# pad_sequences - add dummy in place of no words
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ============================================
# Step 2: Create Dataset
# ============================================

english_sentences = [
    "hello",            
    "how are you",      
    "good morning",     
    "thank you",        
    "good night"        
]

telugu_sentences = [
    "నమస్కారం",
    "మీరు ఎలా ఉన్నారు",
    "శుభోదయం",
    "ధన్యవాదాలు",
    "శుభ రాత్రి"
]

# ============================================
# Step 3: Tokenization
# ============================================

tokenizer = Tokenizer()

# Learn words from English sentences
tokenizer.fit_on_texts(english_sentences)

# Convert words to numbers
input_sequences = tokenizer.texts_to_sequences(english_sentences)

print("Tokenized Sequences:")
print(input_sequences)

# ============================================
# Step 4: Padding   
# ============================================

# Find longest sentence automatically
max_length = max(len(seq) for seq in input_sequences)

print("Max Length:", max_length)

# Make all sequences same size
input_sequences = pad_sequences(
    input_sequences,
    maxlen=max_length
)

print("After Padding:")
print(input_sequences)

# ============================================
# Step 5: Create Labels
# ============================================

# Assign number to each Telugu sentence
output_labels = np.array([1, 2, 3, 4, 5])

# Telugu dictionary mapping
telugu_mapping = {
    1: "నమస్కారం",
    2: "మీరు ఎలా ఉన్నారు",
    3: "శుభోదయం",
    4: "ధన్యవాదాలు",
    5: "శుభ రాత్రి"
}

# ============================================
# Step 6: Build RNN Model
# ============================================

model = Sequential()

# Embedding Layer
model.add(
    Embedding(
        input_dim=50,
        output_dim=8,                
        input_length=max_length
    )
)

# RNN Layer
model.add(SimpleRNN(16))

# Output Layer
model.add(Dense(6, activation='softmax'))

# ============================================
# Step 7: Compile Model
# ============================================

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ============================================
# Step 8: Train Model
# ============================================

model.fit(
    input_sequences,
    output_labels,
    epochs=500,
    verbose=1
)

#================================
# save the model
#================================
model.save("translator_model.h5")


# ============================================
# Step 9: Test Translator
# ============================================

test_sentence = ["hello"]

# Convert to sequence
test_seq = tokenizer.texts_to_sequences(test_sentence)

# Padding
test_seq = pad_sequences(test_seq, maxlen=max_length)

# Predict
prediction = model.predict(test_seq)

# Get highest probability index
predicted_class = np.argmax(prediction)

# ============================================
# Step 10: Print Telugu Output
# ============================================

print("\nEnglish Input:", test_sentence[0])

print("Predicted Telugu Output:")

print(telugu_mapping[predicted_class])

# ============================================
# Optional Probability Output
# ============================================

print("\nPrediction Probabilities:")
print(prediction)