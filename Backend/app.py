import os
import re
import requests
import streamlit as st
import google.generativeai as genai
import googlemaps
from dotenv import load_dotenv
from streamlit_folium import st_folium
import folium

# ----------------- CONFIG -----------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ----------------- HELPERS -----------------
def get_coordinates(place_name):
    """Return latitude and longitude for a given place name."""
    try:
        geocode_result = gmaps.geocode(place_name)
        if geocode_result:
            loc = geocode_result[0]['geometry']['location']
            return loc['lat'], loc['lng']
    except Exception:
        return None, None
    return None, None


def get_daywise_itinerary(user_input, days):
    """Ask Gemini for a day-by-day itinerary (structured)."""
    prompt = f"""
You are an expert travel planner.
Create a detailed day-by-day itinerary for {days} days.
Trip Details: {user_input}

For each day, use the format:

Day 1: <MainCityOrArea>
- Morning: ...
- Afternoon: ...
- Evening: ...
...
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else "No itinerary generated."
    except Exception as e:
        st.error(f"AI error: {e}")
        return None


def extract_day_blocks(itinerary_text):
    """
    Extract full Day blocks (Day 1 ... Day N) as separate text blocks.
    Returns list of strings like ['Day 1: ...', 'Day 2: ...', ...]
    """
    if not itinerary_text:
        return []

    # Split by "Day X" headers (keeps the header)
    parts = re.split(r'(?=(Day\s*\d+\b))', itinerary_text)
    blocks = []
    # parts example: ['', 'Day 1', ': rest...', 'Day 2', ': rest...']
    # Reconstruct day blocks
    i = 1
    while i < len(parts):
        header = parts[i].strip()
        body = parts[i+1] if i+1 < len(parts) else ""
        blocks.append(header + body)
        i += 2
    if not blocks:
        # Fallback: treat whole text as Day 1
        blocks = [itinerary_text]
    return blocks


def guess_main_location(day_block, fallback_destination):
    """
    Try to guess a main location/city for the day's block.
    Strategy:
    1. Look for `Day N: <City/Area>` pattern
    2. Otherwise fallback to provided destination
    """
    m = re.search(r"Day\s*\d+[:\-]?\s*([A-Za-z0-9 ,\-()]+)", day_block)
    if m:
        loc = m.group(1).strip()
        # if it looks like a long sentence, fallback
        if len(loc) < 60:
            return loc
    return fallback_destination


def get_weather(lat, lng):
    """Fetch current weather from OpenWeatherMap (returns temp, desc, icon_url)."""
    try:
        if not WEATHER_API_KEY:
            return None, None, None
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lng}&appid={WEATHER_API_KEY}&units=metric"
        )
        r = requests.get(url, timeout=8)
        data = r.json()
        if data and data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].title()
            icon = data["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
            return temp, desc, icon_url
    except Exception:
        return None, None, None
    return None, None, None


