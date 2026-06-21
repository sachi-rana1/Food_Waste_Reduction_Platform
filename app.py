from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "foodwaste"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodwaste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# DATABASE MODELS
# ======================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Restaurant, NGO, Delivery Partner, Admin
    role = db.Column(db.String(50), nullable=False)

    # Delivery partner ke liye
    available = db.Column(db.Boolean, default=True)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    food_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    food_type = db.Column(db.String(50))
    location = db.Column(db.String(200))
    contact = db.Column(db.String(20))

    # Available, Accepted, Completed
    status = db.Column(db.String(50), default="Available")

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey('donation.id')
    )

    delivery_partner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    # Assigned, Delivered
    status = db.Column(
        db.String(50),
        default="Assigned"
    )


# ======================
# HOME
# ======================

@app.route("/")
def home():
    return render_template("index.html")


# ======================
# REGISTER
# ======================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "Email already exists."

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


# ======================
# LOGIN
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ======================
# DASHBOARD
# ======================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    role = session["role"]

    # -------------------
    # RESTAURANT
    # -------------------
    if role == "Restaurant":

        donations = Donation.query.filter_by(
            restaurant_id=session["user_id"]
        ).all()

        return render_template(
            "dashboard.html",
            donations=donations,
            user_name=session["user_name"]
        )

    # -------------------
    # NGO
    # -------------------
    elif role == "NGO":

        donations = Donation.query.filter_by(
            status="Available"
        ).all()

        return render_template(
            "ngo_dashboard.html",
            donations=donations,
            user_name=session["user_name"]
        )

    # -------------------
    # DELIVERY PARTNER
    # -------------------
    elif role == "Delivery Partner":

        deliveries = Delivery.query.filter_by(
            delivery_partner_id=session["user_id"]
        ).all()

        return render_template(
            "delivery_dashboard.html",
            deliveries=deliveries,
            user_name=session["user_name"]
        )

    # -------------------
    # ADMIN
    # -------------------
    elif role == "Admin":

        restaurants = User.query.filter_by(
            role="Restaurant"
        ).all()

        ngos = User.query.filter_by(
            role="NGO"
        ).all()

        partners = User.query.filter_by(
            role="Delivery Partner"
        ).all()

        donations = Donation.query.all()

        deliveries = Delivery.query.all()

        return render_template(
            "admin_dashboard.html",
            restaurants=restaurants,
            ngos=ngos,
            partners=partners,
            donations=donations,
            deliveries=deliveries,
            user_name=session["user_name"]
        )

    return redirect("/")


# ======================
# DONATE FOOD
# ======================

@app.route("/donate", methods=["GET", "POST"])
def donate():

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Restaurant":
        return redirect("/dashboard")

    if request.method == "POST":

        donation = Donation(
            food_name=request.form["food_name"],
            quantity=request.form["quantity"],
            food_type=request.form["food_type"],
            location=request.form["location"],
            contact=request.form["contact"],
            restaurant_id=session["user_id"]
        )

        db.session.add(donation)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("donate.html")


# ======================
# DELETE DONATION
# ======================

@app.route("/delete/<int:id>")
def delete(id):

    donation = Donation.query.get_or_404(id)

    if donation.restaurant_id != session["user_id"]:
        return redirect("/dashboard")

    db.session.delete(donation)
    db.session.commit()

    return redirect("/dashboard")


# ======================
# NGO ACCEPT DONATION
# ======================

@app.route("/accept/<int:id>")
def accept(id):

    if session["role"] != "NGO":
        return redirect("/dashboard")

    donation = Donation.query.get_or_404(id)

    donation.status = "Accepted"
    donation.ngo_id = session["user_id"]

    # First available delivery partner
    partner = User.query.filter_by(
        role="Delivery Partner",
        available=True
    ).first()

    if partner:

        delivery = Delivery(
            donation_id=donation.id,
            delivery_partner_id=partner.id
        )

        db.session.add(delivery)

        partner.available = False

    db.session.commit()

    return redirect("/dashboard")


# ======================
# DELIVERY COMPLETED
# ======================

@app.route("/delivered/<int:id>")
def delivered(id):

    if session["role"] != "Delivery Partner":
        return redirect("/dashboard")

    delivery = Delivery.query.get_or_404(id)

    delivery.status = "Delivered"

    donation = Donation.query.get(
        delivery.donation_id
    )

    donation.status = "Completed"

    partner = User.query.get(
        delivery.delivery_partner_id
    )

    partner.available = True

    db.session.commit()

    return redirect("/dashboard")


# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("role", None)

    return redirect("/")


# ======================
# RUN APP
# ======================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)