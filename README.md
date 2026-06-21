# 🍽️ Food Waste Reduction Platform

## 📌 Overview

The Food Waste Reduction Platform is a web-based application designed to connect **Restaurants, NGOs, Delivery Partners, and Admins** to reduce food wastage and help distribute surplus food to people in need.

The platform allows restaurants to donate excess food, NGOs to claim available donations, delivery partners to transport the food, and administrators to monitor all activities on the platform.

---

## 🚀 Features

### 👨‍🍳 Restaurant

* Register and Login
* Add food donations
* View only their own donations
* Delete donations
* Track donation status

### 🏢 NGO

* Register and Login
* View available food donations
* Accept food donations
* Track accepted donations

### 🚚 Delivery Partner

* Register and Login
* View assigned deliveries
* Mark deliveries as completed
* Automatically become available for new deliveries after completion

### 👨‍💼 Admin

* Register and Login
* View all restaurants
* View all NGOs
* View all delivery partners
* Monitor all donations
* Monitor all deliveries and statuses

---

## 🔄 Workflow

1. Restaurant registers and logs in.
2. Restaurant adds a food donation.
3. Donation status becomes **Available**.
4. NGOs can view and accept available donations.
5. The system automatically assigns the first available delivery partner.
6. Delivery partner picks up and delivers the food.
7. Delivery is marked as **Delivered**.
8. Donation status changes to **Completed**.
9. Admin can monitor all activities and users.

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Database

* SQLite

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
FoodWastePlatform/
│
├── app.py
├── foodwaste.db
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── donate.html
│   ├── ngo_dashboard.html
│   ├── delivery_dashboard.html
│   └── admin_dashboard.html
│
├── static/
│   └── css/
│       └── style.css
│
└── README.md
```

---

## 🗄️ Database Models

### User

* id
* name
* email
* password
* role
* available

### Donation

* id
* food_name
* quantity
* food_type
* location
* contact
* status
* restaurant_id
* ngo_id

### Delivery

* id
* donation_id
* delivery_partner_id
* status

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/sachi-rana1/Food_Waste_Reduction_Platform.git
cd Food_Waste_Reduction_Platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install flask
pip install flask-sqlalchemy
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 🌟 Future Enhancements

* Google Maps API Integration
* Delivery Scheduling
* Email Notifications
* SMS Notifications
* AI-based Nearest NGO Recommendation
* Food Expiry Prediction
* Analytics Dashboard
* Charts and Reports
* Secure Password Hashing
* Real-time Delivery Tracking

---

## 🎯 Project Goal

The primary goal of this project is to reduce food wastage by creating an efficient ecosystem where surplus food can be quickly distributed to NGOs and people in need through coordinated delivery services.

---

## 👩‍💻 Developed By

**Sachi Rana**

B.Tech CSE Student | Aspiring Software Engineer | AI & Full Stack Enthusiast
