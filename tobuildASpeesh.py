#
# #
#GUI
from pyexpat import model
import tkinter as xpp
from turtle import width
from PIL import Image, ImageTk
#reconocimiento de voz
import speech_recognition as uwu
import pyttsx3 as watsher
#operating systema
import os
import glob
#text to image AI
import torch
from torch import autocast
from diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl_img2img import  StableDiffusionXLImg2ImgPipeline
from diffusers.utils.loading_utils import load_image
#TIEMPO
import time
import threading
import win32api

#checar si hay gpu disponible, tambien da el modelo a ocupar por el difusor asi como donde guardar las fotos generadas di
print("PyTorch version:", torch.__version__)
print("CUDA dispo:", torch.cuda.is_available())
#model_id = "runwayml/stable-diffusion-v1-5" #para pipeline : StableDiffusionPipeline
model_id="stabilityai/stable-diffusion-xl-refiner-1.0"

GUARDAR_FOTO= os.path.join(os.environ['USERPROFILE'],'Documents','PIC_POOL')

#GUARDADOR DE IMAGENES CON NUMERO DE SERIE PA QUE NO SE REPITAN NI SE SOBRE ESCRIBAN
def muchasPics(pathos):
    nombre, extensio = os.path.splitext(pathos)
    fileCounta = 1

    while os.path.exists(pathos):
        pathos= nombre + ' (' + str(fileCounta) + ')' + extensio
        fileCounta += 1
    return pathos

#iniciar voz a texto
reconoce = uwu.Recognizer()

def grabaTexta():

    #checa el audio e intenta si no te entienden
    while(1):
        try:
            #microfono
            with uwu.Microphone() as fuenteB:
                reconoce.adjust_for_ambient_noise(fuenteB,duration=2)
                #escucha input de voz
                audia = reconoce.listen(fuenteB)
                #con google
                nosdijo= reconoce.recognize_google(audia)

                return nosdijo
        except uwu.RequestError as errr:
            print("chale; {0}.format{errr}")
        except uwu.UnknownValueError:
            #print('?')
            aaaaa=9


    return

def documentaTexta(testa):
    f = open("outputi.txt", "a")
    f.write(testa)
    f.write("\n")
    f.close()    
    return

#PROMPT INGENIERIA DI
pictonary = "moss and lichen metahaven design style"
nega_pic = "ugly,bad contrast,poorly drawn,low poly meshes,bad typography"
estilos= {
    "none" : " ",
    "3D Render" : "Realistic lighting, ambient occlusion, ray tracing, depth of field, texture mapping, bump mapping, specular highlights, soft shadows, reflection, refraction, global illumination, indirect lighting, caustics, volumetric lighting, cloth simulation, hair simulation, particle systems, fluid simulation, crowd simulation, motion capture, keyframe animation, procedural animation, camera movement, camera angles,virtual reality, augmented reality, mixed reality, photorealism, stylized realism, maximalist, futuristic, steampunk, cyberpunk, fantasy, sci-fi, original art, concept art",
    "Macro Photography" : "Extreme close-up, depth of field, high detail, natural light, bokeh, water droplets, insect photography, flower photography, texture detail, abstract, patterns in nature, microcosm, vibrant colors, contrast, soft focus, sharp focus, ambient light, backlighting, sidelighting, diffused light, reflectors, tripods, macro lenses, extension tubes, ring flash, manual focus, stacking focus, slow shutter speed, fast shutter speed, aperture priority, manual mode, RAW format, post-processing, Adobe Lightroom, Adobe Photoshop, noise reduction, color correction, cropping, composition",
    "Wika" : "pefect lighting, trevor wisecup style,reflections in buildings,analog photography, warp-up view,fashion urban design,rule of thirds, leading lines, framing, negative space, fill the frame, simplicity, balance, viewpoint, awe, wonder, curiosity, persistence, timing, luck, serendipity, creativity, imagination, artistry, emotion, transcendence, transformation, evolution,  commercial"
           }

alto = 1024
ancho = 1024
num_inference_steps = 60
device_type = 'cuda' #que vamos a ocupar 
low_vram = True
num_images_per_prompt=1


def RealPromto(vozAtext):

    #crear el formato de como se van a guardar los archivos en el folder JIJODESU
    prompt_Corto = (vozAtext[:25] + '...')if len(vozAtext) > 25 else vozAtext
    prompt_Corto = prompt_Corto.replace(' ', '_')
    #generation_path = os.path.join(GUARDAR_FOTO, prompt_Corto.removesuffix('...'))

    if not os.path.exists(GUARDAR_FOTO):
        os.mkdir(GUARDAR_FOTO)

    #LLama a la pipeline (ESCOGE SI QUIERES GPU O CPU PUES)
    if device_type == 'cuda':
        if low_vram:
            pipa = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32
                
            )
        else:
            pipa = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_id,torch_dtype=torch.float16)
        pipa=pipa.to('cuda')

        if low_vram:
            pipa.enable_attention_slicing() #Reduce GPUV-ram

    elif device_type == 'cpu':
        pipa = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_id)
    else:
        print("Dispositivo Invalido, 'cpu' o 'cuda' exclusivamente")
        return
    
    #agarrar imagen como semilla para la siguiente imagen
    most_recent_image_path = "C:\\Users\\iuibu\\Documents\\PIC_POOL\\seq0.png"
    init_image= load_image(most_recent_image_path).convert("RGB")

    #creacion de prompt con estilos PASO FINAL
    for style_type,style_prompt in estilos.items():#esto lit solo hace que se pongan distintos stilos en los renders, se puede saltar
        prompt_stylized = f"{vozAtext},{style_prompt}"

        print(f"prompt: \n{prompt_stylized}\n")
        print(f"Cnum in Prompt: {len(prompt_stylized)}, limit:200")

        for jiji in range(num_images_per_prompt):
             # Save the image in the folder

            if device_type == 'cuda':
                with autocast('cuda'):
                    imagen = pipa(prompt_stylized,image= init_image).images[0] # type: ignore
            else:
                imagen = pipa(vozAtext).images[0] # type: ignore

            ubica_imagen= muchasPics(os.path.join(GUARDAR_FOTO,style_type + " - " +prompt_Corto) + '.png') # type: ignore
            print(ubica_imagen)
            imagen.save(ubica_imagen)
    #HAZ QUE LA ANTERIOR IMAGEN SEA LA SIGUIENTE SEMILLA(PURO PITO ELIMINAR PLS)
            init_image = imagen
    print("\nYa quedo\n")
        

#tinkerWINKER(APLICACION PANTASHA VAYA)
#RESOLUCION WIN API BB
s_width, s_height = win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)

#EMPIEZA EL MODULO DE DISPLAY DE IMAGEN CON RESIZE INCLUIDO y SECUENCIADOR
raiz= xpp.Tk()
raiz.title("@@.@@ @@ o @@ @@.@@")
raiz.geometry("500x500")

#imagen
fotoshut= ImageTk.PhotoImage(file="seq0.png")
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




#pasa las fotos
# etiqueta las imagenes
#label = xDD.Label(ventanon)
#label.pack()
#PARA ESTO NECESITAMOS UN LABEL(un elixir...)

#AUDIO TO TEXT PARA PROMPT
def AUDIOTEXTUAL():
    dori_count= 0
    while(dori_count < 3):

        dijiste = grabaTexta()
        if dijiste != '?':   
            print(dijiste)
            # de voz a prompt papitow Uwu
            pictonary = dijiste
            RealPromto(pictonary) 
        else:
            nada = 1
        time.sleep(1)
        print("end/start nueva prompt",dori_count)
        dori_count += 1

#CACHE DE IMAGENES(Para no cargar la misma imagen 2 veces o mas)
image_cache = { }

#THREAD DE LA VOZ
threading.Thread(target=AUDIOTEXTUAL,daemon=True).start()
# Update cde acuerdo a tiempo que pongas
threading.Thread(target=update_image, daemon=True).start()



raiz.mainloop()

