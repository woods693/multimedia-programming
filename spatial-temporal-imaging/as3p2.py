import cv2
import numpy as np
from Tkinter import *
import tkFileDialog
import time
import math



def browse_file():
    #allows for selection of file in GUI
    fname = tkFileDialog.askopenfilename(filetypes = (("Video files", "*.ogg"), ("All files", "*")))
    #0Blue, 1Green, 2Red
    try:
        count = 0

        last_opened_file.place(x=0, y=200)
        cap = cv2.VideoCapture(fname)

        #template
        template = cv2.imread("hist_template.jpg")
        (h2,w2) = template.shape[:2]

        #video width and height
        w_float = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        width = int(w_float)
        h_float = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        height = int(h_float)

        #[y][x]
        B = 0
        G = 0
        G_Cal = 0
        R = 0
        R_Cal = 0
        den = 0
        #603
        while(count<603):
            ret, frame = cap.read()

            if (frame == None):
                break
            for i in range(0,width):
                hist_array = [[0 for x in range(7)] for y in range(7)]
                for j in range(0,height):
                    B = int(frame[j,i,0])
                    G = int(frame[j,i,1])
                    R = int(frame[j,i,2])
                    if((B+G+R) == 0):
                        G_Cal = 0
                        R_Cal = 0
                    else:
                        G_Cal = float(G)/(B+G+R)
                        R_Cal = float(R)/(B+G+R)
                    hist_array[int(round(G_Cal*6))][int(round(R_Cal*6))]+=1

                for x in range(0,7):
                    for y in range(0,7):
                        temp = hist_array[x][y]
                        hist_array[x][y] = float(temp) / height
                if(count > 0):
                    I = 0
                    for x in range(0,7):
                        for y in range(0,7):
                            if(hist_array[x][y] >= hist_array_prev[x][y]):
                                I += hist_array_prev[x][y]
                            else:
                                I += hist_array[x][y]
                        if(I > 0.9):
                            template.itemset((i,count,0),255)
                            template.itemset((i,count,1),255)
                            template.itemset((i,count,2),255)
                        else:
                            template.itemset((i,count,0),0)
                            template.itemset((i,count,1),0)
                            template.itemset((i,count,2),0)
                hist_array_prev = hist_array[:]

            count += 1
            cv2.imshow('image',frame)


            #write frame info to external pic
            #time.sleep(0.02)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.imwrite("sti.jpg", template)

    except (IOError, AttributeError ) as e:
        print "Invalid file"


GUI = Tk()
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
file_nm = None
GUI.configure(background='black')
GUI.title("Project James Araujo & Woody Chang")
GUI.geometry("800x800")
GUI.resizable(width=False, height=False)
header = Label(GUI, text="Spatial Temporal Images", font=("Arial", 30), fg="red", bg="black")
header.grid(row=0, column=1)
credit_Label = Label(GUI, text="CMPT365 Project", font=("Arial",18), fg="white", bg="black")
credit_Label.grid(row=1, column=1, sticky=W)
blankspace = Label(GUI, text="", bg="black")
blankspace.grid(row=2,column=1)
blankspace2 = Label(GUI, text="", bg="black")
blankspace2.grid(row=3,column=1)
browseButton = Button(GUI, text="Browse for File", width = 24, command = browse_file, bg="black", fg="white")
browseButton.grid(row=4, column=1, sticky=W)
file_descript = Entry(GUI, width=60, state='readonly', textvariable = file_nm)
file_descript.place(x=0,y=225)

ja_wc = Label(GUI, text="By James Araujo & Woody Chang", font=("Arial", 22), bg="black", fg="white")
ja_wc.place(x=1,y=750)
last_opened_file = Label(GUI, text="Last Opened File:", font=("Arial", 12), bg="black", fg="white")



GUI.mainloop()
