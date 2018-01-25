import numpy as np
import pandas as pd
from PIL import Image, ImageFilter

try:
 	image = np.asarray(Image.open("Lenna.png").convert('LA'))
except:
	print("Unable to load image")

#temp = np.copy(image)

image_array = np.array(np.copy(image))

# the height of the printed part will be shortest in the bright spots and darkest in the tall spots.  This is the opposite of how the image is saved
# 	(the brightest spots will have higher values) so we reverse these values.  If spot [0,0] was 255, it is now 0, if it was 1, it is not 254, etc.
heights = (image_array[:,:,0].astype(np.int) - 255) * -1

print(heights)
print(heights.shape)
