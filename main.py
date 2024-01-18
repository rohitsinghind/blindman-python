import cv2 as cv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gtts
import os
import keyboard

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def capture_image():
    cam_port = 0
    cam = cv.VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        # cv.imshow("Captured Image", image)
        # cv.imwrite("Image.png", image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        return image
    else:
        print("No image detected. Please try again.")
        return None



def generate_caption():
    # Capture the image
    captured_image = capture_image()

    raw_image = Image.fromarray(cv.cvtColor(captured_image, cv.COLOR_BGR2RGB))



    # raw_image = Image.open("Image.png").convert('RGB')

    inputs = processor(raw_image, return_tensors="pt")

    # Adjust max_length as needed
    out = model.generate(**inputs, max_length=150)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def text_to_speech(text):
    print(text)
    t1 = gtts.gTTS(text)
    t1.save("welcome.mp3")
    os.system("welcome.mp3")

while True:
    print("press any key")
    keyboard.wait("a")
    text_to_speech(generate_caption())