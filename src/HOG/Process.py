import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
from scipy import ndimage

stats = False


# Step 1: crop out parts with low information (outer part of image)
def crop(image, thresh):
    temp = pd.DataFrame(image)
    temp = temp.replace([0, 255, 254], np.nan)
    temp = temp.dropna(thresh=temp.shape[0] * thresh, axis=1)
    temp = temp.dropna(thresh=temp.shape[1] * thresh, axis=0)

    if 0 in temp.shape:
        temp = pd.DataFrame(np.zeros((1, 1)))
    from_y, to_y = temp.columns[0], temp.columns[-1]
    from_x, to_x = temp.index[0], temp.index[-1]
    to_y = to_y + 8 - (to_y - from_y) % 8
    to_x = to_x + 8 - (to_x - from_x) % 8

    cropped = np.copy(image)
    cropped = cropped[from_x:to_x, from_y:to_y]

    if stats: print('Original shape {} \nNew Shape {}'.format(image.shape, cropped.shape))
    return cropped, from_x, from_y


# Step 2: Blur to reduce noise
def blur(image, size):
    return ndimage.median_filter(image, size=size)


# Step 3: Adjust brightness
def brighten(image, strength):
    temp = Image.fromarray(image)
    converter = ImageEnhance.Brightness(temp)
    return np.array(converter.enhance(strength))


# Step 4: Sharpen image (?)
def sharpen(image, strength):
    temp = Image.fromarray(image)
    converter = ImageEnhance.Sharpness(temp)
    return np.array(converter.enhance(strength))


# Step 5: Exaggerate differences by squaring pixels and bring back to range [0, 255]
def square(image):
    temp = image.astype(np.int32)
    temp = temp ** 2
    temp = np.interp(temp, [temp.min(), temp.max()], [0, 255])
    return temp.astype(np.uint8)


# All together:
def process(image, crop_thresh=0.2, blur_size=10, bright_strength=1, sharp_strength=1, square_step=True):
    cr, from_x, from_y = crop(image, crop_thresh)
    if cr.shape[0] == 0 or cr.shape[1] == 0:
        print('cropped whole image')
        return np.array([[0, 0]])
    bl = blur(cr, blur_size)
    bi = brighten(bl, bright_strength)
    sh = sharpen(bi, sharp_strength)
    if square_step:
        ss = square(sh)
        return ss, from_x, from_y
    return sh, from_x, from_y
