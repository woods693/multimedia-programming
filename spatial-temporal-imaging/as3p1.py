import cv2
import numpy as np
from Tkinter import *
import tkFileDialog
import time



def browse_file():
    #allows for selection of file in GUI
    fname = tkFileDialog.askopenfilename(filetypes = (("Video files", "*.ogg"), ("All files", "*")))

    try:
        count = 0;
        last_opened_file.place(x=0, y=200)
        cap = cv2.VideoCapture(fname)
        template = cv2.imread("template.jpg")
        (h2,w2) = template.shape[:2]
        #print h2
        #print w2
        while(count<603):
            ret, frame = cap.read()
            (h, w) = frame.shape[:2]
            w_center = (w / 2)
            template[0:h, count] = frame[0:h, w_center]
            #cv2.imwrite("sti.jpg", template)
            count += 1;
            #print h
            #print w
            #print count
            #pix = frame[w_center,h]
            #print pix
            #for x in range(0,h):
                #pix = frame[w_center,x]
                #print pix



            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('frame',gray)

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
