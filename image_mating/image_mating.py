import cv2
import numpy as np
import PySimpleGUI as sg
import utils

im_size = 300
# initial image
img = np.zeros((im_size, im_size, 3), 'uint8')
data = utils.img_to_bytes(img) 
# gui composition
# load image button
file_browse1 = sg.FileBrowse("Mainimage", key="Browse1", enable_events=True)
file_browse2 = sg.FileBrowse("Background", key="Browse2", enable_events=True)
file_browse3 = sg.FileBrowse("Thresholded", key="Browse3", enable_events=True)
# image viewing fields
img_boxes = [sg.Image(data=data, key=f"Image{i}") for i in range(4)]
# button to process image
bin_button = sg.Button('Process', key="Process")

layout = [
    [file_browse1, file_browse2, file_browse3], # load_images
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
    # choosing image
    # tu jest jakis dziwny bug z labelami kolejnych przyciskow XD
    elif event == 'Browse1':
        filename = values['Browse1']
        bg_img = utils.load_image(filename, img_boxes[1], im_size=im_size)
    elif event == 'Browse2':
        filename = values['Browse2']
        th_img = utils.load_image(filename, img_boxes[2], im_size=im_size)
    elif event == 'Browse3':
        filename = values['Browse3']
        main_img = utils.load_image(filename, img_boxes[0], im_size=im_size)

    
    # processing algorithm based on currently set option
    elif event == 'Process':
        bg_a = np.zeros((im_size, im_size, 4))
        for c in range(0, 3):
            bg_a[:, :, c] = 1-bg_img[:, :, c]
        bg_a[:, :, 3] = utils.grayscale(th_img)

        fg_a = np.zeros((im_size, im_size, 4))
        for c in range(0, 3):
            fg_a[:, :, c] = main_img[:, :, c]
        fg_a[:, :, 3] = utils.grayscale(th_img)

        out = bg_a + fg_a

        cv2.imwrite('image_mating/test.png', out)
        utils.load_image('image_mating/test.png', img_boxes[3], im_size=im_size)
        
        #data = utils.img_to_bytes(rgba)
        #img_boxes[3].update(data = data)

window.close()


