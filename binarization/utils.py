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
    out = img.mean(axis=2)
    out = out.astype('uint8')
    return out


def binarize(img, threshold=127):
    '''
    binarization
    '''
    gray = grayscale(img)
    gray[gray>=threshold] = 255
    gray[gray<threshold] = 0

    return gray


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





def sauvola(img, n, k, r):
    '''
    img, n - size of kernel, k - strength of thresholding, R - scaling
    '''
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
            T = roi.mean()*(1 -k*(1 - roi.std()/r))
            out[i, j] = 0 if gray[i, j] < T else 255
    
    return out


def rid_calvard(img):
    '''
    Automaticaly finds thresholding value by assuming corner of image as image background
    Then iteratively computes new threshold by comparing means of regions where thresholding is applied
    '''
    # original grayscale
    gray = grayscale(img)
    out = np.zeros_like(gray)

    # corner size
    cor_size = 150
    ## Initial thresholding value calculation
    # threshold bg = 4 corners
    t_bg1 = gray[:cor_size, :cor_size]   # UL
    t_bg2 = gray[:cor_size:, -cor_size:] # UR
    t_bg3 = gray[-cor_size:, :cor_size]  # DL
    t_bg4 = gray[-cor_size:, -cor_size:] # DR
    t_bg = np.concatenate([t_bg1, t_bg2, t_bg3, t_bg4])
    # threshold foreground
    t_fg1 = gray[:cor_size,  cor_size:-cor_size] # UP
    t_fg2 = gray[-cor_size:, cor_size:-cor_size] # DOWN
    t_fg3 = gray[cor_size:-cor_size,:]  # Middle
    t_fg = np.concatenate([t_fg1.flatten(), t_fg2.flatten(), t_fg3.flatten()])
    # threshold value
    threshold_zero = (t_bg.mean() + t_fg.mean())/2

    # generating new thresholding value
    while True:
        # pixels above threshold
        t1_above = gray[gray >= threshold_zero]
        # pixels below threshold
        t1_below = gray[gray < threshold_zero]
        # new threshold
        threshold_one = (t1_above.mean() + t1_below.mean())/2

        # while threshold changes update, else break
        if threshold_one != threshold_zero:
            threshold_zero = threshold_one
        else:
            break
    
    out[gray>=threshold_zero] = 255
    out[gray<threshold_zero] = 0
            
    return out