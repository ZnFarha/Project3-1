# TODO maybe normalize size of cropped images in some way (ex only multiples of 8)
import pathlib
import os.path
from csv import reader
from BasicFunctions import resources_path, save_image, read_image, show_image


def save_img(row, subsection):
    directory = os.path.join(os.path.normpath(resources_path + os.sep + os.pardir), 'features', row[0])
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    save_image(directory + "/" + row[5], subsection)


def extract_subsection(row, img):
    from_x = int(row[1])
    from_y = int(row[2])
    to_x = from_x + int(row[3])
    to_y = from_y + int(row[4])
    return img[from_y:to_y, from_x:to_x]


def crop_from_csv(csv_path, image_folder_path, show=True, wait=True, save=False):
    with open(csv_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            img = read_image(os.path.join(image_folder_path, row[5]))
            subsection = extract_subsection(row, img)
            if subsection.shape[0] == 0 or subsection.shape[1] == 0:
                continue
            if show:
                print(row)
                show_image(subsection, row[0], wait)
            if save:
                save_img(row, subsection)
