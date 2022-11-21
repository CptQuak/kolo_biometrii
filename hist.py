import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('images/wave.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imshow('i1', gray)

# histogram
def histo_plot(bins = 256):
    hist = cv2.calcHist([gray], [0], None, [bins], [0,256])

    plt.figure(1)
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()

def histo_plot_numpy(image, bins = 256, color = 'b'):
    plt.figure(1)
    plt.hist(image.flatten(), bins=bins, color=color, histtype='stepfilled')
    plt.xlim([0, 256])
    plt.show()

print(gray.shape)

#histo_plot_numpy(gray, color='b')

def histo_plot_numpy_rgb(image, bins = 256, colors = ('b', 'g', 'r')):
    # bgr bo taka jest reprezentacja w opencv
    plt.figure(1)
    for i, color in enumerate(colors):
        plt.hist(image[:, :, i].flatten(), bins=bins, color=color, histtype='step')
    plt.xlim([0, 256])
    plt.show()
    

histo_plot_numpy_rgb(img)