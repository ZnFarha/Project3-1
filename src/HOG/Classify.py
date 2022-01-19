import glob
import os

import pandas as pd

import Process
import Hog

import numpy as np
import pickle

stats = False


def load_svm(folder, feature=None):
    # Load from file
    if feature is None:
        folder_pwd = os.getcwd()
        os.chdir(folder)
        feature = glob.glob('*.{}'.format('pkl'))
        os.chdir(folder_pwd)
        return load_svm(folder, feature)
    if isinstance(feature, list):
        svms = {}
        for f in feature:
            f = f.replace('.pkl', '')
            svms[f] = load_svm(folder, f)
        return svms

    pkl_filename = folder + '/' + feature
    if not pkl_filename.endswith('.pkl'):
        pkl_filename = pkl_filename + '.pkl'
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


def draw_boxes(image, features_found):
    from numpy import interp
    import cv2

    img_rect = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    for idx, row in features_found.iterrows():
        start = (row['y'], row['x'])
        end = (row['y'] + row['real_size'], row['x'] + row['real_size'])
        color = (
            255 - 255 * interp(row['prediction_val'],
                               [0.7, 1],
                               [0, 1]),
            255 - 255 * (1 - interp(row['prediction_val'],
                                    [0.7, 1],
                                    [0, 1])), 0)
        img_rect = cv2.rectangle(img_rect, start, end, color, 2)
        img_rect = cv2.putText(img_rect, row['feature'] + ' ' + str(row['prediction_val']), (row['y'], row['x'] - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                               color,
                               2)
    return img_rect


def analyse_image(image, svm_models=None, crop_thresh=0.2, blur_size=10, bright_strength=1, sharp_strength=1,
                  square_step=True, hog_func=Hog.compute_hog, base_size=128, step=32, sizes=[32, 64, 96, 128, 160, 196, 224],
                  orientations=9,
                  pixels_per_cell=(16, 16),
                  cells_per_block=(2, 2), pred_threshold=0.9, prune=False):
    if svm_models is None:
        import os
        cwd = os.getcwd()
        resources_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(resources_path)
        os.chdir('../../resources/svm')
        resources_path = os.getcwd()
        os.chdir(cwd)
        pixels_per_cell = (16, 16)
        cells_per_block = (4, 4)
        hog_func = Hog.compute_hog1
        base_size = 128
        svm_models = load_svm(resources_path)

    # I. Pre-process
    processed, x, y = Process.process(image, crop_thresh, blur_size, bright_strength, sharp_strength,
                                square_step)
    # II. Sliding window
    windows = Hog.get_resized_windows(processed, base_size=base_size, step=step, sizes=sizes).reset_index(drop=True)

    if prune:
        windows = Hog.prune_windows(windows)

    # III. HOGs
    windows['hog'] = 0
    hogs = windows.apply(hog_func, orientations=orientations, pixels_per_cell=pixels_per_cell,
                         cells_per_block=cells_per_block, axis=1)

    hogs['x'] = hogs['x'] + x
    hogs['y'] = hogs['y'] + y
    if stats: print('{} windows to analyse, {} features.'.format(len(hogs), hogs.iloc[0]['hog'].shape))

    # IV. Classification
    svms = svm_models.copy()
    master_svm = None
    for clf in svms:
        if len(svms[clf].classes_) > 2:
            master_svm = svms[clf]
            del svms[clf]
            break

    # 1. Classify by master SVM
    def classification(row):
        for f in list(svms.keys())+['none']:
            if f == 'none':
                prob = 0
                for key in svms.keys():
                    p = svms[key].predict_proba(row['hog'])
                    prob += p[0, svms[key].classes_.tolist().index(f)]
                prob = prob/len(svms)
            else:
                p = svms[f].predict_proba(row['hog'])
                prob = p[0, svms[f].classes_.tolist().index(f)]
            row[f] = round(prob, 4)
        return row

    hogs[master_svm.classes_.tolist()] = hogs.reindex(columns=master_svm.classes_.tolist()).fillna(0)
    pred = hogs.apply(classification, axis=1)
    pred['feature'] = pred[master_svm.classes_.tolist()].idxmax(axis=1)
    pred['prediction_val'] = pred[master_svm.classes_.tolist()].max(axis=1)

    # 2. Prune of results

    # 2.a. Below Threshold

    pred = pred.drop(columns=['hog'])
    all_pred = pred

    pred = pred[pred['feature'] != 'none']

    # 2.c. One with most overlaps

    c = ['x', 'y', 'feature']
    idx = pred.reset_index().groupby(c).agg({'prediction_val': ['mean', 'count']})
    idx = idx[idx['prediction_val', 'count'] > 1]

    l = []
    temp = pred.set_index(c).sort_index()
    for i in idx.iterrows():
        t = temp.loc[i[0]]
        t = t.loc[t['real_size'].idxmin()]
        t[i[1].index.levels[1]] = i[1]
        t = t
        l.append(pd.DataFrame(t))

    auto_pass = pred[pred['prediction_val'] > pred_threshold].reset_index(drop=True).set_index(c)
    auto_pass['count'] = 1
    auto_pass['mean'] = auto_pass['prediction_val']
    l.append(auto_pass)
    pred = pd.concat(l).sort_values(['count', 'real_size'], ascending=[False, True])
    pred = pred[~pred.index.duplicated(keep='first')].reset_index()
    pred['strength'] = pred['mean'] + (1 - pred['mean']) * (pred['count'] / all_pred['real_size'].nunique())
    pred = pred.sort_values('strength', ascending=False).groupby('feature').head(1)

    # V. Draw Rectangles
    analysed_image = draw_boxes(image, pred)

    return analysed_image, pred, all_pred
