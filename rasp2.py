import sys

print(sys.version)
import pyttsx3
import RPi.GPIO as GPIO
import time
import requests
from picamera2 import Picamera2

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": f"Bearer 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"}
LED_PIN = 17
TOUCH_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TOUCH_PIN, GPIO.IN)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)
engine.setProperty('rate', 100)

camera = Picamera2()


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    try:
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status()  # Raise error if response status is not OK (200)
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


GPIO.output(LED_PIN, GPIO.HIGH)
print("model loaded")
engine.say("Model Loaded")
engine.runAndWait()

try:
    while True:
        touch_state = GPIO.input(TOUCH_PIN)

        if touch_state == GPIO.HIGH:
            print("Touch sensor is touched!")
            GPIO.output(LED_PIN, GPIO.LOW)
            camera.start()
            camera.capture_file("image.jpg")
            print("Image captured")
            engine.say("Image captured")
            engine.runAndWait()

            result = query("image.jpg")
            print(result)
            if result:
                caption = result[0].get("generated_text", "No caption available")
                print("Caption:", caption)
                engine.say(caption)
                engine.runAndWait()
            else:
                print("Failed to get caption.")
                engine.say("Failed to get caption.")
                engine.runAndWait()

            GPIO.output(LED_PIN, GPIO.HIGH)

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
