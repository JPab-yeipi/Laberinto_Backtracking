'''Version 4.5    Autor: Jose Pablo Garcia Zamudio    Github: JPab-Dev'''
#Librerias ----------------------------------------------------------------------------------------------
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
#Colores disponibles de botones:
colores = ["Rojo", "Azul", "Amarillo", "Verde", "Morado", "Naranja"]
#Distribucion de botones para su respectiva ventana:
botones_MenuPrincipal = [
        ("Maze 1", 1, 1, "Verde"), ("Maze 2", 2, 1, "Verde"),
        ("Maze 3", 1, 2, "Rojo"), ("Maze 4", 2, 2, "Rojo"),
        ("Maze 5", 1, 3, "Azul"), ("Maze 6", 2, 3, "Azul"),
        ("Random Maze", 1, 4, "Morado"),("Your Maze", 2, 4, "Naranja")
]
botones_VentanaLaberinto = [
        ("Return", 1, 1, "Rojo"), ("Start", 2, 1, "Azul"), 
        ("Restart", 3, 1, "Verde")
]
botones_random = [
        ("Easy", 1, 1, "Verde"), ("Medium", 2, 1, "Naranja"), ("Hard", 3, 1, "Rojo")
]
boton_create = [("Create", 0, 0, "Morado")]
boton_aviso = [("Return", 0, 0, "Rojo")]

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

            #Eleccion de colores de acuerdo a el simbolo del laberinto:
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

#Funcion para encontrar el camino mas eficiente del laberinto:
def camino_mas_corto(laberinto, inicio, meta):
    #Inicializa ruta desde el inicio y lo marca como visitado
    queue = deque()
    queue.append((inicio, [inicio]))
    visitados = set()
    visitados.add(inicio)

    #Movimientos posibles que puede tomar la tortuga 
    direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while queue:
        # Saca de la cola la posición actual y su ruta acumulada
        (x, y), ruta = queue.popleft()

        #Si la posicion actual es la meta, devuelve la ruta
        if (x, y) == meta:
            return ruta
        
        #Recorre el laberinto y va marcando las coordenadas visitadas
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(laberinto) and 0 <= nx < len(laberinto[0]):
                if laberinto[ny][nx] != '#' and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    queue.append(((nx, ny), ruta + [(nx, ny)]))

    #Si no se encuentra la meta, se devuelve una lista vacia
    return []

def crear_random_desde_ajustes(alto, ancho, bif, dificultad, ventana_a_cerrar=None):
    # Genera el laberinto random llamando a la funcion en maps
    lab = maps.crear_random_maze(alto, ancho, porcentaje_libres=dificultad, bifurcaciones=bif)

    # Inserta laberinto en el diccionario
    maps.MAZE_DICC["Random Maze"] = lab

    # Cierra ventana anterior 
    if ventana_a_cerrar:
        ventana_a_cerrar.destroy()

    # Abre la ventana de laberinto con el nuevo laberinto random
    crear_ventana_laberinto("Random Maze")

#Funcion para crear la ventana donde se mostrara el laberinto y su informacion/resolucion:
def crear_ventana_laberinto(nombre_laberinto):

    # Configuración básica de la ventana
    ventana_laberinto = tk.Tk()
    ventana_laberinto.title(nombre_laberinto)

    # Centrar la ventana en la pantalla, hacer que aparezca al frente y que no se pueda mover el tamaño
    screen_w = ventana_laberinto.winfo_screenwidth()
    screen_h = ventana_laberinto.winfo_screenheight()
    x = (screen_w - 1000) // 2
    y = (screen_h - 670) // 2
    ventana_laberinto.geometry(f"1000x670+{x}+{y}")
    ventana_laberinto.attributes("-topmost", True)
    ventana_laberinto.configure(bg="#292826")
    ventana_laberinto.resizable(False, False)

    # Frame izquierdo (la tortuga resolviendo el laberinto)
    frame_laberinto = tk.Frame(ventana_laberinto, bg="#292826")
    frame_laberinto.place(x=10, y=10, width=650, height=550)

    # Configuracion de la tortuga:
    canvas_turtle = ScrolledCanvas(frame_laberinto, width=650, height=550)
    canvas_turtle.pack()
    turtle = RawTurtle(canvas_turtle)
    turtle.speed("fastest")
    turtle.penup()
    turtle._tracer(0, 0)
    turtle.screen.bgcolor("#292826")
    turtle.showturtle()

    # Estado de animación controlado por botones
    estado_animacion = {"activa": False, "cancelada": False}

    # Obtener el laberinto desde el diccionario
    laberinto = maps.MAZE_DICC[nombre_laberinto]

    # Obtener informacion del laberinto
    alto = len(laberinto)
    ancho = len(laberinto[0])
    total_celdas = alto * ancho
    muros = sum(row.count('#') for row in laberinto)
    densidad_mu = round((muros / total_celdas) * 100, 2)

    # Encontrar coordenadas de inicio y de la meta para mostrar en la informacion
    coord_inicio = None
    coord_meta = None
    for y in range(alto):
        for x in range(ancho):
            if laberinto[y][x] == 'S':
                coord_inicio = (x, y)
            elif laberinto[y][x] == 'G':
                coord_meta = (x, y)
    if coord_inicio is None: coord_inicio = ("N/A", "N/A")
    if coord_meta is None: coord_meta = ("N/A", "N/A")

    # Detectar bifurcaciones (celdas con >2 vecinos libres)
    bifurcaciones = []
    for y in range(alto):
        for x in range(ancho):
            if laberinto[y][x] != '#':
                libres = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= ny < alto and 0 <= nx < ancho and laberinto[ny][nx] != '#':
                        libres += 1
                if libres > 2:
                    bifurcaciones.append((x, y))
    num_bifurc = len(bifurcaciones)

    # Dibujar el laberinto al abrir la ventana, pero sin resolver
    turtle.clear()
    dibujar_laberinto(turtle, laberinto)
    turtle._update()

    # Frame derecho (informacion del laberinto)
    frame_info = tk.Frame(ventana_laberinto, bg="#3EA44F")
    frame_info.place(x=670, y=10, width=315, height=550)

    # Altura para el título
    label_altura = 40

    # Titulo con el nombre del laberinto
    lbl_nombre = tk.Label(
        frame_info,
        text=nombre_laberinto,
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#3EA44F"
    )
    lbl_nombre.place(x=0, y=0, width=315, height=label_altura)

    #Configuracion del espacio donde se mostrara la informacion del laberinto:
    txt_info = tk.Text(
        frame_info,
        font=("Courier", 14),
        bg="white",
        fg="black"
    )
    txt_info.place(
        x=5,
        y=label_altura + 5,
        width=305,
        height=550 - (label_altura + 10)
    )
    txt_info.configure(state="disabled")

    # Agregar tag para texto en bold
    txt_info.tag_configure("bold", font=("Courier", 14, "bold"))

    def agregar_linea_info(texto, tag=None):
        txt_info.configure(state="normal")
        if tag:
            txt_info.insert("end", texto + "\n", tag)
        else:
            txt_info.insert("end", texto + "\n")
        txt_info.see("end")
        txt_info.configure(state="disabled")

    # Frame inferior para botones
    frame_canvas = tk.Frame(ventana_laberinto, bg="#292826")
    frame_canvas.place(x=0, y=570, width=1000, height=130)

    canvas = tk.Canvas(frame_canvas, width=1000, height=130, bg="#292826", highlightthickness=0)
    canvas.pack()

    # Cargar imágenes ON/OFF según colores definidos globalmente
    botones_on  = {c: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{c}On.png'))  for c in colores}
    botones_off = {c: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{c}Off.png')) for c in colores}

    espacio_x = 335
    espacio_y = 85

    # Diccionario para guardar referencias y estado de cada botón
    botones_ids = {}

    # Mostrar laberinto con informacion basica
    def mostrar_laberinto(nombre, turtle, estado_animacion):
        # Limpiar contenido previo
        txt_info.configure(state="normal")
        txt_info.delete("1.0", "end")
        txt_info.configure(state="disabled")

        # Mostrar datos basicos al inicio
        agregar_linea_info(f"Tamaño: {ancho}×{alto}")
        agregar_linea_info(f"Celdas totales: {total_celdas}")
        agregar_linea_info(f"Muros (#): {muros}")
        agregar_linea_info(f"Densidad muros: {densidad_mu}%")
        agregar_linea_info("")
        agregar_linea_info(f"Inicio (S): {coord_inicio}")
        agregar_linea_info(f"Meta (G): {coord_meta}")
        agregar_linea_info("")
        agregar_linea_info(f"Bifurcaciones: {num_bifurc}")
        agregar_linea_info(f"Coords bifurcaciones: {bifurcaciones}")
        agregar_linea_info("")

        # Variables para contar nodos visitados y cronometrar
        nodos_visitados = 0
        tiempo_ini_busqueda = time.time()

        # Dibujar laberinto base
        turtle.clear()
        dibujar_laberinto(turtle, laberinto)
        turtle._update()
        turtle.showturtle()
        agregar_linea_info("Estado: Explorando...")

        if estado_animacion["cancelada"]:
            estado_animacion["cancelada"] = False
            estado_animacion["activa"] = False
            return

        if estado_animacion["activa"]:
            return  # Evita ejecuciones duplicadas

        #Se inicia en coordenadas de inicio y se inicializa ruta_actual, visitados y estado_animacion a 0
        x_ini, y_ini = coord_inicio if isinstance(coord_inicio, tuple) else encontrar_inicio(turtle, laberinto)
        ruta_actual = []
        visitados = set()
        estado_animacion["activa"] = True

        # buscar la meta por backtracking
        def buscar_meta_ext(turtle, laberinto, x, y, visitados, ruta_actual, estado_animacion):
            nonlocal nodos_visitados
            if estado_animacion["cancelada"]:
                return False

            # Contar y mostrar nodo visitado con coordenada
            if (x, y) not in visitados:
                nodos_visitados += 1
                agregar_linea_info(f"Nodos visitados: {nodos_visitados}, ({x}, {y})")

            # Si encuentra la celda G, registra la posicion en la ruta
            if laberinto[y][x] == 'G':
                ruta_actual.append((x, y))
                screen_x = -ancho * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
                screen_y = alto * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
                turtle.goto(screen_x, screen_y)
                turtle.dot(10, "blue")
                turtle.getscreen().update()
                return True

            # Si hay un muro o el camino ya fue visitado, no se recorre
            if (x, y) in visitados or laberinto[y][x] == '#':
                return False

            # Marca la posición (x, y) como visitada y la agrega a la ruta actual
            visitados.add((x, y))
            ruta_actual.append((x, y))
            screen_x = -ancho * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
            screen_y = alto * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
            turtle.goto(screen_x, screen_y)
            turtle.dot(10, "green")
            turtle.getscreen().update()
            time.sleep(0.02)
            if estado_animacion["cancelada"]:
                return False

            # Explora vecinos libres, orienta la tortuga y llama recursivamente; retorna True si halla la meta:
            direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= ny < alto and 0 <= nx < ancho and laberinto[ny][nx] != '#' and (nx, ny) not in visitados:
                    orientacion_turtle(turtle, (dx, dy))
                    if buscar_meta_ext(turtle, laberinto, nx, ny, visitados, ruta_actual, estado_animacion):
                        return True

            #Pinta de naranja los caminos en donde la tortuga se regresa
            turtle.dot(10, "orange")
            ruta_actual.pop()

            if ruta_actual:
                xa, ya = ruta_actual[-1]
                dx = xa - x
                dy = ya - y
                orientacion_turtle(turtle, (dx, dy))
                sx = -ancho * Tamaño_celda // 2 + xa * Tamaño_celda + Tamaño_celda // 2
                sy = alto * Tamaño_celda // 2 - ya * Tamaño_celda - Tamaño_celda // 2
                turtle.goto(sx, sy)
                #pinta de verde el camino actual para ir mostrando la solucion de la tortuga por backtracking:
                turtle.dot(10, "green")
                turtle.getscreen().update()
                time.sleep(0.02)
                if estado_animacion["cancelada"]:
                    return False

            return False

        #Se llama a la funcion de buscar meta para la animacion de la tortuga:
        buscar_meta_ext(turtle, laberinto, x_ini, y_ini, visitados, ruta_actual, estado_animacion)

        #Añade el tiempo de busqueda a la informacion del laberinto:
        tiempo_fin_busqueda = time.time()
        duracion_busqueda = round(tiempo_fin_busqueda - tiempo_ini_busqueda, 3)
        agregar_linea_info("")
        agregar_linea_info(f"Tiempo búsqueda: {duracion_busqueda} s")
        agregar_linea_info("")

        if not ruta_actual:
            estado_animacion["activa"] = False
            return

        x_meta, y_meta = ruta_actual[-1]
        ruta_corta = camino_mas_corto(laberinto, (x_ini, y_ini), (x_meta, y_meta))
        longitud_ruta = len(ruta_corta)

        #Se agrega las coordenadas de la ruta mas optima en la informacion:
        agregar_linea_info(f"Longitud ruta óptima: {longitud_ruta} pasos")
        agregar_linea_info("")
        agregar_linea_info("Camino más corto:")
        for coord in ruta_corta:

            # Inserta cada coordenada en negrita
            txt_info.configure(state="normal")
            txt_info.insert("end", f"  {coord}\n", "bold")
            txt_info.see("end")
            txt_info.configure(state="disabled")
        agregar_linea_info("")

        # Pintar paso a paso con porcentaje y tiempo
        tiempo_ini_pintar = time.time()
        agregar_linea_info("Estado: Dibujando ruta óptima...")

        def pintar_paso(i=0):
            if i >= longitud_ruta or estado_animacion["cancelada"]:
                estado_animacion["activa"] = False
                estado_animacion["cancelada"] = False
                tiempo_fin_pintar = time.time()
                duracion_pintar = round(tiempo_fin_pintar - tiempo_ini_pintar, 3)
                agregar_linea_info(f"Tiempo pintar ruta: {duracion_pintar} s")
                return

            x_c, y_c = ruta_corta[i]
            porcentaje = int(((i + 1) / longitud_ruta) * 100)

            # Insertar texto "Solución paso i/M " y luego coordenada en negrita
            txt_info.configure(state="normal")
            txt_info.insert("end", f"Solución paso {i+1}/{longitud_ruta} ({porcentaje}%) ", )
            txt_info.insert("end", f"({x_c}, {y_c})\n", "bold")
            txt_info.see("end")
            txt_info.configure(state="disabled")

            if i > 0:
                x_a, y_a = ruta_corta[i - 1]
                dx = x_c - x_a
                dy = y_c - y_a
                orientacion_turtle(turtle, (dx, dy))

            sx = -ancho * Tamaño_celda // 2 + x_c * Tamaño_celda + Tamaño_celda // 2
            sy = alto * Tamaño_celda // 2 - y_c * Tamaño_celda - Tamaño_celda // 2
            turtle.goto(sx, sy)
            turtle.dot(10, "blue")
            turtle.getscreen().update()

            turtle.screen.ontimer(lambda: pintar_paso(i + 1), 50)

        pintar_paso()

    # Crear los botones (Return, Start, Restart)
    for texto, col, fila, color in botones_VentanaLaberinto:
        x_btn = espacio_x * col - espacio_x // 2
        y_btn = espacio_y * fila - espacio_y // 2

        img_id = canvas.create_image(x_btn, y_btn + 2, image=botones_off[color])
        sombra_id = canvas.create_text(x_btn + 2, y_btn + 2, text=texto, font=fuente, fill="black")
        txt_id    = canvas.create_text(x_btn, y_btn, text=texto, font=fuente, fill="white")

        botones_ids[texto] = {
            "imagen": img_id,
            "texto": txt_id,
            "sombra": sombra_id,
            "color": color,
            "habilitado": True
        }

        #Efecto de los botones al ser presionados:
        def al_presionar(event, btn=texto):
            info = botones_ids[btn]
            if btn == "Start" and not info["habilitado"]:
                return
            canvas.itemconfig(info["imagen"], image=botones_on[info["color"]])
            canvas.itemconfig(info["texto"], fill="gray")
            canvas.move(info["texto"], 0, 6)
            canvas.move(info["sombra"], 0, 6)

        def al_soltar(event, btn=texto):
            info = botones_ids[btn]
            if btn == "Start" and not info["habilitado"]:
                return

            if btn != "Start":
                canvas.itemconfig(info["imagen"], image=botones_off[info["color"]])
                canvas.itemconfig(info["texto"], fill="white")
                canvas.move(info["texto"], 0, -6)
                canvas.move(info["sombra"], 0, -6)
            else:
                info["habilitado"] = False

            #Funcion de boton dependiendo al nombre:
            if btn == "Return":
                ventana_laberinto.destroy()
                menu_principal()

            elif btn == "Start":
                if not estado_animacion["activa"]:
                    mostrar_laberinto(nombre_laberinto, turtle, estado_animacion)

            elif btn == "Restart":
                ventana_laberinto.destroy()
                crear_ventana_laberinto(nombre_laberinto)

        for item in (img_id, txt_id, sombra_id):
            canvas.tag_bind(item, "<ButtonPress-1>", al_presionar)
            canvas.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    ventana_laberinto.mainloop()

#Funcion que crea la ventana de ajustes para crear el laberinto random:
def ventana_random_Maze():
    ventana_random = tk.Tk()
    ventana_random.title('Random Maze Settings')
    #Abre la ventana al frente y al centro de la pantalla
    screen_w = ventana_random.winfo_screenwidth()
    screen_h = ventana_random.winfo_screenheight()
    x = (screen_w - 1000) // 2
    y = (screen_h - 540) // 2
    ventana_random.geometry(f"1000x540+{x}+{y}")
    ventana_random.attributes("-topmost", True)
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

    estado_seleccion = {"actual_nombre": None, "actual_valor": None}
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
            if estado_seleccion["actual_nombre"] and estado_seleccion["actual_nombre"] != nombre_boton:
                img_id, txt_id, sombra_id, col_ant = botones_ids[estado_seleccion["actual_nombre"]]
                canvas_dificultad.itemconfig(img_id, image=botones_off[col_ant])
                canvas_dificultad.itemconfig(txt_id, fill="white")
                canvas_dificultad.move(txt_id, 0, -6)
                canvas_dificultad.move(sombra_id, 0, -6)

            img_id, txt_id, sombra_id, col = botones_ids[nombre_boton]
            canvas_dificultad.itemconfig(img_id, image=botones_on[col])
            canvas_dificultad.itemconfig(txt_id, fill="gray")
            canvas_dificultad.move(txt_id, 0, 6)
            canvas_dificultad.move(sombra_id, 0, 6)
            niveles_dificultad = {
                "Easy": 0.50,
                "Medium": 0.35,
                "Hard": 0.20
            }
            estado_seleccion["actual_nombre"] = nombre_boton
            estado_seleccion["actual_valor"] = niveles_dificultad.get(nombre_boton)

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
    slider_alto = tk.Scale(ventana_random, from_=15, to=35, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#81F1CA", highlightthickness=0)
    slider_alto.set(20)
    slider_alto.place(x=240, y=220)

    tk.Label(ventana_random, text="Ancho:", font=fuente, fg="white", bg="#292826").place(x=155, y=280)
    slider_ancho = tk.Scale(ventana_random, from_=15, to=35, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#FFF152", highlightthickness=0)
    slider_ancho.set(20)
    slider_ancho.place(x=240, y=270)

    tk.Label(ventana_random, text="Elige porcentaje de bifurcaciones:", font=fuente, fg="white", bg="#292826").place(x=312, y=340)
    slider_bif = tk.Scale(ventana_random, from_=1, to=20, orient="horizontal", length=500, bg="#292826", fg="white", troughcolor="#63DCF5", highlightthickness=0)
    slider_bif.set(5)
    slider_bif.place(x=240, y=380)

    #Canvas para el botón Create abajo
    frame_create = tk.Frame(ventana_random, bg="#292826")
    frame_create.place(x=0, y=450, width=1000, height=100)

    canvas_create = tk.Canvas(frame_create, width=1000, height=100, bg="#292826", highlightthickness=0)
    canvas_create.pack()

    # Boton Create, ajustes para dar efecto al boton:
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

    #Función de creacion del laberinto con un mensaje en la terminal con los ajustes elegidos:
    def crear_laberinto():
        dificultad = estado_seleccion["actual_valor"]
        alto = slider_alto.get()
        ancho = slider_ancho.get()
        bif = slider_bif.get()
        print(f"Generando laberinto con dificultad={dificultad}, alto={alto}, ancho={ancho}, bifurcaciones={bif}")
        crear_random_desde_ajustes(
            alto=slider_alto.get(),
            ancho=slider_ancho.get(),
            bif=slider_bif.get(),
            dificultad = estado_seleccion["actual_valor"],
            ventana_a_cerrar=ventana_random
        )

    ventana_random.mainloop()

#Funcion que muestra una ventana con un aviso de alerta
def aviso_laberinto_vacio():
    # Ventana de aviso cuando no hay laberinto importado
    ventana_aviso = tk.Tk()
    ventana_aviso.title("Aviso")
    # Centrar en pantalla y abrirla al frente:
    screen_w = ventana_aviso.winfo_screenwidth()
    screen_h = ventana_aviso.winfo_screenheight()
    w, h = 400, 200
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    ventana_aviso.geometry(f"{w}x{h}+{x}+{y}")
    ventana_aviso.attributes("-topmost", True)
    ventana_aviso.configure(bg="#292826")
    ventana_aviso.resizable(False, False)

    # Mensaje de aviso:
    mensaje = tk.Label(
        ventana_aviso,
        text="No se encontró ningún laberinto\n"
            "importado, Accede a maps.py para\n"
             "importar tu laberinto.",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#292826",
        justify="center"
    )
    mensaje.pack(pady=(30, 20))

    # Frame para el boton unico
    frame_bot = tk.Frame(ventana_aviso, bg="#292826")
    frame_bot.place(x=0, y=120, width=w, height=80)

    canvas = tk.Canvas(frame_bot, width=w, height=80, bg="#292826", highlightthickness=0)
    canvas.pack()

    # Cargar imagenes  de botones ON/OFF
    botones_on  = {c: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{c}On.png'))  for c in colores}
    botones_off = {c: PhotoImage(file=os.path.join(RUTA_BOTONES, f'BtnMaze{c}Off.png')) for c in colores}

    espacio_x = w
    espacio_y = 80

    botones_ids = {}

    # Solo un boton (Return), ajustes para efecto de ser presionado:
    for texto, col, fila, color in boton_aviso:
        x_btn = espacio_x // 2
        y_btn = espacio_y // 2

        img_id = canvas.create_image(x_btn, y_btn + 2, image=botones_off[color])
        sombra_id = canvas.create_text(x_btn + 2, y_btn + 2, text=texto, font=fuente, fill="black")
        txt_id    = canvas.create_text(x_btn, y_btn, text=texto, font=fuente, fill="white")

        botones_ids[texto] = {
            "imagen": img_id,
            "texto": txt_id,
            "sombra": sombra_id,
            "color": color,
            "habilitado": True
        }

        def al_presionar(event, btn=texto):
            info = botones_ids[btn]
            canvas.itemconfig(info["imagen"], image=botones_on[info["color"]])
            canvas.itemconfig(info["texto"], fill="gray")
            canvas.move(info["texto"], 0, 6)
            canvas.move(info["sombra"], 0, 6)

        def al_soltar(event, btn=texto):
            info = botones_ids[btn]
            canvas.itemconfig(info["imagen"], image=botones_off[info["color"]])
            canvas.itemconfig(info["texto"], fill="white")
            canvas.move(info["texto"], 0, -6)
            canvas.move(info["sombra"], 0, -6)

            #con el boton de return se regresa al menu principal
            if btn == "Return":
                ventana_aviso.destroy()
                menu_principal()

        for item in (img_id, txt_id, sombra_id):
            canvas.tag_bind(item, "<ButtonPress-1>", al_presionar)
            canvas.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    ventana_aviso.mainloop()

#Funcion del menu principal para seleccionar laberinto
def menu_principal():

    #Configuracion de la ventana:
    menu_principal = tk.Tk()
    menu_principal.title("A-MAZE-ZING")
    # centra la ventana en la pantalla, y la abre al frente:
    screen_w = menu_principal.winfo_screenwidth()
    screen_h = menu_principal.winfo_screenheight()
    x = (screen_w - 525) // 2
    y = (screen_h - 820) // 2
    menu_principal.geometry(f"525x750+{x}+{y}")
    menu_principal.attributes("-topmost", True)
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
                if maps.YOUR_MAZE == []:
                    menu_principal.destroy()
                    aviso_laberinto_vacio()
                else:
                    abrir_ventana_laberinto("Your Maze")
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

    #Funcion para cerrar la ventana del menu y abrir el ajuste para el laberinto random:
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