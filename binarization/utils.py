import cv2
import numpy as np


def img_to_bytes(img):
    '''
    img to bytes for viewing
    '''
    img_encode = cv2.imencode('.png', img)[1]
    data = img_encode.tobytes()
    return data


def grayscale(img):
    '''
    rgb2gray using simple mean
    '''
    h, w = img.shape[:2]
    out = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            out[i, j] = img[i,j,:].mean()
    
    return out


def binarize(img, threshold=127):
    '''
    binarization
    '''
    gray = grayscale(img)
    h, w = gray.shape[:2]
    out = np.zeros_like(gray)

    for i in range(h):
        for j in range(w):
            out[i, j] = 0 if gray[i,j] < threshold else 255
            
    return out


def niblack(img, n, k):
    '''binaryzacja niblacka
    n = kernel size defined by the number of neighbours
    1 -> 3x3, 2 -> 5x5'''
    n = int(n)
    h, w = img.shape[:2]
    # original grayscale
    gray_temp = grayscale(img)
    # grayscale with a n size border of black pixels 
    gray = np.zeros((h+2*n, w+2*n))
    gray[n:-n, n:-n] = gray_temp
    out = np.zeros_like(gray_temp)

    for i in range(n, h-n):
        for j in range(n, w-n):
            # current kernel
            roi = gray[i-n:i+n+1, j-n:j+n+1]
            # thresholding for this kernel
            T = roi.mean() -k*roi.std()
            out[i, j] = 0 if gray[i, j] < T else 255
    
    return out


