import os
import requests
from dotenv import load_dotenv
from .config import AMADEUS_API_KEY, AMADEUS_API_SECRET, DB_PATH

load_dotenv()

def _get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    client_id = AMADEUS_API_KEY or os.getenv("AMADEUS_CLIENT_ID", "")
    client_secret = AMADEUS_API_SECRET or os.getenv("AMADEUS_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        return None, (
            "Missing Amadeus credentials. Set AMADEUS_API_KEY/AMADEUS_API_SECRET "
            "(or AMADEUS_CLIENT_ID/AMADEUS_CLIENT_SECRET) in your environment."
        )

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    res = requests.post(url, data=payload)
    if res.status_code == 200:
        return res.json().get("access_token"), None
    else:
        try:
            details = res.json()
        except Exception:
            details = res.text
        return None, f"Failed to authenticate Amadeus API: {res.status_code} {details}"

def get_flight_price(origin, destination, date):
    """Fetch top 3 direct business class flights from Amadeus API"""
    token, auth_err = _get_amadeus_token()
    if auth_err:
        return auth_err

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin[:3].upper(),
        "destinationLocationCode": destination[:3].upper(),
        "departureDate": date,
        "adults": 1,
        "travelClass": "BUSINESS",
        "nonStop": "true",
        "max": 3  # fetch top 3
    }
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        return f"API Error: {res.status_code} - {res.text}"

    try:
        data = res.json()["data"]
        if not data:
            return f"No direct business class flights found from {origin.title()} to {destination.title()} on {date}."

        # build a friendly chat-like message
        flights = []
        for i, f in enumerate(data[:3], 1):
            airline = f["validatingAirlineCodes"][0]
            price = f["price"]["total"]
            duration = f["itineraries"][0]["duration"].replace("PT", "").lower()  # e.g., "10h30m"
            flights.append(f"{i}. {airline} – ${price}, Duration: {duration}")

        reply = f"Top {len(flights)} direct business class flights from {origin.title()} to {destination.title()} on {date}:\n" + "\n".join(flights)
        reply += "\n\nWould you like to proceed with booking one of these?"
        return reply

    except Exception as e:
        return f"Error parsing flight data: {e}"

def get_ticket_price(city):
    """Local SQLite fallback if available"""
    import sqlite3
    DB = DB_PATH
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
            result = cursor.fetchone()
            if result:
                return f"Ticket price to {city.title()} is ${result[0]} (local data)"
            else:
                return "No local price data for this city."
    except Exception as e:
        return f"Database error: {e}"
