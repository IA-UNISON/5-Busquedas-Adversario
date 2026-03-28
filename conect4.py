"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax

class Conecta4(js.JuegoZT2):
    def inicializa(self):
        return tuple([0 for _ in range(6 * 7)])
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        simbolos = {1: ' X ', -1: ' O ', 0: '   '}
        print()
        print('      0   1   2   3   4   5   6   ')
        print('    ┌───┬───┬───┬───┬───┬───┬───┐')
        for fila in range(6):
            cuadritos = '│'.join(simbolos[s[fila * 7 + c]] for c in range(7))
            print(f'    │{cuadritos}│')
            if fila < 5:
                print('    ├───┼───┼───┼───┼───┼───┼───┤')
        print('    └───┴───┴───┴───┴───┴───┴───┘')
        print()
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def ordena_centro(jugadas, jugador, s=None):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)
    return promedio

# Todas las ternas de 4 en línea (horizontales, verticales, diagonales).
LINEAS_GANADORAS = []
TIPO_LINEA = []

#líneas horizontales
for fila in range(6):
    for col in range(4):
        linea = tuple(fila * 7 + col + k for k in range(4))
        LINEAS_GANADORAS.append(linea)
        TIPO_LINEA.append('horizontal')

#líneas verticales
for col in range(7):
    for fila in range(3):
        linea = tuple((fila + k) * 7 + col for k in range(4))
        LINEAS_GANADORAS.append(linea)
        TIPO_LINEA.append('vertical')

# diagonales (descendentes hacia la derecha)
for fila in range(3):
    for col in range(4):
        linea = tuple((fila + k) * 7 + col + k for k in range(4))
        LINEAS_GANADORAS.append(linea)
        TIPO_LINEA.append('diagonal')

# diagonales (descendentes hacia la izquierda)
for fila in range(3):
    for col in range(3, 7):
        linea = tuple((fila + k) * 7 + col - k for k in range(4))
        LINEAS_GANADORAS.append(linea)
        TIPO_LINEA.append('diagonal')

# creamos un diccionario para saber rápido a qué líneas ganadoras pertenece cada cuadrito
LINEAS_POR_CUADRITO = {i: [] for i in range(42)}
for indice_linea, linea in enumerate(LINEAS_GANADORAS):
    for cuadrito in linea:
        LINEAS_POR_CUADRITO[cuadrito].append(indice_linea)

PESO_COLUMNAS = (0, 0.5, 1.0, 1.5, 1.0, 0.5, 0)

def obtener_fila_disponible(s, columna):
    """
    Fila más baja vacía en `columna` (índice de fila: 0 arriba, 5 abajo).

    Devuelve:
        int: fila donde cae la ficha, o -1 si la columna está llena.
    """
    for fila in range(5, -1, -1):
        if s[columna + 7 * fila] == 0:
            return fila
    return -1 # La columna está llena

def evalua_ventanas(s):
    """
    Evalúa qué tan bien posicionado está el tablero.
    Suma puntos por tener fichas alineadas donde todavía hay espacio para conectar 4.
    """
    puntuacion_total = 0.0
    # puntos base: 0 fichas = 0pts, 1 ficha = 1pt, 2 fichas = 8pts, 3 fichas = 80pts
    puntos_por_fichas = {0: 0, 1: 1, 2: 8, 3: 80, 4: 10000}

    for linea, tipo in zip(LINEAS_GANADORAS, TIPO_LINEA):
        # vemos que fichas hay en esta linea
        valores_linea = [s[cuadrito] for cuadrito in linea]
        fichas_j1 = valores_linea.count(1)
        fichas_j2 = valores_linea.count(-1)

        # si ambos jugadores tienen fichas aquí, la línea está bloqueada, no sirve a nadie
        if fichas_j1 > 0 and fichas_j2 > 0:
            continue
        # si la línea está totalmente vacía, no aporta valor inmediato
        if fichas_j1 == 0 and fichas_j2 == 0:
            continue

        # determinamos de quién es la ventaja en esta línea
        if fichas_j1 > 0:
            fichas_alineadas = fichas_j1
            signo = 1 # Beneficia al jugador 1
        else:
            fichas_alineadas = fichas_j2
            signo = -1 # Beneficia al jugador 2 (resta puntuación general)

        # las diagonales son más difíciles de ver y defender, valen un poco más
        multiplicador = 1.3 if tipo == 'diagonal' else 1.0

        # si ya hay al menos 2 fichas, checamos qué tan rápido se puede completar la línea
        if fichas_alineadas >= 2:
            for cuadrito in linea:
                if s[cuadrito] == 0: # Encontramos la cuadrito que falta llenar
                    fila_cuadrito = cuadrito // 7
                    tiene_soporte = (fila_cuadrito == 5) or (s[cuadrito + 7] != 0)
                    if tiene_soporte:
                        multiplicador *= 2.5 if fichas_alineadas == 3 else 1.4
                        break

        puntuacion_total += signo * puntos_por_fichas[fichas_alineadas] * multiplicador

    for cuadrito in range(42):
        if s[cuadrito] != 0:
            columna = cuadrito % 7
            puntuacion_total += s[cuadrito] * PESO_COLUMNAS[columna]

    return max(-0.999, min(0.999, puntuacion_total / 3500))


def ordena_consecuencias(jugadas, jugador, s):
    """
    Ordena las jugadas disponibles priorizando las más urgentes o ventajosas:
    1. Ganar.
    2. Bloquear victoria del rival.
    3. Armar ataques / Bloquear ataques.
    4. No regalarle la victoria al rival arriba.
    """
    rival = -jugador

    def calificar_jugada(columna):
        fila = obtener_fila_disponible(s, columna)
        if fila < 0:
            return -10000

        cuadrito_destino = columna + 7 * fila
        puntos_jugada = 0.0

        simulacion_mia = list(s)
        simulacion_mia[cuadrito_destino] = jugador

        for indice_linea in LINEAS_POR_CUADRITO[cuadrito_destino]:
            linea = LINEAS_GANADORAS[indice_linea]
            valores_linea = [simulacion_mia[i] for i in linea]
            mis_fichas = valores_linea.count(jugador)
            fichas_rival = valores_linea.count(rival)

            if fichas_rival == 0:
                if mis_fichas == 4:
                    return 10000
                if mis_fichas == 3:
                    puntos_jugada += 40

        simulacion_rival = list(s)
        simulacion_rival[cuadrito_destino] = rival

        for indice_linea in LINEAS_POR_CUADRITO[cuadrito_destino]:
            linea = LINEAS_GANADORAS[indice_linea]
            valores_linea = [simulacion_rival[i] for i in linea]
            mis_fichas = valores_linea.count(jugador)
            fichas_rival = valores_linea.count(rival)

            if mis_fichas == 0:
                if fichas_rival == 4:
                    puntos_jugada += 5000
                elif fichas_rival == 3:
                    puntos_jugada += 25

        if fila > 0:
            cuadrito_arriba = columna + 7 * (fila - 1)
            simulacion_trampa = list(s)
            simulacion_trampa[cuadrito_destino] = jugador
            simulacion_trampa[cuadrito_arriba] = rival

            for indice_linea in LINEAS_POR_CUADRITO[cuadrito_arriba]:
                linea = LINEAS_GANADORAS[indice_linea]
                if all(simulacion_trampa[i] == rival for i in linea):
                    puntos_jugada -= 3000
                    break

        puntos_jugada += (3 - abs(columna - 3)) * 0.5
        return puntos_jugada

    return sorted(jugadas, key=calificar_jugada, reverse=True)

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Negamax",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Tiempo",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 6,
        "tiempo": 10,
        "ordena": ordena_consecuencias, #Puede ser None o una función f(jugadas, j, s) -> lista de jugadas ordenada
        "evalua": evalua_ventanas      #Puede ser None o una función f(estado) -> número entre -1 y 1
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorMinimaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()
