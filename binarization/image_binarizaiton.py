import cv2
import numpy as np
import PySimpleGUI as sg
import utils

# initial image
img = np.zeros((400, 400, 3), 'uint8')
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
    [img_box1, img_box2], # drugi rząd
    [bin_button, combobox],
    [sg.Text("Threshold: "), slider1, sg.Text("K param: "),slider2,],
    [sg.Text("Neighbors: "), slider3, sg.Text("R param: "), slider4] 
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)

# gui loop
while True:
    # current event and slider value
    event, values = window.read() 
    
    # event processing
    if event is None:
        break 
    
    # choosing file
    elif event == 'Browse1':
        filename = values['Browse1']
        img = cv2.imread(filename)
        img = cv2.resize(img, (400, 400), interpolation=cv2.INTER_AREA)
        data = utils.img_to_bytes(img)
        img_box1.update(data = data) 
    
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

        data = utils.img_to_bytes(img_processed)
        img_box2.update(data = data)

window.close()


