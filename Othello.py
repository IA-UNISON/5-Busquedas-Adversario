"""
Juego othello o reversi.

0  1  2  3  4  5  6  7
 8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63

- El juego es suma cero (lo que le beneficia a uno, le afecta al otro)
- Es obviamente de dos jugadores (blanco y negro)
- El juego consiste en un tablero de 8x8
- Se inicia con cuatro fichas en el centro, donde se colocan dos fichas blancas y dos negras. Ambas en diagonal.
- Se necesitan 32 fichas para cada jugador, en donde las fichas contienen de una cara el color blanco y de la otra el negro.
- Inicia siempre el jugador negro.
- El juego consiste basicamente en flanquear.
- TODAS las jugadas deben consistir en flanquear. Si no tienes oportunidad de hacerlo, pasas turno.
- El juego termina una vez que o se llena el tablero, o que ya no hayan jugadas legales disponibles.
- Gana el jugador con mas fichas de su color en el tablero.
"""

import juegos_simplificado as js
import minimax

class Othello(js.JuegoZT2):
    def inicializa(self):
        s = [0] * 64
        s[27] = -1 # O
        s[28] = 1 # X
        s[35] = 1 # x
        s[36] = -1 # O
        return tuple(s)
    
    def borde_valido(self, casilla, vecino):
            return abs(casilla % 8 - vecino % 8) <= 1
    
    def jugadas_legales(self, s, j):
        """
        Una jugada es legal si:

        1. La casilla esta vacia
        2. Al colocar tu ficha, volteas al menos una ficha del oponente,
        lo cual ocurre cuando hay una linea en cualquiera de las 8 direcciones
        que empiece con fichas del oponente y termine con una tuya
        """

        direcciones = [-9, -8, -7, -1, 1, 7, 8, 9]

        def es_legal(casilla):
            if s[casilla] != 0:
                return False
            for d in direcciones:
                vecino = casilla + d
                if 0 <= vecino < 64 and self.borde_valido(casilla, vecino) and s[vecino] == -j:
                    vecino += d
                    if not (0 <= vecino < 64 and self.borde_valido(vecino - d, vecino)):
                        continue
                    while 0 <= vecino < 64 and self.borde_valido(vecino - d, vecino) and s[vecino] == -j:
                        vecino += d
                    if 0 <= vecino < 64 and self.borde_valido(vecino - d, vecino) and s[vecino] == j:
                        return True
            return False
        
        return (casilla for casilla in range(64) if es_legal(casilla))
    
    def sucesor(self, s, a, j):
        s = list(s[:])
        s[a] = j #colocamos la ficha en la casilla a

        direcciones = [-9, -8, -7, -1, 1, 7, 8, 9]

        for d in direcciones:
            fichas_a_voltear = []
            vecino = a + d

            if 0 <= vecino < 64 and self.borde_valido(a, vecino):
            # recolecta fichas del oponente en la direccion dada
                while 0 <= vecino < 64 and self.borde_valido(vecino - d, vecino) and s[vecino] == -j:
                    fichas_a_voltear.append(vecino)
                    vecino += d

                # voltear todo lo recolectado
                if 0 <= vecino < 64 and self.borde_valido(vecino - d, vecino) and s[vecino] == j:
                    for casilla in fichas_a_voltear:
                        s[casilla] = j
        
        return tuple(s)
    
    def ganancia(self, s):
        fichas_j1 = s.count(1)
        fichas_j2 = s.count(-1)
        if fichas_j1 > fichas_j2:
            return 1
        if fichas_j2 > fichas_j1:
            return -1
        else:
            return 0
    
    def terminal(self, s):
        if 0 not in s or (not any(self.jugadas_legales(s, 1)) and not any(self.jugadas_legales(s, -1))):
            return True
        return False
    
class InterfaceOthello(js.JuegoInterface):
    def muestra_estado(self, s):
        print('\n    ', end='')
        for col in range(8):
            print(f'  {col} ', end='')
        print()
        for i in range(8):
            print(f'{i} ', end='')
            for j in range(8):
                casilla = 8 * i + j
                if s[casilla] == 1:
                    contenido = ' X '
                elif s[casilla] == -1:
                    contenido = ' O '
                else:
                    contenido = f'{casilla:2d} '
                print(f'|{contenido}', end='')
            print('|')
            print('  ' + '+---' * 8 + '+')

    def muestra_ganador(self, g):
        if g == 1:
            print("Gana el jugador X")
        elif g == -1:
            print("Gana el jugador O")
        else:
            print("Empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada (0-63): "))
        return jugada

if __name__ == '__main__':
    cfg = {
        "Jugador 1": "Humano",
        "Jugador 2": "Aleatorio",
        "profundidad máxima": 3,
        "tiempo": 10,
        "ordena": None,
        "evalua": None
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

    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("Juego de Othello")
    interfaz.juega()