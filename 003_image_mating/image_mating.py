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

slider = sg.Slider(default_value=0, range=(0,30), orientation="horizontal", key='Slider')

layout = [
    [sg.Button('Process', key="Process"), slider],
    img_boxes, # images
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
        fg_img = np.array(images_l[0])
        th_img = np.array(images_l[2])
        times = int(values['Slider'])
        th_img = utils.dilate(times, th_img)
        # th_img = utils.erode(times, th_img)
        new_img = utils.combine_img_mask(fg_img, th_img)

        data = utils.img_to_bytes(th_img)
        img_boxes[2].update(data)
        data = utils.img_to_bytes(new_img)
        img_boxes[3].update(data)

window.close()


