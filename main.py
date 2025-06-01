'''Version 4.0    Autor: Jose Pablo Garcia Zamudio    Github: JPab-Dev'''
#Librerias ----------------------------------------------------------------------------------------------
import turtle as t
import time
import maps
import tkinter as tk
from tkinter import PhotoImage
import os
from collections import deque
from turtle import RawTurtle, ScrolledCanvas

#Ruta de assets -----------------------------------------------------------------------------------------
RUTA_TITULO_AMZ = os.path.join("Assets", "AMAZEZINGTtl.png")
RUTA_BOTONES = os.path.join("Assets", "Botones")
RUTA_PREVIEWS = os.path.join("Assets", "Preview")

#Variables  ---------------------------------------------------------------------------------------------
Tamaño_celda = 15
#Fuente en variable para que concuerden los textos:
fuente = ("Arial Black", 20)
colores = ["Rojo", "Azul", "Amarillo", "Verde", "Morado", "Naranja"]
botones_MenuPrincipal = [
        ("Maze 1", 1, 1, "Verde"), ("Maze 2", 2, 1, "Verde"),
        ("Maze 3", 1, 2, "Rojo"), ("Maze 4", 2, 2, "Rojo"),
        ("Maze 5", 1, 3, "Azul"), ("Maze 6", 2, 3, "Azul"),
        ("Random Maze", 1, 4, "Morado"),("Your Maze", 2, 4, "Naranja")
]
botones_VentanaLaberinto = [
        ("Return", 1, 1, "Rojo"), ("Start/Pause", 2, 1, "Amarillo"), 
        ("Restart", 3, 1, "Verde"), ("Extra", 4, 1, "Azul")
]
botones_random = [
        ("Easy", 1, 1, "Verde"), ("Medium", 2, 1, "Naranja"), ("Hard", 3, 1, "Rojo")
]

boton_create = [("Create", 0, 0, "Morado")]

#Funciones ----------------------------------------------------------------------------------------------
#Funcion para dibujar cuadrados:
def dibujar_cuadrado(turtle, x, y, color):

    #Configuracion basica del cuadrado:
    turtle.color(color)
    turtle.goto(x, y)

    #dibujo del cuadrado:
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(Tamaño_celda)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()

#Funcion para dibujar laberintos:
def dibujar_laberinto(turtle, laberinto):
    #Recorre las celdas del laberinto:
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            #centra el laberinto en el frame:
            screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda
            screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda

            #Guarda el valor de la celda actual:
            celda = laberinto[y][x]

            #Eleccion de colores de acuerdo a el simbolo:
            if celda == '#':
                dibujar_cuadrado(turtle, screen_x, screen_y, "black")

            elif celda == 'G':
                dibujar_cuadrado(turtle, screen_x, screen_y, "green")

            elif celda == 'S':
                dibujar_cuadrado(turtle, screen_x, screen_y, "blue")

            else:
                dibujar_cuadrado(turtle, screen_x, screen_y, "white")
 
#Funcion para encontrar el inicio del laberinto:
def encontrar_inicio(turtle, laberinto):
    #Recorre las celdas del laberinto:
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            #Detecta la celda con la letra S (Start):
            if laberinto[y][x] == 'S':
                
                #Coordenadas de S:
                screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda
                screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda

                #la tortuga se coloca en S
                turtle.penup()
                turtle.goto(screen_x + Tamaño_celda // 2, screen_y - Tamaño_celda // 2)
                turtle.setheading(0)

                #Devuelve la posicion de S:
                return x, y
    
    #Si no se encuentra S, manda un error:
    raise ValueError("No se encontró el punto de inicio en el laberinto.")

#Funcion para orientar tortuga depende a la direccion a la cual ira:
def orientacion_turtle(turtle, direccion):

    #Modifica el angulo de direccion de acuerdo a la direccion deseada:
    if direccion == (1,0):
        turtle.setheading(0)
    elif direccion == (0, 1):
        turtle.setheading(270)
    elif direccion == (-1, 0):
        turtle.setheading(180)
    elif direccion == (0, -1):
        turtle.setheading(90)

#Funcion para encontrar la meta con backtracking:
def buscar_meta(turtle, laberinto, x, y, visitados, ruta_actual):
    #En caso de que se encuentre la meta:
    if laberinto[y][x] == 'G':
        ruta_actual.append((x, y))
        screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
        screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
        turtle.goto(screen_x, screen_y)
        turtle.dot(10, "blue")  # Marca exacta sobre G
        turtle.hideturtle()
        turtle.getscreen().update()
        return True

    #Evitar repetir o chocar con muros:
    if (x, y) in visitados or laberinto[y][x] == '#':
        return False

    #Marca la celda actual como visitada para futuro conocimiento:
    visitados.add((x, y))
    ruta_actual.append((x, y))

    # Mover la tortuga a la celda actual
    screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
    screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
    turtle.goto(screen_x, screen_y)
    turtle.dot(10, "green")  # Celda explorada
    turtle.getscreen().update()
    time.sleep(0.02)

    # Direcciones: derecha, abajo, izquierda, arriba
    direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    #Explora en cada direccion:
    for dx, dy in direcciones:
        nuevo_x, nuevo_y = x + dx, y + dy

        if 0 <= nuevo_y < len(laberinto) and 0 <= nuevo_x < len(laberinto[0]):
            if laberinto[nuevo_y][nuevo_x] != '#' and (nuevo_x, nuevo_y) not in visitados:
                orientacion_turtle(turtle, (dx, dy))

                if buscar_meta(turtle, laberinto, nuevo_x, nuevo_y, visitados, ruta_actual):
                    turtle.dot(10, "blue")
                    return True

    # Punto sin salida se marca de color naranja:
    turtle.dot(10, "orange")

    # Retroceso físico
    ruta_actual.pop()
    if len(ruta_actual) > 0:
        paso_anterior = ruta_actual[-1]
        dx = paso_anterior[0] - x
        dy = paso_anterior[1] - y
        orientacion_turtle(turtle, (dx, dy))

        screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + paso_anterior[0] * Tamaño_celda + Tamaño_celda // 2
        screen_y = len(laberinto) * Tamaño_celda // 2 - paso_anterior[1] * Tamaño_celda - Tamaño_celda // 2
        turtle.goto(screen_x, screen_y)
        turtle.dot(10, "green")  # Camino correcto
        turtle.getscreen().update()
        time.sleep(0.02)

    return False

#Funcion para encontrar el camino mas eficiente del laberinto:
def camino_mas_corto(laberinto, inicio, meta):
    queue = deque()
    queue.append((inicio, [inicio]))
    visitados = set()
    visitados.add(inicio)

    while queue:
        (x, y), ruta = queue.popleft()

        if (x, y) == meta:
            return ruta
        
        for dx, dy in [(1,0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(laberinto) and 0 <= nx < len(laberinto[0]):
                if laberinto[ny][nx] != '#' and (nx, ny) not in visitados:
                    queue.append(((nx, ny), ruta + [(nx, ny)]))
                    visitados.add((nx, ny))
    return []

#Funcion para crear laberinto random:
def crear_random_maze(dificultad, alto, ancho, bifurcaciones):
    pass

#Funcion que imprime el laberinto a resolver:
def mostrar_laberinto(nombre, turtle):

    #Configuracion basica:
    turtle.screen.bgcolor("#292826")
    laberinto = maps.MAZE_DICC[nombre]

    # Dibuja laberinto sin animación
    dibujar_laberinto(turtle, laberinto)
    turtle._update()  # Dibuja todo de golpe
#'''
    # le otorga a la tortuga las coordenadas de las que debe empezar:
    x_inicio, y_inicio = encontrar_inicio(turtle, laberinto)

    #llamada a la funcion buscar_meta con backtracking
    ruta_actual = []
    visitados = set()
    buscar_meta(turtle, laberinto, x_inicio, y_inicio, visitados, ruta_actual)

    x_meta, y_meta = ruta_actual[-1]
    ruta_corta = camino_mas_corto(laberinto, (x_inicio, y_inicio), (x_meta, y_meta))

    turtle.showturtle()
    def pintar_paso(i=0):
        if i >= len(ruta_corta):
            return
        
        x, y = ruta_corta[i]
 
        # Orientar tortuga
        if i > 0:
            x_ant, y_ant = ruta_corta[i - 1]
            dx = x - x_ant
            dy = y - y_ant
            orientacion_turtle(turtle, (dx, dy))

        # Mover y pintar
        screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
        screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
        turtle.goto(screen_x, screen_y)
        turtle.dot(10, "blue")
        turtle.getscreen().update()
        
        # Llama al siguiente paso después de 50 ms
        turtle.screen.ontimer(lambda: pintar_paso(i + 1), 50)

    # Comienza la animación con el primer paso
    pintar_paso()
#'''

#Funcion para crear la ventana donde se mostrara el laberinto y su informacion/resolucion:
def crear_ventana_laberinto(nombre_laberinto):
    #Configuracion basica de la ventana que mostrara el laberinto:
    ventana_laberinto = tk.Tk()
    ventana_laberinto.title(f'Laberinto - {nombre_laberinto}')
    ventana_laberinto.geometry("1000x670")
    ventana_laberinto.configure(bg="#292826")
    ventana_laberinto.resizable(False, False)

    #Frame izquierdo (lugar donde se muestra la resolucion del laberinto):
    frame_laberinto = tk.Frame(ventana_laberinto, bg="#92149D")
    frame_laberinto.place(x=10, y=10, width=650, height=550)

    #mostrar la resolucion del laberinto llamando a la funcion mostrar_laberinto():
    canvas_turtle = ScrolledCanvas(frame_laberinto, width=650, height=550)
    canvas_turtle.pack()
    turtle = RawTurtle(canvas_turtle)
    turtle.speed("fastest")
    turtle.penup()
    turtle.hideturtle()
    turtle._tracer(0, 0)
    turtle.screen.bgcolor("#292826")

    #Frame derecho (Informacion del laberinto)
    frame_info = tk.Frame(ventana_laberinto, bg="#3EA44F")
    frame_info.place(x=670, y=10, width=315, height=550)

    # Canvas para botones (abajo de los recuadros):
    frame_canvas = tk.Frame(ventana_laberinto, bg="#292826")
    frame_canvas.place(x=0, y=570, width=1000, height=130)

    canvas = tk.Canvas(frame_canvas, width=1000, height=130, bg="#292826", highlightthickness=0)
    canvas.pack()

    #Cargar botones:
    botones_on = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}On.png')) for color in colores}
    botones_off = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}Off.png')) for color in colores}

    espacio_x = 251
    espacio_y = 85

    #Botones con efecto al ser presionados:
    for texto, col, fila, color in botones_VentanaLaberinto:
        x = espacio_x * col - espacio_x / 2
        y = espacio_y * fila - espacio_y / 2

        imagen_id = canvas.create_image(x, y + 2, image=botones_off[color])
        sombra_id = canvas.create_text(x + 2, y + 2, text=texto, font=fuente, fill="black")
        texto_id = canvas.create_text(x, y, text=texto, font=fuente, fill="white")

        def al_presionar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color):
            canvas.itemconfig(img, image=botones_on[col])
            canvas.itemconfig(txt, fill="gray")
            canvas.move(txt, 0, 6)
            canvas.move(sombra, 0, 6)

        def al_soltar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color, nombre_boton=texto):
            canvas.itemconfig(img, image=botones_off[col])
            canvas.itemconfig(txt, fill="white")
            canvas.move(txt, 0, -6)
            canvas.move(sombra, 0, -6)

            #Diferentes comandos dependiendo del boton
            if nombre_boton == "Return":
                ventana_laberinto.destroy()
                menu_principal()
            elif nombre_boton == "Start/Pause":
                mostrar_laberinto(nombre_laberinto, turtle)
            elif nombre_boton == "Restart":
                turtle.clear()
                turtle.reset()
                turtle.speed("fastest")
                turtle.penup()
                turtle.hideturtle()
                turtle._tracer(0, 0)
                turtle.screen.bgcolor("#292826")
                mostrar_laberinto(nombre_laberinto, turtle)  # Redibuja el laberinto
            elif nombre_boton == "Extra":
                pass

        for item in [imagen_id, texto_id, sombra_id]:
            canvas.tag_bind(item, "<ButtonPress-1>", al_presionar)
            canvas.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    ventana_laberinto.mainloop()
    return ventana_laberinto, turtle

#Funcion que crea la ventana de ajustes para crear el laberinto random:
def ventana_random_Maze():
    ventana_random = tk.Tk()
    ventana_random.title('Random Maze Settings')
    ventana_random.geometry("1000x540")
    ventana_random.configure(bg="#292826")
    ventana_random.resizable(False, False)

    #Texto para elegir la dificultad
    etiqueta_titulo = tk.Label(ventana_random, text="Elige la dificultad del laberinto:", font=fuente, fg="white", bg="#292826")
    etiqueta_titulo.pack(pady=20)

    #frame para los botones de dificultad
    frame_dificultad = tk.Frame(ventana_random, bg="#292826")
    frame_dificultad.place(x=40, y=70, width=1000, height=130)

    canvas_dificultad = tk.Canvas(frame_dificultad, width=1000, height=130, bg="#292826", highlightthickness=0)
    canvas_dificultad.pack()

    botones_on = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}On.png')) for color in colores}
    botones_off = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}Off.png')) for color in colores}

    espacio_x = 300
    espacio_y = 65

    estado_seleccion = {"actual": None}
    botones_ids = {}

    #Botones de dificultad
    for texto, col, fila, color in botones_random:
        x = espacio_x * col - espacio_x / 2
        y = espacio_y * fila - espacio_y / 2

        imagen_id = canvas_dificultad.create_image(x, y + 2, image=botones_off[color])
        sombra_id = canvas_dificultad.create_text(x + 2, y + 2, text=texto, font=fuente, fill="black")
        texto_id = canvas_dificultad.create_text(x, y, text=texto, font=fuente, fill="white")

        botones_ids[texto] = (imagen_id, texto_id, sombra_id, color)

        def al_soltar(event, nombre_boton=texto):
            if estado_seleccion["actual"] and estado_seleccion["actual"] != nombre_boton:
                img_id, txt_id, sombra_id, col_ant = botones_ids[estado_seleccion["actual"]]
                canvas_dificultad.itemconfig(img_id, image=botones_off[col_ant])
                canvas_dificultad.itemconfig(txt_id, fill="white")
                canvas_dificultad.move(txt_id, 0, -6)
                canvas_dificultad.move(sombra_id, 0, -6)

            img_id, txt_id, sombra_id, col = botones_ids[nombre_boton]
            canvas_dificultad.itemconfig(img_id, image=botones_on[col])
            canvas_dificultad.itemconfig(txt_id, fill="gray")
            canvas_dificultad.move(txt_id, 0, 6)
            canvas_dificultad.move(sombra_id, 0, 6)
            estado_seleccion["actual"] = nombre_boton

            #Liberar botón Create si sigue bloqueado
            if "Create" in botones_ids:
                img_c, txt_c, sombra_c, col_c = botones_ids["Create"]
                if canvas_create.itemcget(txt_c, "fill") == "gray":
                    canvas_create.itemconfig(img_c, image=botones_off[col_c])
                    canvas_create.itemconfig(txt_c, fill="white")
                    canvas_create.move(txt_c, 0, -6)
                    canvas_create.move(sombra_c, 0, -6)

        for item in [imagen_id, texto_id, sombra_id]:
            canvas_dificultad.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    #Sliders para elegir el tamaño y las bifurcaciones
    tk.Label(ventana_random, text="Elige las dimensiones del laberinto:", font=fuente, fg="white", bg="#292826").place(x=300, y=170)

    tk.Label(ventana_random, text="Alto:", font=fuente, fg="white", bg="#292826").place(x=180, y=230)
    slider_alto = tk.Scale(ventana_random, from_=15, to=40, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#81F1CA", highlightthickness=0)
    slider_alto.set(20)
    slider_alto.place(x=240, y=220)

    tk.Label(ventana_random, text="Ancho:", font=fuente, fg="white", bg="#292826").place(x=155, y=280)
    slider_ancho = tk.Scale(ventana_random, from_=15, to=40, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#FFF152", highlightthickness=0)
    slider_ancho.set(20)
    slider_ancho.place(x=240, y=270)

    tk.Label(ventana_random, text="Elige cantidad de bifurcaciones:", font=fuente, fg="white", bg="#292826").place(x=320, y=340)
    slider_bif = tk.Scale(ventana_random, from_=1, to=10, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#63DCF5", highlightthickness=0)
    slider_bif.set(5)
    slider_bif.place(x=240, y=380)

    #Canvas para el botón Create abajo
    frame_create = tk.Frame(ventana_random, bg="#292826")
    frame_create.place(x=0, y=450, width=1000, height=100)

    canvas_create = tk.Canvas(frame_create, width=1000, height=100, bg="#292826", highlightthickness=0)
    canvas_create.pack()

    # Botón Create
    for texto, col, fila, color in boton_create:
        x = 800
        y = 40

        imagen_id = canvas_create.create_image(x, y + 2, image=botones_on[color])
        sombra_id = canvas_create.create_text(x + 2, y + 2, text=texto, font=fuente, fill="black")
        texto_id = canvas_create.create_text(x, y, text=texto, font=fuente, fill="gray")

        botones_ids[texto] = (imagen_id, texto_id, sombra_id, color)

        def al_soltar_create(event, nombre_boton=texto):
            if canvas_create.itemcget(texto_id, "fill") == "gray":
                return

            canvas_create.itemconfig(imagen_id, image=botones_on[color])
            canvas_create.itemconfig(texto_id, fill="gray")
            canvas_create.move(texto_id, 0, 6)
            canvas_create.move(sombra_id, 0, 6)

            ventana_random.after(150, lambda: (
                canvas_create.itemconfig(imagen_id, image=botones_off[color]),
                canvas_create.itemconfig(texto_id, fill="white"),
                canvas_create.move(texto_id, 0, -6),
                canvas_create.move(sombra_id, 0, -6),
                crear_laberinto()
            ))

        for item in [imagen_id, texto_id, sombra_id]:
            canvas_create.tag_bind(item, "<ButtonRelease-1>", al_soltar_create)

    #Función de creación
    def crear_laberinto():
        dificultad = estado_seleccion["actual"]
        alto = slider_alto.get()
        ancho = slider_ancho.get()
        bif = slider_bif.get()
        print(f"Generando laberinto con dificultad={dificultad}, alto={alto}, ancho={ancho}, bifurcaciones={bif}")
        #crear_random_maze()

    ventana_random.mainloop()

#Funcion main (llama las funciones anteriores en el orden deseado) --------------------------------------
def menu_principal():

    #Configuracion de la ventana:
    menu_principal = tk.Tk()
    menu_principal.title("A-MAZE-ZING")
    menu_principal.geometry("525x750")
    menu_principal.configure(bg="#292826")
    menu_principal.resizable(False, False)

    #Agregar el logo de la aplicacion:
    Titulo_Amazezing = PhotoImage(file=RUTA_TITULO_AMZ)
    frame_titulo = tk.Frame(menu_principal, bg="#292826")
    frame_titulo.pack(pady=10)
    tk.Label(frame_titulo, image=Titulo_Amazezing, bg="#292826").pack(pady=10)

    #Canvas para botones:
    frame_canvas = tk.Frame(menu_principal, bg="#292826")
    frame_canvas.pack()
    canvas = tk.Canvas(frame_canvas, width=1100, height=340, bg="#292826", highlightthickness=0)
    canvas.pack()

    #Cargar botones:
    botones_on = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}On.png')) for color in colores}
    botones_off = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{color}Off.png')) for color in colores}

    #Diccionario para guardar previews:
    previews = {}
    for texto, _, _, _ in botones_MenuPrincipal:
        numero = ''.join(filter(str.isdigit, texto))
        if numero:
            nombre_preview = f"Maze{numero}_preview.png"
            ruta_preview = os.path.join(RUTA_PREVIEWS, nombre_preview)
            if os.path.exists(ruta_preview):
                previews[texto] = PhotoImage(file=ruta_preview)

    #Label de preview oculto:
    label_preview = tk.Label(menu_principal, bg="#292826")
    
    espacio_x = 260
    espacio_y = 85

    #Botones con efecto al ser presionados:
    for texto, col, fila, color in botones_MenuPrincipal:
        x = espacio_x * col - espacio_x / 2
        y = espacio_y * fila - espacio_y / 2

        imagen_id = canvas.create_image(x, y + 2, image=botones_off[color])
        sombra_id = canvas.create_text(x + 2, y + 2, text=texto, font=fuente, fill="black")
        texto_id = canvas.create_text(x, y, text=texto, font=fuente, fill="white")

        def al_presionar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color):
            canvas.itemconfig(img, image=botones_on[col])
            canvas.itemconfig(txt, fill="gray")
            canvas.move(txt, 0, 6)
            canvas.move(sombra, 0, 6)

        def al_soltar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color, nombre=texto):
            canvas.itemconfig(img, image=botones_off[col])
            canvas.itemconfig(txt, fill="white")
            canvas.move(txt, 0, -6)
            canvas.move(sombra, 0, -6)
            if nombre == "Random Maze":
                abrir_ventana_random()
            elif nombre == "Your Maze":
                pass
            else:
                abrir_ventana_laberinto(nombre)

        #Cambia el texto a gris cuando el mouse entra
        def resaltar_texto(event, txt=texto_id):  
            canvas.itemconfig(txt, fill="yellow")    

        #Restaura el texto a blanco cuando el mouse sale
        def restaurar_texto(event, txt=texto_id):  
            canvas.itemconfig(txt, fill="white")   

        #Funciones para mostrar/ocultar preview según el botón
        def mostrar_preview(event, nombre=texto):
            if nombre in previews:
                label_preview.config(image=previews[nombre])
                x = event.x_root - menu_principal.winfo_rootx() + 5
                y = event.y_root - menu_principal.winfo_rooty() + 14
                label_preview.place(x=x, y=y)

        def mover_preview(event, nombre=texto):
            if nombre in previews:
                x = event.x_root - menu_principal.winfo_rootx() + 5
                y = event.y_root - menu_principal.winfo_rooty() + 14
                label_preview.place(x=x, y=y)

        def ocultar_preview(event):
            label_preview.place_forget()

        def al_entrar(event, nombre=texto, txt=texto_id):  
            resaltar_texto(event, txt=txt)                 
            mostrar_preview(event, nombre=nombre)          

        def al_salir(event, txt=texto_id):                
            restaurar_texto(event, txt=txt)                
            ocultar_preview(event)                         

        for item in [imagen_id, texto_id, sombra_id]:
            canvas.tag_bind(item, "<Enter>", al_entrar)           
            canvas.tag_bind(item, "<Motion>", mover_preview) 
            canvas.tag_bind(item, "<Leave>", al_salir)           
            canvas.tag_bind(item, "<ButtonPress-1>", al_presionar)
            canvas.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    #Funcion para cerrar la ventana del menu al seleccionar laberinto:
    def abrir_ventana_laberinto(nombre):
        menu_principal.destroy()
        crear_ventana_laberinto(nombre)

    def abrir_ventana_random():
        menu_principal.destroy()
        ventana_random_Maze()

    #Texto con derechos de autor en el inferior de la ventana:
    derechos_autor = tk.Label(
        menu_principal,
        text="Developed by Jose Pablo Garcia Zamudio. All rights reserved.",
        font=("Arial", 16),
        fg="white",
        bg="#292826"
    )
    derechos_autor.pack(side="bottom", pady=5)

    menu_principal.mainloop()

#Ejecucion de la funcion main:
if __name__ == "__main__":
    menu_principal()