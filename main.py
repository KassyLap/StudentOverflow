from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session, render_template, flash
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from flask import Flask, send_from_directory


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route("/home")
def homepage():
    username = session.get("username")
    questions_result = supabase.table("questions").select("id,question,subject,period,user_id").execute()
    questions = questions_result.data if questions_result.data else []
    users_result = supabase.table("users").select("id,username").execute()
    users = {u["id"]: u["username"] for u in users_result.data} if users_result.data else {}

    comments_result = supabase.table("comments").select("question_id,comment,user_id").execute()
    comments = comments_result.data if comments_result.data else []

    comments_by_question = {}
    for c in comments:
        comments_by_question.setdefault(c["question_id"], []).append({
            "author": users.get(c["user_id"], "Unknown"),
            "comment": c["comment"]
        })

    for q in questions:
        q["author"] = users.get(q["user_id"], "Unknown")
        q["comments"] = comments_by_question.get(q["id"], [])

    return render_template('HomePage.html', username=username, questions=questions) 

@app.route("/login")
def sign_up_page():
    return render_template('Login.html')


@app.route("/index")
def index():
    return render_template('Index.html')

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    role_admin = request.form.get("role_admin")
    role_student = request.form.get("role_student")

    if role_admin:
        rol = 1
    elif role_student:
        rol = 2
    else:
        rol = None

    response = supabase.table("users").insert({
        "username": username,
        "email": email,
        "password": password,
        "rol": rol
    }).execute()

    return redirect("/home")

@app.route("/signin", methods=["POST"])
def signin():
    username = request.form.get("username")
    password = request.form.get("password")
    result = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    if result.data and len(result.data) > 0:
        session["username"] = username
        return redirect("/home")
    else:
        return render_template('Login.html')

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    subject = request.form.get("subject")
    period = request.form.get("period")
    username = session.get("username")

    user_result = supabase.table("users").select("id").eq("username", username).execute()
    if not user_result.data or len(user_result.data) == 0:
        return redirect("/home")

    user_id = user_result.data[0]["id"]

    supabase.table("questions").insert({
        "user_id": user_id,
        "question": question,
        "subject": subject,
        "period": period
    }).execute()

    return redirect("/home")

@app.route("/comment", methods=["POST"])
def comment():
    question_id = request.form.get("question_id")
    comment_text = request.form.get("comment")
    username = session.get("username")

    user_result = supabase.table("users").select("id").eq("username", username).execute()
    if not user_result.data or len(user_result.data) == 0:
        return jsonify({"error": "User not found"}), 400

    user_id = user_result.data[0]["id"]

    response = supabase.table("comments").insert({
        "user_id": user_id,
        "question_id": question_id,
        "comment": comment_text
    }).execute()

    return jsonify({"status": "ok", "data": response.data})

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
