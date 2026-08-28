# ✈️ Agentic AI Travel Planner

An intelligent **multi-agent travel planning system** that helps users plan trips using specialized agents, external APIs, and **Google Gemini** for personalized travel recommendations.

---

## 🚀 Features

- 🌍 Dynamic travel planning for Indian destinations
- 📍 Destination geocoding using Geoapify API
- 🏛️ Real tourist attraction recommendations using OpenTripMap API
- 🌦️ Real-time weather information using Open-Meteo
- ✈️ Simulated flight options
- 🏨 Simulated hotel recommendations
- 💰 Automatic trip budget calculation
- 🤖 AI-generated personalized travel itinerary using Google Gemini
- 🧠 Multi-agent architecture
- 🗺️ Interactive destination map
- 📊 Gradio dashboard
- ✅ Agent execution status visualization

---

## 🏗️ Architecture

```text
User
  ↓
Gradio User Interface
  ↓
Travel Workflow
  ↓
┌─────────────────────────────────┐
│       Specialized Agents        │
├─────────────────────────────────┤
│ Transport Agent                 │
│ Accommodation Agent             │
│ Activity Agent                  │
│ Weather Agent                   │
│ Budget Agent                    │
│ Recommendation Agent            │
└─────────────────────────────────┘
  ↓
Tools
  ↓
External APIs / Simulated Data
  ↓
Complete AI Travel Plan
```

---

## 🤖 Agents

| Agent                   | Responsibility                                         |
| ----------------------- | ------------------------------------------------------ |
| ✈️ Transport Agent      | Provides simulated flight options                      |
| 🏨 Accommodation Agent  | Provides simulated hotel options                       |
| 📍 Activity Agent       | Finds real tourist attractions                         |
| 🌦️ Weather Agent       | Retrieves weather information                          |
| 💰 Budget Agent         | Calculates estimated trip expenses                     |
| 🤖 Recommendation Agent | Generates a personalized travel itinerary using Gemini |

---

## 🔌 API Integrations

🤖 Google Gemini API

Generates personalized travel recommendations and a day-wise itinerary.

📍 Geoapify API

Converts the user-entered destination into geographical coordinates.

```bash
Destination
    ↓
Latitude + Longitude
```

🏛️ OpenTripMap API

Uses destination coordinates to find real tourist attractions and places to visit.

```bash
Latitude + Longitude
        ↓
OpenTripMap API
        ↓
Tourist Attractions
```

🌦️ Open-Meteo API

Retrieves weather information based on destination coordinates.

---

## 🔄 Application Workflow

```text
User enters trip details
        ↓
Gradio UI
        ↓
TravelWorkflow
        ↓
Geoapify API → Destination Coordinates
        ↓
OpenTripMap API → Tourist Attractions
        ↓
Open-Meteo API → Weather Information
        ↓
Transport Agent → Simulated Flights
        ↓
Accommodation Agent → Simulated Hotels
        ↓
Budget Agent → Estimated Trip Cost
        ↓
Gemini Recommendation Agent
        ↓
Personalized AI Travel Itinerary
```

---

## 🖥️ User Interface

The application provides an interactive Gradio dashboard where users can enter:

Origin

Destination

Number of travel days

The application displays:

✈️ Flight options

🏨 Hotel options

📍 Tourist attractions

🌦️ Weather information

💰 Estimated trip budget

🤖 AI-generated travel itinerary

🗺️ Destination map

📊 Agent execution status

## 🔑 Environment Variables

Create a .env file in the root directory:

```bash
GEMINI_API_KEY=your_gemini_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key
OPENTRIPMAP_API_KEY=your_opentripmap_api_key
```

## ▶️ Run the Application

```bash
python ui/gradio_app.py
```

## 🛠️ Technology Stack

Python

Gradio

Google Gemini

Geoapify API

OpenTripMap API

Open-Meteo API

Multi-Agent Architecture

OpenStreetMap

## 🔮 Future Improvements

Integration with real flight APIs

Integration with real hotel APIs

User authentication

Save previous trips

User travel preferences

Database integration

Cloud deployment

Real-time pricing

Advanced agent orchestration
