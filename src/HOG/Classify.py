import Process
import Hog

import numpy as np
import pickle

stats = False


def load_svm(folder, feature=['head', 'spine', 'leg', 'arm', 'foot', 'hand']):
    # Load from file
    if isinstance(feature, list):
        svms = {}
        for f in feature:
            svms[f] = load_svm(folder, f)
        return svms

    pkl_filename = folder + '/' + feature + '.pkl'
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)

        if stats: print('Loaded SVM ' + pkl_filename)

        return pickle_model


def analyse_hog(row, svms):
    for feature in svms:
        p = svms[feature].predict_proba(np.reshape(row['hog'], (1, -1)))
        prob = p[0, svms[feature].classes_.tolist().index(feature)]
        row[feature] = prob
    return row


def analyse_svm_results(df, threshold):
    df['highest'] = df.drop(['x', 'y', 'hog', 'window_size', 'window'], axis=1).idxmax(axis=1)
    df['highest_pred'] = df.drop(['x', 'y', 'hog', 'window_size', 'window'], axis=1).max(axis=1)
    df['best_none'] = 1 - df.drop(['x', 'y', 'hog', 'window_size', 'window'], axis=1).min(axis=1)
    df = df[df['highest_pred'] >= threshold]

    if stats: print('{} features found?'.format(len(df)))

    return df


def draw_boxes(image, features_found):
    from numpy import interp
    import cv2

    img_rect = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    for idx, row in features_found.iterrows():
        start = (row['y'], row['x'])
        end = (row['y'] + row['window_size'][1], row['x'] + row['window_size'][0])
        color = (
            255 - 255 * interp(row['highest_pred'],
                               [0.95, 1],
                               [0, 1]),
            255 - 255 * (1 - interp(row['highest_pred'],
                                    [0.95, 1],
                                    [0, 1])), 0)
        img_rect = cv2.rectangle(img_rect, start, end, color, 2)
        img_rect = cv2.putText(img_rect, row['highest'], (row['y'], row['x'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                               color,
                               2)
    return img_rect


def analyse_image(image, svm_models, crop_thresh=0.2, blur_size=10, bright_strength=2, sharp_strength=2,
                  square_step=True, windows=[(64, 64), (128, 128)], window_stride=16, pred_threshold=0.9):
    # 1. Process image and extract HOGs
    processed = Process.process(image, crop_thresh, blur_size, bright_strength, sharp_strength,
                                square_step)
    x = processed[0][0]
    y = processed[0][1]

    hogs = Hog.hog(processed, windows=windows, window_stride=window_stride)
    hogs['x'] = hogs['x'] + y
    hogs['y'] = hogs['y'] + x

    if stats: print('{} windows to analyse.'.format(len(hogs)))

    # 2. Get Probabilities for each SVM
    pred = hogs.apply(lambda row: analyse_hog(row, svms=svm_models), axis=1)
    result = analyse_svm_results(pred, pred_threshold)

    if stats:
        print(result)
    # 3. Draw Rectangles
    analysed_image = draw_boxes(image, result)

    return analysed_image, result, pred


if __name__ == "__main__":
    import os, random, cv2
    from matplotlib import pyplot as plt

    os.chdir('..')
    os.chdir('../resources')
    pwd = os.getcwd()

    # 1. Load image(s)
    img_name = random.choice(os.listdir(pwd + '/images/1'))
    print(img_name)
    img = cv2.imread(pwd + '/images/1/' + img_name, 0)

    # 2. Load models
    classifiers = load_svm(pwd + '/SVM')
    print(classifiers)

    # 3. Analyse image
    wanted_classifiers = ['head', 'spine']  # The keys you want
    wanted_classifiers = dict((k, classifiers[k]) for k in wanted_classifiers if k in classifiers)
    feat_image, _, _ = analyse_image(img, wanted_classifiers, crop_thresh=0.2, blur_size=10, bright_strength=2,
                                     sharp_strength=2,
                                     square_step=True, windows=[(32, 32), (64, 64), (96, 96), (128, 128)],
                                     window_stride=32)

    ####################
    #####
    #
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    plt.imshow(np.concatenate((img, feat_image), axis=1))
    #
    ####
    ###################
