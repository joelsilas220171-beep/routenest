from datetime import date, timedelta
import app as app_module
import pytest

@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    app_module.RESERVATIONS.clear()
    for bus in app_module.BUSES:
        bus["seats"] = app_module.BUS_SEAT_DEFAULTS[bus["id"]]
    with app_module.app.test_client() as test_client:
        yield test_client
    for bus in app_module.BUSES:
        bus["seats"] = app_module.BUS_SEAT_DEFAULTS[bus["id"]]
    app_module.RESERVATIONS.clear()

def booking_form(**overrides):
    data = {"passenger": "Alex Example", "email": "alex@example.com", "phone": "9876543210",
            "travel_date": (date.today() + timedelta(days=4)).isoformat(), "seats": "2"}
    data.update(overrides)
    return data

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Your next journey" in response.data
    assert b"RouteNest" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_bus_api_returns_demo_buses(client):
    response = client.get("/api/buses")
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload) >= 5
    assert all("operator" in bus and "seats" in bus for bus in payload)

def test_bus_search_filters_route(client):
    response = client.get("/buses?from=Chennai&to=Madurai")
    assert response.status_code == 200
    assert b"Southern Express" in response.data
    assert b"GreenLine Travels" in response.data
    assert b"Coastal Cruiser" not in response.data

def test_booking_reduces_available_seats(client):
    bus = next(item for item in app_module.BUSES if item["id"] == 101)
    response = client.post("/book/101", data=booking_form(), follow_redirects=True)
    assert response.status_code == 200
    assert b"Booking confirmed" in response.data
    assert bus["seats"] == app_module.BUS_SEAT_DEFAULTS[101] - 2
    assert len(app_module.RESERVATIONS) == 1

def test_booking_rejects_too_many_seats(client):
    bus = next(item for item in app_module.BUSES if item["id"] == 101)
    response = client.post("/book/101", data=booking_form(seats=str(bus["seats"] + 1)), follow_redirects=True)
    assert response.status_code == 200
    assert b"Only" in response.data
    assert bus["seats"] == app_module.BUS_SEAT_DEFAULTS[101]
    assert len(app_module.RESERVATIONS) == 0

def test_booking_rejects_invalid_email(client):
    response = client.post("/book/101", data=booking_form(email="not-an-email"), follow_redirects=True)
    assert response.status_code == 200
    assert b"valid email" in response.data
    assert len(app_module.RESERVATIONS) == 0

def test_booking_rejects_past_date(client):
    past_date = (date.today() - timedelta(days=1)).isoformat()
    response = client.post("/book/101", data=booking_form(travel_date=past_date), follow_redirects=True)
    assert response.status_code == 200
    assert b"future travel date" in response.data
    assert len(app_module.RESERVATIONS) == 0

def test_my_bookings_finds_existing_reference(client):
    client.post("/book/101", data=booking_form(), follow_redirects=True)
    reference = app_module.RESERVATIONS[0]["reference"]
    response = client.post("/my-bookings", data={"reference": reference.lower()}, follow_redirects=True)
    assert response.status_code == 200
    assert reference.encode() in response.data
    assert b"Alex Example" in response.data

def test_about_and_contact_pages_load(client):
    assert client.get("/about").status_code == 200
    assert client.get("/contact").status_code == 200

def test_contact_form_validation(client):
    response = client.post("/contact", data={"name": "", "email": "bad", "message": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"valid email" in response.data

def test_stats_api(client):
    payload = client.get("/api/stats").get_json()
    assert payload["bus_count"] == len(app_module.BUSES)
    assert payload["booking_count"] == 0

def test_unknown_page_returns_404(client):
    assert client.get("/not-a-real-page").status_code == 404
