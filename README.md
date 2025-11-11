# ☂ Umbrella Reminder Bot

### 🌤 Project Overview
This Python automation project fetches live weather data from the OpenWeatherMap API and sends an umbrella reminder email using Gmail SMTP if the forecast is cloudy or rainy. It also logs daily weather details into a CSV file for record-keeping.

### ⚙️ Features
- Fetches real-time weather data.
- Sends automated daily email reminders.
- Uses Gmail App Password for secure SMTP login.
- Logs temperature and condition to a CSV file.
- Runs daily at a specified time using the `schedule` library.

### 🧰 Tools & Libraries
- Python 3
- `requests` — for API calls
- `smtplib`, `email` — for email automation
- `schedule` — for daily task scheduling
- `csv` — for logging


