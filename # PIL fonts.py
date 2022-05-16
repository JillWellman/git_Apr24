# PIL fonts
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

font = ImageFont.load_default().font
font = ImageFont.truetype("Verdana.ttf",36)

img=Image.new("RGBA", (500,250),(255,255,255))
draw1 = ImageDraw.Draw(img)
draw1.text((0, 0),"This is a test",(0,0,0),font=font)
draw1 = ImageDraw.Draw(img)
img.save("a_test.png")
img.show()


