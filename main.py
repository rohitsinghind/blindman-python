import cv2 as cv
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def capture_image():
	cam_port = 0
	cam = cv.VideoCapture(cam_port)
	result, image = cam.read()
	if result:
		# cv.imshow("Image", image)
		cv.imwrite("Image.png", image)
		# cv.waitKey(0)
		# cv.destroyWindow("GeeksForGeeks")
	else:
		print("No image detected. Please! try again")


capture_image()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# conditional image captioning
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))