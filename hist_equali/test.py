import cv2
import numpy as np
import PySimpleGUI as sg

def nakladanie(img):
    img_encode = cv2.imencode('.png', img)[1]
    bytes_encode = img_encode.tobytes()

    return bytes_encode



img = np.zeros((250, 250, 3), 'uint8') # czarny obraz

## deklaracja kontrolek w oknie
# kontrolki wyboru pliku
file_browse1 = sg.FileBrowse(
    "Choose file 1", 
    key="Browse1", enable_events=True)

bin_button = sg.Button('Bin')
# kontrolka z etykietą tekstową

data = nakladanie(img) # początkowa wartość zwracana przez funkcję => biały obrazek
img_box = sg.Image(data=data, key="Image") # przypisanie obrazka do kontrolki

# określenie układu kontrolek
layout = [
    [file_browse1], # pierwszy rząd
    [img_box], # drugi rząd
    [bin_button], # trzeci rząd
]
# nowe okno: nazwa okna, układ kontrolek
window = sg.Window("Simple Gui App", layout)




# główna pętla okna - reagowanie na pojawiające się eventy
while True:
    event, values = window.read() # czytaj eventy
    # zamknięcie okna
    if event is None:
        break 
    elif event == 'Slider':
        slider_val = values['Slider']
        data = nakladanie(img) # aktualizuj obrazek
        img_box.update(data = data) # ustaw aktualny obrazek
    elif event == 'Browse1': # jeśli wybrano obrazek 1
        filename = values['Browse1'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img1 = cv2.imread(filename)
        img1 = cv2.resize(img1, (250, 250), interpolation=cv2.INTER_AREA)

window.close() # zamknij okno


