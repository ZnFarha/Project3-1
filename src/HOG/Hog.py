import Process

import numpy as np
import pandas as pd
from skimage.transform import resize
from skimage.feature import hog

stats = False


def get_windows(img, size, step, ratio=1.0):
    og_step = step
    step = int(step * ratio)
    strides = list(2 * img.strides)
    strides[0] = strides[0] * step
    strides[1] = strides[1] * step

    shape = (int((img.shape[0] - size) / step) + 1, int((img.shape[1] - size) / step) + 1, size, size)
    patches = np.lib.stride_tricks.as_strided(img, shape=shape, strides=strides)
    patches = patches.reshape(-1, size, size)

    windows_y = shape[0]
    windows_x = shape[1]
    y_arr = np.tile(np.arange(windows_x), windows_y) * og_step
    x_arr = np.repeat(np.arange(windows_y), windows_x) * og_step
    w = pd.DataFrame({'x': x_arr, 'y': y_arr, 'window_size': [size] * len(patches), 'window': list(patches)})
    return w


def get_resized_windows(img, base_size=128, step=32, sizes=[64, 96, 128, 196]):
    def roundUp8(x):
        x = int(x)
        return (x + 7) & (-8)

    windows = pd.DataFrame(columns=['x', 'y', 'window_size', 'window', 'real_size'])
    for s in sizes:
        ratio = (base_size / s)
        resize_size = (roundUp8(img.shape[0] * ratio), roundUp8(img.shape[1] * ratio))
        if s > min(resize_size[0], resize_size[1]):
            continue
        resized = (resize(img, resize_size) * 255).astype(np.uint8)
        w = get_windows(resized, size=base_size, step=step, ratio=ratio)
        w['real_size'] = s
        windows = windows.append(w)
    return windows


def prune_windows(windows, threshhold=0.9):
    def zero_perc(arr):
        return (np.count_nonzero(arr == 0)) / (arr.shape[0] * arr.shape[1])

    windows['zero_perc'] = windows['window'].apply(zero_perc)
    windows = windows.drop(windows[windows['zero_perc'] > threshhold].index)
    return windows


def compute_hog(windows, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)):
    w = windows['window']
    windows['hog'] = hog(w, orientations=orientations, pixels_per_cell=pixels_per_cell, cells_per_block=cells_per_block)
    windows['hog'] = np.reshape(windows['hog'], (1, -1))
    return windows


def compute_hog1(df, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)):
    import cv2
    cell_size = pixels_per_cell  # h x w in pixels
    block_size = cells_per_block  # h x w in cells
    nbins = orientations  # number of orientation bins
    img = df['window']
    # winSize is the size of the image cropped to an multiple of the cell size
    # cell_size is the size of the cells of the img patch over which to calculate the histograms
    # block_size is the number of cells which fit in the patch
    hog_desc = cv2.HOGDescriptor(_winSize=(img.shape[1] // cell_size[1] * cell_size[1],
                                           img.shape[0] // cell_size[0] * cell_size[0]),
                                 _blockSize=(block_size[1] * cell_size[1],
                                             block_size[0] * cell_size[0]),
                                 _blockStride=(cell_size[1], cell_size[0]),
                                 _cellSize=(cell_size[1], cell_size[0]),
                                 _nbins=nbins)
    df['hog'] = hog_desc.compute(img)
    df['hog'] = np.reshape(df['hog'], (1, -1))
    return df
