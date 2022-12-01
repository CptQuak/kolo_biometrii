import numpy as np
import PySimpleGUI as sg
import PIL
from PIL import Image
# file path to utility file
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import utils
from ImageLoader import ImageLoader


loader = ImageLoader()
# initial image
img = np.zeros((400, 400, 3), 'uint8')
img = Image.open('000_images/book_page.jpg').resize((400, 400))

data = loader.img_to_bytes(img) 
# gui composition
# load image button
file_browse1 = sg.FileBrowse("Choose file 1", key="Browse1", enable_events=True)
# image viewing fields
img_boxes = [sg.Image(data=data, key=f"Image{i}") for i in range(1, 3)]

# algorithm selection
algorithms = ['Gray', 'Thresholding', 'Niblack', 'Sauvola', 'Rid_Calvard', 'Otsu']
combobox = sg.Combo(algorithms, default_value=algorithms[0], key='Combo')

# thresholding value for thresholding alg
slider1 = sg.Slider(default_value=127, range=(0,255), orientation="horizontal", key='Slider1')
# k value for niblack algo
slider2 = sg.Slider(default_value=0.2, range=(0,1), orientation="horizontal", key='Slider2', resolution=0.1)
# n value for niblack algo
slider3 = sg.Slider(default_value=1, range=(1,10), orientation="horizontal", key='Slider3')
# r for sauvola
slider4 = sg.Slider(default_value=127, range=(0,255), orientation="horizontal", key='Slider4')
# określenie układu kontrolek
layout = [
    [file_browse1], # pierwszy rząd
    img_boxes, # drugi rząd
    [sg.Button('Process', key="Process"), combobox, sg.Button('Save', key="Save")],
    [sg.Text("Threshold: "), slider1, sg.Text("K param: "),slider2,],
    [sg.Text("Neighbors: "), slider3, sg.Text("R param: "), slider4] 
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)

# gui loop
while True:
    event, values = window.read() 
    # event processing
    if event is None:
        break 
    # choosing file
    elif event == 'Browse1':
        filename = values['Browse1']
        loader.load_image(filename, img_boxes[0], 400)
    # processing algorithm based on currently set option
    elif event == 'Process':
        if values['Combo'] == algorithms[0]:
            img_processed = utils.grayscale(img)
        elif values['Combo'] == algorithms[1]:
            T = values['Slider1'] 
            img_processed = utils.binarize(img, T)
        elif values['Combo'] == algorithms[2]:
            k = values['Slider2'] 
            n = values['Slider3'] 
            img_processed = utils.niblack(img, n, k)
        elif values['Combo'] == algorithms[3]:
            k = values['Slider2'] 
            n = values['Slider3'] 
            r = values['Slider4'] 
            img_processed = utils.sauvola(img, n, k, r)
        elif values['Combo'] == algorithms[4]:
            img_processed = utils.rid_calvard(img)
        elif values['Combo'] == algorithms[5]:
            img_processed = utils.otsu(img)
        # update image field
        data = loader.img_to_bytes(img_processed)
        img_boxes[1].update(data = data)
    elif event == 'Save':
        img_save = Image.fromarray(img_processed)
        img_save.save('000_images/thresholded.jpg')

window.close()


