"""
Modulo con el minimax con algunos poderes

    1- Poda alfa-beta
    2- Ordenamiento de jugadas
    3- Evaluacion de estados
    4- Busqueda iterativa
    5- Tablas de transposicion
    6- Trazabilidad
"""
import juegos_simplificado as js
from random import shuffle
from time import time

def negamax( juego, s, j, alpha=-1e10, beta=1e10, ordena=None, d=None, evalua=None, transp={}, traza=[]):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    Parametros
    ----------
    juego:             juego que hereda de la clase js.JuegoZT2
    s (tuple):         estado del juego
    j (-1, 1):         jugador que realiza la jugada
    alpha (float):     limite inferior
    beta (float):      limite superior
    ordena (fun):      funcion de ordenamiento, si None, ordena aleatoriamente
    d (int):           profundidad, si None, busca hasta el final
    evalua (fun):      function de evaluación, siempre evalua para el jugador 1
    transp (dict):     tabla de transposición
    traza (list):      trazabilidad
    
    Regresa
    -------
    tuple: (lista mejores jugadas, valor)
    
    """

    # Validaciones
    if d != None and evalua == None:
        raise ValueError("Se necesita la función evalua")
    if type(ordena) != type(None) and type(ordena) != type(lambda x: x):
        raise ValueError("ordena debe ser una función o None")
    if type(evalua) != type(None) and type(evalua) != type(lambda x: x):
        raise ValueError("evalua debe ser una función")
    if type(transp) != dict:
        raise ValueError("transp debe ser un diccionario")
    if type(traza) != list: 
        raise ValueError("traza debe ser una lista")

    if juego.terminal(s):
        return [], j * juego.ganancia(s)
    if d == 0:
        return [], j * evalua(s)
    if d != None and s in transp and transp[s][1] >= d:
        return [], transp[s][0]
    
    v = -1e10
    jugadas = list(juego.jugadas_legales(s, j))
    # if ordena != None:
    #     jugadas = ordena(jugadas, j)
    if ordena != None:
        jugadas = ordena(s, jugadas, j)
    else:
        shuffle(jugadas)
    if traza:
        a_pref = traza.pop(0)
        if a_pref in jugadas:
            jugadas = [a_pref] + [a for a in jugadas if a != a_pref]
    for a in jugadas:
        traza_actual, v2 = negamax(
            juego, juego.sucesor(s, a, j), -j, -beta, -alpha, 
            ordena, d if d == None else d - 1, evalua, transp, traza
        )
        v2 = -v2
        if v2 > v:
            v = v2
            mejor = a
            mejores = traza_actual[:]
        if v >= beta:
            break
        if v > alpha:
            alpha = v
    transp[s] = (v, d)
    return [mejor] + mejores, v 

class JugadorNegamax(js.Jugador):
    """
    Jugador que escoge la mejor jugada usando negamax
    """
    def __init__(self, ordena=None, d=None, evalua=None):
        self.ordena = ordena
        self.d = d
        self.evalua = evalua
    
    def jugada(self, juego, s, j):
        return negamax(
            juego, s, j, ordena=self.ordena, d=self.d, evalua=self.evalua, transp={}
        )[0][0]


def minimax_iterativo( juego, s, j, tiempo=10, ordena=None, evalua=None):  
    """
    Devuelve la mejor jugada para el jugador en el estado
    acotando a un periodo de tiempo
    
    """
    t0 = time()
    d, traza = 2, []
    while time() - t0 < tiempo/2:
        traza, _ = negamax(
            juego, s, j, -1e10, 1e10, ordena=ordena, d=d, 
            evalua=evalua, transp={}, traza=traza
        )
        d += 1
    return traza[0]

class JugadorMinimaxIterativo(js.Jugador):
    """
    Jugador que escoge la mejor jugada usando minimax iterativo
    """
    def __init__(self, tiempo = 10, ordena=None, evalua=None):
        self.tiempo = tiempo
        self.ordena = ordena
        self.evalua = evalua
    
    def jugada(self, juego, s, j):
        return minimax_iterativo(juego, s, j, tiempo=self.tiempo, ordena=self.ordena, evalua=self.evalua)
