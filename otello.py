"""
Juego de Otello

Tablero de 8x8, cada cuadrito vale 0 (vacía), 1 (negra/X) o -1 (blanca/O).
Se inicia el juego con 4 fichas en el centro y mueven primero las negras.

La jugada consiste en poner una ficha de tu color de modo que "encierres"
fichas del rival en línea recta (horizontal, vertical o diagonal).
Las fichas encerradas se voltean a tu color.
Si no puedes mover, pasas. Si ambos pasan, se acabó el juego.
Gana quien tenga más fichas al final.

tablero:
 0  1  2  3  4  5  6  7
 8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63
"""

import juegos_simplificado as js
import minimax

# las 8 direcciones en las que se puede voltear una ficha
direcciones = [(-1, -1), (-1, 0), (-1, 1),
         ( 0, -1),          ( 0, 1),
         ( 1, -1), ( 1, 0), ( 1, 1)]


def volteos(s, pos, j):
    """
    regresa la lista de posiciones que se voltean si el jugador j pone ficha en pos.
    s: estado del tablero
    pos: posición de la ficha
    j: jugador
    """
    fila, columna = divmod(pos, 8)
    resultado = []
    for df, dc in direcciones:
        temp = []
        f, c = fila + df, columna + dc
        while 0 <= f < 8 and 0 <= c < 8:
            idx = f * 8 + c
            if s[idx] == -j:
                temp.append(idx)
            elif s[idx] == j:
                resultado.extend(temp)
                break
            else:
                break
            f += df
            c += dc
    return resultado


def movimientos(s, j):
    """cuadritos vacíos donde el jugador j puede colocar ficha (voltea al menos una)."""
    return [i for i in range(64) if s[i] == 0 and volteos(s, i, j)]


# juego
class Otello(js.JuegoZT2):
    """juego otello."""

    def inicializa(self):
        """tablero vacío y pone las cuatro fichas del centro."""
        t = [0] * 64
        t[27], t[28] = -1,  1   # d4 blanca, e4 negra
        t[35], t[36] =  1, -1   # d5 negra,  e5 blanca
        return tuple(t)

    def jugadas_legales(self, s, j):
        """movimientos reales o [-1] si toca pasar porque no hay donde jugar."""
        movs = movimientos(s, j)
        return movs if movs else [-1]

    def sucesor(self, s, a, j):
        """estado despues de que j hace a; el pase (-1) deja el tablero igual."""
        if a == -1:
            return s
        t = list(s)
        t[a] = j
        for idx in volteos(s, a, j):
            t[idx] = j
        return tuple(t)

    def terminal(self, s):
        """True si ya no hay cuadritos vacíos o si ninguno de los dos puede mover."""
        if 0 not in s:
            return True
        return not movimientos(s, 1) and not movimientos(s, -1)

    def ganancia(self, s):
        """desde el punto de vista del jugador 1: gana negras (1), blancas (-1) o empate (0)."""
        diff = sum(s)
        return 1 if diff > 0 else (-1 if diff < 0 else 0)


class InterfaceOtello(js.JuegoInterface):
    """imprime el tablero en consola."""

    def muestra_estado(self, s):
        """dibuja el 8x8 con letras arriba y números al costado, más conteo de fichas."""
        sim = {1: ' X ', -1: ' O ', 0: '   '}
        print('\n     a   b   c   d   e   f   g   h')
        print('   ┌───┬───┬───┬───┬───┬───┬───┬───┐')
        
        for f in range(8):
            fila = '│'.join(sim[s[f * 8 + c]] for c in range(8))
            print(f' {f + 1} │{fila}│')
            if f < 7:
                print('   ├───┼───┼───┼───┼───┼───┼───┼───┤')
                
        print('   └───┴───┴───┴───┴───┴───┴───┴───┘')
        
        nx = sum(1 for x in s if x == 1)
        no = sum(1 for x in s if x == -1)
        print(f'\n  X (negras): {nx}    O (blancas): {no}\n')

    def muestra_ganador(self, g):
        """Mensaje simple según g (1 negras, -1 blancas, 0 empate)."""
        print("-" * 35)
        if g == 1:
            print(" Ganaron las negras (X)")
        elif g == -1:
            print(" Ganaron las blancas (O)")
        else:
            print(" Empate")
        print("-" * 35 + "\n")

    def pide_jugada(self, jugador_actual, s, j):
        if isinstance(jugador_actual, js.Jugador):
            try:
                return jugador_actual.jugada(self.juego, s, j)
            except IndexError:
                # si minimax colapsa y devuelve [], 
                # forzamos el primer movimiento legal válido.
                movs = self.juego.jugadas_legales(s, j)
                return movs[0]
        else:
            return self.jugador_humano(s, j)

    def jugador_humano(self, s, j):
        """Pide columna+fila hasta que el movimiento sea uno de los legales (o pase)."""
        ficha = 'X' if j == 1 else 'O'
        movs = movimientos(s, j)
        
        if not movs:
            print(" No hay movimientos posibles. Pasas turno.")
            return -1
            
        nombres = [chr(97 + p % 8) + str(p // 8 + 1) for p in movs]
        print(f" Jugador {ficha} - movimientos: {', '.join(nombres)}")
        
        while True:
            txt = input(" Tu jugada (ej: d3): ").strip().lower()
            if len(txt) == 2 and txt[0] in 'abcdefgh' and txt[1] in '12345678':
                pos = (int(txt[1]) - 1) * 8 + (ord(txt[0]) - 97)
                if pos in movs:
                    return pos
            print(" Esa jugada no es válida, intenta otra.")

    def juega(self, max_pasos=200):
        """
        Partida completa: alterna jugadores, cuenta pases seguidos y para si el
        juego es terminal o si los dos pasan uno tras otro.
        """
        s = self.juego.inicializa()
        self.muestra_estado(s)
        j = 1
        pases = 0

        for _ in range(max_pasos):
            if self.juego.terminal(s):
                break

            movs = movimientos(s, j)
            if not movs:
                print(f"  {'X' if j == 1 else 'O'} no puede mover, pasa turno.")
                pases += 1
                if pases >= 2:
                    break
                j = -j
                continue

            pases = 0
            a = self.pide_jugada(self.jugador[j], s, j)
            s = self.juego.sucesor(s, a, j)
            self.muestra_estado(s)
            j = -j

        self.muestra_ganador(self.juego.ganancia(s))


# evaluacion y ordenamiento

# pesos de cada cuadrito segun que tan buena es para colocar ficha.
# las esquinas tienen el valor mas alto porque no se pueden voltear.
# los cuadritos junto a una esquina vacia tienen valor negativo
# porque facilitan que el rival tome la esquina.
pesos = [
    100, -25,  10,   5,   5,  10, -25, 100,
    -25, -45,   1,   1,   1,   1, -45, -25,
     10,   1,   5,   2,   2,   5,   1,  10,
      5,   1,   2,   1,   1,   2,   1,   5,
      5,   1,   2,   1,   1,   2,   1,   5,
     10,   1,   5,   2,   2,   5,   1,  10,
    -25, -45,   1,   1,   1,   1, -45, -25,
    100, -25,  10,   5,   5,  10, -25, 100,
]

esquinas = {0, 7, 56, 63}

# vecinos de esquina (si la esquina sigue vacia no conviene jugar en ella)
vecinos_esquina = {
    0:  [1, 8, 9],
    7:  [6, 14, 15],
    56: [48, 49, 57],
    63: [54, 55, 62],
}


def evalua_otello(s):
    """
    Evalua que tan bien va el jugador considerando:
      - la posicion de sus fichas (segun la tabla de pesos)
      - la movilidad (tener mas movimientos disponibles que el rival)
      - el control de esquinas (son las posiciones mas valiosas)
    Cuando ya queda poco tablero (menos de 8 cuadritos vacios), solo cuenta quien tiene mas fichas.
    """
    cuadritos_vacios = s.count(0)

    # --- FASE FINAL DEL JUEGO ---
    if cuadritos_vacios <= 8:
        diferencia_fichas = sum(s)
        return max(-0.999, min(0.999, diferencia_fichas / 64))

    pos = sum(s[i] * pesos[i] for i in range(64) if s[i])

    m1 = len(movimientos(s, 1))
    m2 = len(movimientos(s, -1))
    mob = 30 * (m1 - m2) / (m1 + m2) if (m1 + m2) else 0

    esq = sum(s[e] for e in esquinas) * 25

    total = pos + mob + esq
    return max(-0.999, min(0.999, total / 800))


def ordena_otello(jugadas, jugador, s):
    """
    Ordena las jugadas para explorar primero las mas prometedoras:
      - esquinas van primero (son las mejores del tablero)
      - despues los cuadritos con buen peso posicional
      - al final los cuadritos junto a una esquina vacia (suelen ser malas posiciones)
    """
    if jugadas == [-1]:
        return jugadas

    def prioridad(pos):
        """Número grande = conviene explorar esa jugada antes."""
        if pos in esquinas:
            return 200
        for esq, vecinos in vecinos_esquina.items():
            if pos in vecinos and s[esq] == 0:
                return -100
        return pesos[pos]

    return sorted(jugadas, key=prioridad, reverse=True)

# para jugar
if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",       # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Aleatorio",        # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10 ,
        "ordena": ordena_otello,
        "evalua": evalua_otello,
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

    juego = Otello()
    interfaz = InterfaceOtello(
        juego,
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"]),
    )

    print("=== OTELLO ===")
    print(f"  Jugador 1 (X negras): {cfg['Jugador 1']}")
    print(f"  Jugador 2 (O blancas): {cfg['Jugador 2']}")
    print()
    interfaz.juega()