from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "foodwaste"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodwaste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    food_type = db.Column(db.String(50))
    location = db.Column(db.String(200))
    contact = db.Column(db.String(20))
    status = db.Column(db.String(50), default="Pending")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            role=request.form["role"]
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.name
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donation = Donation(
            food_name=request.form["food_name"],
            quantity=request.form["quantity"],
            food_type=request.form["food_type"],
            location=request.form["location"],
            contact=request.form["contact"]
        )

        db.session.add(donation)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("donate.html")


@app.route("/dashboard")
def dashboard():
    donations = Donation.query.all()
    return render_template(
        "dashboard.html",
        donations=donations
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    donation = Donation.query.get_or_404(id)

    db.session.delete(donation)
    db.session.commit()

    return redirect("/dashboard")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)