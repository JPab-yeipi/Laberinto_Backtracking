#Librerias:
import turtle as t
import time
import maps
import tkinter as tk
from collections import deque
from turtle import RawTurtle, ScrolledCanvas

#Variables:
Tamaño_celda = 15

#Funciones:
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
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda
            screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda
            celda = laberinto[y][x]

            if celda == '#':
                dibujar_cuadrado(turtle, screen_x, screen_y, "black")

            elif celda == 'G':
                dibujar_cuadrado(turtle, screen_x, screen_y, "green")

            elif celda == 'S':
                dibujar_cuadrado(turtle, screen_x, screen_y, "blue")

            else:
                dibujar_cuadrado(turtle, screen_x, screen_y, "white")
 
def encontrar_inicio(turtle, laberinto):
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            if laberinto[y][x] == 'S':

                screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda
                screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda

                turtle.penup()
                turtle.goto(screen_x + Tamaño_celda // 2, screen_y - Tamaño_celda // 2)
                turtle.setheading(0)

                return x, y
     
    raise ValueError("No se encontró el punto de inicio en el laberinto.")

def orientacion_turtle(turtle, direccion):

    if direccion == (1,0):
        turtle.setheading(0)
    elif direccion == (0, 1):
        turtle.setheading(270)
    elif direccion == (-1, 0):
        turtle.setheading(180)
    elif direccion == (0, -1):
        turtle.setheading(90)


def buscar_meta(turtle, laberinto, x, y, visitados, ruta_actual):
    if laberinto[y][x] == 'G':
        ruta_actual.append((x, y))
        screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda + Tamaño_celda // 2
        screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda - Tamaño_celda // 2
        turtle.goto(screen_x, screen_y)
        turtle.dot(10, "blue")  # Marca exacta sobre G
        turtle.hideturtle()
        turtle.getscreen().update()
        return True

    if (x, y) in visitados or laberinto[y][x] == '#':
        return False

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

    for dx, dy in direcciones:
        nuevo_x, nuevo_y = x + dx, y + dy

        if 0 <= nuevo_y < len(laberinto) and 0 <= nuevo_x < len(laberinto[0]):
            if laberinto[nuevo_y][nuevo_x] != '#' and (nuevo_x, nuevo_y) not in visitados:
                orientacion_turtle(turtle, (dx, dy))

                if buscar_meta(turtle, laberinto, nuevo_x, nuevo_y, visitados, ruta_actual):
                    turtle.dot(10, "blue")
                    return True

    # Punto sin salida (gris)
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

def mostrar_laberinto(nombre):
    ventana_laberinto = tk.Tk()
    ventana_laberinto.title(f'Laberinto - {nombre}')
    ventana_laberinto.geometry("1000x700")
    ventana_laberinto.configure(bg="white")

    canvas_turtle = ScrolledCanvas(ventana_laberinto, width=600, height=600)
    canvas_turtle.place(x=50, y=50)

    turtle = RawTurtle(canvas_turtle)
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    turtle._tracer(0, 0)  # ❗ Esto evita que se vea la animación de construcción

    laberinto = maps.MAZE_DICC[nombre]

    # Dibuja laberinto sin animación
    dibujar_laberinto(turtle, laberinto)
    turtle._update()  # ❗ Dibuja todo de golpe

    # Ya puedes continuar como normalmente con la búsqueda
    x_inicio, y_inicio = encontrar_inicio(turtle, laberinto)

    ruta_actual = []
    visitados = set()
    buscar_meta(turtle, laberinto, x_inicio, y_inicio, visitados, ruta_actual)

    x_meta, y_meta = ruta_actual[-1]
    ruta_corta = camino_mas_corto(laberinto, (x_inicio, y_inicio), (x_meta, y_meta))

    time.sleep(1)  # Espera tras la búsqueda

    turtle.showturtle()
    for i in range(len(ruta_corta)):
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
        time.sleep(0.05)

    ventana_laberinto.mainloop()

def main():

    menu_principal = tk.Tk()
    menu_principal.title("Menu de laberintos")
    menu_principal.geometry("400x650")
    menu_principal.configure(bg="#34b800")

    #Agregar texto dentro de la ventana
    titulo = tk.Label(
        menu_principal,
        text="MENU DE LABERINTOS",
        font=("Arial", 30, "bold"),
        bg="#34b800",
        fg="black"
    )
    titulo.pack(pady=20)

    def abrir_ventana_laberinto(nombre):
        menu_principal.destroy()
        mostrar_laberinto(nombre)

    for nombre in maps.MAZE_DICC:
        boton = tk.Button(
            menu_principal,
            text=nombre,
            font=("Arial", 16, "bold"),
            width=20,
            height=2,    
            fg="black",            
            bd=2,
            command=lambda n=nombre: abrir_ventana_laberinto(n)
        )
        boton.pack(pady=5)

    menu_principal.mainloop()

if __name__ == "__main__":
    main()