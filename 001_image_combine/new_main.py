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

# deklaracja tymczasowych obrazków
img1 = np.zeros((250, 250, 3), 'uint8') # czarny obraz
img2 = np.ones((250, 250, 3), 'uint8') * 255 # bialy obraz

## deklaracja kontrolek w oknie
file_browsers = [
    sg.FileBrowse(f"Choose file {i}", size=(14, 1), 
    key=f"Browse{i}", enable_events=True) for i in range(1, 3)]
slider = sg.Slider(
    default_value=0, range=(0,100), orientation="horizontal", 
    key='Slider', enable_events=True)
# kontrolka wyświetlająca obrazek
img1 = Image.open('000_images/dog.png').resize((250, 250))
img2 = Image.open('000_images/beach.png').resize((250, 250))
proc_img = utils.nakladanie(img1, img2, 0.35) # początkowa wartość zwracana przez funkcję => szary
data = utils.img_to_bytes(proc_img)
img_box = sg.Image(data=data, key="Image")

# określenie układu kontrolek
layout = [
    file_browsers, # pierwszy rząd
    [img_box], # drugi rząd
    [sg.Text("Ratio:"), slider], # trzeci rząd
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
        proc_img = utils.nakladanie(img1, img2, slider_val/100) # aktualizuj obrazek
        data = utils.img_to_bytes(proc_img)
        img_box.update(data = data) # ustaw aktualny obrazek
    elif event == 'Browse1': # jeśli wybrano obrazek 1
        filename = values['Browse1'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img1 = Image.open(filename).resize((250, 250))
        print('1',values['Browse1'])
        print('2',values['Browse2'])
    elif event == 'Browse2': # jeśli wybrano obrazek 2
        filename = values['Browse2'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img2 = Image.open(filename).resize((250, 250))
        print('1',values['Browse1'])
        print('2',values['Browse2'])

window.close() # zamknij okno