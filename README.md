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
