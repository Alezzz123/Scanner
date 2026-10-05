from dataclasses import dataclass

@dataclass
class Token:
    codigo: int
    lexema: str
    linea: int
    columna: int

RESERVADAS = {
    "var": 120,
    "num": 121,
    "dec": 122,
    "if": 123,
    "otherwise": 124,
    "loop": 125,
    "do": 126,
    "end": 127,
    "ask": 128,
    "show": 129
}
NOMBRES = {
    100: "IDENTIFICADOR",
    101: "ENTERO",
    102: "REAL",
    103: "CADENA",
    104: "SALTO",
    105: "COMENTARIO",
    106: "ASIGNACION",
    107: "IGUAL A",
    108: "DIFERENTE A",
    109: "MENOR QUE",
    110: "MENOR IGUAL QUE",
    111: "MAYOR QUE",
    112: "MAYOR IGUAL QUE",
    113: "ADICION",
    114: "SUSTRACCION",
    115: "MULTIPLICACION",
    116: "DIVISION",
    117: "APERTURA",
    118: "CIERRE",
    119: "EOF",
    130: "COMA",
    131: "DOS PUNTOS"
}

ERRORES = {
    500: "carácter no válido",
    501: "! sin = despues",
    502: "= sin = despues (la asignacion es con <-)",
    503: "cadena sin cerrar",
    504: "real mal formado"
}
SIMBOLOS = {'.': 2, '#': 3, '"': 4, '<': 5, '>': 6, '=': 7, '!': 8,
            '-': 9, '+': 10, '*': 11, '/': 12, '(': 13, ')': 14,
            ',': 15, ':': 16, '\n': 17}
def columna(c):
    if c is None:
        return 19                        # EOF
    if c.isascii() and c.isalpha():
        return 0                         # letra
    if c.isascii() and c.isdigit():
        return 1                         # dígito
    if c in ' \t\r':
        return 18                        # blanco
    return SIMBOLOS.get(c, 20)           # símbolo conocido u "otro"

TABLA_TEXTO = [
    "1 2 500 5 6 7 8 9 10 114 113 115 116 117 118 130 131 104 0 119 500",  # q0
    "1 1 " + "100* " * 19,                                                  # q1
    "101* 2 3 " + "101* " * 18,                                             # q2
    "504* 4 " + "504* " * 19,                                               # q3
    "102* 4 " + "102* " * 19,                                               # q4
    "5 " * 17 + "105* 5 105* 5",                                            # q5
    "6 6 6 6 103 " + "6 " * 12 + "503* 6 503* 6",                           # q6
    "109* " * 7 + "110 109* 106 " + "109* " * 11,                           # q7
    "111* " * 7 + "112 " + "111* " * 13,                                    # q8
    "502* " * 7 + "107 " + "502* " * 13,                                    # q9
    "501* " * 7 + "108 " + "501* " * 13,                                    # q10
]
TABLA = [fila.split() for fila in TABLA_TEXTO]
assert all(len(fila) == 21 for fila in TABLA), "Una fila no tiene 21 columnas"

def decodificar(celda):
    return int(celda.rstrip('*')), celda.endswith('*')


if __name__ == "__main__":
    print(decodificar(TABLA[0][16]))   # q0 con ':'   → (131, False)
    print(decodificar(TABLA[7][9]))    # q7 con '-'   → (106, False)
    print(decodificar(TABLA[1][17]))   # q1 con '\n'  → (100, True)
    print(decodificar(TABLA[6][17]))   # q6 con '\n'  → (503, True)