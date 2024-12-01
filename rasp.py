import pyttsx3
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.HIGH)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
picam2 = Picamera2()

TOUCH_PIN = 12
GPIO.setup(TOUCH_PIN, GPIO.IN)
prev_touch_state = GPIO.LOW

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)
engine.setProperty('rate', 100)

GPIO.output(LED_PIN, GPIO.LOW)
print("model loaded")
engine.say("Model Loaded")
engine.runAndWait()

try:
    while True:
        touch_state = GPIO.input(TOUCH_PIN)

        if touch_state != prev_touch_state:
            if touch_state == GPIO.HIGH:
                print("Touch sensor is touched!")
                picam2.start()
                picam2.capture_file("image.jpg")
                print("image captured")
                GPIO.output(LED_PIN, GPIO.HIGH)
                engine.say("Image captured")
                engine.runAndWait()

                raw_image = Image.open("image.jpg").convert('RGB')
                inputs = processor(raw_image, return_tensors="pt")
                out = model.generate(**inputs, max_length=150)
                result = processor.decode(out[0], skip_special_tokens=True)
                print(result)

                engine.say(result)
                engine.runAndWait()
                GPIO.output(LED_PIN, GPIO.LOW)

        prev_touch_state = touch_state
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
