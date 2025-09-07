from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

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


if __name__ == "__main__":
    app.run(debug=True)
