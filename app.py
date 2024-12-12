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
    "INTJ": {
        "name": "A.M. Turing",
        "description": "Turing was methodical, focused on his goal, and saw the world through a highly analytical lens by asking questions such as 'Can machines think? I believe to be too meaningless to deserve discussion' (Turing 126); 'Is this feeling illusory?' (Turing 129); 'Instead of trying to produce a programme to simulate the adult mind, why not rather try to produce one which stimulates the child’s?' (Turing 140). His work in computing and theoretical science reflects the INTJ's long-term planning and focus on systems.",
    #    "image": "assets/turing.png"
    },
    "ENTJ": {
        "name": "Wang Xifeng",
        "description": "In The Story of The Stone by Cao Xueqin, Wang Xifeng is known for her wit and intelligence, her vivacious manner, her great beauty, her multiple-faced personality, and her fierce sense of fidelity. By pleasing and flattering Grandmother Jia, Xifeng becomes influential and rules the entire household. Even in the first chapters, Grandmother Jia says 'You don’t know her, she’s a holy terror this one' (Cao Xueqin 188). Her traits become more multifaceted, showing her kind-heartedness toward the poor but also her cruelty. Wang Xifeng's assertion of authority reflects the ENTJs strong leadership and need for control.",
    #    "image": "assets/xifeng.png"
    },
    "INTP": {
        "name": "Michel Foucault",
        "description": "As a philosopher who questioned societal structures and norms, Foucault embodies intellectual curiosity and critical thinking. His theoretical work in analyzing power structures exemplifies the focus on abstract ideas. In The Great Confinement, he argues 'In this sense, confinement conceals both a metaphysics of government and a politics of religion... police conceived of itself as the civil equivalent of religion for the identification of a perfect city' (Foucault 389). His eagerness to explore the dynamics of power and resistance fits the INTP's critical, abstract thinking.",
    #    "image": "assets/foc.png"
    },
    "ENTP": {
        "name": "Kang Youwei",
        "description": "As a reformist and thinker, Kang Youwei constantly challenged traditions and proposed new ideas. In The Turk Travelogue, he critiques and compares Turkey’s culture, history, and society with China's modernization path: 'The degeneration of our country and the belittlement of both Turkey and our country by others arise from the fact that governance is lacking, there is no other reason' (Kang Youwei 251). His bold challenges to traditional systems embody the ENTP's drive for innovation.",
    #    "image": "assets/Kang.png"
    },
    "INFJ": {
        "name": "Seneca",
        "description": "Seneca, with his Stoic philosophy, focused on personal growth and societal well-being. In Seneca’s Letters to Lucilius, he conveys practical Stoic philosophy, emphasizing the pursuit of virtue, self-discipline, and inner peace as the path to a meaningful life. 'Exhort yourself, toughen yourself, against such events as befall even the most powerful' (Seneca 311). His reflections on the brevity of life and introspection align with the INFJ’s quest for purpose.",
    #    "image": "assets/Seneca.png"
    },
    "ENFJ": {
        "name": "Tevye",
        "description": "In Chava by Sholem Aleichem, Tevye’s character is central as a devout and loving father, grappling with the tension between his religious convictions and his unconditional love for his daughter when she marries outside their faith. His sense of responsibility for his loved ones and community exemplifies compassionate leadership. 'When children cause you grief, you must count it as love' (Aleichem 267). Tevye’s ability to guide his family through difficult times reflects the ENFJ’s empathetic nature.",
    #    "image": "assets/Tevye.png"
    },
    "INFP": {
        "name": "Juliet",
        "description": "In Romeo and Juliet by Shakespeare, Juliet’s pursuit of love regardless of societal norms and her idealism about true love fit the INFP's values. For example: 'O, by this count I shall be much in years Ere I again behold my Romeo' (Shakespeare 478), 'Wash thy his wounds with tears? Mine shall be spent when theirs are dry, for Romeo’s banishment' (Shakespeare 468). Her deep emotional conflicts and pursuit of love reflect the INFP's authenticity.",
    #    "image": "assets/Juliet.png"
    },
    "ENFP": {
        "name": "Gyalo",
        "description": "Gyalo is a vibrant, passionate character who thrives on new ideas and social interaction. In Eight Sheep by Pema Tseden, even though he seems anxious due to a language barrier, he shows a lively, upbeat approach to life: 'The man’s shadow was almost identical to his, so Gyalo relaxed a little and smiled' (Tseden 288). His zest for life and drive to explore new possibilities align with the ENFP’s love for novelty and creativity.",
    #    "image": "assets/Gyalo.png"
    },
    "ESTJ": {
        "name": "Thomas Hobbes",
        "description": "In Leviathan, Thomas Hobbes aims to justify the necessity of a strong, centralized authority to prevent the chaos and violence of the natural state of humanity, advocating for a social contract where individuals surrender certain freedoms in exchange for security and order. 'A Common-Wealth is said to be Instituted, when a Multitude of men do Agree, and Covenant... or Assembly of Men, shall be given by the major part, the Right to Present Person the Person of them all' (Hobbes 235). His focus on social order and societal structure aligns with the ESTJ's dedication to rules and stability.",
    #    "image": "assets/Hobbes.png"
    },
    "ISTJ": {
        "name": "Mr. Yee",
        "description": "In Lust and Caution by Eileen Chang, Mr. Yee’s intentions revolve around his political survival and loyalty to the oppressive regime he serves. His complex and guarded relationship with Wang Chia-chih reveals vulnerability and deep mistrust of others. 'As soon as he’d reached safety, he’d immediately telephoned to get the whole area sealed off... that evening they’d all been shot' (Chang 448). Mr. Yee’s careful and methodical approach to his duties reflects the ISTJ’s practicality and sense of responsibility.",
        "image": "assets/Mr Yee.png"
    },
    "ISFJ": {
        "name": "Chava",
        "description": "In Chava by Sholem Aleichem, Chava's character represents a courageous and independent spirit, choosing love and personal conviction over tradition. This decision places her at odds with her family and community, as she states, 'God created all people equal' (Aleichem 270). Her commitment to her family and sense of duty reflect the ISFJ's loyalty and protective nature.",
        "image": "assets/Cheve.png"
    },
    "ESFJ": {
        "name": "Plato",
        "description": "In The Republic of Plato, Plato explores the nature of justice, the ideal structure of a just society, and the role of philosophy and education in achieving a harmonious and virtuous state. 'Such men would hold that the truth is nothing other than the shadows of artificial things' (Plato 98). His vision of an ideal society and his focus on justice and societal roles align with the ESFJ's desire to build order and harmony.",
        "image": "assets/Plato.png"
    },
    "ISTP": {
        "name": "Lu Hsun",
        "description": "In Preface to Call to Arms, Lu Hsun aims to awaken and inspire his readers to recognize and resist societal stagnation and oppression, using literature to provoke thought and drive reform. 'Anyone who studied \"foreign subjects\" was looked down as a fellow good for nothing, who, out of desperation, was forced to sell his soul to foreign devils' (Lu Hsun 356). His practicality and hands-on approach to addressing complex social issues reflect the ISTP's problem-solving nature.",
        "image": "assets/lu hsun.png"
    },
    "ESTP": {
        "name": "Gilgamesh",
        "description": "As a legendary hero who seeks out challenges and fame, Gilgamesh embodies a love for adventure, risk-taking, and excitement. In Book II, Enkidu says, 'Gilgamesh, you are unique among humans. Your mother, the goddess Ninsun, made you stronger and braver than any mortal' (Gilgamesh 45). Gilgamesh’s desire for immortality through fame and his adventurous quest reflect the ESTP's pursuit of action and high-stakes challenges.",
        "image": "assets/gilgamesh.png"
    },
    "ISFP": {
        "name": "The Foreigner",
        "description": "In Eight Sheep by Pema Tseden, the foreigner shows traits such as reflecting and emotionally driven approaches to life. 'I wanted to understand Tibetan culture, so I came alone to the Tibetan areas to experience it on-site first and then engage in deeper research' (Tseden 290). His reflective and curious nature mirrors the ISFP's focus on freedom and beauty.",
        "image": "assets/Foreigner.png"
    },
    "ESFP": {
        "name": "Mercutio",
        "description": "In Romeo and Juliet, Mercutio serves as a witty, free-spirited foil to Romeo, injecting humor and cynicism into the play while emphasizing the impulsive nature of the characters. 'A plague o' both your houses! I am sped.' (Shakespeare 459). His fiery and spontaneous personality reflects the ESFP's playful and expressive nature.",
        "image": "assets/mercutio.png"
    }
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
