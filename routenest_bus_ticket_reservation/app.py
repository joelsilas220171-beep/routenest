from datetime import datetime, timezone
from uuid import uuid4
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-demo-secret-key"

# Illustrative data for exploring the website. Bookings are kept in memory.
BUS_SEED = [
    {"id": 101, "operator": "Southern Express", "from": "Chennai", "to": "Madurai", "departure": "06:30", "arrival": "13:15", "duration": "6h 45m", "price": 620, "seats": 32, "type": "AC Sleeper", "rating": 4.6},
    {"id": 102, "operator": "GreenLine Travels", "from": "Chennai", "to": "Madurai", "departure": "21:00", "arrival": "04:10", "duration": "7h 10m", "price": 780, "seats": 18, "type": "AC Sleeper", "rating": 4.8},
    {"id": 103, "operator": "City Connect", "from": "Chennai", "to": "Coimbatore", "departure": "07:15", "arrival": "14:45", "duration": "7h 30m", "price": 690, "seats": 24, "type": "AC Seater", "rating": 4.4},
    {"id": 104, "operator": "Kongu Roadways", "from": "Madurai", "to": "Coimbatore", "departure": "08:00", "arrival": "13:50", "duration": "5h 50m", "price": 540, "seats": 20, "type": "Non-AC Seater", "rating": 4.2},
    {"id": 105, "operator": "Night Owl Bus", "from": "Bengaluru", "to": "Chennai", "departure": "22:15", "arrival": "05:45", "duration": "7h 30m", "price": 850, "seats": 16, "type": "AC Sleeper", "rating": 4.7},
    {"id": 106, "operator": "Coastal Cruiser", "from": "Chennai", "to": "Puducherry", "departure": "09:00", "arrival": "12:30", "duration": "3h 30m", "price": 280, "seats": 28, "type": "AC Seater", "rating": 4.3},
    {"id": 107, "operator": "Temple Trail", "from": "Madurai", "to": "Chennai", "departure": "20:30", "arrival": "05:30", "duration": "9h", "price": 720, "seats": 22, "type": "AC Sleeper", "rating": 4.5},
    {"id": 108, "operator": "Western Star", "from": "Coimbatore", "to": "Bengaluru", "departure": "23:00", "arrival": "06:00", "duration": "7h", "price": 760, "seats": 19, "type": "AC Sleeper", "rating": 4.6},
]
BUS_SEAT_DEFAULTS = {bus["id"]: bus["seats"] for bus in BUS_SEED}
BUSES = [dict(bus) for bus in BUS_SEED]
RESERVATIONS = []


def available_buses(source="", destination="", travel_date="", bus_type=""):
    results = []
    for bus in BUSES:
        if source and bus["from"].lower() != source.lower():
            continue
        if destination and bus["to"].lower() != destination.lower():
            continue
        if bus_type and bus_type != "Any type" and bus_type != bus["type"]:
            continue
        results.append({**bus, "travel_date": travel_date})
    return results


@app.context_processor
def inject_globals():
    return {"current_year": datetime.now().year}


@app.route("/")
def home():
    cities = sorted({bus["from"] for bus in BUSES} | {bus["to"] for bus in BUSES})
    return render_template("index.html", cities=cities)


@app.route("/buses")
def buses_page():
    source = request.args.get("from", "").strip()
    destination = request.args.get("to", "").strip()
    travel_date = request.args.get("date", "").strip()
    bus_type = request.args.get("type", "Any type").strip()
    results = available_buses(source, destination, travel_date, bus_type)
    cities = sorted({bus["from"] for bus in BUSES} | {bus["to"] for bus in BUSES})
    return render_template("buses.html", buses=results, cities=cities, source=source,
                           destination=destination, travel_date=travel_date, bus_type=bus_type)


@app.route("/book/<int:bus_id>", methods=["GET", "POST"])
def book_bus(bus_id):
    bus = next((item for item in BUSES if item["id"] == bus_id), None)
    if not bus:
        flash("That bus could not be found. Please search again.", "error")
        return redirect(url_for("buses_page"))
    if request.method == "POST":
        passenger = request.form.get("passenger", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        travel_date = request.form.get("travel_date", "").strip()
        try:
            seats = int(request.form.get("seats", "1"))
        except (ValueError, TypeError):
            seats = 0
        try:
            parsed_date = datetime.strptime(travel_date, "%Y-%m-%d").date()
            valid_date = parsed_date >= datetime.now().date()
        except ValueError:
            valid_date = False
        if not passenger or not email or not phone or not travel_date:
            flash("Please complete every passenger and travel field.", "error")
        elif "@" not in email or "." not in email.split("@")[-1]:
            flash("Please enter a valid email address.", "error")
        elif not phone.isdigit() or len(phone) < 10:
            flash("Enter a phone number with at least 10 digits.", "error")
        elif not valid_date:
            flash("Choose today or a future travel date.", "error")
        elif seats < 1:
            flash("Choose at least one seat.", "error")
        elif seats > bus["seats"]:
            flash(f"Only {bus['seats']} seats are currently available.", "error")
        else:
            booking = {
                "reference": uuid4().hex[:8].upper(), "bus_id": bus["id"],
                "operator": bus["operator"], "source": bus["from"], "destination": bus["to"],
                "departure": bus["departure"], "arrival": bus["arrival"], "travel_date": travel_date,
                "passenger": passenger, "email": email, "phone": phone, "seats": seats,
                "total": seats * bus["price"],
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            }
            bus["seats"] -= seats
            RESERVATIONS.append(booking)
            session["last_booking"] = booking["reference"]
            flash(f"Booking confirmed! Your reference is {booking['reference']}.", "success")
            return redirect(url_for("booking_confirmation", reference=booking["reference"]))
    return render_template("book.html", bus=bus, travel_date=request.args.get("date", ""))


@app.route("/confirmation/<reference>")
def booking_confirmation(reference):
    booking = next((item for item in RESERVATIONS if item["reference"] == reference), None)
    if not booking:
        flash("Booking reference not found.", "error")
        return redirect(url_for("my_bookings"))
    return render_template("confirmation.html", booking=booking)


@app.route("/my-bookings", methods=["GET", "POST"])
def my_bookings():
    found = None
    reference = ""
    if request.method == "POST":
        reference = request.form.get("reference", "").strip().upper()
        found = next((item for item in RESERVATIONS if item["reference"] == reference), None)
        if not found:
            flash("No booking matched that reference. Check it and try again.", "error")
    return render_template("my_bookings.html", booking=found, reference=reference)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message or "@" not in email:
            flash("Please enter your name, a valid email, and a message.", "error")
        else:
            flash("Thanks for contacting us. This demo does not permanently store messages.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/api/buses")
def buses_api():
    return jsonify(available_buses(request.args.get("from", "").strip(),
                                   request.args.get("to", "").strip(),
                                   bus_type=request.args.get("type", "").strip()))


@app.route("/api/stats")
def stats_api():
    return jsonify({"bus_count": len(BUSES), "booking_count": len(RESERVATIONS)})


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
