"""
Juego del Othello

El estado se representará como una lista de 64 estados, tal que:
   __ __ __ __ __ __ __ __
|  0  1  2  3  4  5  6  7   |
|  8  9  10 11 12 13 14 15  |
|  16 17 18 19 20 21 22 23  |
|  24 25 26 27 28 29 30 31  |
|  32 33 34 35 36 37 38 39  |
|  40 41 42 43 44 45 46 47  |
|  48 49 50 51 52 53 54 55  |
|  56 57 58 59 60 61 62 63  |
|  __ __ __ __ __ __ __ __  |  

Cada elemento puede ser:
    0: Vacío
    1: Ficha del Jugador 1
   -1: Ficha del Jugador 2

La acciones son poner una ficha en una casilla, el cual se representa como
un número de 0 a 63 (a excepcion del 27, 28, 35, 36, ya que aquí se
posicicionan las fichas iniciales).

El estado terminal es aquel en el que el tablero se queda sin espacios para colocar
fichas.

La ganancia es:
    1 si gana el jugador 1.
   -1 si gana el jugador 2.
    0 si hay empate.
"""

import juegos_simplificado as js
import minimax

class Othello(js.JuegoZT2):
    def inicializa(self):
        tablero = [0] * 64

        tablero[3 * 8 + 3] = 1
        tablero[3 * 8 + 4] = -1
        tablero[4 * 8 + 3] = -1
        tablero[4 * 8 + 4] = 1

        return  tuple(tablero)
    
    def jugadas_legales(self, s, j):
        jugadas = [a for a in range(64) if s[a] == 0 and self.es_legal(s, a, j)]
        
        # Si no hay jugadas, no devuelvas opciones
        if not jugadas:
            return [None]
        
        # Si las hay, devuelvelas
        return jugadas
    
    def sucesor(self, s, a, j):
        # Si no no se puede actuar (por jugadas_legales devolviendo None) salta turno
        if a is None:
            return s

        s = list(s[:])
        s[a] = j

        # Esto es para buscar en todas las direcciones posibles para ver si se pueden hacer lineas
        direcciones = (
            (-1,0), (1,0), (0,-1), (0,1),
            (-1, 1), (-1, -1), (1, 1), (1, -1)
        )

        for df, dc in direcciones:
            fila = a // 8
            columna = a % 8

            fila_actual = fila + df
            columna_actual = columna + dc

            capturadas = []

            while 0 <= fila_actual < 8 and 0 <= columna_actual < 8:
                pos = fila_actual * 8 + columna_actual 
                
                if s[pos] == 0: 
                    break
                
                if s[pos] == -j:
                    capturadas.append(pos)

                if s[pos] == j:
                    for i in capturadas:
                        s[i] = j
                    break
                
                fila_actual += df
                columna_actual += dc
        
        return tuple(s)
    
    def es_legal(self, s, a, j):
        """
        Esta función ayudante es para ver si una jugada en una casilla es legal, ya que solo puedes jugar si es posible
        capturar alguna ficha. Usa la misma lógica que la función sucesor, simplemente se fija si la acción es
        """

        direcciones = (
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, 1), (-1, -1), (1, 1), (1, -1)
        )

        for df, dc in direcciones:
            fila = a // 8
            columna = a % 8

            fila_actual = fila + df
            columna_actual = columna + dc

            capturadas = []

            while 0 <= fila_actual < 8 and 0 <= columna_actual < 8:
                pos = fila_actual * 8 + columna_actual
                if s[pos] == 0:
                    break
                if s[pos] == -j:
                    capturadas.append(pos)
                if s[pos] == j:
                    if len(capturadas) > 0:
                        return True  # Si hay al menos una ficha capturable, es jugada legal 
                    break
                fila_actual += df
                columna_actual += dc
        return False  # Si ninguna dirección da una ficha capturable, la jugada es illegal

    def ganancia(self, s):
        return s.count(1) - s.count(-1)
    
    def terminal(self, s):
        if 0 not in s:
            return True
        j1 = self.jugadas_legales(s, 1)
        j2 = self.jugadas_legales(s, -1)
        if j1 == [None] and j2 == [None]:
            return True
        return False
    
class InterfaceOthello(js.JuegoInterface):
    def muestra_estado(self, s):
        # Es para los colores de formato
        GRIS = '\033[90m'
        MAGENTA = '\033[95m'
        BLUE = '\033[94m'
        RESET = '\033[0m'

        print("\n")

        a = [
            f'{MAGENTA} B  {RESET}' if x == 1 
            else f'{BLUE} N  {RESET}' if x == -1 
            else f'{GRIS}{i:^4}{RESET}' for i, x in enumerate(s)]

        for i in range(8):
            print('|'.join(a[8 * i:8 * (i + 1)]))
            print('----+----+----+----+----+----+----+----+\n')

    def muestra_ganador(self, g):
        if g > 0:
            print("Gana el jugador B")
        elif g < 0:
            print("Gana el jugador N")
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " BW"[j])
        jugadas = list(self.juego.jugadas_legales(s,j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def ordena_othello(jugadas, j):
    esquinas = [0, 7, 56, 63]
    def prioridad(a):
        if a is None:
            return 3
        if a in esquinas:
            return 0  # Las esquinas son mas importantes como (la esquina superior izquierda por ejemplo, ese tipo de esquina)
        fila = a // 8
        columna = a % 8
        if fila == 0 or fila == 7 or columna == 0 or columna == 7:
            return 1  # Las esquinas de en medio (osea, las esquinas que no son como las de arriba)
        return 2 # Todo lo demas después
    return sorted(jugadas, key=prioridad)

def evalua_othello(s):
    total = s.count(1) + s.count(-1)

    if total == 0:
        return 0
    return ((s.count(1) + s.count(-1)) / total)

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",   # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 3, # Como el Othello tiene MUCHAS casillas, si le pongo profunidades mas grandes se tarda mas que el camión de la une pasando por mi.
        "tiempo": 10,
        "ordena": ordena_othello,
        "evalua": evalua_othello
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
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )
    
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    print("El Juego del Othello")
    print(f"{MAGENTA}Jugador 1 (B):{RESET}", cfg["Jugador 1"])
    print(f"{BLUE}Jugador 2 (N):{RESET}", cfg["Jugador 2"])
    print()

    interfaz.juega()