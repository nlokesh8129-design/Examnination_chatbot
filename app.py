from flask import Flask, render_template, request, jsonify
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


# Load FAQ dataset
with open("faq.json", "r", encoding="utf-8") as file:
    faq_data = json.load(file)


questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]


# Convert FAQ questions into TF-IDF vectors
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

faq_vectors = vectorizer.fit_transform(questions)


def clean_text(text):
    """Basic text cleaning."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()


def get_response(user_question):
    """Find the most relevant FAQ answer."""

    user_question = clean_text(user_question)

    if not user_question:
        return "Please enter a question.", 0.0

    # Convert user question into TF-IDF vector
    user_vector = vectorizer.transform([user_question])

    # Calculate similarity
    similarities = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]

    # Find highest similarity
    best_index = similarities.argmax()
    best_score = similarities[best_index]

    # Minimum confidence threshold
    threshold = 0.20

    if best_score >= threshold:
        return answers[best_index], float(best_score)

    return (
        "Sorry, I could not find a suitable answer. "
        "Please contact the examination office for assistance."
    ), float(best_score)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_question = data.get("message", "")

    response, score = get_response(user_question)

    return jsonify({
        "response": response,
        "confidence": round(score * 100, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)