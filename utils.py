import cv2
import numpy as np


def img_to_bytes(img):
    img_encode = cv2.imencode('.png', img)[1]
    data = img_encode.tobytes()

    return data



def grayscale(img):
    gray = (img[:, :,0] + img[:, :,1] + img[:, :,2])/3
    return gray

def binarize(img, threshold=127):
    h, w = img.shape[:2]
    out = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            out[i, j] = 0 if img[i,j,:].mean()<threshold else 255
    return out



# binaryzacja niblacka
def niblack():
    TODO