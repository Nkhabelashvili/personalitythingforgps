from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Questions with weights for each personality type
questions = [
    {"question": "I enjoy solving complex problems and creating precise systems to achieve my goals.", "weights": {"INTJ": 3, "ENTJ": 1, "ISTJ": 1}},
    {"question": "I thrive in leadership roles where I can strategically manage people and resources.", "weights": {"ENTJ": 3, "INTJ": 1, "ESTJ": 1}},
    {"question": "I am fascinated by societal structures and enjoy analyzing their hidden mechanisms.", "weights": {"INTP": 3, "INTJ": 1, "ENTP": 1}},
    {"question": "I feel passionate about introducing innovative ideas to challenge traditional norms.", "weights": {"ENTP": 3, "INTP": 1, "ENFP": 1}},
    {"question": "I often reflect on ethical questions and strive to live according to my principles.", "weights": {"INFJ": 3, "INFP": 1, "ENFJ": 1}},
    {"question": "I take great joy in guiding and protecting others, often putting their needs before my own.", "weights": {"ENFJ": 3, "INFJ": 1, "ISFJ": 1}},
    {"question": "I am driven by deep emotions and will pursue love or personal ideals at any cost.", "weights": {"INFP": 3, "INFJ": 1, "ENFP": 1}},
    {"question": "I feel energized by the idea of reforming and improving the world around me.", "weights": {"ENFP": 3, "ENTP": 1, "INFP": 1}},
    {"question": "I prefer structure and believe a stable system is essential for progress.", "weights": {"ESTJ": 3, "ISTJ": 1, "ENTJ": 1}},
    {"question": "I approach challenges methodically, paying close attention to details.", "weights": {"ISTJ": 3, "ISFJ": 1, "INTJ": 1}},
    {"question": "I am loyal and self-sacrificing, especially when it comes to my family and loved ones.", "weights": {"ISFJ": 3, "INFJ": 1, "ISTJ": 1}},
    {"question": "I value harmony and strive to create an ideal environment where everyone thrives.", "weights": {"ESFJ": 3, "ENFJ": 1, "ISFJ": 1}},
    {"question": "I enjoy using creativity and innovation to reflect on and critique societal issues.", "weights": {"ISTP": 3, "ISFP": 1, "INTP": 1}},
    {"question": "I thrive in adventurous pursuits and feel alive when I am chasing bold challenges.", "weights": {"ESTP": 3, "ISTP": 1, "ENTP": 1}},
    {"question": "I value freedom and appreciate exploring new places and ideas to express myself.", "weights": {"ISFP": 3, "INFP": 1, "ENFP": 1}},
    {"question": "I feel energized in social settings and enjoy being the center of attention.", "weights": {"ESFP": 3, "ENFP": 1, "ESFJ": 1}},
    {"question": "I feel most fulfilled when I have the freedom to explore new ideas and experiences.", "weights": {"ENFP": 2, "ENTP": 2, "ISFP": 1}},
    {"question": "I prefer taking a logical and systematic approach to solving problems.", "weights": {"INTJ": 2, "ISTJ": 2, "ENTJ": 1}},
    {"question": "I value close personal relationships and strive to maintain harmony in my interactions.", "weights": {"INFJ": 2, "ISFJ": 2, "ESFJ": 1}},
    {"question": "I enjoy taking risks and exploring bold new opportunities.", "weights": {"ESTP": 2, "ENFP": 2, "ISFP": 1}}
]

# Personality descriptions
personalities = {
    "INTJ": "Turing - Logical and strategic, focused on system design and precision.",
    "ENTJ": "Wang Xifeng - A strong and strategic leader.",
    "INTP": "Foucault - Analytical and inquisitive, critiquing societal norms.",
    "ENTP": "Kang Youwei - A reformer challenging traditional norms.",
    "INFJ": "Seneca - Reflective, focused on ethics and spiritual growth.",
    "ENFJ": "Tevye - Compassionate, guiding others through challenges.",
    "INFP": "Juliet - Romantic, pursuing love and personal ideals.",
    "ENFP": "Gyalo - A passionate reformer.",
    "ESTJ": "Hobbes - A strong advocate for structure and stability.",
    "ISTJ": "Mr. Yee - Methodical and precise.",
    "ISFJ": "Chava - Loyal and family-oriented.",
    "ESFJ": "Plato - Creating harmony in society.",
    "ISTP": "Lu Hsun - Creative, using art to critique society.",
    "ESTP": "Gilgamesh - Adventurous and bold.",
    "ISFP": "The Foreigner - Values freedom and exploration.",
    "ESFP": "Mercutio - Charismatic and social."
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Initialize scores for all personality types
        scores = {ptype: 0 for ptype in personalities.keys()}

        try:
            # Process answers and calculate scores
            for i, question in enumerate(questions):
                answer = int(request.form.get(f"q{i}", 0))  # Get user's answer
                for ptype, weight in question["weights"].items():
                    scores[ptype] += answer * weight  # Update score for each type

            # Debug: Print scores before finding the max
            print("Scores before max():", scores)

            # Ensure scores are valid
            if not scores or all(value == 0 for value in scores.values()):
                return redirect(url_for("index"))  # Redirect back if no valid scores

            # Determine the highest-scoring personality type
            result = max(scores, key=scores.get)
            return redirect(url_for("result", personality=result))

        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for("index"))

    # Enumerate questions for rendering in the template
    enumerated_questions = list(enumerate(questions))
    return render_template("index.html", questions=enumerated_questions)



@app.route("/result/<personality>")
def result(personality):
    description = personalities[personality]
    return render_template("result.html", personality=personality, description=description)


if __name__ == "__main__":
    app.run(debug=True)
