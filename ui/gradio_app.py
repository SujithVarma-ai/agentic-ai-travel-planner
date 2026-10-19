
"""Premium Gradio UI for the Agentic AI Travel Planner."""

import html
import os
import sys
from urllib.parse import quote
import traceback

import gradio as gr

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from workflow.travel_workflow import TravelWorkflow

workflow = TravelWorkflow()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(value):
    return html.escape(
        str(value if value is not None else "—")
    )


def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return "N/A"


# ============================================================
# MAP
# Uses an OpenStreetMap iframe instead of injected JavaScript.
# ============================================================


def create_map(destination, activities):
    points = []

    for item in activities or []:
        try:
            lat = float(item["latitude"])
            lon = float(item["longitude"])

            if -90 <= lat <= 90 and -180 <= lon <= 180:
                points.append((lat, lon))

        except (KeyError, TypeError, ValueError):
            continue

    if points:
        latitudes = [point[0] for point in points]
        longitudes = [point[1] for point in points]

        padding = 0.02

        west = max(-180, min(longitudes) - padding)
        east = min(180, max(longitudes) + padding)
        south = max(-90, min(latitudes) - padding)
        north = min(90, max(latitudes) + padding)

        if west == east:
            west = max(-180, west - padding)
            east = min(180, east + padding)

        if south == north:
            south = max(-90, south - padding)
            north = min(90, north + padding)

        bbox = f"{west},{south},{east},{north}"

        map_url = (
            "https://www.openstreetmap.org/export/embed.html?bbox="
            + quote(bbox, safe=",")
        )

        full_map_url = (
            "https://www.openstreetmap.org/#map=12/"
            f"{points[0][0]}/{points[0][1]}"
        )

        safe_destination = html.escape(
            str(destination), quote=True
        )

        return f"""
        <div class="map-frame">
            <iframe
                title="Map of attractions near {safe_destination}"
                src="{html.escape(map_url, quote=True)}"
                width="100%"
                height="480"
                style="border:0"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>

        <p style="font-size:12px;color:#77839a;margin-top:8px">
            Map area is based on coordinates returned by the Activity Agent.
            <a href="{html.escape(full_map_url, quote=True)}"
               target="_blank"
               rel="noopener noreferrer">
                Open larger map
            </a>
        </p>
        """

    search_url = (
        "https://www.openstreetmap.org/search?query="
        + quote(str(destination))
    )

    return f"""
    <div class="empty-state">
        <p>Attraction coordinates are unavailable.</p>

        <a href="{html.escape(search_url, quote=True)}"
           target="_blank"
           rel="noopener noreferrer">
            View {html.escape(str(destination))}
            on OpenStreetMap
        </a>
    </div>
    """



# ============================================================
# FLIGHT OPTIONS
# ============================================================



def format_flights(flights):
    if isinstance(flights, dict):
        if flights.get("error"):
            return f"### Flight options unavailable\n\n{flights['error']}"
        flights = flights.get("transport", [])

    if not isinstance(flights, list) or not flights:
        return "### No flight options returned."

    rows = []

    for flight in flights:
        airline = safe_text(flight.get("airline", "Airline"))
        duration = safe_text(flight.get("duration", "—"))
        stops = int(flight.get("stops", 0) or 0)
        stop_text = "Non-stop" if stops == 0 else f"{stops} stop(s)"
        price = money(flight.get("price"))

        rows.append(
            f"| {airline} | {duration} | {stop_text} | **{price}** |"
        )

    return (
        "### ✈️ Flight Options\n\n"
        "| Airline | Duration | Stops | Estimated Fare |\n"
        "|---|---|---|---:|\n"
        + "\n".join(rows)
        + "\n\n> Fares are simulated estimates, not live booking prices."
    )




# ============================================================
# HOTEL OPTIONS
# ============================================================

def format_hotels(hotels):
    if not hotels:
        return "### No accommodation options returned."

    rows = []

    for hotel in hotels:
        rows.append(
            f"| {safe_text(hotel.get('name', 'Hotel'))} "
            f"| {safe_text(hotel.get('location', '—'))} "
            f"| {safe_text(hotel.get('rating', '—'))}/5 "
            f"| **{money(hotel.get('price_per_night'))}** |"
        )

    return (
        "### 🏨 Accommodation ideas\n\n"
        "| Property | Area | Rating | Per night |\n"
        "|---|---|---:|---:|\n"
        + "\n".join(rows)
        + "\n\n> Hotel names, ratings and prices are simulated "
        "examples, not verified listings."
    )


# ============================================================
# TOURIST ATTRACTIONS
# ============================================================


def format_activities(activities):
    if not activities:
        return (
            "### No attractions found.\n\n"
            "Try a nearby town or a larger search radius. "
            "Check your OpenTripMap API configuration if "
            "the problem continues."
        )

    output = ["### 📍 Places to explore", ""]

    for index, activity in enumerate(activities, 1):
        name = safe_text(activity.get("name", "Attraction"))
        kind = safe_text(
            activity.get("kind") or "Tourist attraction"
        )

        distance = activity.get("distance")

        if isinstance(distance, (int, float)):
            distance_text = (
                f"{distance / 1000:.1f} km from search center"
            )
        else:
            distance_text = "Distance unavailable"

        output.append(
            f"**{index}. {name}**  \n"
            f"<small>{kind} · {distance_text}</small>"
        )
        output.append("")

    return "\n".join(output)



# ============================================================
# WEATHER
# ============================================================

def format_weather(weather):
    if not isinstance(weather, dict):
        return (
            "### Weather unavailable\n\n"
            "The weather agent did not return usable data."
        )

    return f"""
### 🌦️ Weather snapshot

<div class="weather-grid">

    <div class="weather-tile">
        <span>Temperature</span>
        <strong>{safe_text(weather.get('temperature', '—'))}°C</strong>
    </div>

    <div class="weather-tile">
        <span>Humidity</span>
        <strong>{safe_text(weather.get('humidity', '—'))}%</strong>
    </div>

    <div class="weather-tile">
        <span>Wind speed</span>
        <strong>{safe_text(weather.get('wind_speed', '—'))} km/h</strong>
    </div>

    <div class="weather-tile">
        <span>Timezone</span>
        <strong>{safe_text(weather.get('timezone', '—'))}</strong>
    </div>

</div>

*Weather values are an API snapshot. Check the forecast again
close to your departure date.*
"""


# ============================================================
# BUDGET
# ============================================================

def format_budget(budget):
    if not isinstance(budget, dict):
        return "### Budget unavailable\n\nNo valid budget was returned."

    if budget.get("error"):
        return (
            "### Budget calculation unavailable\n\n"
            f"{safe_text(budget['error'])}"
        )

    flight_cost = budget.get("flight_cost", 0)
    hotel_cost = budget.get("hotel_cost", 0)
    other_cost = budget.get("other_expenses", 0)
    total_cost = budget.get("total_estimated_cost", 0)

    selected_flight = budget.get("selected_flight") or {}
    selected_hotel = budget.get("selected_hotel") or {}

    return f"""
### 💳 Estimated Trip Budget

<div class="budget-total">
    <span>Estimated Total</span>
    <strong>{money(total_cost)}</strong>
    <small>Indicative estimate · INR</small>
</div>

| Expense | Details | Estimated Cost |
|---|---|---:|
| ✈️ Flight | {safe_text(selected_flight.get("airline", "Selected flight"))} | **{money(flight_cost)}** |
| 🏨 Accommodation | {safe_text(selected_hotel.get("name", "Selected hotel"))} | **{money(hotel_cost)}** |
| 🍽️ Food and local expenses | Estimated expenses | **{money(other_cost)}** |

> Flight and hotel prices are simulated estimates, not live booking prices.
"""


# ============================================================
# TRIP SUMMARY CARDS
# ============================================================

def summary_cards(
    origin,
    destination,
    days,
    weather,
    activities,
    budget
):
    weather = weather if isinstance(weather, dict) else {}
    budget = budget if isinstance(budget, dict) else {}

    temperature = safe_text(
        weather.get("temperature", "—")
    )

    total = money(
        budget.get("total_estimated_cost")
    )

    return f"""
    <div class="metrics-grid">

        <div class="metric">
            <span>ROUTE</span>
            <strong>
                {safe_text(origin)} → {safe_text(destination)}
            </strong>
            <small>Trip route</small>
        </div>

        <div class="metric">
            <span>DURATION</span>
            <strong>{int(days)} days</strong>
            <small>Planned stay</small>
        </div>

        <div class="metric">
            <span>WEATHER</span>
            <strong>{temperature}°C</strong>
            <small>Latest available snapshot</small>
        </div>

        <div class="metric">
            <span>ATTRACTIONS</span>
            <strong>{len(activities or [])}</strong>
            <small>Places returned by API</small>
        </div>

        <div class="metric metric-highlight">
            <span>ESTIMATED BUDGET</span>
            <strong>{total}</strong>
            <small>Indicative · INR</small>
        </div>

    </div>
    """


# ============================================================
# AGENT STATUS PANEL
# Note: this represents overall workflow completion, not
# independent verification of every agent's execution.
# ============================================================

def status_html(state, detail=""):
    agents = [
        ("Transport Agent", "Flight options"),
        ("Accommodation Agent", "Hotel suggestions"),
        ("Activity Agent", "Tourist attractions"),
        ("Weather Agent", "Destination weather"),
        ("Budget Agent", "Cost estimate"),
        ("Recommendation Agent", "Gemini itinerary"),
    ]

    complete = state == "complete"

    title = (
        "Travel plan generated"
        if complete
        else "Preparing your trip"
    )

    icon = "✓" if complete else "↻"

    status_text = "Workflow returned" if complete else "Queued"

    items = ""

    for agent_name, description in agents:
        check = "✓" if complete else "•"

        items += f"""
        <div class="agent-pill">

            <span class="agent-check">{check}</span>

            <div>
                <strong>{agent_name}</strong>
                <small>{description}</small>
            </div>

            <em>{status_text}</em>

        </div>
        """

    extra = (
        f'<p class="status-detail">{safe_text(detail)}</p>'
        if detail
        else ""
    )

    description = (
        "The workflow returned results from the connected agents."
        if complete
        else "Agents will run through your existing TravelWorkflow."
    )

    return f"""
    <section class="status-panel">

        <div class="status-heading">

            <span class="status-orb">{icon}</span>

            <div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>

        </div>

        <div class="agent-list">
            {items}
        </div>

        {extra}

    </section>
    """


# ============================================================
# MAIN TRAVEL PLANNING FUNCTION
# ============================================================

def plan_trip(origin, destination, days):
    origin = (origin or "").strip()
    destination = (destination or "").strip()

    if not origin or not destination:
        yield (
            '<div class="error-panel">'
            '<strong>Missing trip details</strong>'
            '<p>Enter both your starting city and destination.</p>'
            '</div>',
            gr.update(visible=False),
            "", "", "", "", "", "", "", ""
        )
        return

    try:
        days = int(days)

        if not 1 <= days <= 30:
            raise ValueError(
                "Choose a trip duration between 1 and 30 days."
            )

        # Show progress while the agents are running.
        yield (
            status_html("running"),
            gr.update(visible=False),
            "", "", "", "", "", "", "", ""
        )

        # Run the existing multi-agent workflow.
        result = workflow.run(
            origin=origin,
            destination=destination,
            days=days,
        )

        # Extract agent outputs safely.
        transport_result = result.get("transport") or {}
        accommodation_result = result.get("accommodation") or {}
        activities_result = result.get("activities") or {}
        weather_result = result.get("weather") or {}

        flights = transport_result.get("transport", [])
        hotels = accommodation_result.get("accommodation", [])
        activities = activities_result.get("activities", [])
        weather = weather_result.get("weather")
        budget = result.get("budget") or {}

        recommendation = (
            result.get("recommendation")
            or (
                "The recommendation agent did not return "
                "an itinerary. Check your Gemini API configuration."
            )
        )

        # Display completed results.
        yield (
            status_html("complete"),
            gr.update(visible=True),
            summary_cards(
                origin,
                destination,
                days,
                weather,
                activities,
                budget,
            ),
            format_flights(flights),
            format_hotels(hotels),
            format_activities(activities),
            format_weather(weather),
            format_budget(budget),
            str(recommendation),
            create_map(destination, activities),
        )

    except Exception as e:
        traceback.print_exc()

        # Escape the error before inserting it into HTML.
        message = safe_text(str(e))

        yield (
            f"""
            <div class="error-panel">
                <strong>We could not generate this trip</strong>
                <p>{message}</p>
                <small>
                    Check API keys, network access, and the
                    error details in your terminal.
                </small>
            </div>
            """,
            gr.update(visible=False),
            "", "", "", "", "", "", "", ""
        )



# ============================================================
# CUSTOM CSS
# ============================================================

CSS = r"""
@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
);

:root {
    --travel-ink: #18243b;
    --travel-muted: #77839a;
    --travel-purple: #6657e8;
    --travel-border: #e6eaf2;
}

.gradio-container {
    max-width: 1440px !important;
    margin: auto !important;
    font-family: 'DM Sans', sans-serif !important;
    background: #f6f8fc !important;
}

#travel-shell {
    max-width: 1220px;
    margin: 0 auto;
    padding: 12px 0 38px;
}

.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 4px 22px;
    gap: 12px;
}

.brand {
    font: 800 20px Manrope, sans-serif;
    color: #18243b;
    letter-spacing: -.6px;
}

.brand span {
    color: #6657e8;
}

.nav-note {
    color: #758198;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.hero-banner {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    padding: 48px 44px;
    color: white;

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(167,139,250,.65),
            transparent 30%
        ),
        linear-gradient(
            120deg,
            #152744 0%,
            #293d70 48%,
            #6959dc 100%
        );

    min-height: 270px;
    box-sizing: border-box;
}

.hero-banner:after {
    content: '✈';
    position: absolute;
    right: 8%;
    top: 12%;
    font-size: 160px;
    opacity: .13;
    transform: rotate(-15deg);
}

.hero-kicker {
    color: #cbd5ff;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 800;
    text-transform: uppercase;
}

.hero-banner h1 {
    font: 800 clamp(32px,4vw,48px)/1.1 Manrope, sans-serif;
    letter-spacing: -1.8px;
    margin: 16px 0 12px;
    max-width: 720px;
    color: white;
}

.hero-banner p {
    color: #e3e8ff;
    font-size: 15px;
    line-height: 1.7;
    max-width: 640px;
    margin: 0;
}

.section-label {
    font: 800 19px Manrope, sans-serif;
    color: #1d2b45;
    margin: 0 0 5px;
}

.section-sub {
    color: #8390a6;
    font-size: 13px;
    margin-bottom: 18px;
}

.search-panel {
    background: white;
    border: 1px solid var(--travel-border);
    border-radius: 22px;
    padding: 24px;
    margin-top: -28px;
    position: relative;
    z-index: 2;
    box-shadow: 0 16px 44px rgba(28,44,80,.09);
}

.search-panel label {
    color: #526079 !important;
    font-weight: 700 !important;
}

.search-panel input {
    border-radius: 12px !important;
    min-height: 48px !important;
}

#generate-btn {
    background: linear-gradient(
        100deg,
        #6758e9,
        #8770f3
    ) !important;

    border: 0 !important;
    border-radius: 12px !important;
    min-height: 50px;
    font-weight: 800 !important;
    box-shadow: 0 8px 18px rgba(102,87,232,.22);
}

.results-title {
    font: 800 22px Manrope, sans-serif;
    color: #1b2943;
    margin: 28px 0 14px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 12px;
    margin: 18px 0 22px;
}

.metric {
    background: #fff;
    border: 1px solid var(--travel-border);
    border-radius: 17px;
    padding: 18px 16px;
    min-width: 0;
    box-shadow: 0 4px 15px rgba(32,50,82,.025);
}

.metric span {
    display: block;
    color: #8994a8;
    font-size: 10px;
    letter-spacing: 1.1px;
    font-weight: 800;
    margin-bottom: 12px;
}

.metric strong {
    display: block;
    font: 800 20px Manrope, sans-serif;
    color: #202d47;
    overflow-wrap: anywhere;
}

.metric strong b {
    color: #7669e9;
}

.metric small {
    display: block;
    color: #9aa4b6;
    font-size: 11px;
    margin-top: 8px;
}

.metric-highlight {
    background: linear-gradient(145deg, #f0edff, #fff);
    border-color: #dcd6ff;
}

.status-panel {
    border: 1px solid #e3e8f2;
    background: #fff;
    border-radius: 20px;
    padding: 20px;
    margin: 22px 0;
}

.status-heading {
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 16px;
}

.status-orb {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: #eeeaff;
    color: #6657e8;
    font-size: 20px;
    font-weight: 900;
}

.status-heading h3 {
    margin: 0 0 4px;
    font: 800 17px Manrope, sans-serif;
    color: #1d2b45;
}

.status-heading p,
.status-detail {
    margin: 0;
    font-size: 12px;
    color: #8792a6;
}

.agent-list {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 9px;
}

.agent-pill {
    display: flex;
    align-items: center;
    gap: 9px;
    border: 1px solid #edf0f6;
    background: #fafbfe;
    border-radius: 12px;
    padding: 12px;
    min-width: 0;
}

.agent-check {
    display: grid;
    place-items: center;
    width: 27px;
    height: 27px;
    flex-shrink: 0;
    border-radius: 9px;
    color: #6657e8;
    background: #eeebff;
    font-weight: 900;
}

.agent-pill div {
    min-width: 0;
}

.agent-pill strong {
    display: block;
    font-size: 12px;
    color: #34415b;
}

.agent-pill small {
    display: block;
    font-size: 10px;
    color: #929db0;
    margin-top: 3px;
}

.agent-pill em {
    margin-left: auto;
    font-size: 9px;
    color: #8a94a7;
    font-style: normal;
}

.tabs {
    border: 1px solid #e5eaf2 !important;
    border-radius: 18px !important;
    background: white !important;
    padding: 10px !important;
}

.tab-nav button {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

.tabitem {
    padding: 16px 10px !important;
}

.weather-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin: 14px 0;
}

.weather-tile {
    background: #f7f8ff;
    border: 1px solid #e8eaff;
    border-radius: 13px;
    padding: 16px;
}

.weather-tile span {
    display: block;
    font-size: 11px;
    color: #8490a5;
    margin-bottom: 8px;
}

.weather-tile strong {
    font: 800 19px Manrope, sans-serif;
    color: #2d3a57;
    overflow-wrap: anywhere;
}

.budget-total {
    background: linear-gradient(110deg, #1d2c4a, #5148a7);
    color: white;
    border-radius: 17px;
    padding: 22px;
    margin: 14px 0 18px;
}

.budget-total span,
.budget-total small {
    display: block;
    color: #d4d9ff;
    font-size: 12px;
}

.budget-total strong {
    display: block;
    color: white;
    font: 800 32px Manrope, sans-serif;
    margin: 6px 0;
}

.map-frame {
    height: 480px;
    overflow: hidden;
    border-radius: 16px;
    border: 1px solid #e2e7f0;
}

.empty-state,
.error-panel {
    padding: 22px;
    border-radius: 15px;
    background: #fff;
    border: 1px solid #e5eaf2;
    color: #59667f;
}

.error-panel {
    border-color: #ffd4d4;
    background: #fff8f8;
}

.error-panel strong {
    color: #b42332;
    font-size: 16px;
}

.error-panel p {
    color: #714b54;
}

.footer-note {
    text-align: center;
    color: #9aa4b5;
    font-size: 11px;
    padding: 25px 0 0;
}

@media(max-width: 900px) {
    .metrics-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .agent-list {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .hero-banner {
        padding: 34px 25px;
    }

    .weather-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media(max-width: 560px) {
    #travel-shell {
        padding: 4px 0 24px;
    }

    .hero-banner {
        border-radius: 20px;
        padding: 28px 20px;
    }

    .search-panel {
        padding: 16px;
        margin-top: -16px;
    }

    .metrics-grid,
    .agent-list {
        grid-template-columns: 1fr 1fr;
    }

    .metric {
        padding: 14px 11px;
    }

    .metric strong {
        font-size: 16px;
    }

    .nav-note {
        display: none;
    }
}
"""


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    title="Voyage AI | Agentic Travel Planner",
    theme=gr.themes.Base(
        primary_hue="violet",
        neutral_hue="slate",
    ),
    css=CSS,
) as app:

    with gr.Column(elem_id="travel-shell"):

        gr.HTML("""
        <div class="top-nav">
            <div class="brand">✈ Voyage<span>AI</span></div>

            <div class="nav-note">
                INTELLIGENT TRIP PLANNING · MULTI-AGENT AI
            </div>
        </div>

        <section class="hero-banner">
            <div class="hero-kicker">
                Your next journey, thoughtfully planned
            </div>

            <h1>
                Travel better.<br>
                Discover more.
            </h1>

            <p>
                Build a personalized itinerary with specialized AI
                agents, destination discovery, weather insights
                and a practical trip budget.
            </p>
        </section>
        """)

        with gr.Group(elem_classes=["search-panel"]):

            gr.HTML("""
            <div class="section-label">
                Plan your journey
            </div>

            <div class="section-sub">
                Enter your route and trip duration to get a
                tailored travel plan.
            </div>
            """)

            with gr.Row():
                origin = gr.Textbox(
                    label="Starting city",
                    placeholder="e.g. Hyderabad",
                    scale=2,
                )

                destination = gr.Textbox(
                    label="Destination",
                    placeholder="e.g. Goa",
                    scale=2,
                )

                days = gr.Number(
                    label="Days",
                    value=3,
                    precision=0,
                    minimum=1,
                    maximum=30,
                    scale=1,
                )

            plan_button = gr.Button(
                "✦  Generate my travel plan",
                variant="primary",
                size="lg",
                elem_id="generate-btn",
            )

        agent_status = gr.HTML()

        with gr.Column(visible=False) as results_section:

            gr.HTML("""
            <div class="results-title">
                Your trip at a glance
            </div>
            """)

            summary_output = gr.HTML()

            with gr.Tabs():

                with gr.Tab("✈ Flights"):
                    flights_output = gr.Markdown()

                with gr.Tab("⌂ Hotels"):
                    hotels_output = gr.Markdown()

                with gr.Tab("📍 Attractions"):
                    activities_output = gr.Markdown()

                with gr.Tab("☼ Weather"):
                    weather_output = gr.Markdown()

                with gr.Tab("₹ Budget"):
                    budget_output = gr.Markdown()

                with gr.Tab("✧ AI itinerary"):
                    recommendation_output = gr.Markdown()

                with gr.Tab("⌖ Map"):
                    map_output = gr.HTML()

        gr.HTML("""
        <div class="footer-note">
            Voyage AI · Powered by your existing travel agents
            and connected APIs.
            <br>
            Flight and hotel data are currently simulated;
            weather and attractions depend on API availability.
        </div>
        """)

    plan_button.click(
        fn=plan_trip,
        inputs=[
            origin,
            destination,
            days,
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
            map_output,
        ],
    )


if __name__ == "__main__":
    app.queue().launch()
