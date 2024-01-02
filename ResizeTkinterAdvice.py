import os
import time
import tkinter as xpp
from tkinter import ttk
from PIL import Image,ImageTk

raiz= xpp.Tk()
raiz.title("@@.@@ @@ o @@ @@.@@")
raiz.geometry("500x500")

#imagen
fotoshut= ImageTk.PhotoImage(file="astre.png")
#canvas approach(tambien puede ser con un label o grid )
#crealo
area_Canvs= xpp.Canvas(raiz,width=500,height=500)
area_Canvs.pack(fill="both",expand=True)
#poner imagen
area_Canvs.create_image(0,0,image= fotoshut,anchor= "nw")

#Cambiar tamagno conformw pantasha
def Resizox():
    global futi1,cambio,futishoot
    #resize it(futil1 pa ser especificos, esta es la VARIABLE en todo el uso de la palabra)
    cambio= futi1.resize((raiz.winfo_width(),raiz.winfo_height()),Image.LANCZOS)
    #imagen resizeseada
    futishoot= ImageTk.PhotoImage(cambio)
    #pal CANVAS
    area_Canvs.create_image(0,0,image=futishoot,anchor="nw")

def update_image(image_path):
    global futi1,futishoot  # Make sure to use global keyword to change global photo
    futi1= Image.open(image_path)
    futishoot = ImageTk.PhotoImage(futi1)
    area_Canvs.create_image(0, 0, image=futishoot, anchor='nw')
    Resizox()#cambia el tamagno aqui ya que aqui se actualizan las imagenes

image_folder = 'C:\\Users\\iuibu\\Videos\\SERIUS MODE'
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.png')]
image_indexo=0
def Refrescala():
    global image_files,futi1,image_indexo
     # Update the image list to include any new images
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.png')]
    if image_files:  # if there are still images left
       # image_file = image_files.pop(0)  # get the next image
        image_file = image_files[image_indexo] #siguiente imagen
        futi1 = Image.open(image_file)  # Open the image file
        update_image(image_file)
        image_indexo = (image_indexo + 1) % len(image_files)
    raiz.after(420, Refrescala)  # schedule the next update

Refrescala()  # start the updates
raiz.mainloop() 