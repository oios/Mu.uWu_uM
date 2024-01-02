import os
import threading
import time
#reconocimiento de voz
import speech_recognition as uwu

#iniciar voz a texto
reconoce = uwu.Recognizer()

prompt="ea"
print(f"primeria = {prompt}")
formalos=[]
#print(help(formalos)) 
enfila=0
def grabaTexta():
    global prompt,nosdijo,enfila
    #checa el audio e intenta si no te entienden
    while True:
        try:
            #microfono
            with uwu.Microphone() as fuenteB:
                reconoce.adjust_for_ambient_noise(fuenteB,duration=2)
                #escucha input de voz
                audia = reconoce.listen(fuenteB)
                #con google
                nosdijo= reconoce.recognize_google(audia)
                #reconoce.recognize_google(audia,)
                print(nosdijo)
                prompt = nosdijo
                enfila += 1
                print(f"en fila :: {enfila}")
                return nosdijo
        except uwu.RequestError as errr:
            print(F"error con la request; {0}.format{errr}")
        except uwu.UnknownValueError:
            print("no msg")

def LAFILA():
    global enfila
    while True:
        formalos.insert(enfila,grabaTexta())
        print(formalos)
        time.sleep(1)

threading.Thread(target= LAFILA(),daemon= True).start()