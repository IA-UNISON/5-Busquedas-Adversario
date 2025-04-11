"""
Juego del Otello

El estado se va a representar como una tupla de 64 elementos 
pensandolo como una matriz de 8x8, donde `estado[8*i + j]`
es la casilla en la fila `i` y la columna `j`.

0  1  2  	3  4  	5  6  7
8  9  10 	11 12 	13 14 15
16 17 18 	19 20 	21 22 23

24 25 26 	27 28 	29 30 31
32 33 34 	35 36 	37 38 39

40 41 42	43 44 	45 46 47
48 49 50 	51 52	53 54 55
56 57 58 	59 60 	61 62 63

Esta tupla va a guardar el estado de cada casilla

0 si está vacía
1 si hay una ficha negra
-1 si hay una ficha blanca

Las negras empiezan primero en Otello.

Las acciones van a ser representadas como una tupla de números
`(i,j)` que representa la casilla en la que se pone una ficha,
donde `i` es el índice de la fila y `j` es el índice de la
columna.

En Otello, cuando no hay acciones legales para un jugador
pero si para el otro se omite el turno.

En dicho caso consideraré omitir turno como una acción legal
y la representaré como `None`.

"""

from juegos_simplificado import ModeloJuegoZT2
from re import match
from minimax import jugador_negamax
from minimax import minimax_iterativo

class Otello(ModeloJuegoZT2):
    def inicializa(self):
        return ((0, 0, 0, 0, 0, 0, 0, 0,
        		 0, 0, 0, 0, 0, 0, 0, 0,
        		 0, 0, 0, 0, 0, 0, 0, 0,
        		 0, 0, 0,-1, 1, 0, 0, 0,
        		 0, 0, 0, 1,-1, 0, 0, 0,
        		 0, 0, 0, 0, 0, 0, 0, 0,
        		 0, 0, 0, 0, 0, 0, 0, 0,
        		 0, 0, 0, 0, 0, 0, 0, 0,),
        		1)

    def jugadas_legales(self, s, jugador):
        def es_legal(a):
            if s[a[0] * 8 + a[1]] != 0:
                return False

            for inc_i in (-1,0,1):
                for inc_j in (-1,0,1):
                    i = a[0] + inc_i
                    j = a[1] + inc_j

                    if((inc_i == inc_j == 0) or
                       (not (0 <= i < 8)) or 
                       (not (0 <= j < 8)) or
                       (s[i * 8 + j] != -jugador)):
                            continue

                    i += inc_i
                    j += inc_j

                    while (0 <= i < 8) and (0 <= j < 8): 
                        if s[i * 8 + j] == jugador:
                            return True
                        if s[i * 8 + j] == 0:
                            break
                        i += inc_i
                        j += inc_j
            return False

        acciones = ()
        for fila in range(8):
            for columna in range(8):
                accion = (fila, columna)
                if es_legal(accion):
                    acciones += (accion,)

        return (acciones if acciones else (None,))

    def transicion(self, s, a, jugador):
        if a == None:
            return s

        estado = list(s)
        for inc_i in (-1,0,1): 
            for inc_j in (-1,0,1):
                if inc_i == inc_j == 0:
                    continue

                i, j = a
                contador = 0

                while(True):
                    i += inc_i
                    j += inc_j

                    if ((not (0 <= i < 8)) or
                        (not (0 <= j < 8)) or
                        (estado[i * 8 + j] == 0)):
                            contador = 0
                            break

                    if estado[i * 8 + j] == jugador:
                        break

                    contador += 1

                while contador > 0:
                    i -= inc_i
                    j -= inc_j
                    contador -= 1
                    estado[i * 8 + j] = jugador

        estado[a[0]*8 + a[1]] = jugador
        return tuple(estado)

    def ganancia(self, s):
        suma_piezas = sum(s)
        return (1 if suma_piezas > 0 else
                0 if suma_piezas == 0 else -1)

    def terminal(self, s):
        return (self.jugadas_legales(s,1) == (None,) ==
                self.jugadas_legales(s,-1))

def evaluar(s):
    salida = 0
    for i in range(64):
        salida += s[i]

    salida += 9*(s[0] + s[7] + s[56] + s[63])

    return salida/100 # 64 + 4*9


    return 0

def ordenar(jugadas, jugador):
    def casillas_peligrosas(a):
        if a == None:
            return 0

        # centro
        if (a[0]-2) in range(4) and (a[1]-2) in range(4):
            return 1

        # cuadros peligrosos
        if a in ((0,1),(1,0),(0,6),(6,0),
                 (1,6),(6,1),(1,7),(7,1),
                 (6,7),(7,6),(1,1),(6,6)):
            return 3

        # esquinas
        if ((a[0] == 0 or a[0] == 7) and (a[1] == 0 or a[1] == 7)):
            return 0

        return 2
    return sorted(jugadas, key=casillas_peligrosas)

# se muestra con un `*` las casillas indicadas por
# `acciones`, esto se usa para mostrar las acciones legales
def pprint_estado(s,acciones=()):
    acciones = list(acciones)
    print(' |', end='')
    for i in 'abcdefgh':
        print(i + '|', end='')
    print('')
    for i in range(8):
        print('-+'*9)

        print(i+1, end='|')
        for j in range(8):
            if (acciones and (acciones[0] != None) and
               (acciones[0] == (i, j) )):
                print('*',end='|')
                acciones.pop(0)
            else:
                print(' NB'[s[i * 8 + j]],end='|')

        print('')

def pprint_accion(accion, fin='\n'):
    print('abcdefgh'[accion[1]] + str(accion[0]+1),end=fin)

def jugador_artificial(iterativo, num):

    def jugador(juego, estado, jugador):
        acciones = juego.jugadas_legales(estado,jugador)
        pprint_estado(estado,acciones)

        accion = None
        if iterativo:
            accion = minimax_iterativo(
                juego, estado, jugador,
                ordena=ordenar, evalua=evaluar, tiempo=num)
        else:
            accion = jugador_negamax(
                juego, estado, jugador,
                ordena=ordenar, evalua=evaluar, d=num)

        return accion

    return jugador

def jugador_manual(juego, estado, jugador):
    acciones = juego.jugadas_legales(estado,jugador)
    pprint_estado(estado, acciones)
    accion = None

    while accion not in acciones:
        print('\nElige acción ([a-h][1-8]):')
        entrada = input()
        if match("[a-h][1-8]\\Z", entrada):
            accion = (int(entrada[1]) - 1, 'abcdefgh'.find(entrada[0]))

    if accion == None:
        print('No hay acciones legales para las piezas ',end='')
        print(('negras' if jugador == 1 else 'blancas'),end='\n\n')

    return accion

def simulacion_otello(jugador1, jugador2):
    juego = Otello()
    s, j = juego.inicializa()
    while not juego.terminal(s):
        a = jugador1(juego, s, j) if j == 1 else jugador2(juego, s, j)
        s = juego.transicion(s, a, j)

        if a == None:
            print('\nNo hay acciones legales para las piezas ',end='')
            print(('negras' if j == 1 else 'blancas'),end='\n\n')
        else:
            print("\nSe jugó ", end='')
            pprint_accion(a,'\n\n')

        j = -j
    return juego.ganancia(s), s

def menu():
    jugs = []
    for j in [1, -1]:
        print(f"Selección del jugador {"negro (j1)" if j == 1 else "blanco (j2)"}:")
        sel = 0
        print("   1. Jugador manual")
        print("   2. Jugador negamax limitado en profundidad")
        print("   3. Jugador negamax limitado en tiempo\n")

        sel = ""
        while not match("[1-3]\\Z", sel):
            sel = input("Introduce opcion: ")

        sel = int(sel)
        if sel == 1:
            jugs.append(jugador_manual)

        elif sel == 2:
            d = ""
            while not match("[0-9]+\\Z", d) or int(d) < 1:
                d = input("Profundidad: ")
            jugs.append(jugador_artificial(False, int(d)))

        else:
            t = ""
            while not match("[0-9]+\\Z", t) or int(t) < 1:
                t = input("Tiempo: ")
            jugs.append(jugador_artificial(True, int(t)))
        
        print('')
    return jugs

if __name__ == '__main__':
    j1, j2 = menu()
    ganancia, estado_final = simulacion_otello(j1, j2)
    pprint_estado(estado_final)
    print('\nGanaron las piezas ' + ('negras' if ganancia == 1 else 'blancas'))