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
from ImageLoader import ImageLoader


loader = ImageLoader()
# deklaracja tymczasowych obrazków
im_shape = (250, 250)

## deklaracja kontrolek w oknie
file_browsers = [
    sg.FileBrowse(f"Choose file {i}", size=(14, 1), 
    key=f"Browse{i}", enable_events=True) for i in range(1, 3)]
# kontrolka wyświetlająca obrazek
try:
    img1 = Image.open('000_images/dog.png').resize(im_shape)
    img2 = Image.open('000_images/beach.png').resize(im_shape)
except:
    img1 = np.zeros(im_shape + (3), 'uint8') # czarny obraz
    img2 = np.ones(im_shape + (3), 'uint8') * 255 # bialy obraz


merged_img = utils.merging(img1, img2, 0.35)
data = loader.img_to_bytes(merged_img)
img_box = sg.Image(data=data, key="Image")

# określenie układu kontrolek
layout = [
    file_browsers, # pierwszy rząd
    [img_box], # drugi rząd
    [sg.Text("Ratio:"), sg.Slider(default_value=0.35, range=(0,100), 
    orientation="horizontal", key='Slider', enable_events=True)], # trzeci rząd
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)

# główna pętla okna - reagowanie na pojawiające się eventy
while True:
    event, values = window.read() # czytaj eventy
    if event is None: # jeśli zamknięcie okna
        break # wyjdź z pętli
    elif event == 'Slider': # jeśli zmieniła się wartość suwaka
        slider_val = values['Slider'] # pobierz aktualną wartość ratio
        merged_img = utils.merging(img1, img2, slider_val/100) # aktualizuj obrazek
        data = loader.img_to_bytes(merged_img)
        img_box.update(data = data) 
    elif event == 'Browse1': 
        filename = values['Browse1'] 
        img1 = Image.open(filename).resize((250, 250))
    elif event == 'Browse2': 
        filename = values['Browse2'] 
        img2 = Image.open(filename).resize((250, 250))

window.close() # zamknij okno