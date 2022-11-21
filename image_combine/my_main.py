import cv2
import numpy as np
import PySimpleGUI as sg


def nakladanie(img, img1, img2, rescale):
    # funkcja w opencv
    # img = cv2.addWeighted(img1, rescale, img2, 1-rescale, 0)

    # działania na macierzach w numpy; 
    # ponieważ img1 i img2 maja dtype int8, ich suma capuje sie na wartosci 255; 
    # nie musimy sie rowniez martwic wartosciami po przecinku, ale tak dla pewnosci
    img = (img1*rescale + img2*(1-rescale)).astype('uint8')

    # np array2png img; [0] - boolean suc/fail [1] - img
    img_encode = cv2.imencode('.png', img)[1]
    bytes_encode = img_encode.tobytes()

    return bytes_encode



# deklaracja tymczasowych obrazków
img = np.zeros((250, 250, 3), 'uint8')
img1 = np.zeros((250, 250, 3), 'uint8') # czarny obraz
img2 = np.ones((250, 250, 3), 'uint8') * 255 # bialy obraz

## deklaracja kontrolek w oknie
# kontrolki wyboru pliku
file_browse1 = sg.FileBrowse(
    "Choose file 1", size=(14, 1), 
    key="Browse1", enable_events=True)
file_browse2 = sg.FileBrowse(
    "Choose file 2", size=(14, 1), 
    key="Browse2", enable_events=True)
# kontrolka z etykietą tekstową
label = sg.Text("Ratio:")
# suwak; domyślna wartość: 0, skala 0-100, orientacja pozioma, klucz, 
# enable_events=True -> włącz eventy (inaczej nie będzie można reagować na zmianę wartości)
slider = sg.Slider(
    default_value=0, range=(0,100), orientation="horizontal", 
    key='Slider', enable_events=True)
# kontrolka wyświetlająca obrazek
data = nakladanie(img, img1, img2, 0.35) # początkowa wartość zwracana przez funkcję => biały obrazek
img_box = sg.Image(data=data, key="Image") # przypisanie obrazka do kontrolki

# określenie układu kontrolek
layout = [
    [file_browse1, file_browse2], # pierwszy rząd
    [img_box], # drugi rząd
    [label, slider], # trzeci rząd
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
        data = nakladanie(img, img1, img2, slider_val/100) # aktualizuj obrazek
        img_box.update(data = data) # ustaw aktualny obrazek
    elif event == 'Browse1': # jeśli wybrano obrazek 1
        filename = values['Browse1'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img1 = cv2.imread(filename)
        img1 = cv2.resize(img1, (250, 250), interpolation=cv2.INTER_AREA)
    elif event == 'Browse2': # jeśli wybrano obrazek 2
        filename = values['Browse2'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img2 = cv2.imread(filename)
        img2 = cv2.resize(img2, (250, 250), interpolation=cv2.INTER_AREA)

window.close() # zamknij okno
