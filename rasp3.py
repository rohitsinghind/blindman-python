import sys
import time
import requests
import pyttsx3
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from io import BytesIO

# --- Configurations ---
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
API_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

LED_PIN = 17
TOUCH_PIN = 12

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TOUCH_PIN, GPIO.IN)

# --- Text-to-Speech Setup ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
selected_voice = voices[10] if len(voices) > 10 else voices[0]
engine.setProperty('voice', selected_voice.id)
engine.setProperty('rate', 100)

# --- Camera Setup ---
camera = Picamera2()

# --- Speak Helper ---
def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- API Query Helper ---
def get_caption_from_bytes(image_bytes):
    try:
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "No caption available") if result else "No result"
    except Exception as e:
        print("Error querying model:", e)
        return None

# --- Initialization Feedback ---
GPIO.output(LED_PIN, GPIO.HIGH)
print("Model loaded")
speak("Model Loaded")

# --- Main Loop ---
try:
    while True:
        if GPIO.input(TOUCH_PIN) == GPIO.HIGH:
            print("Touch sensor is touched!")
            GPIO.output(LED_PIN, GPIO.LOW)

            camera.start()
            stream = BytesIO()
            camera.capture_file(stream, format="jpeg")
            camera.stop()
            image_bytes = stream.getvalue()
            stream.close()

            print("Image captured")
            speak("Image captured")

            caption = get_caption_from_bytes(image_bytes)
            if caption:
                print("Caption:", caption)
                speak(caption)
            else:
                print("Failed to get caption.")
                speak("Failed to get caption.")

            GPIO.output(LED_PIN, GPIO.HIGH)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
