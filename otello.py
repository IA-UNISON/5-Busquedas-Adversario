"""

Juego de Otello

El estado se va a representar como una tupla de 64 elementos, 

0  1  2  3  4  5  6  7
8  9  10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63

donde cada elemento puede ser 0, 1 o -1. 0 representa una casilla vacía, 1 
representa una ficha del jugador 1 y -1 representa una ficha del jugador 2.

El estado terminal se alcanza cuando no hay más jugadas legales, o cuando
el tablero se llena completamente.

La ganancia es de 1 para el jugador 1 y -1 para el jugador 2. 0 si es 
empate.

"""

import juegos_simplificado as js
import minimax

class Otello(js.JuegoZT2):
    def inicializa(self):
        estado_inicial = [0 for _ in range(64)]
        estado_inicial[27] = -1
        estado_inicial[28] = 1
        estado_inicial[35] = 1
        estado_inicial[36] = -1
        return tuple(estado_inicial)


    def jugadas_legales_aux(self, s, jugador):
        jugadas = []
        for i in range(64):
            if s[i] == 0:
                fila = i // 8
                col = i % 8
                jugada_valida = False
                for dx in [1, 0, -1]:
                    for dy in [1, 0, -1]:
                        if dx == 0 and dy == 0:
                            continue
                        x = col + dx
                        y = fila + dy
                        oponente_encontrado = False
                        while 0 <= x < 8 and 0 <= y < 8:
                            if s[y * 8 + x] == -jugador:
                                oponente_encontrado = True
                                x += dx
                                y += dy
                            elif s[y * 8 + x] == jugador and oponente_encontrado:
                                jugada_valida = True
                                break
                            else:
                                break
                        if jugada_valida:
                            break
                    if jugada_valida:
                        break
                if jugada_valida:
                    jugadas.append(i)
        return jugadas
    
    def jugadas_legales(self, s, jugador):
        jugadas = self.jugadas_legales_aux(s, jugador)
        if not jugadas and not self.terminal(s):
            jugadas.append(None)
        return jugadas

    def sucesor(self, s, a, jugador):
        if a is None:
            return s
        s = list(s[:])
        fila = a // 8
        col = a % 8
        s[a] = jugador
        for dx in [1, 0, -1]:
            for dy in [1, 0, -1]:
                if dx == 0 and dy == 0:
                    continue
                x = col + dx
                y = fila + dy
                oponente_encontrado = False
                while 0 <= x < 8 and 0 <= y < 8:
                    if s[y * 8 + x] == -jugador:
                        oponente_encontrado = True
                        x += dx
                        y += dy
                    elif s[y * 8 + x] == jugador and oponente_encontrado:
                        while True:
                            x -= dx
                            y -= dy
                            if x == col and y == fila:
                                break
                            s[y * 8 + x] = jugador
                        break
                    else:
                        break
        return tuple(s)
    
    def ganancia(self, s):
        if s.count(1) > s.count(-1):
            return 1
        elif s.count(1) < s.count(-1):
            return -1
        else:
            return 0
        
    def pasar_turno(self, s, jugador):
        if self.jugadas_legales(s, -jugador): 
           return -jugador
        elif self.jugadas_legales(s, jugador): 
           return jugador
        else:
           return None 
        
    def terminal(self, s):
        return not self.jugadas_legales_aux(s, 1) and not self.jugadas_legales_aux(s, -1)

class InterfaceOtello(js.JuegoInterface):
    def muestra_estado(self, s):
        for i in range(8):
            fila_str = []
            for j in range(8):
                idx = i * 8 + j
                if s[idx] == 1:
                    val = "X"
                elif s[idx] == -1:
                    val = "O"
                else:
                    val = str(idx)
                fila_str.append(f"{val:>2}")

            print(" | ".join(fila_str))
            print("-" * 40)
        print("\n")
        
    def muestra_ganador(self, g):
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego.

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

def ordena_esquinas(jugadas, jugador):
    esquinas = [0, 7, 56, 63]
    return sorted(jugadas, key=lambda x: 0 if x in esquinas else 1 if x is not None else 2)
 
def evalua_otello(s):
    juego = Otello()
    puntos = 0

    esquinas = [0, 7, 56, 63]
    
    esquinas_max = sum(1 for e in esquinas if s[e] == 1)
    esquinas_min = sum(1 for e in esquinas if s[e] == -1)

    # Heurística de capturación de esquinas
    if esquinas_max + esquinas_min != 0:
        valor_esquinas = 100 * (esquinas_max - esquinas_min) / (esquinas_max + esquinas_min)
    else:
        valor_esquinas = 0

    # Heurística de fichas
    fichas_max = s.count(1)
    fichas_min = s.count(-1)
    
    if fichas_max + fichas_min != 0:
        valor_fichas = 100 * (fichas_max - fichas_min) / (fichas_max + fichas_min)
    else:
        valor_fichas = 0

    # Heurística de movilidad
    mov_max = len(juego.jugadas_legales_aux(s, 1))
    mov_min = len(juego.jugadas_legales_aux(s, -1))
    
    if mov_max + mov_min != 0:
        valor_movilidad = 100 * (mov_max - mov_min) / (mov_max + mov_min)
    else:
        valor_movilidad = 0

    puntos += (valor_esquinas * 5) + (valor_movilidad * 3) + (valor_fichas * 2)
    return puntos
 
if __name__ == '__main__':
 
    cfg = {
        "Jugador 1": "Humano",
        "Jugador 2": "Negamax",
        "profundidad máxima": 4,
        "tiempo": 10,
        "ordena": ordena_esquinas,
        "evalua": evalua_otello
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
 
    interfaz = InterfaceOtello(
        Otello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )
 
    print("El Juego del Otello")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()
 
    interfaz.juega()