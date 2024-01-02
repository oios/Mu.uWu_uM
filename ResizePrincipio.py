#GUI SHIT
import tkinter as uWu
from tkinter import ttk
from PIL import Image,ImageTk
import win32api

#RESOLUCION WIN API BB
s_width, s_height = win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)

print(f"alto= {s_height} ancho {s_width}")

#crear la window TKINTER le dice 'root'
roto= uWu.Tk()
roto.title("xD XXX xD")
roto.geometry("{}x{}".format(s_width//2,s_height//2)) #Set sze of window here

#carga IMAGEN
imgg= Image.open("seq0.png")

#resize concorde a la ventana(LA IMAGEN)
photo= imgg.resize((1200,820),Image.LANCZOS)#innecesario porque tendremos funcion pata hacerlo
photo_NE= ImageTk.PhotoImage(photo)

#PARA ESTO NECESITAMOS UN LABEL
red_label= uWu.Label(roto, image=photo_NE)
red_label.pack(pady=1)

#resize funK

def printSizeandResize(event):
    
    print(f"wH= {event.height}, wW= {event.width}")
         # Get the new size of the window
    new_width = event.width
    new_height = event.height
    # Resize the image to the new size
    resized_image = imgg.resize((new_width, new_height), Image.LANCZOS)
    # Convert the resized image to a Tkinter-compatible format
    new_photo = ImageTk.PhotoImage(resized_image)
    # Update the label with the new image
    red_label.config(image=new_photo)
    red_label.image = new_photo # type: ignore

roto.bind("<Configure>", printSizeandResize)

roto.mainloop()