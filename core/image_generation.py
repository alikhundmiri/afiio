from django.core.files.storage import default_storage
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def generate_image():
	thumb_1 = Image.new('RGB', (180, 300))
	default_storage.save("testing_ono.jpg", thumb_1)



