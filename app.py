from flask import Flask, render_template, request
import spacy
import sqlite3
import re

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Simple text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

def get_db():
    return sqlite3.connect("nlp.db", check_same_thread=False)


@app.route("/", methods=["GET", "POST"])
def home():
    tokens = lemmas = entities = []

    if request.method == "POST":
        text = request.form["text"]

        # User text be cleaned
        cleaned = clean_text(text)

        doc = nlp(cleaned)

        tokens = [t.text for t in doc]
        lemmas = [
    t.lemma_
    for t in doc
    if not t.is_stop and not t.is_punct and not t.is_space
]

        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))

        # Store in DB
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO processed_text(original_text, cleaned_text) VALUES (?,?)",
            (text, cleaned)
        )

        text_id = cur.lastrowid

        for e in entities:
            cur.execute(
                "INSERT INTO entities(text_id, entity, entity_type) VALUES (?,?,?)",
                (text_id, e[0], e[1])
            )

        conn.commit()
        conn.close()

    return render_template(
        "index.html",
        tokens=tokens,
        lemmas=lemmas,
        entities=entities
    )

if __name__ == "__main__":
    app.run(debug=True)