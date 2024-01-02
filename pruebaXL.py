#ML calculazzioni
from functools import cache
from sched import scheduler
from colorama import init
import torch 
#modelo XL
from diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl_img2img import StableDiffusionXLImg2ImgPipeline
from diffusers.schedulers.scheduling_euler_discrete import EulerDiscreteScheduler
from diffusers.utils.loading_utils import load_image
#random numbers
import random
#GUI SHIT
import tkinter as xpp
from PIL import Image,ImageTk
import win32api
import os
import threading
import time
#reconocimiento de voz
import speech_recognition as uwu
from PIL import ImageFile
import pyttsx3 as watsher
negativosss= ["deformed","disfigured","mutated","asymetric","distorted","ugly","bad contrast","weird fingers and legs","deformed face","blurred face,hands and legs","weird body","unrealistic pose","merged body parts"]

ImageFile.LOAD_TRUNCATED_IMAGES= True
#iniciar voz a texto
reconoce = uwu.Recognizer()
#RESOLUCION WIN API BB
s_width, s_height = win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)
#VOICE2TEXT
prompt="naruto like surfboard with arms and legs made of emojis"
 #voice RECOG
def grabaTexta():
    global prompt,nosdijo
    #checa el audio e intenta si no te entienden
    while True:
        try:
            #microfono
            with uwu.Microphone() as fuenteB:
                reconoce.adjust_for_ambient_noise(fuenteB,duration=3)
                #escucha input de voz
                audia = reconoce.listen(fuenteB)
                #con google
                nosdijo= reconoce.recognize_google(audia)
                #reconoce.recognize_google(audia,)
                print(nosdijo)
                prompt = nosdijo

                return nosdijo
        except uwu.RequestError as errr:
            print("error con la request; {0}.format{errr}")
        except uwu.UnknownValueError:
            print("f")
      
GUARDAR_FOTO= os.path.join(os.environ['USERPROFILE'],'Videos','SERIUS MODE')

#empieza pipeline
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16,use_safetensors= True
)
pipe = pipe.to("cuda")
scheduler= EulerDiscreteScheduler.from_config(pipe.scheduler.config,use_karras_sigmas=True)
pipe.scheduler = scheduler
#prompt Structura
imoo=0
semilla = f"C:\\Users\\iuibu\\Videos\\SERIUS MODE\\hh0.png"
init_image = load_image(semilla).convert("RGB")


num_inference_steps = 50  
#esto guarda y nombra las imagenes en al carpeta del proyect
def doitBABY():
    while True:
        global init_image,imoo,semilla
        prompt = grabaTexta()
        print(f"New prompt: {prompt}")
        
        image= init_image
        for imgSeqqq in range(1,12):
            rando_seed = random.randint(0,1009800)
            torch.manual_seed(rando_seed)
            image = pipe(prompt, image=init_image,num_inference_steps= num_inference_steps,guidance_scale=8.0,negative_keywords=negativosss,strength= 0.70).images[0]
            image.save(f"hh{imoo}.png")
            semilla = f"C:\\Users\\iuibu\\Videos\\SERIUS MODE\\hh{imoo}.png"
            init_image = image.convert("RGB")
            imoo +=1
            if (imoo >= 10):
                imoo=0
            print(f"imoo= {imoo}, for= {imgSeqqq}")
       
    
        print(f"afuera, ultima seed= {init_image}")
############################################################################
#EMPIEZA EL MODULO DE DISPLAY DE IMAGEN CON RESIZE INCLUIDO y SECUENCIADOR
raiz= xpp.Tk()
raiz.title("@@.@@ @@ o @@ @@.@@")
raiz.geometry("1024x1024")
#imagen
fotoshut= ImageTk.PhotoImage(file="hh0.png")
#canvas approach(tambien puede ser con un label o grid )
#crealo
area_Canvs= xpp.Canvas(raiz,width=1024,height=1024)
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
    raiz.after(190, Refrescala)  # schedule the next update

Refrescala()  # Actualiza las iamgenes en el folder y aparte las resizea y cambia

#THREAD DE LA VOZ
threading.Thread(target=doitBABY,daemon=True).start()
raiz.mainloop() 

