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


# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="Multi-Day AI Travel Planner", layout="wide")
st.title("🗺️ Multi-Day AI Travel Planner — Daywise Maps + Weather")

# Inputs
starting_location = st.text_input("Starting Location")
destination = st.text_input("Destination")
budget = st.selectbox("Budget", ["Budget", "Mid-range", "Luxury"])
duration = st.slider("Trip Duration (days)", 1, 14, 5)
purpose = st.text_area("Purpose of Travel (e.g., leisure, adventure, work)")
preferences = st.text_area("Any special preferences? (e.g., food, hidden gems)")

if st.button("Generate Multi-Day Itinerary"):
    if not (starting_location and destination):
        st.warning("Please enter both starting location and destination.")
    else:
        user_input = (
            f"Starting: {starting_location}, Destination: {destination}, "
            f"Budget: {budget}, Duration: {duration} days, Purpose: {purpose}, Preferences: {preferences}"
        )

        with st.spinner("Generating day-by-day itinerary from AI... ⏳"):
            itinerary_text = get_daywise_itinerary(user_input, duration)

        if not itinerary_text:
            st.error("Could not generate itinerary.")
        else:
            st.success("Itinerary generated!")
            st.markdown("### Full Itinerary")
            st.markdown(itinerary_text.replace("\n", "  \n"))  # keep newlines in markdown

            # Split into day blocks
            day_blocks = extract_day_blocks(itinerary_text)

            st.markdown("---")
            st.markdown("### Day-by-Day Visuals (map + current weather)")

            # Use tabs for each day for neat UI
            tabs = st.tabs([f"Day {i}" for i in range(1, len(day_blocks) + 1)])

            for idx, tab in enumerate(tabs):
                day_block = day_blocks[idx]
                with tab:
                    st.markdown(f"#### {day_block.splitlines()[0]}")
                    # Show the day's text (exclude the header line if present)
                    rest_text = "\n".join(day_block.splitlines()[1:]).strip()
                    if rest_text:
                        st.markdown(rest_text.replace("\n", "  \n"))
                    else:
                        st.info("No detailed activities for this day in the AI output.")

                    # Guess main location for the day (or fallback to destination)
                    main_loc = guess_main_location(day_block, destination)
                    lat, lng = get_coordinates(main_loc)

                    if lat and lng:
                        # Weather
                        temp, desc, icon_url = get_weather(lat, lng)
                        if temp is not None and desc is not None:
                            cols = st.columns([1, 4])
                            with cols[0]:
                                if icon_url:
                                    st.image(icon_url, width=80)
                            with cols[1]:
                                st.markdown(f"**Current weather in {main_loc}:** {temp}°C — {desc}")

                        # Map centered on main location
                        m = folium.Map(location=[lat, lng], zoom_start=12)
                        folium.Marker([lat, lng], tooltip=main_loc, icon=folium.Icon(color="blue")).add_to(m)
                        st_folium(m, width=900, height=450)
                    else:
                        st.warning(f"Could not find coordinates for \"{main_loc}\". Weather/map unavailable for this day.")
