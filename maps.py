'''Version 4.6    Autor: Jose Pablo Garcia Zamudio    Github: JPab-Dev'''
#Librerias ----------------------------------------------------------------------------------------------
import random
import math

#INGRESA TU LABERINTO AQUI: ----------------------|
YOUR_MAZE = []   #<-------------------------------|

#Laberintos pre-establecidos --------------------------------------------------------------------------------------
MAZE_1 = [
    "#####################",
    "#S#       #         #",
    "# # ##### # ####### #",
    "# # #   # # #     # #",
    "# # # # # # # ### # #",
    "# # # # # #   # # # #",
    "# # # # # ### # # # #",
    "#   #         # # #G#",
    "#####################"
]

MAZE_2 = [
    "############",
    "#S         #",
    "########## #",
    "#          #",
    "# ##########",
    "# #        #",
    "# ######## #",
    "#          #",
    "# ##########",
    "#          #",
    "# ###### # #",
    "#        # #",
    "# ######## #",
    "#G#        #",
    "############",
]

MAZE_3 = [
    "#################################",
    "#S    #       #               # #",
    "# ### # #####   ##### ####### # #",
    "# #           #     #       # # #",
    "# # ####### ####### ##### ### # #",
    "# #         #   #           #   #",
    "# ######### # ######### # ### ###",
    "#       #     #G      # #     # #",
    "####### # ### ##### # ######### #",
    "#     # #   #     # #     #     #",
    "# ### # ### ##### ### ### ### # #",
    "#   #     # #   #     # #   # # #",
    "### ##### # # # ####### # # # # #",
    "#   #     # # #       # # #   # #",
    "# # # ##### # ## ## ### ####### #",
    "# # #       #     #   #         #",
    "# # ############# ### ######### #",
    "# #                             #",
    "#################################"
]

MAZE_4 = [
    "#################################",
    "#S# #   #   #   # #   # # # # # #",
    "# # # # # # # # # # # # #   # # #",
    "# # # #   # # # #   # # # # # # #",
    "# # # # # # # # ### #   # # # # #",
    "# # # # # # # #   # # # # # #   #",
    "# # # # # # # # # # # # # # # # #",
    "# # # # # # #   # # # # # # # # #",
    "# # # ### # # # # # # # # # # # #",
    "# # # # # #   # # # # # # # # # #",
    "# # # # # # # # # # # # # # # # #",
    "# # # # # # # # # # ### # # # # #",
    "# # # #   # # # # # # # # # # # #",
    "# # # # # # # # # # # # # # # # #",
    "# # # # # # # # #   # # # # # # #",
    "# # # # # ### # # # # # # # # # #",
    "# # # # # # # # # # # # # # # # #",
    "# # # # # # # # # # # # # # # # #",
    "# #   # #   # # # # # # # # # # #",
    "# # # # # # #   # # # # # # # # #",
    "# # # # ### # # # # # #   # # # #",
    "# # # # # # # # # # # # # #   # #",
    "# # # # #   # # # # # # # # # # #",
    "# # # # # # ### # #   # # # # # #",
    "#   # # # # # # # # # # # # # #G#",
    "#################################"
]

MAZE_5 = [
    "################################",
    "#S      #     #                #",
    "# ##### # # # # #### ######### #",
    "#   #   # #   #    # # #     # #",
    "# ### ### # # # ## ### # ### # #",
    "#   #   # # # ###  #     #     #",
    "### ### # # # #   ## ##### ### #",
    "#   #   # # # # ###  #     #   #",
    "# ##### # # # # #   ## ##### ###",
    "# #     # # #   # ###  #     # #",
    "# # ##### # # ###     ## ##### #",
    "# #     # #   # # ### ## # # # #",
    "# ##### # ### #   # # #  # # # #",
    "# #   # #   ####### # ##       #",
    "#   ### # #   #G       # #######",
    "# # #   # ### ##########       #",
    "### ## ##     #   #    ### ### #",
    "#    #    ##### # # ##   #     #",
    "# #########   ###   #### ## ####",
    "#           ### ### #### ## ####",
    "# ###### ##   # ###   #        #",
    "# #    #  ### #   # # ##########",
    "#   ## ##  ## # # # #          #",
    "# ####  ##    # # ############ #",
    "# #   #  #### # # #            #",
    "# # # ## #### # # ### ##########",
    "# # #  #    # # # #            #",
    "# # ## #### # # # ############ #",
    "# #             #              #",
    "################################"
]

MAZE_6 = [
    "###################################",
    "#S                                #",
    "################################# #",
    "#                               # #",
    "# ######## #################### # #",
    "# #                           # # #",
    "# # ################# ####### # # #",
    "# # #                       # # # #",
    "# # # ############### ##### # # # #",
    "# # # #                   # # # # #",
    "# # # # ################# # # # # #",
    "# # # # #               # # # # # #",
    "# # # # # ###### ###### # # # # # #",
    "# # # # # #           # # # # # # #",
    "# # # #   # ######### # # # # # # #",
    "# # # # # # #       # # # # # # # #",
    "# # # ### # # ##### # # # # # # # #",
    "# # #   # # # #G    # # # # # # # #",
    "# # # # # # # ####### # # # # # # #",
    "# # # # # # #         # # # # # # #",
    "# # # # # # ########### # # # # # #",
    "# # # # # #             # # # # # #",
    "# #   # # ######## ###### # # # # #",
    "# # # # #                 # # # # #",
    "# # # # ################### # # # #",
    "# # # #                     # # # #",
    "# # # ####### ############### # # #",
    "# # #                         # # #",
    "# # ################# ######### # #",
    "# #               #             # #",
    "# ############################### #",
    "#                                 #",
    "###################################"
]

#Funcion que crea laberintos random ---------------------------------------------------------------------------------
def crear_random_maze(alto, ancho, porcentaje_libres, bifurcaciones, seed=None, callback=None):
    
    if seed is not None:
        random.seed(seed)

    # Asegura dimensiones impares
    if alto % 2 == 0:   alto += 1
    if ancho % 2 == 0:  ancho += 1

    #Crea matriz llena de muros
    laberinto = [["#" for _ in range(ancho)] for _ in range(alto)]

    # verifica que (x,y) quede dentro de bordes internos
    def en_rango(x, y):
        return 0 < x < ancho - 1 and 0 < y < alto - 1

    # funcion para creacion de pasillos con DFS recursivo
    def carve(x, y):
        laberinto[y][x] = " "
        if callback:
            callback("carve", x, y)
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if en_rango(nx, ny) and laberinto[ny][nx] == "#":
                laberinto[y + dy//2][x + dx//2] = " "
                carve(nx, ny)

    # elige punto inicial aleatorio y talla pasillos
    inicio_x = random.randrange(1, ancho, 2)
    inicio_y = random.randrange(1, alto, 2)
    carve(inicio_x, inicio_y)
    laberinto[inicio_y][inicio_x] = "S"

    # funcion que halla celda libre más lejana para marcar meta
    def manhattan(x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)
    max_d, meta = -1, (inicio_x, inicio_y)
    for yy in range(alto):
        for xx in range(ancho):
            if laberinto[yy][xx] == " ":
                d = manhattan(inicio_x, inicio_y, xx, yy)
                if d > max_d:
                    max_d, meta = d, (xx, yy)
    gx, gy = meta
    laberinto[gy][gx] = "G"

    # ajusta cantidad de celdas libres dependiendo de la dificultad:
    total = alto * ancho
    destino_libres = math.floor(porcentaje_libres * total)
    libres = sum(1 for row in laberinto for c in row if c == " ")
    # Recolecta TODOS los muros que toquen al menos 1 pasillo
    muros_candidatos = []
    for yy in range(1, alto-1):
        for xx in range(1, ancho-1):
            if laberinto[yy][xx] != "#":
                continue
            vecinos_libre = sum(
                1 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]
                if en_rango(xx+dx, yy+dy) and laberinto[yy+dy][xx+dx] == " "
            )
            if vecinos_libre >= 1 and (xx,yy) not in [(inicio_x,inicio_y), (gx,gy)]:
                muros_candidatos.append((xx,yy))
    random.shuffle(muros_candidatos)
    for mx, my in muros_candidatos:
        if libres >= destino_libres:
            break
        laberinto[my][mx] = " "
        libres += 1
        if callback:
            callback("densidad", libres, destino_libres)

    # inserta bucles exactos según bifurcaciones pedidas
    muros_para_bucles = []
    for yy in range(1, alto-1):
        for xx in range(1, ancho-1):
            if laberinto[yy][xx] != "#":
                continue
            # Horizontal
            if xx % 2 == 1 and yy % 2 == 0:
                if laberinto[yy-1][xx] == " " and laberinto[yy+1][xx] == " ":
                    muros_para_bucles.append((xx, yy))
            # Vertical
            elif yy % 2 == 1 and xx % 2 == 0:
                if laberinto[yy][xx-1] == " " and laberinto[yy][xx+1] == " ":
                    muros_para_bucles.append((xx, yy))
    random.shuffle(muros_para_bucles)
    for i in range(min(bifurcaciones, len(muros_para_bucles))):
        wx, wy = muros_para_bucles[i]
        if (wx,wy) in [(inicio_x,inicio_y), (gx,gy)]:
            continue
        laberinto[wy][wx] = " "
        if callback:
            callback("bucle", i+1, bifurcaciones)

    return laberinto

#Diccionario de laberintos por nombre: --------------------------------------------------------------------------------
MAZE_DICC = {
    "Laberinto 1": MAZE_1,
    "Laberinto 2": MAZE_2,
    "Laberinto 3": MAZE_3,
    "Laberinto 4": MAZE_4,
    "Laberinto 5": MAZE_5,
    "Laberinto 6": MAZE_6,
    "Laberinto random": [],
    "Tu Laberinto": YOUR_MAZE
}
