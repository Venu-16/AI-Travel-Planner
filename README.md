# AI Travel Planner

The **AI Travel Planner** is a Streamlit-based web application that allows users to generate personalized travel itineraries using Google's Gemini AI. Users can specify trip details such as starting location, destination, budget, trip duration, travel purpose, preferences, dietary restrictions, and preferred transportation mode. The application then generates a comprehensive itinerary with meal recommendations, accommodation options, and activities.

## Features
- **User-Friendly Interface**: Developed with Streamlit for seamless interaction.
- **AI-Driven Itinerary Creation**: Uses Gemini AI to generate personalized trip plans.
- **Budget Options**: Provides budget, mid-range, and luxury choices.
- **Meal & Accommodation Recommendations**: Tailored to dietary preferences and budget.
- **Transportation Suggestions**: Offers travel options for convenience.
- **Map Integration**: Displays location-based information.
- **Downloadable Itineraries**: Enables users to save their itinerary as a file.

## Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Google Generative AI SDK

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Venu-16/ai-travel-planner.git
   ```
2. Change to the project directory:
   ```sh
   cd ai-travel-planner
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure Gemini API Key:
   - Get an API key from [Google AI Studio](https://ai.google.dev/).
   - Create a `.streamlit/secrets.toml` file and add the following:
     ```toml
     GEMINI_KEY = "your-api-key"
     ```
5. Run the application:
   ```sh
   streamlit run app.py
   ```

## Code Structure
- `app.py`: Main Streamlit application file.
- `requirements.txt`: List of required dependencies.
- `.streamlit/secrets.toml`: Securely stores API keys.

## Usage
1. Open the web app.
2. Enter the trip details in the sidebar:
   - **Starting Location & Destination**
   - **Budget** (Budget, Mid-range, Luxury)
   - **Trip Duration**
   - **Purpose of Travel** (Leisure, Adventure, Work, etc.)
   - **Special Preferences** (Cultural, Food Choices, etc.)
3. Click "Generate Itinerary".
4. View and save the itinerary.
## Deployed Link: [link](https://ai-travel-planner-k989nuvrbsqwgsbgpir9cb.streamlit.app)

## Contributors
Developed by [Venu-16](https://github.com/Venu-16).

---
Feel free to contribute by opening issues or pull requests!
