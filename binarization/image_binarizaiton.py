import cv2
import numpy as np
import PySimpleGUI as sg
import utils

# initial image
img = np.zeros((250, 250, 3), 'uint8')
data = utils.img_to_bytes(img) 
# gui composition
# load image button
file_browse1 = sg.FileBrowse("Choose file 1", key="Browse1", enable_events=True)
# image viewing fields
img_box1 = sg.Image(data=data, key="Image1") 
img_box2 = sg.Image(data=data, key="Image2") 
# button to process image
bin_button = sg.Button('Process', key="Process")
# algorithm selection
algorithms = ['Gray', 'Thresholding', 'Niblack']
combobox = sg.Combo(algorithms, default_value=algorithms[0], key='Combo')
# thresholding value if algorithm uses it
slider = sg.Slider(default_value=127, range=(0,255), orientation="horizontal", key='Slider')
# określenie układu kontrolek
layout = [
    [file_browse1], # pierwszy rząd
    [img_box1, img_box2], # drugi rząd
    [bin_button, combobox],
    [slider], 
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)

# gui loop
while True:
    # current event and slider value
    event, values = window.read() 
    slider_val = values['Slider'] 
    
    # event processing
    if event is None:
        break 
    # choosing file
    elif event == 'Browse1':
        filename = values['Browse1']
        img = cv2.imread(filename)
        img = cv2.resize(img, (250, 250), interpolation=cv2.INTER_AREA)
        data = utils.img_to_bytes(img)
        img_box1.update(data = data) 
    # processing algorithm based on currently set option
    elif event == 'Process':
        if values['Combo'] == algorithms[0]:
            img_processed = utils.grayscale(img)
        elif values['Combo'] == algorithms[1]:
            img_processed = utils.binarize(img, slider_val)
        elif values['Combo'] == algorithms[2]:
            img_processed = utils.niblack(img, 1)
        data = utils.img_to_bytes(img)
        img_box2.update(data = data)

window.close()


