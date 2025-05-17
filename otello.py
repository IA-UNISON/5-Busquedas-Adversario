"""

Implementación del Otello.

Autora: Ana Sofía Matti Ríos

"""


from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo

class otello(ModeloJuegoZT2):

    def inicializa(self):

        tablero_inicial= [[0 for _ in range(8)] for _ in range(8)]

        #negras
        tablero_inicial[3][3] = -1
        tablero_inicial[4][4] = -1

        #blancas
        tablero_inicial[3][4] = 1
        tablero_inicial[4][3] = 1

        return(tuple(tuple(fila) for fila in tablero_inicial), 1)

    def representacion_tablero(self, s):
        """Convierte el estado (tupla de tuplas) a una lista de listas."""
        return [list(fila) for fila in s]

    def jugadas_legales(self, s, j):

        jugadas = []
        tablero = self.representacion_tablero(s)

        for fila in range(8):
            for columna in range(8):
                if tablero[fila][columna] == 0:
                    if self.movimiento_legal(tablero, j, fila, columna):
                        jugadas.append((fila, columna))
        return jugadas

    def movimiento_legal(self, s, j, fila, columna):

        oponente = -j
        direcciones = [(0,1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, 1), (1, -1), (-1, -1)]

        for df, dc in direcciones:

            fila_nueva, columna_nueva = fila + df, columna + dc
            fichas_capturadas = []

            while 0 <= fila_nueva < 8 and 0 <= columna_nueva < 8 and s[fila_nueva][columna_nueva] == oponente:
                fichas_capturadas.append((fila_nueva, columna_nueva))

                fila_nueva += df
                columna_nueva += dc

            if 0 <= fila_nueva < 8 and 0 <= columna_nueva < 8 and s[fila_nueva][columna_nueva] == j and fichas_capturadas:
                return True
        return False

    def transicion(self, s, a, j):
        tablero_lista = [list(fila) for fila in s]
        fila, columna = a
        oponente = -j

        #tablero_lista[fila][columna] = j

        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in direcciones:
            nueva_fila, nueva_columna = fila + dr, columna + dc
            fichas_capturadas=[]

            while 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and tablero_lista[nueva_fila][nueva_columna] == oponente:
                fichas_capturadas.append((nueva_fila, nueva_columna))
                nueva_fila += dr
                nueva_columna += dc

            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and tablero_lista[nueva_fila][nueva_columna] == j:
                for fr, fc in fichas_capturadas:
                    tablero_lista[fr][fc] = j

        tablero_lista[fila][columna] = j
        nuevo_estado = tuple(tuple(fila) for fila in tablero_lista)
        return nuevo_estado

    def terminal(self, s):

        tablero = self.representacion_tablero(s)
        jugador1 = 1
        jugador2 = -1

        for fila in tablero:
            if 0 in fila:
                return False

        if not self.jugadas_legales(s, jugador1) and not self.jugadas_legales(s, jugador2):
            return True

        return False

    def ganancia(self, s):

        tablero = self.representacion_tablero(s)
        contador_jugador1 = 0
        contador_jugador2 = 0

        for fila in tablero:
            for casilla in fila:
                if casilla == 1:
                    contador_jugador1 += 1
                elif casilla == -1:
                    contador_jugador2 += 1

        return contador_jugador1 - contador_jugador2

    def evalua(self, s):
        """
        Función de evaluación básica: diferencia del número de fichas.
        Evalúa el estado 's' para el jugador Blanco (1).
        """
        tablero = self.representacion_tablero(s)
        fichas_blancas = sum(fila.count(1) for fila in tablero)
        fichas_negras = sum(fila.count(-1) for fila in tablero)
        return fichas_blancas - fichas_negras

def pprint_otello(s):
    """
    Imprime el estado del juego de Othello.
    """
    tablero = [list(fila) for fila in s]
    print("  0 1 2 3 4 5 6 7")
    print("-----------------")
    for i, fila in enumerate(tablero):
        print(f"{i}|", end="")
        for casilla in fila:
            if casilla == 1:
                print(" W ", end="")  # Blanca
            elif casilla == -1:
                print(" B ", end="")  # Negra
            else:
                print(" . ", end="")  # Vacía
        print()
    print("-----------------")


def jugador_manual_otello(juego, s, j):
    """
    Jugador manual para el juego del Othello.
    """
    jugada = None
    print("Estado actual:")
    pprint_otello(s)
    if j == 1:
        color = "Blanca (W)"
    else:
        color = "Negra (B)"
    print(f"Jugador: {j} ({color})")
    jugadas = juego.jugadas_legales(s, j)
    print("Jugadas legales:", jugadas)
    while jugada not in jugadas:
        try:
            fila = int(input("Fila (0-7): "))
            columna = int(input("Columna (0-7): "))
            jugada = (fila, columna)
            if jugada not in jugadas:
                print("¡Jugada inválida! Por favor, elige una de las jugadas legales.")
        except ValueError:
            print("¡Entrada inválida! Por favor, ingresa números para la fila y la columna.")
        except IndexError:
            print("¡Coordenadas fuera del tablero! Por favor, ingresa valores entre 0 y 7.")
    return jugada


def juega_otello(jugador='W'):
    """
    Juega el juego del Othello.
    El jugador puede elegir ser 'B' (Negro, -1) o 'W' (Blanco, 1).
    Las Negras siempre empiezan.
    """
    if jugador not in ['B', 'W']:
        raise ValueError("El jugador solo puede tener los valores 'B' (Negro) o 'W' (Blanco)")

    juego = otello()

    print("El juego del Otello")
    print("Las Negras (B) siempre empiezan.")

    depth = 3
    eval_funcion = lambda estado: juego.evalua(estado)
    #print(f"Tipo de eval_funcion: {type(eval_funcion)}") 
    if jugador == 'W':
        print("Tú juegas con las Blancas (W).")
        g, s = juega_dos_jugadores(juego, jugador_manual_otello, lambda *args: jugador_negamax(*args, d=depth, evalua=eval_funcion))
    else: #jugador == 'B'
        print("Tú juegas con las Negras (B).")
        g, s = juega_dos_jugadores(juego, lambda *args: jugador_negamax(*args, d=depth, evalua=eval_funcion), jugador_manual_otello)

    print("\nSE ACABÓ EL JUEGO\n")
    pprint_otello(s)
    jugador_humano = 1 if jugador == 'W' else -1
    jugador_ia = -1 if jugador == 'W' else 1
    ganancia_jugador_humano = 0
    for fila in s:
        ganancia_jugador_humano += fila.count(jugador_humano)
        ganancia_jugador_humano -= fila.count(jugador_ia)

    if ganancia_jugador_humano > 0:
        print("\n¡Ganaste!")
    elif ganancia_jugador_humano < 0:
        print("\n¡Perdiste!")
    else:
        print("\n¡Asqueroso Empate!")

if __name__ == '__main__':
    juega_otello('W') # jugador humanos juega las blancas