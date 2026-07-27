from flask import Flask, render_template, request
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ----------------------------
# Upload Folder
# ----------------------------
UPLOAD_FOLDER = "static/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ----------------------------
# MySQL Connection
# ----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="internship_portal"
)

cursor = db.cursor()

# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# Submit Form
# ----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    fullname = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]
    college = request.form["college"]
    course = request.form["course"]
    year = request.form["year"]
    semester = request.form["semester"]
    skills = request.form["skills"]

    resume = request.files["resume"]

    filename = ""

    if resume.filename != "":
        filename = secure_filename(resume.filename)
        resume.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    sql = """
    INSERT INTO applications
    (Fullname, Email, PhoneNumber, CollegeName, Course, Year, Semester, Skills, Resume)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        fullname,
        email,
        phone,
        college,
        course,
        year,
        semester,
        skills,
        filename
    )

    cursor.execute(sql, values)
    db.commit()

    return render_template(
        "index.html",
        message="Application Submitted Successfully!"
    )

# ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)