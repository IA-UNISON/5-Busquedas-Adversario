"""
Modulo para las clases básicas para realizar un juego de forma muy simplificada
    
Vamos a usar una orientación funcional en este modulo

"""

from random import shuffle, choice
    
class JuegoZT2: # En primer lugar, este es un molde. Es como un parent del GameMaker 2. Provee la estructura para que otros juegos la sigan y la modifiquen. No la modifiques ni sus funciones.
    """
    Clase abstracta para juegos de suma cero, por turnos, dos jugadores.
    
    Se asumen que los jugadores son 1 y -1
    
    """
    def inicializa(self): # Esto solamente declara la función y argumentos base. No tiene codigo porque se supone que los objetos hijos (ej. el juego del Gato) lo tienen que modificar-
        """
        Inicializa el estado inicial del juego, siempre inicia el jugador 1
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues") # Esta función solamente esta aquí para que el programa te avise que no has implementado una función.
    
    def jugadas_legales(self, s, j): # Está funcion se declara igual que la primera que vimos y esto se hace igual para las demas funciones que siguen del "molde"
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")      
    
    def sucesor(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual,
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    

class JuegoInterface: # Es un molde para la interfaz en donde el usuario va a ver como va el juego. Muestra información sobre el juego.
    """
    Clase abstracta para mostrar el estado del juego, y pedir la jugada al usuario

    """
    def __init__(self, juego, jugador1, jugador2): # Es como un evento create del GameMaker 2. Establece el valor de variables internas del objeto al ser creado
        self.juego = juego  # Guarda una referencia al objeto juego que se esta usand.
        self.jugador = [None, jugador1, jugador2] # Establece los jugadores que van a jugar. Se pone None en [0] para que se puedar referir a los demas jugadores con jugador1 = [1] y jugador2 = [2]
    
    def muestra_estado(self, s): # Molde de función para los hijos, definido de manera similar a las funciones de la clase Juego ZT2
        """
        Muestra el estado del juego
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def muestra_ganador(self, ganancia):
        """
        Muestra el ganador del juego, al finalizar
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def jugador_humano(self, s, j):
        """
        Pide al usuario que ingrese una jugada, y la devuelve
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def pide_jugada(self, jugador, s, j): # Esta función regresa la desición del jugador que toca.
        """
        Pide al jugador escoger la jugada a realizar, entre las acciones posibles

        Regresa la acción escogida por el usuario, por defalt, se asume que el jugador es una interface
        
        """
        if isinstance(self.jugador[j], Jugador):    # Se asegura que el Jugador1 sea un objeto Jugador (osea que sea la IA), si lo es... 
            return self.jugador[j].jugada(self.juego, s, j) # Regresa la decisión de la IA. Es como si aquí se ejecutara un State Machine de un NPC en Game Maker 2 
        else:   # Si no lo es
            return self.jugador_humano(s, j) # El jugador escoge su jugada

    def juega(self, max_pasos=1_000): # Comienza el juego, para cuando se encuentra un estado terminal (como 3 en raya en el caso del gato) y anunica al ganador
        """
        Juega el juego, mostrando el estado del juego, y al finalizar, muestra el ganador
        
        """
        s = self.juego.inicializa() # Se inicia el juego y empieza en un estado inicial
        self.muestra_estado(s) # Se muestra el estado inicial
        j = 1 # Empieza el jugador1 = [1]
        pasos = 0 # Numero de jugadas dadas
        while not self.juego.terminal(s) and pasos < max_pasos: # Mientras no se encuentre un estado terminal o no se exceda el numero de pasos, vamos a seguir jugando (Until were both dead).
            a = self.pide_jugada(self.jugador[j], s, j) # Conseguimos la accion (a) a tomar pidiendole la jugada al guador que toca este paso (el humano [1] o la IA [-1] => [2])
            s = self.juego.sucesor(s, a, j) # Se calcula el estado sucesor del juego para que se vuelva el estado actual.
            self.muestra_estado(s) # Mostramos el estado actual
            j = -j # Cambiamos de jugador
            pasos += 1 # Añadimos un paso a nuestro contador (Another step towards the inevitable).
        self.muestra_ganador(self.juego.ganancia(s)) # Si termino el juego, mostramos el ganador
        

class Jugador: # Esta clase representa a jugador IA
    """
    Clase abstracta para un jugador, que recibe el estado del juego y devuelve la jugada a realizar
    """
    def jugada(self, juego, s, j): # Aquí se pone el algoritmo que utiliza la IA para hacer su decisión
        """
        Devuelve la jugada a realizar por el jugador j en el estado s del juego
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")


class JugadorAleatorio(Jugador): # Este es una clase de un jugador que agarra a lo tonto. Reemplaza la funcion de jugada del clase Jugador
    """
    Jugador que escoge una jugada al azar entre las legales
    """
    def jugada(self, juego, s, j): 
        return choice(list(juego.jugadas_legales(s, j))) # Aquí se regresa una acción aleatoria de la lista de acciones legales que se pueden tomar en un juego (An IQ too low?)


def minimax(juego, s, j): # Describe el algoritmo min max. De aquí para adelante son definciones de algoritmos y clases que reemplazan
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    def max_val(s, j): # Describe el procedimiento que se debe dar en un nodo max

        if juego.terminal(s):
            return j * juego.ganancia(s)
        v = -1e10
        for a in juego.jugadas_legales(s, j):
            v = max( v, min_val( juego.sucesor(s, a, j), -j))
        return v
    
    def min_val(s, j):
        if juego.terminal(s):
            return -j * juego.ganancia(s)
        v = 1e10
        for a in juego.jugadas_legales(s, j):
            v = min( v, max_val(juego.sucesor(s, a, j), -j))   
        return v
    
    return max(
        juego.jugadas_legales(s, j),
        key=lambda a: min_val( juego.sucesor(s, a, j), -j))
    
class JugadorMinimax(Jugador):
    """
    Jugador que escoge la mejor jugada usando minimax
    """
    def jugada(self, juego, s, j):
        return minimax(juego, s, j)


def alpha_beta(juego, s, j, ordena=None):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    if ordena is not None and not callable(ordena):
        raise ValueError("El argumento ordena debe ser una función o None")
    elif ordena is None:
        def _ordena(lista):
            shuffle(lista)
            return lista
        ordena = _ordena

    def max_val(s, j, alfa, beta):
        if juego.terminal(s):
            return j * juego.ganancia(s)
        v = -1e10
        jugadas = ordena(list(juego.jugadas_legales(s, j)))
        for a in jugadas:
            v = max(v, min_val(juego.sucesor(s, a, j), -j, alfa, beta))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return alfa
    
    def min_val(s, j, alfa, beta):
        if juego.terminal(s):
            return -j * juego.ganancia(s)
        v = 1e10
        jugadas = ordena(list(juego.jugadas_legales(s, j)))
        for a in jugadas:
            v = min( v, max_val(juego.sucesor(s, a, j), -j, alfa, beta))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return beta
    
    jugadas = ordena(list(juego.jugadas_legales(s, j)))
    return max(
        jugadas,
        key=lambda a: min_val(juego.sucesor(s, a, j), -j, -1e10, 1e10))

class JugadorAlphaBeta(Jugador):
    """
    Jugador que escoge la mejor jugada usando alpha-beta
    """
    def __init__(self, ordena=None):
        self.ordena = ordena
    
    def jugada(self, juego, s, j):
        return alpha_beta(juego, s, j, self.ordena)