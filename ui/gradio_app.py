import os
import sys
import html
import gradio as gr

# Add main project folder to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from workflow.travel_workflow import TravelWorkflow


workflow = TravelWorkflow()


# ---------------------------------------------------
# CREATE MAP
# ---------------------------------------------------

def create_map(destination, activities):

    if not activities:
        return """
        <div class="empty-card">
            No location data available.
        </div>
        """

    first_lat = activities[0].get("latitude")
    first_lon = activities[0].get("longitude")

    if first_lat is None or first_lon is None:
        return """
        <div class="empty-card">
            Map coordinates are not available.
        </div>
        """

    markers = ""

    for activity in activities:

        name = html.escape(
            str(activity.get("name", "Unknown Place"))
        )

        kind = html.escape(
            str(activity.get("kind", "Tourist Attraction"))
        )

        lat = activity.get("latitude")
        lon = activity.get("longitude")

        if lat is not None and lon is not None:

            markers += f"""
            L.marker([{lat}, {lon}])
                .addTo(map)
                .bindPopup(
                    "<b>{name}</b><br>{kind}"
                );
            """

    destination_name = html.escape(destination)

    map_content = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="utf-8">

        <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        />

        <style>

            html,
            body,
            #map {{
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }}

        </style>

    </head>

    <body>

        <div id="map"></div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

        <script>

            const map = L.map("map").setView(
                [{first_lat}, {first_lon}],
                10
            );

            L.tileLayer(
                "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
                {{
                    maxZoom: 19,
                    attribution: "&copy; OpenStreetMap contributors"
                }}
            ).addTo(map);

            L.marker([{first_lat}, {first_lon}])
                .addTo(map)
                .bindPopup("<b>{destination_name}</b>");

            {markers}

        </script>

    </body>

    </html>
    """

    escaped_content = html.escape(map_content)

    return f"""
    <iframe
        srcdoc="{escaped_content}"
        width="100%"
        height="500"
        style="
            border: none;
            border-radius: 16px;
        "
    >
    </iframe>
    """

# ---------------------------------------------------
# FORMAT FLIGHTS
# ---------------------------------------------------

def format_flights(flights):

    if not flights:
        return "## No flight options found."

    text = "## ✈️ Available Flight Options\n\n"

    for i, flight in enumerate(flights, start=1):

        stops = flight.get("stops", 0)

        if stops == 0:
            stop_text = "Non-stop"
        else:
            stop_text = f"{stops} stop(s)"

        text += f"""
### {i}. ✈️ {flight.get("airline", "Unknown Airline")}

| Detail | Information |
|---|---|
| 💰 Price | ₹{flight.get("price", "N/A")} |
| ⏱️ Duration | {flight.get("duration", "N/A")} |
| 🛑 Stops | {stop_text} |

"""

    text += """
> ⚠️ **Note:** Flight information is currently simulated for demonstration purposes.
"""

    return text


# ---------------------------------------------------
# FORMAT HOTELS
# ---------------------------------------------------

def format_hotels(hotels):

    if not hotels:
        return "## No hotel options found."

    text = "## 🏨 Accommodation Options\n\n"

    for i, hotel in enumerate(hotels, start=1):

        text += f"""
### {i}. 🏨 {hotel.get("name", "Unknown Hotel")}

| Detail | Information |
|---|---|
| 📍 Location | {hotel.get("location", "N/A")} |
| 💰 Per Night | ₹{hotel.get("price_per_night", "N/A")} |
| ⭐ Rating | {hotel.get("rating", "N/A")} / 5 |

"""

    text += """
> ⚠️ **Note:** Hotel information is currently simulated for demonstration purposes.
"""

    return text


# ---------------------------------------------------
# FORMAT ACTIVITIES
# ---------------------------------------------------

def format_activities(activities):

    if not activities:
        return "## No tourist attractions found."

    text = "## 📍 Recommended Places to Visit\n\n"

    for i, activity in enumerate(activities, start=1):

        name = activity.get("name", "Unknown Place")
        kind = activity.get("kind", "Tourist Attraction")

        text += f"""
### {i}. 📍 {name}

**Category:** {kind}

"""

    return text


# ---------------------------------------------------
# FORMAT WEATHER
# ---------------------------------------------------

def format_weather(weather):

    return f"""
# 🌦️ Current Weather

| Weather Detail | Value |
|---|---|
| 🌡️ Temperature | **{weather.get("temperature", "N/A")}°C** |
| 💧 Humidity | **{weather.get("humidity", "N/A")}%** |
| 💨 Wind Speed | **{weather.get("wind_speed", "N/A")} km/h** |
| ☁️ Weather Code | **{weather.get("weather_code", "N/A")}** |
| 🌍 Timezone | **{weather.get("timezone", "N/A")}** |

"""


# ---------------------------------------------------
# FORMAT BUDGET
# ---------------------------------------------------

def format_budget(budget):

    return f"""
# 💰 Estimated Trip Budget

### ✈️ Flight

**₹{budget.get("flight_cost", "N/A")}**

### 🏨 Accommodation

**₹{budget.get("hotel_cost", "N/A")}**

### 🍽️ Other Expenses

**₹{budget.get("other_expenses", "N/A")}**

---

# 💰 Total Estimated Cost

## ₹{budget.get("total_estimated_cost", "N/A")}

"""


# ---------------------------------------------------
# SUMMARY CARDS
# ---------------------------------------------------

def create_summary_cards(destination, days, weather, activities, budget):

    temperature = weather.get("temperature", "N/A")
    attractions = len(activities)
    total_budget = budget.get("total_estimated_cost", "N/A")

    return f"""
    <div class="summary-grid">

        <div class="summary-card">
            <div class="card-icon">📍</div>
            <div class="card-label">DESTINATION</div>
            <div class="card-value">{destination}</div>
        </div>

        <div class="summary-card">
            <div class="card-icon">📅</div>
            <div class="card-label">TRIP DURATION</div>
            <div class="card-value">{days} Days</div>
        </div>

        <div class="summary-card">
            <div class="card-icon">🌡️</div>
            <div class="card-label">TEMPERATURE</div>
            <div class="card-value">{temperature}°C</div>
        </div>

        <div class="summary-card">
            <div class="card-icon">📍</div>
            <div class="card-label">ATTRACTIONS</div>
            <div class="card-value">{attractions} Found</div>
        </div>

        <div class="summary-card">
            <div class="card-icon">💰</div>
            <div class="card-label">ESTIMATED BUDGET</div>
            <div class="card-value">₹{total_budget}</div>
        </div>

    </div>
    """


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def plan_trip(origin, destination, days):

    # Validate inputs
    if not origin or not destination:
        error = """
        <div class="error-box">
            ⚠️ Please enter both Origin and Destination.
        </div>
        """

        yield (
            error,
            gr.update(visible=False),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        )

        return

    try:

        days = int(days)

        if days <= 0:
            raise ValueError("Number of days must be greater than 0.")

        # ---------------------------------------------------
        # SHOW EXECUTION STATUS FIRST
        # ---------------------------------------------------

        status_running = """
        <div class="agent-status">

            <h3>🤖 Multi-Agent System Execution</h3>

            <div class="agent-item">🔄 Transport Agent → Finding flight options...</div>
            <div class="agent-item">🔄 Accommodation Agent → Finding hotels...</div>
            <div class="agent-item">🔄 Activity Agent → Fetching tourist attractions...</div>
            <div class="agent-item">🔄 Weather Agent → Fetching live weather...</div>
            <div class="agent-item">🔄 Budget Agent → Calculating trip expenses...</div>
            <div class="agent-item">🔄 Recommendation Agent → Gemini is generating your itinerary...</div>

        </div>
        """

        yield (
            status_running,
            gr.update(visible=False),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        )

        # ---------------------------------------------------
        # RUN COMPLETE WORKFLOW
        # ---------------------------------------------------

        result = workflow.run(
            origin=origin,
            destination=destination,
            days=days
        )

        # ---------------------------------------------------
        # EXTRACT RESULTS
        # ---------------------------------------------------

        flights = result["transport"]["transport"]

        hotels = result["accommodation"]["accommodation"]

        activities = result["activities"]["activities"]

        weather = result["weather"]["weather"]

        budget = result["budget"]

        recommendation = result["recommendation"]

        # ---------------------------------------------------
        # FORMAT RESULTS
        # ---------------------------------------------------

        flights_text = format_flights(flights)

        hotels_text = format_hotels(hotels)

        activities_text = format_activities(activities)

        weather_text = format_weather(weather)

        budget_text = format_budget(budget)

        summary_cards = create_summary_cards(
            destination=destination,
            days=days,
            weather=weather,
            activities=activities,
            budget=budget
        )

        map_html = create_map(
            destination=destination,
            activities=activities
        )

        # ---------------------------------------------------
        # COMPLETED AGENT STATUS
        # ---------------------------------------------------

        status_completed = """
        <div class="agent-status success">

            <h3>✅ Multi-Agent System Completed Successfully</h3>

            <div class="agent-item">✅ Transport Agent → Flight options generated</div>
            <div class="agent-item">✅ Accommodation Agent → Hotel options generated</div>
            <div class="agent-item">✅ Activity Agent → Tourist attractions fetched</div>
            <div class="agent-item">✅ Weather Agent → Live weather data fetched</div>
            <div class="agent-item">✅ Budget Agent → Trip budget calculated</div>
            <div class="agent-item">🤖 Recommendation Agent → Gemini itinerary generated</div>

        </div>
        """

        # ---------------------------------------------------
        # RETURN FINAL RESULTS
        # ---------------------------------------------------

        yield (
            status_completed,
            gr.update(visible=True),
            summary_cards,
            flights_text,
            hotels_text,
            activities_text,
            weather_text,
            budget_text,
            recommendation,
            map_html
        )

    except Exception as e:

        error_message = f"""
        <div class="error-box">

        <h3>❌ Something went wrong</h3>

        <p>{html.escape(str(e))}</p>

        </div>
        """

        yield (
            error_message,
            gr.update(visible=False),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        )


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

custom_css = """

.gradio-container {
    max-width: 1400px !important;
    margin: auto !important;
}

.hero {
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 20px;
    text-align: center;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
    opacity: 0.8;
}

.input-section {
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 15px;
    margin: 20px 0;
}

.summary-card {
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    text-align: center;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.card-label {
    font-size: 12px;
    opacity: 0.7;
    margin-bottom: 8px;
}

.card-value {
    font-size: 18px;
    font-weight: bold;
}

.agent-status {
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    border: 1px solid rgba(128,128,128,0.3);
}

.agent-status h3 {
    margin-top: 0;
}

.agent-item {
    padding: 8px;
    margin: 5px 0;
    border-radius: 8px;
}

.error-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #cc4444;
}

.map-container {
    width: 100%;
    height: 500px;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(128,128,128,0.3);
}

#travel-map {
    width: 100%;
    height: 500px;
}

.empty-card {
    padding: 30px;
    text-align: center;
    border: 1px solid rgba(128,128,128,0.3);
    border-radius: 12px;
}

@media (max-width: 900px) {

    .summary-grid {
        grid-template-columns: repeat(2, 1fr);
    }

}

"""


# ---------------------------------------------------
# GRADIO UI
# ---------------------------------------------------

with gr.Blocks(
    title="Agentic AI Travel Planner",
    theme=gr.themes.Soft(),
    css=custom_css
) as app:

    # HERO SECTION

    gr.HTML("""
    <div class="hero">

        <h1>✈️ Agentic AI Travel Planner</h1>

        <p>
            Plan intelligent trips using
            <b>Multi-Agent AI</b>,
            <b>Real-Time APIs</b>
            and
            <b>Gemini Generative AI</b>.
        </p>

    </div>
    """)

    # INPUT SECTION

    with gr.Group():

        gr.Markdown("## 🧳 Plan Your Journey")

        with gr.Row():

            origin = gr.Textbox(
                label="📍 From",
                placeholder="Example: Hyderabad",
                scale=2
            )

            destination = gr.Textbox(
                label="📍 To",
                placeholder="Example: Goa",
                scale=2
            )

            days = gr.Number(
                label="📅 Days",
                value=3,
                precision=0,
                minimum=1,
                scale=1
            )

        plan_button = gr.Button(
            "✨ Generate AI Travel Plan",
            variant="primary",
            size="lg"
        )

    # AGENT STATUS

    agent_status = gr.HTML()

    # RESULTS

    with gr.Column(visible=False) as results_section:

        gr.Markdown("## 📊 Trip Overview")

        summary_output = gr.HTML()

        with gr.Tabs():

            # FLIGHTS
            with gr.Tab("✈️ Flights"):
                flights_output = gr.Markdown()

            # HOTELS
            with gr.Tab("🏨 Hotels"):
                hotels_output = gr.Markdown()

            # ACTIVITIES
            with gr.Tab("📍 Places to Visit"):
                activities_output = gr.Markdown()

            # WEATHER
            with gr.Tab("🌦️ Weather"):
                weather_output = gr.Markdown()

            # BUDGET
            with gr.Tab("💰 Budget"):
                budget_output = gr.Markdown()

            # AI ITINERARY
            with gr.Tab("🤖 AI Travel Plan"):
                recommendation_output = gr.Markdown()

            # MAP
            with gr.Tab("🗺️ Destination Map"):
                map_output = gr.HTML()

    # BUTTON CLICK

    plan_button.click(
        fn=plan_trip,

        inputs=[
            origin,
            destination,
            days
        ],

        outputs=[
            agent_status,
            results_section,
            summary_output,
            flights_output,
            hotels_output,
            activities_output,
            weather_output,
            budget_output,
            recommendation_output,
            map_output
        ]
    )


# ---------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------

if __name__ == "__main__":

    app.launch()