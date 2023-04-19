"""
Symmetry Melody v1.0
by @Brick_Briceno 2023
"""

#Librerias uwu
import tkinter as tk
from tkinter import ttk
from threading import Thread
from multiprocessing import Process
import random
import numpy as np
import time
from pygame import mixer
import pyaudio
from webbrowser import open


"""Codigo de editor de melodias"""

Piano_Roll = [0 for x in range(64*35)]
color_boton = "#00CA65"
color_boton_pulso = "#FC19A5"
color_tonica = "#171717"

def posicion_lista(tono, corchea): #esto calcula el indice de la lista mediante sus 2 argumetos
    return ((34-tono)*64)+(corchea)


def tono_y_corchea_desde_indice(indice):
    corchea = indice % 64 + 1
    tono = 35 - (indice // 64)
    return tono, corchea

#lista con los 64*35 botones de las partituras
buttons_c1 = [0 for x in range(64*35)]

def cambiar_color_e_indice(indice):
    if Piano_Roll[indice]:
        Piano_Roll[indice] = 0
        if not ((34 - (indice // 64))%7):
            buttons_c1[indice].configure(bg=color_tonica)
        else:
            buttons_c1[indice].configure(bg="black")
    else:
        Piano_Roll[indice] = 1
        buttons_c1[indice].configure(bg=color_boton)
        seno = Thread(target=reproducir_seno, args=(
            volumen, 30/tempo, Tono_a_Hz(
            tono_y_corchea_desde_indice(indice)[0],
            escalas_list[tipo_escala_n], tono_de_escala, octava_a_anadir)))
        seno.start()

def pulso_boton(indice, lalala):
    buttons_c1[indice].configure(bg=color_boton_pulso)
    time.sleep(55/tempo)
    buttons_c1[indice].configure(bg=color_boton)

"""Parte de generación de Ritmos"""

#Configuración de Sonido

#paramrtros aplican a mas partes del programa a parte de esta uwu
frecuencia_muestreo = 44100
buffer = 1024

mixer.pre_init(frecuencia_muestreo,-16, 2, buffer)
mixer.init()

sample1 = mixer.Sound("Sonidos/Kick_defecto.wav")
sample2 = mixer.Sound("Sonidos/Clap_defecto.wav")
sample3 = mixer.Sound("Sonidos/Snare_defecto.wav")
sample4 = mixer.Sound("Sonidos/Hat_defecto.wav")

claqueta_fuerte = mixer.Sound("Sonidos/golpe_fuerte.wav")
claqueta_suave = mixer.Sound("Sonidos/golpe_suave.wav")

#Sonidos de inicio y final:
inicio = mixer.Sound("Sonidos/inicio.wav")
final = mixer.Sound("Sonidos/final.wav")


def GeneradorBrick_v2(a, b, c):
    if a > b:
        print("A es mayor a B!!! ")#que si no no tendria sentido el calculo
        return
    if a == 0:
        return [0 for i in range(c)]

    pattern = []    
    counts = []
    remainders = []
    divisor = b - a
    remainders.append(a)
    level = 0
    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)

    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)         
        else:
            for i in range(0, counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]

    n = 0
    final_pattern = []
    while c != len(final_pattern):
        if n == len(pattern):
            n = 0
        final_pattern.append(pattern[n])
        n += 1

    return final_pattern #Yeii :D

def lista_binaria_a_decimal(l1, l2, l3, l4, p):
    suma = 0
    if l1[p] == 1:
        suma += 1

    if l2[p] == 1:
        suma += 2

    if l3[p] == 1:
        suma += 4

    if l4[p] == 1:
        suma += 8 

    return suma

def convertir_valores_entrada(dato):
	a = ""
	b = ""

	numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	posicion = 0

	try:
		while dato[posicion] in numeros:
			a = a + dato[posicion]
			posicion += 1
	
		posicion += 1

		while dato[posicion] in numeros:
			b = b + dato[posicion]
			posicion += 1

	except:
		a = int(a)
		b = int(b)
		return a,b # los datos te los devuelve en forma de tupla :)

def invertir(r):
    for x in range(len(r)):
        r[x] = int(not r[x])
    return r

def revertir(r):
    r.reverse()
    return r

def mover_ritmo_izquierda(lista_a_mover):
    lista_a_mover.append(lista_a_mover[0])
    lista_a_mover.pop(0)
    return lista_a_mover

def mover_ritmo_derecha(lista_a_mover):
    for i in range(len(lista_a_mover) -1):
        lista_a_mover.append(lista_a_mover[0])
        lista_a_mover.pop(0)
    return lista_a_mover


"""Reproductor de Melodias y Ritmos"""

def teclado(grado):
    seno = Thread(target=reproducir_seno, args=(volumen, .5, Tono_a_Hz(grado, escalas_list[tipo_escala_n], tono_de_escala, 1+octava_a_anadir)))
    seno.start()

def reproducir_seno(amplitud, duracion, frecuencia):
    # Generamos la onda senoidal
    num_muestras = int(duracion * frecuencia_muestreo)
    t = np.linspace(0, duracion, num_muestras)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)

    # Creamos un objeto PyAudio para reproducir el sonido
    py_audio = pyaudio.PyAudio()
    
    # Creamos un stream de audio
    stream = py_audio.open(format=pyaudio.paFloat32,
                           channels=1,
                           rate=frecuencia_muestreo,
                           output=True)

    # Reproducimos la onda senoidal
    stream.write(onda.astype(np.float32).tobytes())

notas_octava_0={"C": 16.35, "C#": 17.32, "D": 18.35,
                "D#": 19.45, "E": 20.6, "F": 21.83,
                "F#": 23.12, "G": 24.5, "G#": 25.96,
                "A": 27.5, "A#": 29.14, "B": 30.87}

def notaSTR_a_frecuencia(nota):
    if nota[1] == "#":
        return notas_octava_0.get(nota[0:2])* pow(2, int(nota[2])-1)*2
    else:
        return notas_octava_0.get(nota[0])* pow(2, int(nota[1])-1)*2

tempo = 128

#las escalas o mejor llamarlos modos
#se construyen en tuplas poniendo 7 valores
#poniendo su pocisión cromatica

#vease que las variables mayor y menor
#son identicas salvo el 3er, 6to y 7mo grado

mayor = (1, 3, 5, 6, 8, 10, 12)
menor = (1, 3, 4, 6, 8, 9, 11)
menor_melodico = (1, 3, 4, 6, 8, 9, 12)
lidio = (1, 3, 5, 7, 8, 10, 12)
mixolidio = (1, 3, 5, 6, 8, 10, 11)
dorico = (1, 3, 4, 6, 8, 10, 11)
frigio = (1, 2, 4, 6, 8, 9, 11)
locrio = (1, 2, 4, 6, 7, 9, 11)
arabe = (1, 2, 5, 6, 8, 9, 12)

escalas_list = [mayor, menor, menor_melodico,
                lidio, mixolidio, dorico,
                frigio, locrio, arabe]

#tono es es valor del tono de 1 a 31
#escala es la tupla con los tonos a sumar
#octava es la octava a añadir
#3 es la octava que se suma por defecto

def Tono_a_Hz(tono, escala, tono_de_escala, octava):
    octava_anadir = 2
    grado = tono
    while grado > 7:
        octava_anadir += 1
        grado -= 7
    else:
        return (2**((((octava+octava_anadir)*12)+escalas_list[tipo_escala_n][grado-1]+tono_de_escala-58)/12)) * 440

"""
Tono escalas:
C = 0
C#/Db = 1
D = 2
D#/Eb = 3
E = 4
F = 5
F#/Gb = 6
G = 7
G#/Ab = 8
A = 9
A#/Bb = 10
B = 11
"""

activador = False
tipo_escala_n = 0
tono_de_escala = 5
octava_a_anadir = 0
#volumen maximo 1 y minimmo 0, 50% = 0.5
volumen = 1

def reproductor():
    corchea = 0
    global activador
    activador = True
    while activador:
        #Melodia
        for tono in range(35):
            if Piano_Roll[posicion_lista(tono, corchea)]:
                seno = Thread(target=reproducir_seno,
                            args=(volumen, 15/tempo,
                            Tono_a_Hz(tono+1, escalas_list[tipo_escala_n],
                            tono_de_escala,
                            octava_a_anadir)))
                seno.start()
                #pulso del boton
                pulso_f = Thread(target=pulso_boton, args=(posicion_lista(tono, corchea), None))
                pulso_f.start()

        #Claqueta
        if claqueta_activada and (corchea in [x*4 for x in range(16)]):
            claqueta_suave.play()
        elif claqueta_activada and (corchea in [x*16 for x in range(4)]):
            claqueta_fuerte.play()

        corchea += 1
        if corchea == 64:
            corchea = 0
        time.sleep(15/tempo)



def play_pause():
    global activador
    if activador:
        activador = False
        boton_play_pause.configure(bg="black", fg="white")
    else:
        re = Thread(target=reproductor)
        re.start()
        boton_play_pause.configure(bg="white", fg="black")

claqueta_activada = False
def claqueta():
    global claqueta_activada
    claqueta_activada = not claqueta_activada

def fuerza_bruta(lista):
    print("La lista " + str(lista) + " se genera con:\n")
    c = len(lista)
    intentos = 0
    solucion = 0
    invertida = "No"
    for x in range(2):
        lista_corrida = 0
        while lista_corrida != c:
            a = 0
            b = 0
            while not a == b == 32:
                if a == b:
                    b += 1
                    a = 1
                else:
                    a += 1
                intentos += 1
                if GeneradorBrick_v2(a, b, c) == lista:
                    solucion += 1
                    print("Solucion #" + str(solucion) + "\n")
                    print("A: " + str(a) + " B: " + str(b) + " C: " + str(c) + "\nLista corrida:\n"
                    + str(lista_corrida) + " bytes a la izquierda\n¿Invertida? "
                    + invertida + "\nIntentos: " + str(intentos))

            lista = mover_ritmo_izquierda(lista)
            lista_corrida += 1

        lista.reverse()
        invertida = "Si"


#Funciones de Botones

def redondear_tempo():
    global Tempo
    tempo = round(tempo)
    #TempoD.set(Tempo)

LastPulseTime = 0
bpm_media = []
def tempo_calc():
    global LastPulseTime
    global tempo
    global bpm_media
    CurrentTime = time.time()
    if LastPulseTime == 0:
          LastPulseTime = CurrentTime
    #Aquí se calcula el valor BPM
    bpm = 60/(CurrentTime-LastPulseTime)
    bpm_media.append(bpm)
    LastPulseTime = CurrentTime
    tempo = sum(bpm_media)/len(bpm_media)
    tempo = round(tempo)
    print(bpm_media)
    print(tempo)
    actualizar_barra(None)
    if bpm < 45:
        LastPulseTime = 0
        bpm_media = []

#Menú bar

mensaje_brick = ""

mensajes_ramdon_brick = ("Con la tecla ¨T¨ puedes marcar el tempo :)",
                         "Con las teclas de numeros tienes samples de ritmos ;)",
                         "Una vez me hice la paja con gasolina O:",
                         "No es necesario que uses muchas notas en una canción, con 5 o hasta 3 está bien uwu",
                         "Con la tecla ¨Y¨ activas una claqueta para llevar el tempo 0w0",
                         "tienes un teclado con las teclas: ¨z¨ hasta ¨-¨",
                         "No pienses en tu ex amigo! enfocate en la musica!!! B)",
                         "Los momentos de ispiración llegan cuando estás en el baño, Brick Briceño - 2020",
                         "Puedes usar tecnicas como la harmonia negativa o cambiar el ritmo de una melodia ;D",
                         "Buscame en redes como @Brick_briceno ;)")

mostrar_mensaje = True
def random_brick():
    n = len(mensajes_ramdon_brick)-1
    while mostrar_mensaje:
        time.sleep(random.randint(15, 16))
        n_anterior = n
        while n == n_anterior:
            n = random.randint(0, len(mensajes_ramdon_brick)-1)
        n_anterior = n

        global mensaje_brick
        mensaje_brick = "   -   Tip " + str(n+1) + ": " + mensajes_ramdon_brick[n]
        actualizar_barra(None)
        time.sleep(random.randint(10, 15))
        mensaje_brick = ""
        actualizar_barra(None)


msj_br = Thread(target=random_brick)
msj_br.start()

def cafe():
    open("https://paypal.me/BrickUwu")
    """Esto me ayuda a seguir creando
    Sofware Libre para Todos :D
    """

"""Interfaz"""

root = tk.Tk()
root.geometry("1024x560") # Establecer el tamaño de la ventana
root.title("Symmetry Melody v1.0")
root.iconbitmap("icon.ico")
root.resizable(0, 0)

# Crear un ttk.Style para personalizar la apariencia de los widgets
style = ttk.Style()
style.theme_use("alt")

"""Ventana 1: editor de melodias"""

frame_melodia = tk.Frame(root, bg="black")
frame_melodia.pack(expand=True, fill="both")

tono_r = [x for x in range(35)]
tono_r.reverse()
for tono in range(35):
    for corchea in range(64):
        button_c1 = tk.Button(frame_melodia, command=lambda arg= posicion_lista(tono, corchea): cambiar_color_e_indice(arg), width=1, height=1, bg="black", font=("Helvetica", 5))
        if not (tono%7):
            button_c1.configure(bg=color_tonica)
        button_c1.grid(row=tono_r[tono], column=corchea, padx=0, pady=0)
        buttons_c1[posicion_lista(tono, corchea)] = button_c1
del tono_r

#Controles Melodia
frame_controles_melodia = tk.Frame(root, bg="snow")
frame_controles_melodia.place(x=5, y=430)

def subir_bajar_tonalidad(subir):
    global tono_de_escala
    if subir:
        tono_de_escala += 1
        if tono_de_escala > 11:
            tono_de_escala = 0
    else:
        tono_de_escala -= 1
        if tono_de_escala < 0:
            tono_de_escala = 11

    actualizar_barra(None)
    

boton_play_pause = tk.Button(frame_controles_melodia, text="Play", bg="black", fg="white", command=play_pause, font=("Helvetica", 18))
boton_play_pause.grid(row=0, column=0)

boton_bajar_tonalidad = tk.Button(frame_controles_melodia, text="<T", bg="black", fg="white", command=lambda arg= 0: subir_bajar_tonalidad(arg), font=("Helvetica", 18))
boton_bajar_tonalidad.grid(row=0, column=2)

boton_suibir_tonalidad = tk.Button(frame_controles_melodia, text="T>", bg="black", fg="white", command=lambda arg= 1: subir_bajar_tonalidad(arg), font=("Helvetica", 18))
boton_suibir_tonalidad.grid(row=0, column=1)


#Menú bar
menu_bar = tk.Menu(root)

# Crear el menú "Archivo"
archivo_menu = tk.Menu(menu_bar, tearoff=0)
archivo_menu.add_command(label="Abrir")
archivo_menu.add_command(label="Guardar")
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=root.quit)
archivo_menu.config(bg="black", fg="snow")

menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

#Escalas Menú
escalas_menu = tk.Menu(menu_bar, tearoff=0)

"""Barra de Estado"""

nombres_escalas = ["Mayor", "Menor", "Menor melodico",
                    "Lidio", "Mixolidio", "Dorico", "Frigio",
                    "Locrio", "Arabe"]

def actualizar_barra(n_esc):
    global tipo_escala_n
    if n_esc != None:
        tipo_escala_n = n_esc
    statusbar_label.configure(text="Tempo: " +
                              str(tempo) + "    -   Ecala: " +
                              ["C", "C#", "D", "D#", "E", "F",
                               "F#", "G", "G#", "A", "A#", "B"][tono_de_escala]+
                               " " +
                               nombres_escalas[tipo_escala_n] + mensaje_brick)

statusbar = tk.Frame(root, bg="black", width=400, height=20)
statusbar.pack(fill=tk.X)
statusbar_label = tk.Label(statusbar, text="", bg="#262626", fg="white", width=400, anchor=tk.W, font=("Helvetica", 12))
statusbar_label.pack(fill=tk.X)
actualizar_barra(None)

for x in range(len(nombres_escalas)):
    escalas_menu.add_command(label=nombres_escalas[x], command=lambda arg=x: actualizar_barra(arg))

escalas_menu.config(bg="black", fg="snow")

menu_bar.add_cascade(label="Escalas", menu=escalas_menu)

ayuda_menu = tk.Menu(menu_bar, tearoff=0)
ayuda_menu.add_command(label="Ayuda")
ayuda_menu.add_command(label="Dame un Cafe <3", command=cafe)
ayuda_menu.config(bg="black", fg="snow")

menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)

#Asignar el menú bar a la ventana
root.config(menu=menu_bar)


"""Atajos de Teclado"""

#controles basicos
root.bind("<space>", lambda event: play_pause())
root.bind("t", lambda event: tempo_calc())
root.bind("T", lambda event: tempo_calc())
root.bind("y", lambda event: claqueta())
root.bind("}", lambda event: subir_bajar_tonalidad(0))
root.bind("{", lambda event: subir_bajar_tonalidad(1))

#Ritmos samples

root.bind("1", lambda event: sample1.play())
root.bind("2", lambda event: sample2.play())
root.bind("3", lambda event: sample3.play())
root.bind("4", lambda event: sample4.play())


#teclado
root.bind("Z", lambda event: teclado(1))
root.bind("z", lambda event: teclado(1))
root.bind("X", lambda event: teclado(2))
root.bind("x", lambda event: teclado(2))
root.bind("C", lambda event: teclado(3))
root.bind("c", lambda event: teclado(3))
root.bind("V", lambda event: teclado(4))
root.bind("v", lambda event: teclado(4))
root.bind("B", lambda event: teclado(5))
root.bind("b", lambda event: teclado(5))
root.bind("N", lambda event: teclado(6))
root.bind("n", lambda event: teclado(6))
root.bind("M", lambda event: teclado(7))
root.bind("m", lambda event: teclado(7))
root.bind(",", lambda event: teclado(8))
root.bind(".", lambda event: teclado(9))
root.bind("-", lambda event: teclado(10))


inicio.play()
root.mainloop()
activador = False
mostrar_mensaje = False
msj_br.join()
final.play()
