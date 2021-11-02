# Add folder of non-cropped images to resources/images
# Add CSV to resources/images
# Change 'csv_to_read' and 'image_folder' variables to correct values

# CSV headers: type, from_y, from_x, section_height, section_width, imageName, image_height, image_width
# TODO maybe normalize size of cropped images in some way (ex only multiples of 8)
import pathlib
import os.path
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import filters
from csv import reader


def save_img(row, subsection):
    directory = os.path.join(resources_path, 'features', row[0])
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    plt.imsave(directory + "/" + row[5], subsection)


def extract_subsection(row, img):
    from_x = int(row[1])
    from_y = int(row[2])
    to_x = from_x + int(row[3])
    to_y = from_y + int(row[4])
    return img[from_y:to_y, from_x:to_x]


def loop_through_csv(path, show=True, wait=True, save=False):
    with open(path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            img = mpimg.imread(os.path.join(resources_path, 'images', image_folder, row[5]))
            subsection = extract_subsection(row, img)
            if subsection.shape[0] == 0 or subsection.shape[1] == 0:
                continue
            if show:
                print(row)
                plt.imshow(subsection)
                plt.title(row[0])
                plt.show(block=False)
                plt.pause(0.001)
                if wait:
                    input("Press Enter to continue...")
                plt.close()
            if save:
                save_img(row, subsection)


def median_filter(img):
    return filters.median(img)


# edge detection filter, worked well when i attempted
def sobel_filter(img):
    return filters.sobel(img)


# gaussian filter takes the average of surrounding pixel values
def gaussian_filter(img):
    return filters.gaussian(img)


resources_path = os.path.join(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0], 'resources')
csv_to_read = 'emery-labels-1.csv'
image_folder = '1'
loop_through_csv(os.path.join(resources_path, 'images', csv_to_read), True, True, True)