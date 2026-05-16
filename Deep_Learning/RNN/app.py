from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np

app = Flask(__name__)

# Load trained model
model = load_model("translator_model.h5")

# Training words
english_sentences = [
    "hello",
    "how are you",
    "good morning",
    "thank you",
    "good night"
]

# Telugu mapping
telugu_mapping = {
    1: "నమస్కారం",
    2: "మీరు ఎలా ఉన్నారు",
    3: "శుభోదయం",
    4: "ధన్యవాదాలు",
    5: "శుభ రాత్రి"
}

# Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(english_sentences)

max_length = 3

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        text = request.form["english"]

        seq = tokenizer.texts_to_sequences([text])

        seq = pad_sequences(seq, maxlen=max_length)

        prediction = model.predict(seq)

        predicted_class = np.argmax(prediction)

        result = telugu_mapping[predicted_class]

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)