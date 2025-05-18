#Librerias:
import turtle as t
import time

#Creacion de pantalla:
pantalla = t.Screen()
pantalla.bgcolor("#34b800")

#Configuracion basica:
t.title("Laberinto con backtracking - Jose Pablo Garcia Zamudio")
t.shape("turtle")
t.speed(5)

#Variables:
Tamaño_celda = 24

#Laberintos:

'''
" " (espacio): casilla libre.
• "#": pared o casilla bloqueada.
• "S": punto de inicio (Start).
• "G": punto objetivo (Goal).
'''

Laberinto_1 = [
    "###########",
    "#S   #    #",
    "### # ### #",
    "#   #   # #",
    "# ##### # #",
    "#     #  G#",
    "###########"
]

def dibujar_cuadrado(x, y, color):

    #Configuracion basica del cuadrado:
    t.color(color)
    t.goto(x, y)

    t.begin_fill()
    for i in range(4):
        t.pendown()
        t.forward(Tamaño_celda)
        t.right(90)
    t.end_fill()
    t.penup()

def dibujar_laberinto(laberinto):
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            screen_x = -len(laberinto[0]) * Tamaño_celda // 2 + x * Tamaño_celda
            screen_y = len(laberinto) * Tamaño_celda // 2 - y * Tamaño_celda
            celda = laberinto[y][x]

            if celda == '#':
                dibujar_cuadrado(screen_x, screen_y, "black")

            elif celda == 'G':
                dibujar_cuadrado(screen_x, screen_y, "green")

            elif celda == 'S':
                dibujar_cuadrado(screen_x, screen_y, "blue")

            else:
                dibujar_cuadrado(screen_x, screen_y, "white")
 
def main():
    #Codigo de main 
    t.tracer(0)
    dibujar_laberinto(Laberinto_1)
    t.update()
    t.mainloop()

if __name__ == "__main__":
    main()


