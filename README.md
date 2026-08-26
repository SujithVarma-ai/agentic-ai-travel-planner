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

---

🤖 Agents

| Agent                   | Responsibility                                         |
| ----------------------- | ------------------------------------------------------ |
| ✈️ Transport Agent      | Provides simulated flight options                      |
| 🏨 Accommodation Agent  | Provides simulated hotel options                       |
| 📍 Activity Agent       | Finds real tourist attractions                         |
| 🌦️ Weather Agent       | Retrieves weather information                          |
| 💰 Budget Agent         | Calculates estimated trip expenses                     |
| 🤖 Recommendation Agent | Generates a personalized travel itinerary using Gemini |

---

🔌 API Integrations

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
