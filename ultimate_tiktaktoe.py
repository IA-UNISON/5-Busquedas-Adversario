import juegos_simplificado as js

class tiktaktoe(js.JuegoZT2):
    """Juego ultimate tik tak toe"""
    def inicializa(self):
        return tuple([0] * 90 + [-2])
    
    BLOQUES = {}
    BLOQUE_PADRE = {}

    for i in range(3):
        for j in range(3):
            id_bloque = i * 3 + j
            celdas = []

            for r in range(3):
                for c in range(3):
                    idx = (i * 3 + r) * 9 + (j * 3 + c)
                    celdas.append(idx)
                    BLOQUE_PADRE[idx] = id_bloque
            BLOQUES[id_bloque] = celdas
            

    def jugadas_legales(self, s, j):
        ultima = s[90]

        #Primera jugada
        if ultima == -2:
            return [i for i in range(81) if s[i] == 0]
        
        bloque_destino = (ultima // 9 % 3) * 3 + (ultima % 9 % 3)

        if s[81 + bloque_destino] == 0:
            libres = [i for i in self.BLOQUES[bloque_destino] if s[i] == 0]
            if libres:
                return libres

        legales = []
        for i in range(81):
            # La casilla debe estar vacía 
            # Y el bloque al que pertenece esa casilla debe estar disponible (0)
            if s[i] == 0 and s[81 + self.BLOQUE_PADRE[i]] == 0:
                legales.append(i)
                
        return legales

        
    def gano_bloque(self, tablero, id_bloque, j):
        indices_bloque = self.BLOQUES[id_bloque]
        c = [tablero[i] for i in indices_bloque]

        lineas = [
            (0,1,2), (3,4,5), (6,7,8), # Horizontales
            (0,3,6), (1,4,7), (2,5,8), # Verticales
            (0,4,8), (2,4,6)           # Diagonales
        ]

        for a, b, c_ in lineas:
            if c[a] == c[b] == c[c_] == j:
                return True
        return False


    def sucesor(self, s, a, j):
        if s[a] != 0:
            raise ValueError("Celda ocupada")
        
        # Convertir a lista para poder modificar
        nuevo_estado = list(s)

        # Marcar la jugada en el tablero
        nuevo_estado[a] = j
        
        id_bloque = self.BLOQUE_PADRE[a]
        

        # Si el bloque no estaba ganado revisamos si se ganó
        if nuevo_estado[81 + id_bloque] == 0:
            if self.gano_bloque(nuevo_estado[:81], id_bloque, j):
                nuevo_estado[81 + id_bloque] = j #j ganó ese bloque
        
        nuevo_estado[90] = a

        return tuple(nuevo_estado)



    def terminal(self, s):
        # Tomamos los indices de los 9 bloques
        bloques_ganados = s[81 : 90]

        # Lineas ganadoras
        lineas = [
            (0,1,2), (3,4,5), (6,7,8), # Horizontales
            (0,3,6), (1,4,7), (2,5,8), # Verticales
            (0,4,8), (2,4,6)           # Diagonales
        ]

        # Revisamos si el jugador j gana el tablero global

        for a, b, c in lineas:
            if bloques_ganados[a] == bloques_ganados[b] == bloques_ganados[c] != 0:
                return bloques_ganados[a] # 1 o -1 (el ganador)
            
        # Revisamos si es un empate
        if not self.jugadas_legales(s, 1):
            return 0 # 0 es empate
        
        return None
    
    def evaluar_amenazas_globales(self, meta):
        puntos = 0
        lineas = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        
        for a, b, c in lineas:
            trieta = [meta[a], meta[b], meta[c]]
            # Si j1 tiene 2 bloques y el otro está vacío: peligro inminente
            if trieta.count(1) == 2 and trieta.count(0) == 1:
                puntos += 50
            
            # Si j2 tiene 2 bloques y el otro está vacío
            elif trieta.count(-1) == 2 and trieta.count(0) == 1:
                puntos += -50

        return puntos

    """
        La función de ganancia se establecio de esta manera para priorizar el control del
        tablero antes que ganar un bloque
    """

    def ganancia(self, s):
        res = self.terminal(s)
        if res is not None:
            return res * 100000 # Victoria/Derrota total

        puntuacion = 0
        meta = s[81:90]
        pesos_meta = [30, 20, 30, 20, 40, 20, 30, 20, 30]
        pesos_locales = [3, 2, 3, 2, 4, 2, 3, 2, 3]

        # Valor de bloques ganados (Estado actual del meta-tablero)
        for i in range(9):
            if meta[i] != 0:
                puntuacion += meta[i] * pesos_meta[i] * 50

        # Amenazas globales (2 bloques en línea)
        puntuacion += self.evaluar_amenazas_globales(meta)

        # Evaluación detallada casilla por casilla
        for i in range(81):
            if s[i] != 0:
                id_b = self.BLOQUE_PADRE[i]
                # Si el bloque ya está ganado, las fichas individuales ya no valen
                if meta[id_b] == 0:
                    pos_l = i % 9
                    # Puntos = (Quien tira) * (Valor posición) * (Valor del bloque)
                    puntuacion += s[i] * pesos_locales[pos_l] * pesos_meta[id_b]
        
        return puntuacion
    


class InterfazMetaGato(js.JuegoInterface):
    def __init__(self, juego, jugador1, jugador2):
        super().__init__(juego, jugador1, jugador2)
        self.simbolos = {0: " ", 1: "X", -1: "O"}

    def muestra_estado(self, s):
        tablero = s[:81]
        meta = s[81:90]
        print("\n" + "="*35)
        for fila_bloque in range(3):
            for fila_interna in range(3):
                linea = " "
                for col_bloque in range(3):
                    for col_interna in range(3):
                        idx = (fila_bloque * 27) + (fila_interna * 9) + (col_bloque * 3) + col_interna
                        linea += f" {self.simbolos[tablero[idx]]} "
                        if col_interna < 2: linea += "|"
                    if col_bloque < 2: linea += " ║ "
                print(linea)
                if fila_interna < 2:
                    print(" ---+---+--- ║ ---+---+--- ║ ---+---+---")
            if fila_bloque < 2: print("="*35)
        print("="*35)
        print(f"Estado de bloques (81-89): {s[81:90]}")
        print(f"Puntero de última jugada (90): {s[90]}")
        
    def muestra_ganador(self, ganancia):
        if ganancia > 0: print("\n¡GANADOR: X!")
        elif ganancia < 0: 
            print("\n¡GANADOR: O!")
        else: print("\n¡EMPATE!")

    def jugador_humano(self, s, j):
        print(f"\n--- Turno de: {self.simbolos[j]} ---")
        legales = self.juego.jugadas_legales(s, j)
        
        # 1. Calculamos y mostramos el bloque obligatorio
        ultima_jugada = s[90]
        if ultima_jugada == -2:
            print("ESTADO: Inicio del juego. Puedes tirar en cualquier bloque.")
        else:
            bloque_dest = (ultima_jugada // 9 % 3) * 3 + (ultima_jugada % 9 % 3)
            
            # Verificamos si es "libertad total" porque el bloque destino está lleno/ganado
            # Si la cantidad de jugadas legales es grande, es señal de libertad total
            if len(legales) > 9:
                print(f"BLOQUE DESTINO: {bloque_dest} (¡Pero está lleno o ganado! Tienes LIBERTAD TOTAL)")
            else:
                print(f"BLOQUE DESTINO OBLIGATORIO: {bloque_dest}")

        print(f"Casillas permitidas: {legales}")
        
        jugada = None
        while jugada not in legales:
            try:
                dato = input(f"Elige casilla : ")
                jugada = int(dato)
                
                if jugada not in legales:
                    print(f"Ojo: La casilla {jugada} no está permitida ahora.")
            except ValueError:
                print("Por favor, ingresa un número entero.")
                
        return jugada


class JugadorUltimate(js.Jugador):
    def __init__(self, profundidad=4): # 4 niveles
        self.profundidad = profundidad

    def jugada(self, juego, s, j):
        
        return self.alpha_beta_limitado(juego, s, j, self.profundidad)

    def alpha_beta_limitado(self, juego, s, j, depth):
        def max_val(s, j, alfa, beta, d):
            if juego.terminal(s) or d == 0:
                return juego.ganancia(s) 
            v = -float('inf')
            
            for a in ordena_meta_gato(juego.jugadas_legales(s, j)):
                v = max(v, min_val(juego.sucesor(s, a, j), -j, alfa, beta, d - 1))
                if v >= beta: return v
                alfa = max(alfa, v)
            return v

        def min_val(s, j, alfa, beta, d):
            if juego.terminal(s) or d == 0:
                return juego.ganancia(s)
            v = float('inf')
            
            for a in ordena_meta_gato(juego.jugadas_legales(s, j)):
                v = min(v, max_val(juego.sucesor(s, a, j), -j, alfa, beta, d - 1))
                if v <= alfa: return v
                beta = min(beta, v)
            return v

        jugadas = ordena_meta_gato(juego.jugadas_legales(s, j))
        # Elegimos la mejor jugada basándonos en la evaluación
        return max(jugadas, key=lambda a: min_val(juego.sucesor(s, a, j), -j, -1e10, 1e10, depth - 1))

"""
    Esta es la heurística utilizada, ya que se le otorga prioridad a ganar el centro,
    izquinas y al final los centros a las orillas, para lograr que la poda alfa-beta 
    sea más eficiente
"""
def ordena_meta_gato(jugadas):
    # Pesos de importancia para el ordenamiento (0-8)
    pesos_locales = [2, 1, 2, 
                     1, 3, 1, 
                     2, 1, 2]
    
    # Ordenamos la lista de jugadas basándonos en su posición local
    # reverse=True para que las de mayor peso (el centro) vayan primero
    return sorted(jugadas, key=lambda a: pesos_locales[a % 9], reverse=True)



if __name__ == '__main__':
    juego_meta = tiktaktoe()
    
    interfaz = InterfazMetaGato(
        juego_meta, 
        jugador1=JugadorUltimate(profundidad=4),
        jugador2=js.JugadorAleatorio()
    )
    
    interfaz.juega()