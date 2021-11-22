import cv2
import os
from BasicFunctions import read_image, show_image, show_image_list
from skimage import filters


def get_image_paths(folder):
    images = []
    for filename in os.listdir(folder):
        images.append(folder+"/"+filename)
    return images


def median_filter(img):
    return filters.median(img)


# edge detection filter, worked well when i attempted
def sobel_filter(img):
    return filters.sobel(img)


# gaussian filter takes the average of surrounding pixel values
def gaussian_filter(img):
    return filters.gaussian(img)


def w(image_folder_path):
    images = get_image_paths(image_folder_path)
    for path in images:
        img = read_image(path)
        median = median_filter(img)
        sobel = sobel_filter(img)
        gaussian = gaussian_filter(img)
        show_image_list(list_images=[img, median, sobel, gaussian],
                        list_titles=['base', 'median', 'sobel', 'gaussian'],
                        list_cmaps=['gray', 'gray', 'gray', 'gray'],
                        grid=False,
                        figsize=(10, 10),
                        title_fontsize=10)


