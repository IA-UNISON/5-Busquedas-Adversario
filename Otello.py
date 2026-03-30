"""
Juego de Othello (Reversi)

El tablero es de 8x8. Las posiciones se indexan así:
  0  1  2  3  4  5  6  7
  8  9 10 11 12 13 14 15
 16 17 18 19 20 21 22 23
 24 25 26 27 28 29 30 31
 32 33 34 35 36 37 38 39
 40 41 42 43 44 45 46 47
 48 49 50 51 52 53 54 55
 56 57 58 59 60 61 62 63

Cada celda puede ser 0 (vacía), 1 (jugador 1) o -1 (jugador 2).

El estado es una tupla de 65 elementos: los primeros 64 son el tablero,
el elemento 64 indica si el turno anterior fue un pase (1) o no (0),
para poder detectar cuando ambos jugadores pasan y el juego termina.
"""

import juegos_simplificado as js
import minimax

DIRECCIONES = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1), (0, 1),
               (1, -1), (1, 0), (1, 1)]


def _fila(pos):
    return pos // 8


def _col(pos):
    return pos % 8


def _fichas_a_voltear(s, pos, jugador):
    """
    Devuelve la lista de posiciones a voltear si el jugador coloca
    una ficha en pos. Si la jugada no es válida, devuelve lista vacía.
    """
    if s[pos] != 0:
        return []
    rival = -jugador
    a_voltear = []
    fila, col = _fila(pos), _col(pos)

    for df, dc in DIRECCIONES:
        candidatos = []
        r, c = fila + df, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            idx = r * 8 + c
            if s[idx] == rival:
                candidatos.append(idx)
                r += df
                c += dc
            elif s[idx] == jugador:
                a_voltear.extend(candidatos)
                break
            else:
                break

    return a_voltear


class Othello(js.JuegoZT2):
    """
    Juego de Othello basado en JuegoZT2.
    """

    def inicializa(self):
        tablero = [0] * 64
        # Posición inicial estándar del Othello
        tablero[27] = -1
        tablero[28] = 1
        tablero[35] = 1
        tablero[36] = -1
        # El elemento 64 indica si el turno anterior fue pase
        return tuple(tablero) + (0,)

    def jugadas_legales(self, s, j):
        legales = [pos for pos in range(64) if _fichas_a_voltear(s, pos, j)]
        # Si no hay jugadas válidas, el jugador debe pasar (None)
        return legales if legales else [None]

    def sucesor(self, s, a, j):
        if a is None:
            # Turno pasado, solo se marca el flag de pase
            return s[:64] + (1,)
        tablero = list(s[:64])
        tablero[a] = j
        for pos in _fichas_a_voltear(s, a, j):
            tablero[pos] = j
        return tuple(tablero) + (0,)

    def terminal(self, s):
        # Termina si el tablero está lleno
        if 0 not in s[:64]:
            return True
        # Termina si ambos jugadores no tienen jugadas válidas
        if s[64] == 1:
            j1_bloqueado = not any(_fichas_a_voltear(s, pos, 1) for pos in range(64))
            j2_bloqueado = not any(_fichas_a_voltear(s, pos, -1) for pos in range(64))
            if j1_bloqueado and j2_bloqueado:
                return True
        return False

    def ganancia(self, s):
        fichas1 = s[:64].count(1)
        fichas2 = s[:64].count(-1)
        if fichas1 > fichas2:
            return 1
        elif fichas2 > fichas1:
            return -1
        return 0


class InterfaceOthello(js.JuegoInterface):

    LETRAS = "ABCDEFGH"

    def muestra_estado(self, s):
        print()
        print("   A  B  C  D  E  F  G  H")
        for fila in range(8):
            fila_str = str(fila + 1) + "  "
            for col in range(8):
                celda = s[fila * 8 + col]
                if celda == 1:
                    fila_str += "●  "
                elif celda == -1:
                    fila_str += "○  "
                else:
                    fila_str += ".  "
            print(fila_str)
        fichas1 = s[:64].count(1)
        fichas2 = s[:64].count(-1)
        print(f"\n  ● Jugador 1: {fichas1}   ○ Jugador 2: {fichas2}\n")

    def muestra_ganador(self, g):
        if g == 1:
            print("¡Gana el Jugador 1 (●)!")
        elif g == -1:
            print("¡Gana el Jugador 2 (○)!")
        else:
            print("¡Empate!")

    def jugador_humano(self, s, j):
        simbolo = "●" if j == 1 else "○"
        print(f"Turno del Jugador {1 if j == 1 else 2} ({simbolo})")
        jugadas = list(self.juego.jugadas_legales(s, j))
        if jugadas == [None]:
            input("Sin jugadas disponibles. Presiona Enter para pasar...")
            return None

        def fmt(pos):
            return self.LETRAS[pos % 8] + str(pos // 8 + 1)

        print("Jugadas legales:", [fmt(p) for p in jugadas])
        jugada = None
        while jugada not in jugadas:
            raw = input("Escribe tu jugada (ej. D3): ").strip().upper()
            if len(raw) == 2 and raw[0] in self.LETRAS and raw[1].isdigit():
                col = self.LETRAS.index(raw[0])
                fila = int(raw[1]) - 1
                jugada = fila * 8 + col
            else:
                print("Formato inválido. Usa letra+número, ej. D3")
        return jugada


# Pesos posicionales clásicos de Othello:
# esquinas valen mucho, casillas X (adyacentes a esquina) son peligrosas
_PESOS = [
    120, -20, 20,  5,  5, 20, -20, 120,
    -20, -40, -5, -5, -5, -5, -40, -20,
     20,  -5, 15,  3,  3, 15,  -5,  20,
      5,  -5,  3,  3,  3,  3,  -5,   5,
      5,  -5,  3,  3,  3,  3,  -5,   5,
     20,  -5, 15,  3,  3, 15,  -5,  20,
    -20, -40, -5, -5, -5, -5, -40, -20,
    120, -20, 20,  5,  5, 20, -20, 120,
]


def ordena_othello(jugadas, jugador):
    """
    Ordena las jugadas de mayor a menor peso posicional.
    Las esquinas y bordes se exploran primero, mejorando la poda alfa-beta.
    El pase (None) siempre va al final.
    """
    return sorted(jugadas, key=lambda p: -_PESOS[p] if p is not None else -9999)


def evalua_othello(s):
    """
    Evaluación heurística del estado para el jugador 1. Combina:
    1. Puntaje posicional (tabla de pesos clásica de Othello)
    2. Esquinas conquistadas (valen mucho, son estables)
    3. Movilidad (diferencia de jugadas disponibles)
    4. Paridad de fichas (más importante al final del juego)

    Devuelve un valor entre -1 y 1.
    """
    tablero = s[:64]

    # 1) Puntaje posicional
    pos_score = sum(_PESOS[i] * tablero[i] for i in range(64))

    # 2) Esquinas
    esquinas = [0, 7, 56, 63]
    esq_score = sum(tablero[e] for e in esquinas) * 25

    # 3) Movilidad aproximada
    def movilidad(jugador):
        rival = -jugador
        return sum(
            1 for pos in range(64)
            if tablero[pos] == 0
            and any(
                0 <= _fila(pos) + df < 8 and 0 <= _col(pos) + dc < 8
                and tablero[(_fila(pos) + df) * 8 + (_col(pos) + dc)] == rival
                for df, dc in DIRECCIONES
            )
        )

    mob1 = movilidad(1)
    mob2 = movilidad(-1)
    mob_score = (mob1 - mob2) / max(mob1 + mob2, 1) * 100

    # 4) Paridad de fichas (peso creciente conforme avanza el juego)
    fichas1 = tablero.count(1)
    fichas2 = tablero.count(-1)
    total = fichas1 + fichas2
    paridad = (fichas1 - fichas2) / max(total, 1) * (total / 64) * 50

    total_score = pos_score + esq_score + mob_score + paridad
    return max(-1.0, min(1.0, total_score / 500.0))


if __name__ == '__main__':
    cfg = {
        "Jugador 1": "Humano",
        "Jugador 2": "Negamax",
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": ordena_othello,
        "evalua": evalua_othello,
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"],
                d=cfg["profundidad máxima"],
                evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"],
                ordena=cfg["ordena"],
                evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido: " + cadena)

    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("=" * 40)
    print("      *** Othello (Reversi) ***")
    print("=" * 40)
    print("Jugador 1 (●):", cfg["Jugador 1"])
    print("Jugador 2 (○):", cfg["Jugador 2"])
    print()
    print("Formato de jugada: letra (A-H) + número (1-8)")
    print("  Ejemplo: D3")
    print()
    interfaz.juega()