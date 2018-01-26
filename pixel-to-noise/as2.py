import sys
sys.path.append('packages')
from Tkinter import *
import tkFileDialog
from PIL import Image
import pyaudio
import math
import numpy as np

def browse_file():
    #allows for selection of file in GUI
    fname = tkFileDialog.askopenfilename(filetypes = (("Video files", "*.avi .mov .jpg .jpeg .png .bmp .tiff"), ("All files", "*")))
    imageFile = fname
    file_nm = fname
    try:
        last_opened_file.place(x=240,y=95)


        img = Image.open(imageFile).convert('L')
        img = img.resize(( 64,64), Image.ANTIALIAS)
        img.show()
        file_descript.configure(state='normal')
        file_descript.delete(0,END)
        file_descript.insert(0,file_nm)
        file_descript.configure(state='readonly')
        pix = img.load() #pixels of grayscale

        p = pyaudio.PyAudio()

        fs = 44100       # sampling rate, Hz
        duration = 0.7   # in seconds

        freq = [0] * 64
        freq[31] = 440.0
        for m in range(32,64):
            freq[m] = freq[m - 1] * math.pow(2,1.0/12.0)
            #print freq[m]
            #print m
        for m in range(30,-1,-1):
            freq[m] = freq[m + 1] * math.pow(2,-1.0/12.0)
            #print freq[m]
            #print m
        N = 500

        for col in range(0,64):
            signal = np.array([0]*N, dtype=np.float32)
            for row in range(0,64):
                #   print pix[col,row]
                m = 64 - row - 1

                if pix[col,row] != 0:
                    s = (np.sin(2 * np.pi * np.arange(fs * duration) * freq[m] / fs)).astype(np.float32)

                    stream = p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=fs,
                            output=True)

                            #signal[row] = samples * pix[row,col]
                            #signal = signal + samples * pix[row,col]

                    stream.write(s * pix[col,row])
                    stream.stop_stream()
                    stream.close()
                else:
                    print pix[col,row]
        p.terminate()

    except ( IOError, AttributeError ) as e:
        print "Invalid file"

GUI = Tk()
file_nm = None
GUI.configure(background='black')
GUI.title("Assignment 2 James Araujo & Woody Chang")
GUI.geometry("800x800")
GUI.resizable(width=False, height=False)
header = Label(GUI, text="Converting Video & Images to Audio", font=("Arial", 30), fg="red", bg="black")
header.grid(row=0, column=1)
credit_Label = Label(GUI, text="CMPT365 Assignment 2", font=("Arial",18), fg="white", bg="black")
credit_Label.grid(row=1, column=1, sticky=W)
blankspace = Label(GUI, text="", bg="black")
blankspace.grid(row=2,column=1)
blankspace2 = Label(GUI, text="", bg="black")
blankspace2.grid(row=3,column=1)
browseButton = Button(GUI, text="Browse for File", width = 24, command = browse_file, bg="black", fg="white")
browseButton.grid(row=4, column=1, sticky=W)
file_descript = Entry(GUI, width=60, state='readonly', textvariable = file_nm)
file_descript.place(x=240,y=125)

ja_wc = Label(GUI, text="By James Araujo & Woody Chang", font=("Arial", 22), bg="black", fg="white")
ja_wc.place(x=1,y=750)
last_opened_file = Label(GUI, text="Last Opened File:", font=("Arial", 12), bg="black", fg="white")



GUI.mainloop()
