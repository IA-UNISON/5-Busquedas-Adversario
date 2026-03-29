"""
Juego de reversi

El estado se va a representar como una lista de 64 elementos, tal que


0  1  2  3  4  5  6  7
8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63



y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.
El juego inicia con 4 piesas en el centro 27=-1, 28=1, 35=1, 36=-1

Las acciones son poner una ficha en una casilla vacia

Un estado terminal es aquel en el que ninguno de los 2 jugadores tiene movimientos validos disponibles

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax
class Reversi(js.JuegoZT2):
    def inicializa(self):
            return (
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0, -1,  1,  0,  0,  0,
        0,  0,  0,  1, -1,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0
    )
            
    def jugadas_legales(self, s, j):
        oponente = -j
        movimientos_validos = [] 
  
        for pieza in range(64):
            if s[pieza] == j:
                
                # Arriba (-8)
                i = pieza
                rival = 0
                while True:
                    i -= 8
                    if i < 0: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Abajo (+8) 
                i = pieza
                rival = 0
                while True:
                    i += 8
                    if i > 63: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Izquierda (-1) 
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 0: break 
                    i -= 1
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Derecha (+1)
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 7: break 
                    i += 1
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Diagonal arriba izquierda (-9)
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 0: break 
                    i -= 9
                    if i < 0: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Diagonal arriba derecha (-7)
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 7: break 
                    i -= 7
                    if i < 0: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Diagonal abajo izquieda (+7) 
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 0: break 
                    i += 7
                    if i > 63: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

                # Diagonal abajo derecha (+9)
                i = pieza
                rival = 0
                while True:
                    if i % 8 == 7: break 
                    i += 9
                    if i > 63: break 
                    
                    if s[i] == oponente: 
                        rival += 1
                    elif s[i] == 0:
                        if rival > 0 and i not in movimientos_validos: 
                            movimientos_validos.append(i)
                        break
                    elif s[i] == j:
                        break

        return movimientos_validos
        
    def sucesor(self, s, a, j):
        if a is None:
            return s
        s = list(s[:])
        rival = -j
        s[a] = j
        # Arriba (-8)
        i = a
        volteo = []
        while True:
            i -= 8
            if i < 0: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Abajo (+8)
        i = a
        volteo = []
        while True:
            i += 8
            if i > 63: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Izquierda (-1)
        i = a
        volteo = []
        while True:
            if i % 8 == 0: break 
            i -= 1
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Derecha (+1)
        i = a
        volteo = []
        while True:
            if i % 8 == 7: break 
            i += 1
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Diagonal arriba izquierda (-9)
        i = a
        volteo = []
        while True:
            if i % 8 == 0: break 
            i -= 9
            if i < 0: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Diagonal arriba derecha (-7)
        i = a
        volteo = []
        while True:
            if i % 8 == 7: break 
            i -= 7
            if i < 0: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Diagonal abajo izquierda (+7)
        i = a
        volteo = []
        while True:
            if i % 8 == 0: break 
            i += 7
            if i > 63: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        # Diagonal abajo derecha (+9)
        i = a
        volteo = []
        while True:
            if i % 8 == 7: break 
            i += 9
            if i > 63: break 
            
            if s[i] == rival:
                volteo.append(i)
            elif s[i] == j:
                for p in volteo:
                    s[p] = j
                break
            elif s[i] == 0:
                break

        return tuple(s)

        
        
    def ganancia(self, s):
        return sum(s)
        
    def terminal(self, s):
        if 0 not in s:
            return True
        elif not self.jugadas_legales(s, 1) and not self.jugadas_legales(s, -1):
            return True
        return False

class InterfaceReversi(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el tablero de 8x8. Si la casilla está vacía, muestra su índice (0-63)
        para que el humano sepa exactamente qué número teclear.
        """
        # Formateamos cada casilla. Si es 0 (vacío), ponemos su índice centrado.
        a = [' X ' if x == 1 else ' O ' if x == -1 else f'{i:^3}' for i, x in enumerate(s)]
        
        print('\n')
        for i in range(8):
            # Imprimimos la fila tomando bloques de 8 elementos
            print('|'.join(a[8 * i : 8 * (i + 1)]))
            # Imprimimos los separadores, menos en la última fila
            if i < 7:
                print('---+---+---+---+---+---+---+---')
        print('\n')
    
    def muestra_ganador(self, g):
        """
        Como tu ganancia regresa la suma del tablero (positiva = X, negativa = O),
        evaluamos si es mayor o menor a cero.
        """
        if g > 0:
            print(f"Gana el jugador X por una ventaja de {g} fichas")
        elif g < 0:
            print(f"Gana el jugador O por una ventaja de {abs(g)} fichas")
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
    
        print("Turno del jugador", " XO"[j])
        
        # Ojo: asegúrate de que self.juego.jugadas_legales apunte bien a la función que armamos
        jugadas = self.juego.jugadas_legales(s, j)
        
        # Si la lista de jugadas está vacía, el jugador tiene que pasar turno
        if not jugadas:
            print("¡No tienes jugadas legales! Pasas turno.")
            input("Presiona Enter para continuar...")
            return None # O el valor que tu código principal use para detectar un "salto" de turno
        
            
        print("Jugadas legales:", jugadas)
        jugada = -1
    
        
        while jugada not in jugadas:
            try:
                jugada = int(input("Jugada (teclea el número de la casilla): "))
                if jugada not in jugadas:
                    print("¡Jugada ilegal! Elige uno de los números de la lista.")
            except ValueError:
                print("Por favor, ingresa un número entero válido.")
                
        return jugada
    def juega(self, max_pasos=1_000):
        s = self.juego.inicializa()
        self.muestra_estado(s)
        j = 1
        pasos = 0
        while not self.juego.terminal(s) and pasos < max_pasos:
            if self.juego.jugadas_legales(s, j):
                a = self.pide_jugada(self.jugador[j], s, j)
                s = self.juego.sucesor(s, a, j)
                self.muestra_estado(s)
            j = -j
            pasos += 1
        self.muestra_ganador(self.juego.ganancia(s))
 
    
#mejores jugadas: Esquinas, lados, no a lado de esquinas ni diagonales de ahi
pesos = (
     100, -20,  10,   5,   5,  10, -20,  100,
     -20, -50,  -2,  -2,  -2,  -2, -50,  -20,
      10,  -2,   1,   1,   1,   1,  -2,   10,
       5,  -2,   1,   0,   0,   1,  -2,    5,
       5,  -2,   1,   0,   0,   1,  -2,    5,
      10,  -2,   1,   1,   1,   1,  -2,   10,
     -20, -50,  -2,  -2,  -2,  -2, -50,  -20,
     100, -20,  10,   5,   5,  10, -20,  100
)

def ordena_esquinas(jugadas, jugador, s, juego):
    """
    Ordena las jugadas priorizando las esquinas y los bordes, 
    y dejando hasta el final las casillas peligrosas (adyacentes a esquinas).
    """
    return sorted(jugadas, key=lambda x: pesos[x] if x is not None else -1000, reverse=True)
def evalua_reversi(s):
    """
    Evalua el estado s para Reversi usando un mapa de pesos posicionales
    y control de esquinas.
    """
    # Multiplicamos el valor de cada casilla en el tablero 
    # por el peso estratégico de esa misma casilla.
    evaluacion = sum(s[i] * pesos[i] for i in range(64))
    promedio = evaluacion / 800
    
    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)
        
    return promedio


if __name__ == '__main__':
    
    cfg = {
        "Jugador 1": "Humano",      # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",   # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,    # Puedes subirle a 6 o 7 si ves que tu IA piensa muy rápido
        "tiempo": 10,
        "ordena": ordena_esquinas,  #Puede ser None o una función f(jugadas, j)
        "evalua": evalua_reversi    #Puede ser None o una función f(estado) -> número entre -1 y 1
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

    interfaz = InterfaceReversi(
        Reversi(), 
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("=== El Juego del Reversi ===")
    print("Jugador 1 (X):", cfg["Jugador 1"])
    print("Jugador 2 (O):", cfg["Jugador 2"])
    print("============================")
    print()

    interfaz.juega()