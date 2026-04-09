---
title: Daytrip Agent
emoji: 🚀
colorFrom: gray
colorTo: gray
sdk: gradio
sdk_version: 6.11.0
app_file: app/main.py
pinned: false
license: mit
short_description: A day trip planner agent based on Google Gemini (google-adk)
---

# Travel Agent 📍

Gemini-based agent with tool-calling capabilities to fetch real-time environmental data and recommend the best activities based on current conditions.

## Overview ⛰

The agent acts as your guide and will recommend how to proceed with your plan according to real-time data, with guessing anything by using tools based on external APIs.

This project was built to learn and showcase agent building using Google's framework 🛠

## Stack 🧰

* **Core Agent Model:** Google `gemini-3.1-flash-lite-preview`
* **UI Framework:** Gradio
* **Package Management:** `uv`
* **External APIs:**
  * [Open-Meteo](https://open-meteo.com/) (Geocoding & Air Quality)
  * [OpenWeatherMap](https://openweathermap.org/) (Weather Forecast) (previously [wttr.in](https://wttr.in))
  