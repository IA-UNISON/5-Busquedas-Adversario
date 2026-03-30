"""
El juego del gato para ilustrar los modelos de juegos


"""


import juegos_simplificado as js

class Gato(js.JuegoZT2):
    """

    """
    def inicializa(self):
        """
        Inicializa el juego del gato

        """
        return tuple(9 * [0])
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s

        """
        return [posicion for posicion in range(9) if s[posicion] == 0]
    
    def sucesor(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j

        """
        s = list(s[:])
        s[a] = j
        return tuple(s)
    
    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual,

        """
        if 0 not in s or self.ganancia(s) != 0:
            return True
        return False

    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s

        """
        if s[0] == s[4] == s[8] != 0:
            return s[0]
        if s[2] == s[4] == s[6] != 0:
            return s[2]
        for i in range(3):
            if s[3 * i] == s[3 * i + 1] == s[3 * i + 2] != 0:
                return s[3 * i]
            if s[i] == s[i + 3] == s[i + 6] != 0:
                return s[i]
        return 0   

class GatoInterface(js.JuegoInterface):
    """
    Clase para mostrar el estado del juego del gato, y pedir la jugada al usuario

    """
    def muestra_estado(self, s):
        """
        Muestra el estado del juego del gato

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else str(i).center(3) 
             for (i, x) in enumerate(s)]
        print('\n' + a[0] + '|' + a[1] + '|' + a[2])
        print('---+---+---')
        print(a[3] + '|' + a[4] + '|' + a[5])
        print('---+---+---')
        print(a[6] + '|' + a[7] + '|' + a[8] + '\n')
    
    def muestra_ganador(self, ganancia):
        """
        Muestra el ganador del juego del gato, al finalizar

        """
        if ganancia == 0:
            print("\nY termina con un asqueroso empate")
        elif ganancia == 1:
            print("Ganó el jugador de las X\n")
        else:
            print("Ganó el jugador de las O\n") 

    def jugador_humano(self, s, j):        
        """
        Pide la jugada al usuario para el juego del gato

        """
        jugada = None
        print("Jugador:", 'X' if j == 1 else 'O')
        jugadas = self.juego.jugadas_legales(s, j)
        print("Jugadas legales:", jugadas)
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada
    
        
if __name__ == '__main__':

    juego = Gato()
    interfaz = GatoInterface(
        juego, 
        jugador1=js.JugadorAleatorio(), 
        jugador2='Humano')
    interfaz.juega(10)