import cv2
import numpy as np


def img_to_bytes(img):
    img_encode = cv2.imencode('.png', img)[1]
    data = img_encode.tobytes()

    return data

def grayscale(img):
    h, w = img.shape[:2]
    out = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            out[i, j] = img[i,j,:].mean()
    return out

def binarize(img, threshold=127):
    h, w = img.shape[:2]
    out = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            out[i, j] = 0 if img[i,j,:].mean() < threshold else 255
    return out

def niblack(img, n):
    '''binaryzacja niblacka
    n = kernel size defined by the number of neighbours
    1 -> 3x3, 2 -> 5x5'''
    gray = grayscale(img)
    h, w = gray.shape[:2]
    out = np.zeros_like(gray)

    for i in range(n, h-n):
        for j in range(n, w-n):
            roi = gray[i-n:i+n+1, j-n:j+n+1]
            T = roi.mean() - -0.2 * roi.std()
            out[i, j] = 0 if gray[i, j] < T else 255
    
    return out