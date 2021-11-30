import Process

import numpy as np
import pandas as pd
from skimage.transform import resize
from skimage.feature import hog as h

stats = False


def get_window_coords(x, y, size):
    return np.ix_(np.arange(x, x + size[0]), np.arange(y, y + size[1]))


def sliding_window(image, window_size=(64, 64), win_stride=1):
    windows = []
    x_arr = []
    y_arr = []
    for x in range(0, image.shape[0] - window_size[0] + 1, win_stride):
        for y in range(0, image.shape[1] - window_size[1] + 1, win_stride):
            window = image[get_window_coords(x, y, window_size)]
            x_arr.append(x)
            y_arr.append(y)
            windows.append(window)

    windows = pd.DataFrame({'x': x_arr, 'y': y_arr, 'window_size': [window_size] * len(y_arr), 'window': windows})

    if stats: print('{} {} sized windows were made.'.format(len(windows), window_size))

    return windows


def compute_hog(window, ignore=True):
    if isinstance(window, pd.DataFrame):
        hogs = window['window'].apply(compute_hog, ignore=False)

        if stats: print('{} HOG features per window'.format(hogs.iloc[0].shape))

        return hogs

    resized = resize(window, (128, 128))
    fd = h(resized, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(4, 4)) #,block_norm='L2')

    if stats and ignore: print('{} HOG features per window'.format(fd.shape))

    return np.reshape(fd, (1, -1))


def hog(image, windows=[(64, 64), (128, 128)], window_stride=16):
    windows_df = pd.DataFrame()
    for window in windows:
        windows_df = windows_df.append(sliding_window(image, window, window_stride)).reset_index(drop=True)

    windows_df['hog'] = compute_hog(windows_df)
    return windows_df


if __name__ == "__main__":
    import os, random, cv2

    os.chdir('..')
    os.chdir('../resources')
    pwd = os.getcwd()

    img_name = random.choice(os.listdir(pwd + '/images/1'))
    print(img_name)
    img = cv2.imread(pwd + '/images/1/' + img_name, 0)

    ####################
    #####
    #
    processed = Process.process(img, crop_thresh=0.2, blur_size=10, bright_strength=2, sharp_strength=2)
    wind = hog(processed, window_stride=16)
    #
    ####
    ###################

    print(wind)
