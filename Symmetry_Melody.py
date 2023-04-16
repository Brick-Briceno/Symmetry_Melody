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
#from pygame import mixer
import pyaudio
from webbrowser import open


"""Codigo area de editor de melodias"""

Piano_Roll = [0 for x in range(64*35)]
color_boton = "#00ca65"
color_tonica = "#171717"

def posicion_lista(tono, corchea): #esto calcula el indice de la lista mediante sus 2 argumetos
    return ((34-tono)*64)+(corchea)


def tono_y_corchea_desde_indice(indice):
    corchea = indice % 64 + 1
    tono = 35 - (indice // 64)
    return tono, corchea

#lista con los 64*35 botones de las partituras
buttons_c1 = [0 for x in range(64*35)]
buttons_c2 = [0 for x in range(64*35)]
buttons_c3 = [0 for x in range(64*35)]
buttons_c4 = [0 for x in range(64*35)]
buttons_c5 = [0 for x in range(64*35)]
buttons_c6 = [0 for x in range(64*35)]
buttons_c7 = [0 for x in range(64*35)]
buttons_c8 = [0 for x in range(64*35)]

boton_compas = [buttons_c1, buttons_c2, buttons_c3,
                buttons_c4, buttons_c5, buttons_c6,
                buttons_c7, buttons_c8]

def cambiar_color_e_indice(indice, compas):
    if Piano_Roll[indice]:
        if not ((34 - (indice // 64))%7):
            boton_compas[compas-1][indice].configure(bg=color_tonica)
            Piano_Roll[indice] = 0

        else:
            boton_compas[compas-1][indice].configure(bg="black")
            Piano_Roll[indice] = 0
    else:
        boton_compas[compas-1][indice].configure(bg=color_boton)
        Piano_Roll[indice] = 1
        print(tono_y_corchea_desde_indice(indice)[0])
        seno = Thread(target=reproducir_seno, args=(volumen, 15/tempo, Tono_a_Hz(tono_y_corchea_desde_indice(indice)[0], escala, tono_de_escala, octava_a_anadir)))
        seno.start()


"""Parte de generación de Ritmos"""

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

def invertir_lista(lista):
    lista_final = []
    for x in range(len(lista)):
        lista_final.append(int(not lista[x]))
    return lista_final

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
    seno = Thread(target=reproducir_seno, args=(volumen, .75, Tono_a_Hz(grado, escala, tono_de_escala, 1+octava_a_anadir)))
    seno.start()

frecuencia_muestreo = 44100

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

mayor = (1, 3, 5, 6, 8, 10, 12)
menor = (1, 3, 4, 6, 8, 9, 11)
menor_melodico = (1, 3, 4, 6, 8, 9, 12)
lidio = (1, 3, 5, 7, 8, 10, 12)
mixolidio = (1, 3, 5, 6, 8, 10, 11)
dorico = (1, 3, 4, 6, 8, 10, 11)
frigio = (1, 2, 4, 6, 8, 9, 11)
locrio = (1, 2, 4, 6, 7, 9, 11)
arabe = (1, 2, 5, 6, 8, 9, 12)

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
        return (2**((((octava+octava_anadir)*12)+escala[grado-1]+tono_de_escala-58)/12)) * 440

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
escala = mayor
tono_de_escala = 5
octava_a_anadir = 0
#volumen maximo 1 y minimmo 0, 50% = 0.5
volumen = 1

def reproductor():
    corchea = 0
    global activador
    activador = True
    while activador:
        for tono in range(35):
            if Piano_Roll[posicion_lista(tono, corchea)]:
                print(tono)
                seno = Thread(target=reproducir_seno, args=(volumen, 15/tempo, Tono_a_Hz(tono+1, escala, tono_de_escala, octava_a_anadir)))
                seno.start()

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

def claqueta():
    #print("claqueta activada")
    global claqueta_activada
    if claqueta_activada == False:
        claqueta_activada = True
        claqueta.config(bg="snow", fg="gray10")
    else:
        #print("claqueta desactivada")
        claqueta_activada = False
        claqueta.config(bg="gray10", fg="snow")

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

asignando_tempo = False
primer_pulso = True
tomaM = []
contador = 0


def redondear_tempo():
    global Tempo
    Tempo = round(Tempo)
    #TempoD.set(Tempo)

LastPulseTime = 0
bpm_media = []
def tempo_calc(event):
     global LastPulseTime
     CurrentTime = time.time() # Obtiene el tiempo
     if LastPulseTime == 0:
          LastPulseTime = CurrentTime 
          
 # Aquí se calcula el valor BPM
     bpm = 60/(CurrentTime-LastPulseTime)
     global bpm_media
     bpm_media.append(bpm)
     LastPulseTime = CurrentTime
     if bpm < 45:
          bpm_media = []
     print(sum(bpm_media)/len(bpm_media))


#Menú bar

def cafe():
    open("https://paypal.me/BrickUwu")
    """Esto me ayuda a seguir creando
    Sofware Libre para Todos :D
    """

"""Interfaz"""

root = tk.Tk()
root.geometry("1024x560") # Establecer el tamaño de la ventana
root.title("Symmetry Melody v1.0")
#root.iconbitmap("icon.ico")

# Desactivar la capacidad de redimensionar la ventana
root.resizable(False, False)

# Crear un ttk.Style para personalizar la apariencia de los widgets
style = ttk.Style()

# Cambiar el tema a uno oscuro
style.theme_use("alt")

# Cambiar los colores de fondo y de texto del Notebook y sus pestañas
style.configure('TNotebook', background="black", foreground="black")
style.configure('TNotebook.Tab', background="black", foreground="snow")

# Cambiar el color de fondo de las pestañas
style.map('TNotebook.Tab', background=[('', '#000')])

# Crear el widget Notebook
notebook = ttk.Notebook(root)

#Pestaña #2 Compás #1

tab_c1 = ttk.Frame(notebook)

notebook.add(tab_c1, text="Compás #1")
frame_melodia = tk.Frame(tab_c1, bg="black")
frame_melodia.pack(expand=True, fill="both")

tono_r = [x for x in range(35)]
tono_r.reverse()

for tono in range(35):
    for corchea in range(64):
        button_c1 = tk.Button(frame_melodia, command=lambda arg = posicion_lista(tono, corchea): cambiar_color_e_indice(arg, 1), width=1, height=1, bg="black", font=("Helvetica", 5))

        if not (tono%7):
            button_c1.configure(bg=color_tonica)

        button_c1.grid(row=tono_r[tono], column=corchea, padx=0, pady=0)
        buttons_c1[posicion_lista(tono, corchea)] = button_c1

boton_play_pause = tk.Button(frame_melodia, text="Play", bg="black", fg="white", command=play_pause, width=1, height=1, font=("Helvetica", 18))
boton_play_pause.grid(row=36, column=65, padx=0, pady=0)


#Pestaña #3 Compás #2
#Pestaña #4 Compás #3
#Pestaña #5 Compás #4
#Pestaña #6 Compás #5
#Pestaña #7 Compás #6
#Pestaña #8 Compás #7
#Pestaña #9 Compás #8
#Pestaña #10 Letra


notebook.pack(fill='both', expand=True) #expande las pestañas

#Menú bar
menu_bar = tk.Menu(root)
menu_bar.config(bg="black", fg="snow")

# Crear el menú "Archivo"
archivo_menu = tk.Menu(menu_bar, tearoff=0)
archivo_menu.add_command(label="Abrir")
archivo_menu.add_command(label="Guardar")
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=root.quit)
archivo_menu.config(bg="black", fg="snow")

# Agregar el menú "Archivo" al menú bar
menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

# Crear el menú "Ayuda"
ayuda_menu = tk.Menu(menu_bar, tearoff=0)
ayuda_menu.add_command(label="Ayuda")
ayuda_menu.add_command(label="Dame un Cafe <3", command=cafe)
ayuda_menu.config(bg="black", fg="snow")

# Agregar el menú "Ayuda" al menú bar
menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)

# Asignar el menú bar a la ventana
root.config(menu=menu_bar)

#Atajos de Teclado

"""
1. <Enter>
2. <space>
3. <Tab>
4. <Shift>
5. <Control>
6. <Caps Lock>
7. <Alt>
8. <F1 - F12>
9. <Arrow Keys>
10. <Insert>
11. <Delete>
12. <Home>
13. <End>
14. <Page Up>
15. <Page Down>
"""

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

root.bind("<space>", lambda event: play_pause())


# Mostrar el notebook
notebook.pack()
root.mainloop()

activador = False
