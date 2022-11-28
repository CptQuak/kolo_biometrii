'''
Program z pierwszego spotkania koła (semestr 2022Z) przepisany na język Python.
Nakładanie obrazów.

odpalane na: 
- Python 3.10.4
- SimpleGUI: 4.60.4
- Pillow: 9.1.0
'''

# potrzebne biblioteki:
# pip install PySimpleGUI
# pip install Pillow

import PySimpleGUI as sg
import PIL
from PIL import ImageQt
from io import BytesIO

# sprawdzenie zainstalowanych wersji:
print("PySimpleGUI:", sg.__version__)
print("Pillow:", PIL.__version__)

# funkcja do aktualizacji obrazka
def image_to_data(im, im1, im2, ratio):
    '''
    im: obrazek wynikowy
    im1: obrazek 1
    im2: obrazek 2
    '''
    
    pixels =  im.load() # odczyt pikseli
    pixels1 = im1.load() # z pierwszego obrazka
    pixels2 = im2.load() # z drugiego obrazka
    
    # łączenie obrazków w proporcji określonej przez ratio
    for i in range(im1.size[0]):    # dla każdej kolumny
        for j in range(im1.size[1]):    # dla każdego rzędu
            pixels[i,j] =  (int((ratio*pixels1[i,j][0] + (1-ratio)*pixels2[i,j][0])), 
                            int((ratio*pixels1[i,j][1] + (1-ratio)*pixels2[i,j][1])), 
                            int((ratio*pixels1[i,j][2] + (1-ratio)*pixels2[i,j][2])))
        
    with BytesIO() as output: # piksele => bajty
        im.save(output, format="PNG")
        data = output.getvalue()
        
    return data # zwróć bajty

# deklaracja trzech obrazków
img =  ImageQt.Image.new('RGB', (250,250)) # miejsce na obraz wynikowy do wyświetlania
img1 = ImageQt.Image.new('RGB', (250,250), color='black') # obrazek 1 zainicjowany jako czarny
img2 = ImageQt.Image.new('RGB', (250,250), color='white') # obrazek 2 zainicjowany jako biały

## deklaracja kontrolek w oknie
# kontrolki wyboru pliku
file_browse1 = sg.FileBrowse("Choose file 1", size=(14, 1), key="Browse1", enable_events=True)
file_browse2 = sg.FileBrowse("Choose file 2", size=(14, 1), key="Browse2", enable_events=True)

# kontrolka wyświetlająca obrazek
data = image_to_data(img, img1, img2, 0) # początkowa wartość zwracana przez funkcję => biały obrazek
img_box = sg.Image(data=data, key="Image") # przypisanie obrazka do kontrolki

# kontrolka z etykietą tekstową
label = sg.Text("Ratio:")
# suwak; domyślna wartość: 0, skala 0-100, orientacja pozioma, klucz, 
# enable_events=True -> włącz eventy (inaczej nie będzie można reagować na zmianę wartości)
slider = sg.Slider(default_value=0, range=(0,100), orientation="horizontal", key='Slider', enable_events=True)

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
        data = image_to_data(img, img1, img2, slider_val/100) # aktualizuj obrazek
        img_box.update(data = data) # ustaw aktualny obrazek
    elif event == 'Browse1': # jeśli wybrano obrazek 1
        filename = values['Browse1'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img1 = ImageQt.Image.open(filename).resize((250,250)) # otwórz, dopasuj rozmiar i ustaw jako obrazek 1
    elif event == 'Browse2': # jeśli wybrano obrazek 2
        filename = values['Browse2'] # pobierz aktualnie wybraną ścieżkę do obrazka
        img2 = ImageQt.Image.open(filename).resize((250,250)) # otwórz, dopasuj rozmiar i ustaw jako obrazek 2

window.close() # zamknij okno
