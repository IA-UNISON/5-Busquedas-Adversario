import juegos_simplificado as js
import minimax

# =========================================================
# JUEGO
# =========================================================

class UltimateTTT(js.JuegoZT2):

    def inicializa(self):
        return (tuple([0]*81), None)

    def jugadas_legales(self, estado, j):
        tablero, activo = estado

        #  MODO LIBRE (pero filtrando tableros terminados)
        if activo is None:
            jugadas = []

            for t in range(9):
                inicio = t * 9
                sub = tablero[inicio:inicio+9]

                if self.tablero_terminado(sub):
                    continue

                for i in range(9):
                    if sub[i] == 0:
                        jugadas.append(inicio + i)

            return jugadas

        #  NORMAL
        inicio = activo * 9
        sub = tablero[inicio:inicio+9]

        #  Si ese subtablero ya terminó → modo libre
        if self.tablero_terminado(sub):
            return self.jugadas_legales((tablero, None), j)

        return [inicio + i for i in range(9) if sub[i] == 0]

    def sucesor(self, estado, a, j):
        tablero, activo = estado
        tablero = list(tablero)

        tablero[a] = j

        siguiente = a % 9
        sub = tablero[siguiente*9:(siguiente+1)*9]

        if self.tablero_terminado(sub):
            siguiente = None

        return (tuple(tablero), siguiente)

    def tablero_terminado(self, sub):
        return self.gana_sub(sub) != 0 or 0 not in sub

    def gana_sub(self, s):
        if s[0] == s[4] == s[8] != 0:
            return s[0]
        if s[2] == s[4] == s[6] != 0:
            return s[2]
        for i in range(3):
            if s[3*i] == s[3*i+1] == s[3*i+2] != 0:
                return s[3*i]
            if s[i] == s[i+3] == s[i+6] != 0:
                return s[i]
        return 0

    def ganancia(self, estado):
        tablero, _ = estado

        grande = []
        for i in range(9):
            sub = tablero[i*9:(i+1)*9]
            grande.append(self.gana_sub(sub))

        return self.gana_sub(grande)

    def terminal(self, estado):
        tablero, _ = estado
        return self.ganancia(estado) != 0 or 0 not in tablero


# =========================================================
# INTERFAZ
# =========================================================

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

class UltimateInterface(js.JuegoInterface):

    def muestra_estado(self, estado):
        tablero, activo = estado

        console.print(
            f"\n[bold yellow]Tablero activo:[/bold yellow] "
            f"{activo if activo is not None else '[green]LIBRE[/green]'}\n"
        )

        for bf in range(3):

            table = Table(show_header=False, box=box.SQUARE)

            for _ in range(3):
                table.add_column(justify="center")

            for fila in range(3):
                row = []

                for bc in range(3):
                    base = (bf*3 + bc) * 9
                    inicio = base + fila*3

                    sub = []
                    for k in range(3):
                        val = tablero[inicio + k]

                        if val == 1:
                            sub.append("[bold red]X[/bold red]")
                        elif val == -1:
                            sub.append("[bold blue]O[/bold blue]")
                        else:
                            sub.append("[dim].[/dim]")

                    row.append(" ".join(sub))

                table.add_row(*row)

            console.print(table)
            console.print("")

    def muestra_ganador(self, g):
        if g == 1:
            console.print("[bold red] Gana X [/bold red]")
        elif g == -1:
            console.print("[bold blue] Gana O [/bold blue]")
        else:
            console.print("[bold yellow] Empate [/bold yellow]")

    def jugador_humano(self, estado, j):
        jugadas = self.juego.jugadas_legales(estado, j)

        console.print(f"\n[bold]Jugador:[/bold] {'X' if j == 1 else 'O'}")
        console.print(f"[cyan]Jugadas legales:[/cyan] {jugadas}")

        a = None
        while a not in jugadas:
            try:
                a = int(input("Jugada (0-80): "))
            except:
                continue

        return a


# =========================================================
# HEURÍSTICA
# =========================================================

def evalua_ultimate(estado):
    tablero, _ = estado
    score = 0

    def gana_sub(s):
        if s[0] == s[4] == s[8] != 0: return s[0]
        if s[2] == s[4] == s[6] != 0: return s[2]
        for i in range(3):
            if s[3*i] == s[3*i+1] == s[3*i+2] != 0: return s[3*i]
            if s[i] == s[i+3] == s[i+6] != 0: return s[i]
        return 0

    def eval_sub(sub):
        g = gana_sub(sub)
        if g == 1: return 1
        if g == -1: return -1

        puntos = 0

        lineas = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for l in lineas:
            vals = [sub[i] for i in l]

            if vals.count(1) == 2 and vals.count(0) == 1:
                puntos += 0.4

            if vals.count(-1) == 2 and vals.count(0) == 1:
                puntos -= 0.7  # defender MÁS fuerte

        return puntos

    grandes = []

    for i in range(9):
        sub = tablero[i*9:(i+1)*9]
        g = gana_sub(sub)

        if g == 1:
            score += 0.9
        elif g == -1:
            score -= 0.9

        score += eval_sub(sub)
        grandes.append(g)

    #  SUPER IMPORTANTE: tablero grande
    score += eval_sub(grandes) * 4

    return max(min(score, 1), -1)


# =========================================================
# ORDENAMIENTO (mejor poda)
# =========================================================

def ordena_mejor(jugadas, jugador):
    # centro de cada subtablero
    return sorted(jugadas, key=lambda x: abs((x % 9) - 4))


# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",
        "Jugador 2": "Tiempo",
        "tiempo": 6,
        "evalua": evalua_ultimate,
        "ordena": ordena_mejor
    }

    def jugador_cfg(tipo):
        if tipo == "Humano":
            return "Humano"
        elif tipo == "Aleatorio":
            return js.JugadorAleatorio()
        elif tipo == "Tiempo":
            return minimax.JugadorMinimaxIterativo(
                tiempo=cfg["tiempo"],
                ordena=cfg["ordena"],
                evalua=cfg["evalua"]
            )

    interfaz = UltimateInterface(
        UltimateTTT(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    interfaz.juega()