from flask import Flask, render_template, request
app = Flask(__name__)

EXAMS = [
 {"name":"KPSC KAS","category":"State Civil Services","description":"Explore Karnataka Administrative Service preparation resources."},
 {"name":"KEA PDO","category":"Karnataka Recruitment","description":"Find useful preparation topics for PDO recruitment."},
 {"name":"Karnataka Police PSI","category":"Police Recruitment","description":"Review common Police Sub-Inspector preparation areas."},
 {"name":"Karnataka FDA / SDA","category":"State Government Jobs","description":"Prepare for assistant recruitment examinations."},
 {"name":"SSC CGL","category":"Central Government","description":"Practise aptitude, reasoning, English and general awareness."},
 {"name":"RRB Railway","category":"Railway Recruitment","description":"Explore railway recruitment preparation topics."}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/exams")
def exams():
    q = request.args.get("q", "").strip().lower()
    filtered = [e for e in EXAMS if q in e["name"].lower() or q in e["category"].lower() or q in e["description"].lower()]
    return render_template("exams.html", exams=filtered, query=q)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        message = f"Demo form received for {username}. Real authentication is not configured." if username else "Please enter your username."
    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
