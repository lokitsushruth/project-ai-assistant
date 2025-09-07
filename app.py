import os
from dotenv import load_dotenv
from qa_chain import build_qa
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Dummy user model for demo
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Demo users
users = {"admin": User(1, "admin", "password123")}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    departments = [
        {"name": "FTB", "route": "ftb", "icon": "ftb.jpeg"},
        {"name": "Dept of Motor Vehicles", "route": "oops", "icon": "dmv.jpeg"},
        {"name": "City of San Jose", "route": "oops", "icon": "sanjose.jpeg"},
        {"name": "Employment Development Dept", "route": "oops", "icon": "edd.jpeg"},
        {"name": "Fi$cal", "route": "oops", "icon": "fiscal.jpeg"},
        {"name": "Rancho Cordova", "route": "oops", "icon": "ranchocordova.jpeg"},
        {"name": "CalPERS", "route": "oops", "icon": "calpers.jpeg"},
        {"name": "CDFA", "route": "oops", "icon": "cdfa.jpeg"},
        {"name": "Office of Energy Infrastructure", "route": "oops", "icon": "energy.jpeg"},
    ]
    return render_template("dashboard.html", departments=departments)



@app.route("/ftb")
@login_required
def ftb():
    return render_template("ftb.html")

@app.route("/oops")
@login_required
def oops():
    return render_template("oops.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/insights")
@login_required
def insights():
    return render_template("insights.html")



# For the FTB Enterprise Q&A
# Global QA chain
qa = None

# 1️⃣ Page route
@app.route("/qa_chat", methods=["GET"])
@login_required
def qa_page():
    # Just render the chatbot page
    return render_template("qa_chat.html")


# 2️⃣ API endpoint for queries
@app.route("/qa_api", methods=["POST"])
@login_required
def qa_endpoint():
    global qa
    try:
        if qa is None:
            # Build QA only on first request
            csv_files = [a for a in os.listdir(".") if a.endswith(".csv")]
            if not csv_files:
                return jsonify({"answer": "No CSV files found for data processing. Please upload data files."})
            
            qa = build_qa(csv_files)

        query = request.json.get("query")
        
        if not query or not query.strip():
            return jsonify({"answer": "Please provide a valid question."})
        
        # Call the query function
        result = qa(query)
        
        # Ensure we return a string
        if hasattr(result, 'content'):
            result = result.content
        elif not isinstance(result, str):
            result = str(result)
            
        return jsonify({"answer": result})
        
    except Exception as e:
        print(f"Error in QA endpoint: {e}")
        return jsonify({"answer": "I apologize, but I encountered a system error. Please try again later."})


@app.route("/debug")
def debug():
    return f"""
    <h1>Debug Info</h1>
    <p>Current working directory: {os.getcwd()}</p>
    <p>CSV files in directory: {[f for f in os.listdir('.') if f.endswith('.csv')]}</p>
    <p>FAISS index exists: {os.path.exists('faiss_index')}</p>
    <p>GROQ_API_KEY set: {'GROQ_API_KEY' in os.environ}</p>
    """



if __name__ == "__main__":
    app.run(debug=True)
