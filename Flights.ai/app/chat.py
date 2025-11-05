from .phi3_handler import chat as query_phi3
from .tools import get_ticket_price, get_flight_price

SYSTEM_PROMPT = """
You are FlightAI, a polite and concise airline assistant.
Always use the available tools first:
- get_flight_price(origin, destination, date, class='economy', direct_only=False)
- get_ticket_price(city)

Step-wise behavior:
1. If user asks for flight prices, **fetch the price first** using the tools. Then show top 3 flights with price and duration. Move to next step.
2. Only after showing the price, ask for payment details or visa information if the user wants to book.
3. Do not speculate about visas, payment, or policies before fetching price.
4. Keep replies short (1-2 sentences) and polite.

You are FlightAI, a polite and concise airline assistant. Ignore unrelated topics. Only answer questions about flights, tickets, airline services and places to visit guide in that city.
"""


def detect_tool(message: str):
    """Detect if the message is asking for a flight price"""
    msg = message.lower()
    if "price" in msg or "flight" in msg or "fly" in msg:
        return "flight_api"
    elif "price" in msg:
        return "sqlite"
    else:
        return None


def chat(message, history, last_step=None):
    """
    last_step = None -> price not fetched
                'price_shown' -> price shown, now can ask for booking/payment
    """
    history = history or []

    tool = detect_tool(message)

    if tool == "flight_api" and last_step != "price_shown":
        import re
        match = re.search(r"from (\w+(?: \w+)*) to (\w+(?: \w+)*) on (\d{4}-\d{2}-\d{2})", message)
        if match:
            origin, dest, date = match.groups()
            reply = get_flight_price(origin, dest, date)
            last_step = "price_shown"  # price has been fetched
        else:
            reply = "Please specify your route and date (e.g., from Delhi to London on 2025-12-21)."

    elif last_step == "price_shown":
        reply = "Great! To proceed with booking, please provide your full name as per passport and payment details."

    else:
        reply = query_phi3(message)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return history, reply, last_step
