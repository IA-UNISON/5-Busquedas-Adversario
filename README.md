
# Búsquedas con Adversarios (Minimax + α-β)
Autor: ROSARIO RODOLFO LUNA ORTIZ
## Descripción

Este proyecto implementa algoritmos de búsqueda con adversarios utilizando Minimax con poda α-β, aplicados a juegos de tablero.

Se realizaron dos desarrollos principales:

* Mejora del juego Conecta 4
* Implementación completa del juego Ultimate Tic Tac Toe con inteligencia artificial

## Objetivos cumplidos

* Implementación de Minimax con poda α-β
* Uso de heurísticas avanzadas de evaluación
* Uso de ordenamiento de jugadas para optimización
* Desarrollo de un juego completo con IA capaz de competir contra un humano

---

## Parte 1: Mejora de Conecta 4

### 3.1 Mejora en ordenamiento de jugadas

Se implementó una estrategia que prioriza jugadas cercanas al centro del tablero, lo cual mejora la eficiencia de la poda α-β al explorar primero los movimientos más prometedores.

### 3.2 Mejora en función de evaluación

Se reemplazó la evaluación básica por una heurística más avanzada basada en:

* Evaluación de ventanas de 4 posiciones
* Detección de:

  * 4 en línea (victoria)
  * 3 en línea con espacio libre
  * 2 en línea
* Penalización fuerte de amenazas del oponente
* Control del centro del tablero

Resultado:

Una evaluación más precisa que permite búsquedas más profundas y decisiones más inteligentes.

---

## Parte 2: Ultimate Tic Tac Toe

### Características implementadas

* Representación del tablero como tupla de 81 posiciones
* Control de subtablero activo
* Regla de juego libre cuando el tablero destino está terminado
* Detección de victoria en subtableros y tablero global

### Heurística avanzada

La función de evaluación considera:

* Estado de cada subtablero
* Líneas potenciales (2 en línea, amenazas, etc.)
* Penalización fuerte para defensa
* Peso elevado al tablero global

### Ordenamiento de jugadas

Se priorizan posiciones centrales dentro de cada subtablero, mejorando la poda α-β y reduciendo el tiempo de búsqueda.

---

## Interfaz de usuario

Se implementó una interfaz visual en consola utilizando la librería `rich`.

Permite:

* Visualización clara del tablero
* Uso de colores para distinguir jugadores
* Mejor experiencia de usuario en consola

---
## Requisitos

Instalar la librería necesaria con:

```bash
pip install rich
```

---

## Ejecución

Para ejecutar el juego:

```bash
python ultimate_ttt.py
```

---




![](ia.png)

# Búsquedas con adversarios (minimax)



## Objetivos

1. Reforzar los conocimientos de los métodos de búsquedas por adversarios, en particular el algoritmo Minimax con poda $\alpha$ - $\beta$ en su versión para dos jugadores por turnos.

2. Desarrollar habilidades para establecer heurísticas de ordenamiento de jugadas con el fin de reducir los tiempos de búsqueda.

3. Desarrollar habilidades y conocimientos para establecer medidas de estimación de utilidad, al aprender a generar funciones de características y establecer pesos entre estos. 

4. Desarrollar un juego simple con motor de IA.

Adicionalmente, en los programas se intenta mostrar un estilo de programación más orientado al paradigma funcional.

Si bien se agradece si el juego tiene interfase gráfica, no es necesario y se prioriza el desarrollo de las heurísticas y la programación del juego sobre la GUI.

Es importante resaltar que la UX de una aplicación es fundamental para su éxito, por lo que no debe minimizarse esa parte esencial de todo sistema, pero no es parte de las competencias a desarrollar en el curso de IA.

## Instrucciones

1. En el archivo `juegos_simplificados.py` se ofrecen clases para juego de tablero por turnos. Revisa el código y procura entender a grandes rasgos como funciona. El archivo `gato.py` es un ejemplo de uso sencillo con el juego del gato. Es importante aclarar que este es un ejemplo con fines didácticos y toda posible optimización en tiempo o uso dememoria se evitó siempre que eso implicara obscurecer el proceso de búsqueda con adversarios, por lo que el entorno es bastante ineficiente en estos términos.

2. En el archivo `minimax.py` viene ya el algoritmo de Minimax con algunas de sus adaptaciones básicas a juegos de dos jugadores por turnos. También se propone una adaptación para que juegue limitado en el tiempo y no en la profundidad.

3. En el archivo `conecta4.py` se incluye el juego de conecta 4 (si quieres información de como se juega la puedes consultar [aqui](http://en.wikipedia.org/wiki/Connect_Four)). En el archivo se ofrece el juego programado. Dentro del método hay dos funciones  que impactan mucho en la calidad del juego: `ordena_centro` y `evalua_3con`.  Desarrolla tu propias funciones con el fin de lograr mejores búsquedas a mayor profundidad (20 puntos).

4. Ahora tienes que desarrollar tu propio juego, las heurísticas de ordenamiento y de evaluación, y probarlo. Para esto te propongo dos juegos a escoger:

   - [Ultimate TicTacToe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe)
   - [Otello](https://en.wikipedia.org/wiki/Reversi)
   
   En cualquiera de los dos casos es muy importante desarrollar lo siguiente:

   1. Un juego basado en la clase `JuegoZT2` del módulo `juegos_simplificado.py`.
   2. Al menos una función de ordenamiento
   3. Al menos una función de evaluación
   4. El script necesario para poder jugar el juego (CLI o GUI)
   
Para la evaluación del juego desarrollado, el motor de IA tendrá que ganarme en el juego.


