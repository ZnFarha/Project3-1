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

    from_x, to_x = temp.columns[0], temp.columns[-1]
    from_y, to_y = temp.index[0], temp.index[-1]
    to_x = to_x + 8 - (to_x - from_x) % 8
    to_y = to_y + 8 - (to_y - from_y) % 8

    cropped = pd.DataFrame(image)
    cropped = cropped.iloc[from_y:to_y, from_x:to_x]

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
def process(image, crop_thresh=0.2, blur_size=10, bright_strength=2, sharp_strength=1, square_step=True):
    cr, from_x, from_y = crop(image, crop_thresh)
    bl = blur(cr, blur_size)
    bi = brighten(bl, bright_strength)
    sh = sharpen(bi, sharp_strength)
    if square_step:
        ss = square(sh)
        ss[0][0] = from_x
        ss[0][1] = from_y
        return ss
    else:
        sh[0][0] = from_x
        sh[0][1] = from_y
        return sh


if __name__ == "__main__":
    import os, random, cv2
    import matplotlib.pyplot as plt

    os.chdir('..')
    os.chdir('../resources')
    pwd = os.getcwd()

    img_name = random.choice(os.listdir(pwd + '/images/1'))
    print(img_name)
    img = cv2.imread(pwd + '/images/1/' + img_name, 0)

    ####################
    #####
    #
    processed = process(img, crop_thresh=0.2, blur_size=10, bright_strength=2, sharp_strength=2)
    x = processed[0][0]
    y = processed[0][1]
    print('Amount cropped on left/top: ',x,y)
    #
    ####
    ###################

    diff1, diff2 = img.shape[0] - processed.shape[0], img.shape[1] - processed.shape[1]
    d1 = int(diff1 / 2)
    d2 = d1
    d3 = int(diff2 / 2)
    d4 = d3
    if diff1 % 2 != 0:
        d2 += 1
    if diff2 % 2 != 0:
        d4 += 1
    processed = np.pad(processed, ((d1, d2), (d3, d4)), 'constant', constant_values=255)
    plt.imshow(np.concatenate((img, processed), axis=1), cmap='gray')
