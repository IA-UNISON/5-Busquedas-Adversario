from juegos_simplificado import ModeloJuegoZT2, juega_dos_jugadores
from minimax import jugador_negamax, minimax_iterativo

__author__ = "joaquinsotelo"

class UltimateTicTacToe(ModeloJuegoZT2):


    def inicializa(self):

        tableros = tuple(tuple([0] * 9) for _ in range(9))
        tablero_actual = -1
        ultimo_movimiento = None
        return ((tableros, tablero_actual, ultimo_movimiento), 1)

    def jugadas_legales(self, s, j):


        tableros, tablero_actual, _ = s

        jugadas = []


        if tablero_actual != -1:
            tablero = tableros[tablero_actual]

            if self._tablero_lleno(tablero) or self._hay_ganador(tablero):
                tablero_actual = -1
            else:

                for pos in range(9):
                    if tablero[pos] == 0:
                        jugadas.append((tablero_actual, pos))
                return jugadas


        if tablero_actual == -1:
            for tb in range(9):
                tablero = tableros[tb]

                if not self._tablero_lleno(tablero) and not self._hay_ganador(tablero):
                    for pos in range(9):
                        if tablero[pos] == 0:
                            jugadas.append((tb, pos))

        return jugadas

    def transicion(self, s, a, j):


        tableros, _, _ = s
        tablero_idx, pos = a


        tableros_nuevos = list(tableros)
        for i in range(9):
            if i == tablero_idx:

                tablero = list(tableros[i])
                tablero[pos] = j
                tableros_nuevos[i] = tuple(tablero)
            else:
                tableros_nuevos[i] = tableros[i]


        proximo_tablero = pos
        if (self._tablero_lleno(tableros_nuevos[proximo_tablero]) or
            self._hay_ganador(tableros_nuevos[proximo_tablero])):
            proximo_tablero = -1

        return (tuple(tableros_nuevos), proximo_tablero, (tablero_idx, pos))

    def terminal(self, s):

        tableros, _, _ = s


        if self._hay_ganador_global(tableros):
            return True


        tableros_disponibles = 0
        for tablero in tableros:
            if not self._tablero_lleno(tablero) and not self._hay_ganador(tablero):
                tableros_disponibles += 1

        return tableros_disponibles == 0

    def ganancia(self, s):

        tableros, _, _ = s


        meta_tablero = self._obtener_meta_tablero(tableros)


        for linea in self._lineas_ganadoras():
            if (meta_tablero[linea[0]] == meta_tablero[linea[1]] == meta_tablero[linea[2]] != 0):
                return meta_tablero[linea[0]]

        return 0

    def _tablero_lleno(self, tablero):

        return 0 not in tablero

    def _hay_ganador(self, tablero):

        for linea in self._lineas_ganadoras():
            if (tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] != 0):
                return True
        return False

    def _obtener_ganador_tablero(self, tablero):

        for linea in self._lineas_ganadoras():
            if (tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] != 0):
                return tablero[linea[0]]
        return 0

    def _obtener_meta_tablero(self, tableros):


        meta_tablero = [0] * 9
        for i, tablero in enumerate(tableros):
            meta_tablero[i] = self._obtener_ganador_tablero(tablero)
        return meta_tablero

    def _hay_ganador_global(self, tableros):

        meta_tablero = self._obtener_meta_tablero(tableros)
        for linea in self._lineas_ganadoras():
            if (meta_tablero[linea[0]] == meta_tablero[linea[1]] == meta_tablero[linea[2]] != 0):
                return True
        return False

    def _lineas_ganadoras(self):

        return [

            (0, 1, 2), (3, 4, 5), (6, 7, 8),

            (0, 3, 6), (1, 4, 7), (2, 5, 8),

            (0, 4, 8), (2, 4, 6)
        ]


def pprint_ultimate_tictactoe(s):

    tableros, tablero_actual, ultimo_movimiento = s

    simbolos = {0: ' ', 1: 'X', -1: 'O'}

    print("\n" + "="*31)

    for fila_tableros in range(3):

        for fila_celdas in range(3):
            for tb_col in range(3):
                tb_idx = fila_tableros * 3 + tb_col


                if tb_idx == tablero_actual:
                    print("!", end="")
                else:
                    print(" ", end="")


                for cel_col in range(3):
                    pos = fila_celdas * 3 + cel_col
                    celda = tableros[tb_idx][pos]


                    if ultimo_movimiento and ultimo_movimiento == (tb_idx, pos):
                        print("[" + simbolos[celda] + "]", end="")
                    else:
                        print(" " + simbolos[celda] + " ", end="")


                if tb_col < 2:
                    print(" |", end="")

            print()


        if fila_tableros < 2:
            print("-" * 31)

    print("="*31)


    meta_tablero = [" "] * 9
    for i, tablero in enumerate(tableros):
        ganador = UltimateTicTacToe()._obtener_ganador_tablero(tablero)
        meta_tablero[i] = simbolos[ganador]

    print("\nEstado global:")
    print(" {} | {} | {} ".format(meta_tablero[0], meta_tablero[1], meta_tablero[2]))
    print("---+---+---")
    print(" {} | {} | {} ".format(meta_tablero[3], meta_tablero[4], meta_tablero[5]))
    print("---+---+---")
    print(" {} | {} | {} ".format(meta_tablero[6], meta_tablero[7], meta_tablero[8]))


def jugador_manual_gui(gui):

    def pedir_jugada(juego, estado, jugador):
        jugadas = list(juego.jugadas_legales(estado, jugador))

        gui.jugada_usuario = None
        gui.esperando_jugada = True

        def on_click(jugada):
            gui.esperando_jugada = False
            gui.callback_jugada = None
            gui.root.quit()

        gui.callback_jugada = on_click
        gui.root.mainloop()
        return gui.jugada_usuario

    return pedir_jugada


def jugador_manual_ultimate_tictactoe(juego, s, j):

    pprint_ultimate_tictactoe(s)
    print("\nJugador " + ("X" if j == 1 else "O"))

    tableros, tablero_actual, _ = s


    if tablero_actual != -1:
        print(f"Debes jugar en el tablero {tablero_actual + 1}")
    else:
        print("Puedes jugar en cualquier tablero")

    jugadas = list(juego.jugadas_legales(s, j))


    print("\nJugadas disponibles:")
    for i, (tablero, pos) in enumerate(jugadas):
        fila, col = pos // 3, pos % 3
        print(f"{i+1}. Tablero {tablero + 1}, posición ({fila + 1},{col + 1})")


    seleccion = -1
    while seleccion < 0 or seleccion >= len(jugadas):
        try:
            seleccion = int(input("\nElige una jugada (1-{}): ".format(len(jugadas)))) - 1
        except ValueError:
            print("Por favor, introduce un número válido.")

    return jugadas[seleccion]


def ordena_centro_ultimate(jugadas, jugador=None):


    def valor_posicion(pos):

        valores = {
            4: 3,
            0: 2, 2: 2, 6: 2, 8: 2,
            1: 1, 3: 1, 5: 1, 7: 1
        }
        return valores.get(pos, 0)

    def valor_tablero(tablero):

        valores = {
            4: 3,
            0: 2, 2: 2, 6: 2, 8: 2,
            1: 1, 3: 1, 5: 1, 7: 1
        }
        return valores.get(tablero, 0)


    return sorted(
        jugadas,
        key=lambda jugada: (valor_posicion(jugada[1]) + valor_tablero(jugada[0])),
        reverse=True
    )
def ordena_estrategico_ultimate(jugadas, juego, s, j):


    if juego is None:

        juego = UltimateTicTacToe()
    if s is None:

        global _estado_actual

        s = _estado_actual
    if j is None:

        j = 1
    if s is None:


        return ordena_centro_ultimate(jugadas)
    tableros, _, _ = s
    valoraciones = []

    for jugada in jugadas:
        tablero_idx, pos = jugada


        tablero_original = tableros[tablero_idx]
        tablero_simulado = list(tablero_original)
        tablero_simulado[pos] = j
        tablero_simulado = tuple(tablero_simulado)

        valor = 0


        if pos == 4:
            valor += 3
        elif pos in (0, 2, 6, 8):
            valor += 2
        else:
            valor += 1


        if tablero_idx == 4:
            valor += 3
        elif tablero_idx in (0, 2, 6, 8):
            valor += 2
        else:
            valor += 1


        if not juego._hay_ganador(tablero_original):
            lineas = juego._lineas_ganadoras()
            for linea in lineas:
                if pos in linea:

                    if (all(tablero_simulado[p] == j for p in linea)):
                        valor += 100


        oponente = -j
        for linea in juego._lineas_ganadoras():
            if pos in linea:

                fichas_oponente = sum(1 for p in linea if tablero_original[p] == oponente)

                if fichas_oponente == 2 and all(tablero_original[p] != j for p in linea if p != pos):
                    valor += 50


        siguiente_tablero = pos
        if siguiente_tablero < 9:

            if (juego._hay_ganador(tableros[siguiente_tablero]) or
                juego._tablero_lleno(tableros[siguiente_tablero])):
                valor += 20
            elif siguiente_tablero == 4:
                valor -= 15

        valoraciones.append((jugada, valor))


    valoraciones.sort(key=lambda x: x[1], reverse=True)
    return [v[0] for v in valoraciones]


def evalua_simple_ultimate(s, j=None):


    juego = UltimateTicTacToe()
    tableros, _, _ = s


    if j is None:
        j = 1


    if juego.terminal(s):
        return juego.ganancia(s) * j


    meta_tablero = juego._obtener_meta_tablero(tableros)


    tableros_j = meta_tablero.count(j)
    tableros_oponente = meta_tablero.count(-j)


    return (tableros_j - tableros_oponente) / 9

def evalua_avanzada_ultimate(s, j=None):


    juego = UltimateTicTacToe()
    tableros, tablero_actual, _ = s


    if j is None:
        j = 1


    if juego.terminal(s):
        ganancia = juego.ganancia(s)

        return ganancia * j


    meta_tablero = juego._obtener_meta_tablero(tableros)


    tableros_j = meta_tablero.count(j)
    tableros_oponente = meta_tablero.count(-j)
    valor_tableros = (tableros_j - tableros_oponente) / 9 * 0.5


    valor_lineas = 0
    for linea in juego._lineas_ganadoras():

        fichas_propias = sum(1 for pos in linea if meta_tablero[pos] == j)
        fichas_oponente = sum(1 for pos in linea if meta_tablero[pos] == -j)


        if fichas_propias > 0 and fichas_oponente == 0:
            valor_lineas += fichas_propias * 0.1


        if fichas_oponente > 0 and fichas_propias == 0:
            valor_lineas -= fichas_oponente * 0.1


    valor_estrategico = 0
    posiciones_clave = {
        4: 0.1,
        0: 0.05, 2: 0.05, 6: 0.05, 8: 0.05
    }

    for pos, valor in posiciones_clave.items():
        if meta_tablero[pos] == j:
            valor_estrategico += valor
        elif meta_tablero[pos] == -j:
            valor_estrategico -= valor


    valor_tactico = 0
    for idx, tablero in enumerate(tableros):

        if meta_tablero[idx] == 0 and not juego._tablero_lleno(tablero):

            piezas_j = tablero.count(j)
            piezas_oponente = tablero.count(-j)


            multiplicador = 1.0
            if idx == 4:
                multiplicador = 1.5
            elif idx in (0, 2, 6, 8):
                multiplicador = 1.2

            ventaja_tablero = (piezas_j - piezas_oponente) / 9 * 0.05 * multiplicador
            valor_tactico += ventaja_tablero


            for linea in juego._lineas_ganadoras():

                propias_linea = sum(1 for pos in linea if tablero[pos] == j)
                vacias_linea = sum(1 for pos in linea if tablero[pos] == 0)


                if propias_linea == 2 and vacias_linea == 1:
                    valor_tactico += 0.1


                oponente_linea = sum(1 for pos in linea if tablero[pos] == -j)
                if oponente_linea == 2 and vacias_linea == 1:
                    valor_tactico -= 0.08


    valor_movimiento = 0
    if tablero_actual != -1:

        if juego._hay_ganador(tableros[tablero_actual]) or juego._tablero_lleno(tableros[tablero_actual]):

            valor_movimiento -= 0.05
        elif tablero_actual == 4:

            valor_movimiento += 0.05


    valor_final = (
        valor_tableros * 0.4 +
        valor_lineas * 0.25 +
        valor_estrategico * 0.15 +
        valor_tactico * 0.15 +
        valor_movimiento * 0.05
    )


    return max(min(valor_final, 0.99), -0.99)


_estado_actual = None

def set_estado_actual(estado):

    global _estado_actual
    _estado_actual = estado


def ordena_con_estado_actual(jugadas, j=None):


    global _estado_actual

    if j is None:
        j = 1

    if _estado_actual is None:

        return ordena_centro_ultimate(jugadas)


    return ordena_estrategico_ultimate(jugadas, UltimateTicTacToe(), _estado_actual, j)


def negamax_con_estado_actual(juego, s, j, d):

    set_estado_actual(s)
    return jugador_negamax(juego, s, j, ordena=ordena_con_estado_actual, evalua=evalua_avanzada_ultimate, d=d)


def minimax_iter_con_estado_actual(juego, s, j, tiempo):

    set_estado_actual(s)
    return minimax_iterativo(juego, s, j, ordena=ordena_con_estado_actual, evalua=evalua_avanzada_ultimate, tiempo=tiempo)


if __name__ == '__main__':
    modelo = UltimateTicTacToe()
    print("="*40 + "\n" + "ULTIMATE TIC-TAC-TOE".center(40) + "\n" + "="*40)
    print("\nReglas:")
    print("- El tablero contiene 9 tableros pequeños de Tic-Tac-Toe")
    print("- El movimiento en un tablero pequeño determina en qué tablero jugará el siguiente jugador")
    print("- Para ganar, consigue 3 tableros pequeños en línea")
    print("- Si te envían a un tablero ya ganado o lleno, podrás elegir cualquier tablero")
    print("\nSimbología:")
    print("- X: Jugador 1, O: Jugador 2")
    print("- [X] o [O]: Último movimiento realizado")
    print("- !: Indica el tablero donde toca jugar")
    print("\nVamos a jugar!\n")

    jugs = []
    for j in [1, -1]:
        print(f"Selección de jugadores para las {' XO'[j]}:")
        sel = 0
        print("   1. Jugador humano")
        print("   2. IA simple (prioriza centro, profundidad limitada)")
        print("   3. IA simple (prioriza centro, tiempo limitado)")
        print("   4. IA avanzada (estratégica, profundidad limitada)")
        print("   5. IA avanzada (estratégica, tiempo limitado)")

        while sel not in [1, 2, 3, 4, 5]:
            try:
                sel = int(input(f"Jugador para las {' XO'[j]}: "))
            except ValueError:
                print("Por favor, introduce un número válido.")

        if sel == 1:
            jugs.append(jugador_manual_ultimate_tictactoe)
        elif sel == 2:
            d = None
            while not isinstance(d, int) or d < 1:
                try:
                    d = int(input("Profundidad (recomendado 2-4): "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: jugador_negamax(
                juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, d=d)
            )
        elif sel == 3:
            t = None
            while not isinstance(t, int) or t < 1:
                try:
                    t = int(input("Tiempo en segundos: "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: minimax_iterativo(
                juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, tiempo=t)
            )
        elif sel == 4:
            d = None
            while not isinstance(d, int) or d < 1:
                try:
                    d = int(input("Profundidad (recomendado 2-4): "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: negamax_con_estado_actual(juego, s, j, d))
        else:
            t = None
            while not isinstance(t, int) or t < 1:
                try:
                    t = int(input("Tiempo en segundos: "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: minimax_iter_con_estado_actual(juego, s, j, t))


    print("\n¡Comienza el juego!\n")
    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])


    print("\nFIN DEL JUEGO\n")
    pprint_ultimate_tictactoe(s_final)

    if g != 0:
        print("\nGana el jugador " + " XO"[g])
    else:
        print("\nEmpate")
