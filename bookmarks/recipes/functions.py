from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import textwrap


def resize(image):
	#Defining the target dimensions
	output_left = 100
	output_top = 180
	output_right = 550
	output_bottom = 510

	#Calculating the target lengths
	output_x = output_right - output_left
	output_y = output_bottom - output_top


	image_x = image.size[0]
	image_y = image.size[1]

	k = output_y/image_y

	new_x = image_x*k

	new_size = (int(new_x), output_y)
	image_rescaled = image.resize(new_size, Image.LANCZOS)

	if output_x < image_rescaled.size[0]:
		left = image_rescaled.size[0]//2 - (image_rescaled.size[0]-output_x)//2
		top = 0
		right = image_rescaled.size[0]//2 + (image_rescaled.size[0]-output_x)//2
		bottom = output_y

		image_rescaled = image_rescaled.crop((left, top, right, bottom))

	return image_rescaled

def merge_images(template, image, text):
	size = (450, 330)

	copied_image = template.copy()
	copied_image.paste(image, ((copied_image.size[0] - image.size[0])//2 - 10, 150))

	draw = ImageDraw.Draw(copied_image)
	font = ImageFont.truetype("./media/cookbook/font/PAPYRUS.TTF", 80)

	lines = textwrap.wrap(text, width=10)
	y_text = 600
	w = copied_image.size[0]
	for line in lines:
		width, height = font.getsize(line)
		draw.text(((w - width) / 2, y_text), line, (0,0,0), font=font)
		y_text += height

	return copied_image

def prepare_cookbook_image(template, image, text):
	return merge_images(template, resize(image), text)





