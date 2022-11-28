import numpy as np
import PySimpleGUI as sg
from PIL import Image
# file path to utility file
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import utils

im_size = 300
# initial image
# gui composition
# image viewing fields

images_l = [Image.open(i).resize((im_size, im_size)) 
            for i in 
            ['000_images/dog.png', '000_images/beach.png', '000_images/thImg.jpg']]
images_l.append(np.zeros((im_size, im_size, 3), 'uint8'))

img_boxes = [sg.Image(data=utils.img_to_bytes(images_l[i-1]) , key=f"Image{i}") for i in range(1, 5)]
# button to process image
bin_button = sg.Button('Process', key="Process")

layout = [
    img_boxes, # images
    [bin_button],
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)



# gui loop
while True:
    event, values = window.read() 
    # event processing
    if event is None:
        break 
    # processing algorithm based on currently set option
    elif event == 'Process':
        bg_a = np.zeros((im_size, im_size, 4))
        # for c in range(0, 3):
        #     bg_a[:, :, c] = 1-bg_img[:, :, c]
        # bg_a[:, :, 3] = utils.grayscale(th_img)

        # fg_a = np.zeros((im_size, im_size, 4))
        # for c in range(0, 3):
        #     fg_a[:, :, c] = main_img[:, :, c]
        # fg_a[:, :, 3] = utils.grayscale(th_img)

        # out = bg_a + fg_a

        # cv2.imwrite('image_mating/test.png', out)
        # utils.load_image('image_mating/test.png', img_boxes[3], im_size=im_size)
        
        #data = utils.img_to_bytes(rgba)
        #img_boxes[3].update(data = data)

window.close()


