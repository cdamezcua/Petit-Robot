# Ricochet Robots
# Por: Carlos David Amezcua Canales - A01641742 y 
# Elena Montserrat García García - A01640861
# a 20 de octubre de 2021

# bibliotecas
import os, sys, select, time, random, copy

# Constantes
SANGRIA = 4
RETRASO_EN_INTRO = 0.25
MIN_JUGADORES = 2
MAX_JUGADORES = 8
T_P_ANUNCIAR = 60
ALTO = 19
ANCHO = 67
espcio_de_estados = [0 for i in range(100000000)]

# Variables globales
jugadores = 0
rondas = 0
pantalla_inicial = []
gen_tablero = []
tablero_temp = []
menu = []
configuracion = []
instrucciones = []
creditos = []
tiempo = []
tablero_original = []
tablero = []
tablero_r =[]
tablero_bfs = []
puntajes = []
destinos_validos = []
destino = []
pos_bots_validas = []
pos_bots = []
pos_bots_temp = []
anuncios = []
correcto = []
incorrecto = []
todos_pierden = []
empate = []
victoria = []

def lee_graficos():
    """Función que lee de archivos de texto todos los gráficos que utiliza el
    programa y los almacena en matrices independientes."""
    global pantalla_inicial, gen_tablero, tablero_original, menu
    global configuracion, instrucciones, creditos, tiempo, correcto
    global incorrecto, todos_pierden, empate, victoria, tablero_bfs
    archivo = open("pantalla_inicial.txt", "r")
    pantalla_inicial = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("gen_tablero.txt", "r")
    gen_tablero = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("tablero_original.txt", "r")
    tablero_original = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("menu.txt", "r")
    menu = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("configuracion.txt", "r")
    configuracion = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("instrucciones.txt", "r")
    instrucciones = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("creditos.txt", "r")
    creditos = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("tiempo.txt", "r")
    tiempo = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()  
    archivo = open("correcto.txt", "r")
    correcto = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()  
    archivo = open("incorrecto.txt", "r")
    incorrecto = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()
    archivo = open("todos_pierden.txt", "r")
    todos_pierden = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()  
    archivo = open("empate.txt", "r")
    empate = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()  
    archivo = open("victoria.txt", "r")
    victoria = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()  
    archivo = open("tablero_bfs.txt", "r")
    tablero_bfs = [list(linea.rstrip()) for linea in archivo.readlines()]
    archivo.close()

def establece_color_de_terminal():
    """Función que establece el color la fuente de la terminal en verde y del 
    fondo de la terminal en negro."""
    print("\033[1;32;40m")

def limpia_terminal():
    """Función que limpia la terminal, sin importar el sistema operativo de la
    máquina donde esté corriendo el programa."""
    if os.name == "nt": # Windows
        os.system("cls")
    else: # MacOS / Linux
        os.system("clear")

def inicializa_terminal():
    """Función que inicializa la terminal para poder ser usada. Define su
    color y la limpia."""
    establece_color_de_terminal()
    limpia_terminal()

def sangra(longitud):
    """Función que imprime la cantidad de espacios que se le especifique, sin 
    añadir un salto de linea al final."""
    for i in range(longitud):
        print(" ", end = "")

def input_ct(mensaje, tiempo_en_s = T_P_ANUNCIAR, salida_por_defecto = ""):
    """Función que le da al usuario un rango de tiempo para introducir una
    cadena de caracteres. Si lo hace la lee y la retorna, sino retorna una
    cadena por defecto."""
    print(mensaje, end = "", flush = True)
    entrada, salida, error = select.select([sys.stdin], [], [], tiempo_en_s)
    if entrada:
        return (True, sys.stdin.readline().strip())
    else:
        print()
        return (False, salida_por_defecto)

def espacia(espacios):
    """Función que imprime la cantidad de saltos de linea que se le 
    especifique."""
    for i in range(espacios):
        print()

def imprime_pantalla_inicial(sangria = SANGRIA, retraso = RETRASO_EN_INTRO):
    """Función que imprime la pantalla de bienvenda al juego, de forma 
    pausada."""
    limpia_terminal()
    for renglon in pantalla_inicial:
        sangra(sangria)
        print("".join(renglon))
        time.sleep(retraso)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA CONTINUAR")

def imprime_instrucciones(sangria = SANGRIA):
    """Función que imprime las instrucciones del juego."""
    limpia_terminal()
    for renglon in instrucciones:
        sangra(sangria)
        print(r"".join(renglon))
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER REGRESAR AL MENÚ")

def imprime_creditos(sangria = SANGRIA):
    """Función que imprime los créditos del juego."""
    limpia_terminal()
    for renglon in creditos:
        sangra(sangria)
        print("".join(renglon))
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER REGRESAR AL MENÚ")

def renderiza_tablero(pos_bots):
    """Función que modifica el tablero global para que refleje las posiciones 
    que tienen los robots al momento de ser llamada, así como la posición 
    destino actual y los recorridos que se estén dando."""
    global tablero, tablero_r, tablero_original
    tablero = copy.deepcopy(tablero_original)
    for i in range(len(tablero_r)):
        for j in range(len(tablero_r[i])):
            if "0" <= tablero_r[i][j] <= "9" or tablero_r[i][j] == "#":
                tablero[i][j] = "#"
    tablero[destino[0]][destino[1]] = "X"
    for i in [[-1, -1], [-1, 1], [1, 1], [1, -1]]:
        tablero[destino[0] + i[0]][destino[1] + i[1]] = "▓"
    for i in range(len(pos_bots)):
        tablero[pos_bots[i][0]][pos_bots[i][1]] = str(i)
        for j in [[-1, 0], [0, 1], [1, 0], [0, -1]]: 
            if tablero[pos_bots[i][0] + j[0]][pos_bots[i][1] + j[1]] == " ":
                tablero[pos_bots[i][0] + j[0]][pos_bots[i][1] + j[1]] = "░"

def imprime_pantalla_de_juego(ronda, sangria = SANGRIA):
    """Función que imprime el tablero global como se encuentre en ese momento,
    sin antes renderizarlo o actualizarlo."""
    global puntajes, tablero
    limpia_terminal()
    espacia(2)
    sangra(sangria)
    print(f"Ricochet Robots\tRonda #{ronda}\t")
    sangra(sangria)
    print(f"Marcador = {puntajes}")
    for renglon in tablero:
        sangra(sangria)
        print("".join(renglon))

def lee_anuncios(ronda, sangria = SANGRIA):
    """Función encargada de ejecutar la primera fase de la ronda, en la que 
    se leen los anuncios que hagan los jugadores."""
    global destino, tablero, puntajes, jugadores, anuncios
    turno = 0
    while True:
        imprime_pantalla_de_juego(ronda)
        espacia(1)
        sangra(sangria)
        print("¡Todos los jugadores busquen una solución!")
        espacia(2)
        sangra(sangria)
        basura = input("[!] PRESIONA ENTER PARA ANUNCIAR TU SOLUCIÓN")
        espacia(1)
        sangra(sangria)
        jugador = input("Número de jugador: ")
        if jugador.isdigit() and 0 <= int(jugador) - 1 < jugadores:
            jugador = int(jugador) - 1
        else:
            sangra(sangria)
            basura = input("[!] Número de jugador inválido.")
            continue
        sangra(sangria)
        movimientos = input("Cantidad de movimientos: ")
        if movimientos.isdigit() and 0 <= int(movimientos):
            movimientos = int(movimientos)
        else:
            sangra(sangria)
            basura = input("[!] Cantidad de movimientos inválida.")
            continue
        break
    anuncios[jugador] = (movimientos, turno := turno + 1, jugador)
    imprime_pantalla_de_juego(ronda)
    espacia(1)
    sangra(sangria)
    print("[!] ANUNCIO REGISTRADO CON ÉXITO")
    espacia(1)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA CONTINUAR")
    tiempo_inicial = time.time()
    while True:
        while True:
            if (t_rest := T_P_ANUNCIAR - (time.time() - tiempo_inicial)) <= 0:
                break
            imprime_pantalla_de_juego(ronda)
            espacia(1)
            sangra(sangria)
            print("¡Todos los jugadores busquen una solución!")
            sangra(sangria)
            if (t_rest := T_P_ANUNCIAR - (time.time() - tiempo_inicial)) <= 0:
                break
            print(f"Tiempo restante para hacer anuncios [s]: {t_rest:.0f}")
            espacia(1)
            sangra(sangria)
            hay_entrada, entrada = \
                    input_ct("[!] PRESIONA ENTER PARA ANUNCIAR TU SOLUCIÓN", \
                    max(0, min(t_rest, 1)))
            if not hay_entrada:
                continue
            espacia(1)
            sangra(sangria)
            if (t_rest := T_P_ANUNCIAR - (time.time() - tiempo_inicial)) <= 0:
                break
            hay_jugador, jugador = input_ct("Número de jugador: ", \
                    max(0, t_rest))
            if not hay_jugador:
                continue
            if jugador.isdigit() and 0 <= int(jugador) - 1 < jugadores:
                jugador = int(jugador) - 1
            else:
                sangra(sangria)
                basura = input("[!] Número de jugador inválido.")
                continue
            sangra(sangria)
            if (t_rest := T_P_ANUNCIAR - (time.time() - tiempo_inicial)) <= 0:
                break
            hay_movimientos, movimientos = \
                    input_ct("Cantidad de movimientos: ", max(0, t_rest))
            if not hay_movimientos:
                continue
            if movimientos.isdigit() and 0 <= int(movimientos):
                movimientos = int(movimientos)
            else:
                sangra(sangria)
                basura = input("[!] Cantidad de movimientos inválida.")
                continue
            imprime_pantalla_de_juego(ronda)
            anuncios[jugador] = (movimientos, turno := turno + 1, jugador)
            espacia(1)
            sangra(sangria)
            print("[!] ANUNCIO REGISTRADO CON ÉXITO")
            espacia(1)
            sangra(sangria)
            basura = input("[!] PRESIONA ENTER PARA CONTINUAR")
        if (t_rest := T_P_ANUNCIAR - (time.time() - tiempo_inicial)) <= 0:
            break

def imprime_tiempo(sangria = SANGRIA):
    """Función que imprime la pantalla que le indica a los jugadores que se 
    terminó el tiempo."""
    global tiempo
    limpia_terminal()
    for renglon in tiempo:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA CONTINUAR")

def prioriza_anuncios(anuncios):
    """Funcion que recibe una lista de anuncios, posiblemente con posiciones
    vacías y retorna otra sin esas posiciones vacías y ordenada primero de
    forma ascendente de acuerdo con la cantidad de mivimientos totales y 
    después de forma ascendente de acuerdo con el turno."""
    respuesta = []
    for anuncio in anuncios:
        if anuncio[0] != None:
            respuesta.append(anuncio)
    respuesta_ordenada = sorted(respuesta, key = lambda x: (x[0], x[1]))
    return respuesta_ordenada

def comprueba_formato_de_solucion(solucion):
    """Función que retorna verdadero si la solucion que se le introduce cumple
    con el formato establecido en las instrucciones y falso en caso 
    contrario."""
    if len(solucion) == 0:
        return True
    for ch in solucion:
        if ch not in "01234nseo":
            return False
    if solucion[0] not in "01234":
        return False
    if solucion[-1] not in "nseo":
        return False
    for i in range(len(solucion) - 1):
        if solucion[i] in "01234" and solucion[i + 1] in "01234":
            return False
    return True

def hay_robot_temp(renglon, columna):
    """Función que regresa verdadero si hay algún robot temporal en el renglón
    y columna especificada al momento de comprobar una solución."""
    for pos in pos_bots_temp:
        if pos == [renglon, columna]:
            return True
    return False

def mueve_robot(bot, direc):
    """Función que mueve el robot temporal especificado en la dirección
    especificada una posición hacia adelante en caso de ser posible y que 
    en el proceso renderiza el tablero para ajutarse a las nuevas posiciones 
    de los robots temporales y de los caminos que vallan recorriendo. La 
    función regresa verdadero si logra mover al robot y falso en caso 
    contrario."""
    global tablero_r
    pos = pos_bots_temp[bot]
    direc = "neso".find(direc)
    trans1 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    trans2 = [[-2, 0], [0, 2], [2, 0], [0, -2]]
    if tablero[pos[0] + trans1[direc][0]][pos[1] + trans1[direc][1]] != "█" \
        and not hay_robot_temp(pos[0] + trans2[direc][0], \
            pos[1] + trans2[direc][1]):
        tablero_r[pos[0]][pos[1]] = str(bot)
        tablero_r[pos[0] + trans1[direc][0]][pos[1] + trans1[direc][1]] = \
                str(bot)
        pos[0] = pos[0] + trans2[direc][0]
        pos[1] = pos[1] + trans2[direc][1]
        pos_bots_temp[bot] = pos
        renderiza_tablero(pos_bots_temp)
        return True
    return False

def lee_solucion(ronda, movimientos, jugador, sangria = SANGRIA):
    """Función que comprueba la solución de un jugador mostrando gráficamente
    los movimientos que realiza su propuesta. La función regresa verdadero
    si la solución introducida es correcta y falso en caso contrario."""
    global pos_bots_temp, tablero_r
    renderiza_tablero(pos_bots)
    while True:
        imprime_pantalla_de_juego(ronda)
        espacia(1)
        sangra(sangria)
        if movimientos == 1:
            print(f"¡Jugador {jugador + 1}, comprueba tu solución de "
                    + f"{movimientos} movimiento!")
        else:
            print(f"¡Jugador {jugador + 1}, comprueba tu solución de "
                    + f"{movimientos} movimientos!")
        espacia(1)
        sangra(sangria)
        solucion = input("Introduce tu solución: ")
        solucion = solucion.lower()
        if not comprueba_formato_de_solucion(solucion):
            basura = input("[!] FORMATO INVÁLIDO")
            continue
        return solucion

def comprueba_solucion(ronda, movimientos, solucion, sangria = SANGRIA):
    """Función que comprueba la solución de un jugador mostrando gráficamente
    los movimientos que realiza su propuesta. La función regresa verdadero
    si la solución introducida es correcta y falso en caso contrario."""
    global pos_bots_temp, tablero_r
    paso = 1
    pos_bots_temp = copy.deepcopy(pos_bots)
    for i in range(len(solucion)):
        if solucion[i] in "01234":
            tablero_r = copy.deepcopy(tablero_original)
            for j in range(i + 1, len(solucion)):
                if solucion[j] in "neso":
                    if paso <= movimientos:
                        while mueve_robot(int(solucion[i]), solucion[j]):
                            time.sleep(0.5)
                            imprime_pantalla_de_juego(ronda)
                            espacia(1)
                            sangra(sangria)
                            print(f"Movimiento {paso} / {movimientos}: "
                                    + f"[{solucion[i]} - "
                                    + f"{solucion[j].upper()}]")
                        paso += 1
                    else:
                        break
                else:
                    break
            time.sleep(1)
    tablero_r = copy.deepcopy(tablero_original)
    renderiza_tablero(pos_bots)
    if pos_bots_temp[0] == destino:
        return True
    return False

def imprime_correcto(jugador, sangria = SANGRIA):
    """Función que imrpime la pantalla que le nuestra a los jugadores que uno
    de ellos comprobó su respuesta correctamente, por lo que gana un punto."""
    global correcto
    limpia_terminal()
    for renglon in correcto:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    print(f"¡El jugador {jugador + 1} gana un punto!")
    espacia(1)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA CONTINUAR")

def imprime_incorrecto(sangria = SANGRIA):
    """Función que le muestra a los jugadores que un usuario intentó comprobar
    una solución que era incorrecta."""
    global incorrecto
    limpia_terminal()
    for renglon in incorrecto:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA CONTINUAR")

def soluciona():
    global pos_bots_temp, tablero_r, destino
    pos_bots_temp = copy.deepcopy(pos_bots)



def juega_ronda(ronda):
    """Función que juega una ronda de Ricochet Robots. Leyendo los anuncios y 
    comprobándolos."""
    global destino, tablero, puntajes, jugadores, anuncios, pos_bots
    destino = random.choice(destinos_validos)
    renderiza_tablero(pos_bots)
    anuncios = [(None, None, i) for i in range(jugadores)]
    lee_anuncios(ronda)
    imprime_tiempo()
    limpia_terminal()
    anuncios = prioriza_anuncios(anuncios)
    algun_ganador = False
    for anuncio in anuncios:
        solucion = lee_solucion(ronda, anuncio[0], anuncio[2])
        if comprueba_solucion(ronda, anuncio[0], solucion):
            puntajes[anuncio[2]] += 1
            pos_bots = pos_bots_temp
            time.sleep(1)
            imprime_correcto(anuncio[2])
            algun_ganador = True
            break
        else:
            time.sleep(1)
            imprime_incorrecto()
    if not algun_ganador:
        solucion = soluciona()
        movimientos = 0
        for ch in solucion:
            if ch in "neso":
                movimientos += 1
        comprueba_solucion(ronda, movimientos, solucion)

def inicializa_partida(sangria = SANGRIA):
    """Función que para configura una partida le pide al usuario la cantidad
    de jugadores y la cantidad de rondas y además selecciona al azar las
    posiciones iniciales de los robots y de la posición objetivo."""
    global jugadores, rondas, puntajes, destinos_validos, pos_bots_validas
    global pos_bots
    while True:
        limpia_terminal()
        for renglon in configuracion:
            sangra(sangria)
            print("".join(renglon))
        sangra(sangria)
        jugadores = input("Introduce la cantidad de jugadores [2, 8]: ")
        if jugadores.isdigit() \
                and MIN_JUGADORES <= int(jugadores) <= MAX_JUGADORES:
            jugadores = int(jugadores)
            break
        elif len(jugadores) == 0:
            pass
        else:
            sangra(sangria)
            basura = input("[!] Cantidad de jugadores inválida")
    puntajes = [0 for i in range(jugadores)]
    while True:
        limpia_terminal()
        for renglon in configuracion:
            sangra(sangria)
            print("".join(renglon))
        sangra(sangria)
        print(f"Introduce la cantidad de jugadores [2, 8]: {jugadores}")
        sangra(sangria)
        rondas = input("Introduce la cantidad rondas a jugar [1, ∞): ")
        if rondas.isdigit() and 1 <= int(rondas):
            rondas = int(rondas)
            break
        elif len(rondas) == 0:
            pass
        else:
            sangra(sangria)
            basura = input("[!] Cantidad de rondas inválida")
    sangra(sangria)
    print()
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA COMENZAR LA PARTIDA")
    for i in range(len(gen_tablero)):
        for j in range(len(gen_tablero[i])):
            if gen_tablero[i][j] == "X":
                destinos_validos.append([i, j])
            elif gen_tablero[i][j] == "·":
                pos_bots_validas.append([i, j])
    random.shuffle(pos_bots_validas)
    pos_bots = pos_bots_validas[0 : 5]
    tablero_r = copy.deepcopy(tablero_original)

def imprime_todos_pierden(sangria = SANGRIA):
    """Función que le imprime a los jugadores el mensaje de todos pierden."""
    global todos_pierden
    limpia_terminal()
    for renglon in todos_pierden:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    print(f"Marcador = {puntajes}")
    espacia(1)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA REGRESAR AL MENÚ")

def imprime_empate(ganadores, sangria = SANGRIA):
    """Función que le imprime a los jugadores el mensaje de que hubo un empate
    y les especifica que jugadores fueron los que empataron."""
    global empate
    limpia_terminal()
    for renglon in empate:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    print(f"¡Felicidades jugadores ", end = "")
    for i in range(len(ganadores) - 2):
        print(f"{ganadores[i] + 1}, ", end = "")
    print(f"{ganadores[-2] + 1} y {ganadores[-1] + 1}!")
    espacia(1)
    sangra(sangria)
    print(f"Marcador = {puntajes}")
    espacia(1)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA REGRESAR AL MENÚ")

def imprime_victoria(ganador, sangria = SANGRIA):
    """Función que le imprime a los jugadores el mensaje de voctoria, 
    especificando cuál de los jugadores fue el que resultó victorioso."""
    global victoria
    limpia_terminal()
    for renglon in victoria:
        sangra(sangria)
        print("".join(renglon))
    espacia(2)
    sangra(sangria)
    print(f"¡Felicidades jugador {ganador + 1}!")
    espacia(1)
    sangra(sangria)
    print(f"Marcador = {puntajes}")
    espacia(1)
    sangra(sangria)
    basura = input("[!] PRESIONA ENTER PARA REGRESAR AL MENÚ")

def imprime_resultados():
    """Función que imprime el mensaje de resultado apropiado en función del 
    marcador final de la partida."""
    mayor_valor = 0
    indices_de_mayores = []
    for i in range(len(puntajes)):
        if puntajes[i] > mayor_valor:
            mayor_valor = puntajes[i]
            indices_de_mayores = [i]
        elif puntajes[i] == mayor_valor:
            indices_de_mayores.append(i)
    if mayor_valor == 0:
        imprime_todos_pierden()
    elif len(indices_de_mayores) > 1:
        imprime_empate(indices_de_mayores)
    else:
        imprime_victoria(indices_de_mayores[0])

def imprime_menu(sangria = SANGRIA):
    """Función que imprime el menú del juego. Retorna si tras un minuto
    consecutivo, nadie introduce una opción."""
    while True:
        limpia_terminal()
        for renglon in menu:
            sangra(sangria)
            print("".join(renglon))
        sangra(sangria)
        hay_opc, opc = input_ct("Introduce una opción válida: ", 60)
        if not hay_opc:
            return
        if len(opc) == 0:
            pass
        elif opc == "1":
            inicializa_partida()
            for i in range(1, rondas + 1):
                juega_ronda(i)
            imprime_resultados()
        elif opc == "2":
            imprime_instrucciones()
        elif opc == "3":
            imprime_creditos()
        else:
            sangra(sangria)
            basura = input_ct("[!] Opción inválida", 30)

def main():
    """Función principal del programa."""
    lee_graficos()
    inicializa_terminal()
    while True:
        imprime_pantalla_inicial()
        imprime_menu()

main()
