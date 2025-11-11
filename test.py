import requests
import smtplib
import schedule
import time
import csv
from datetime import datetime
from email.message import EmailMessage

# -----------------------------
# CONFIGURATION
# -----------------------------
CITY = "Hyderabad"
API_KEY = "bd1c1858490583497a2a9d9f0e4f7808"
 # Paste your OpenWeatherMap API key here
SENDER_EMAIL = "sreeja18138@gmail.com"
SENDER_PASS = "qrosczdlweraqkxo"  # Use Gmail App Password
RECEIVER_EMAIL = "sreeja18138@gmail.com"
     # send to self (most reliable)
CSV_FILE = "weather_log.csv"

# Set to True to ALWAYS send a daily email (useful while testing scheduling)
ALWAYS_SEND_DAILY = False

# Weather conditions that should trigger an umbrella reminder
UMBRELLA_CONDITIONS = {"rain", "clouds", "drizzle", "thunderstorm", "haze", "mist", "fog", "smoke"}


# -----------------------------
# FETCH WEATHER DATA
# -----------------------------
def get_weather():
    """Fetch current weather data from OpenWeatherMap API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        print(f"🔎 Calling API: {url}")
        response = requests.get(url, timeout=15)
        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text}

        if response.status_code != 200:
            print("❌ Error fetching weather data:", data)
            return None, None

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["main"]  # e.g., 'Clouds', 'Rain', 'Haze'
        return temperature, condition

    except Exception as e:
        print(f"⚠️ Network or API error: {e}")
        return None, None


# -----------------------------
# SEND EMAIL
# -----------------------------
def send_email(subject, body):
    """Send an email using Gmail SMTP."""
    try:
        print("📧 Preparing to send email...")
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg.set_content(body)

        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASS)
        smtp.send_message(msg)
        smtp.quit()
        print("✅ Email Sent Successfully!")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


# -----------------------------
# LOG TO CSV
# -----------------------------
def log_weather(temp, condition, email_sent):
    """Log daily weather data to CSV for record-keeping."""
    try:
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # header if new file
                writer.writerow(["Date", "City", "Temperature (°C)", "Condition", "Email Sent"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                CITY,
                temp,
                condition,
                email_sent
            ])
        print("🗂 Weather data logged successfully!")
    except Exception as e:
        print(f"⚠️ Could not log data: {e}")


# -----------------------------
# UMBRELLA REMINDER
# -----------------------------
def umbrella_reminder():
    """Check weather and send umbrella reminder if needed."""
    print("\n⏰ Running umbrella_reminder()")
    temp, condition = get_weather()
    if temp is None:
        print("⛔ Skipping: weather fetch failed.")
        return

    cond_lower = (condition or "").lower()
    print(f"🌡 Weather in {CITY}: {condition}, {temp}°C")

    email_sent = False
    should_send = ALWAYS_SEND_DAILY or (cond_lower in UMBRELLA_CONDITIONS)

    if should_send:
        subject = "☂ Umbrella Reminder!" if cond_lower in UMBRELLA_CONDITIONS else "🌤 Daily Weather Update"
        body = (
            f"Hey Sreeja,\n\n"
            f"Today's weather in {CITY}: {condition} with {temp}°C.\n"
            + ("Take an umbrella! ☔\n\n" if cond_lower in UMBRELLA_CONDITIONS else "No umbrella needed today. ☀️\n\n")
            + "— Your Python Weather Bot"
        )
        email_sent = send_email(subject, body)
    else:
        print("☀️ No umbrella needed today! (Email not sent)")
    log_weather(temp, condition, email_sent)


# -----------------------------
# RUN + SCHEDULER
# -----------------------------
# Run once immediately (for testing)
umbrella_reminder()

# 🔔 Schedule daily — set a time you like (24-hr format). Example: "20:12" for 8:12 PM IST.
schedule.every().day.at("07:00").do(umbrella_reminder)

print("\n🌤 Weather Reminder Bot is running... keep this terminal open.\n")

while True:
    schedule.run_pending()
    time.sleep(60)
