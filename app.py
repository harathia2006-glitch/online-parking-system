from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

# -----------------------------
# Create Database and Table
# -----------------------------
def create_table():
    conn = sqlite3.connect("parking.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        vehicle TEXT,
        vehicle_type TEXT,
        mall TEXT,
        date TEXT,
        entry_time TEXT,
        exit_time TEXT,
        slot TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Booking Page
# -----------------------------
@app.route("/booking")
def booking():
    return render_template("booking.html")


# -----------------------------
# Book Parking Slot
# -----------------------------
@app.route("/book", methods=["POST"])
def book():

    name = request.form["name"]
    mobile = request.form["mobile"]
    vehicle = request.form["vehicle"]
    vehicle_type = request.form["vehicle_type"]
    mall = request.form["mall"]
    date = request.form["date"]
    entry_time = request.form["entry_time"]
    exit_time = request.form["exit_time"]

    # Generate Random Parking Slot
    slot = "A-" + str(random.randint(1, 100))

    conn = sqlite3.connect("parking.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings
        (name, mobile, vehicle, vehicle_type, mall,
         date, entry_time, exit_time, slot)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        mobile,
        vehicle,
        vehicle_type,
        mall,
        date,
        entry_time,
        exit_time,
        slot
    ))

    conn.commit()
    conn.close()

    return render_template(
        "success.html",
        name=name,
        vehicle=vehicle,
        mall=mall,
        slot=slot,
        date=date,
        entry_time=entry_time,
        exit_time=exit_time
    )


# -----------------------------
# View Booking Slots
# -----------------------------
@app.route("/view_slots")
def view_slots():

    conn = sqlite3.connect("parking.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()

    conn.close()

    return render_template(
        "view_slots.html",
        bookings=bookings
    )


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("parking.db")
    cur = conn.cursor()

    total_slots = 100

    # Count bookings
    cur.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cur.fetchone()[0]

    occupied = total_bookings
    available = total_slots - occupied

    # Data for Dashboard Table
    cur.execute("""
        SELECT name, vehicle, mall, slot
        FROM bookings
    """)
    bookings = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_slots=total_slots,
        available=available,
        occupied=occupied,
        total_bookings=total_bookings,
        bookings=bookings
    )


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)