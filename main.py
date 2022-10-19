
from tkinter import Tk
from src.FPGrowth import FPGrowth
from tkinter.filedialog import askopenfilename
from src.JsonReader import Json


def main():

    Tk().withdraw()  
    filename = askopenfilename()
    print(filename)
    
    data = Json(filename).read()
    Fp = FPGrowth(data)
    Fp.start()
    


main()
