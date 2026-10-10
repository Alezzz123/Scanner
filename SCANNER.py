from dataclasses import dataclass
#el @dataclass es una herramienta de python que permite crear el objeto, le pasas los atributos y se encarga de crear el constructor, representarlos de manera legible cuando se llamen y permite la comparacion en caso de que tengan atributos de valores distintos
@dataclass
class Token:
    codigo: int
    lexema: str
    linea: int
    columna: int

#Los siguientes son los diccionarios, permiten asignar a cada codigo su categoria o en el caso de las palabras reservadas asignarlas a su codigo 
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
SIMBOLOS = {
    '.': 2,
    '#': 3,
    '"': 4,
    '<': 5,
    '>': 6,
    '=': 7,
    '!': 8,
    '-': 9,
    '+': 10,
    '*': 11,
    '/': 12,
    '(': 13,
    ')': 14,
    ',': 15,
    ':': 16,
    '\n': 17
}

#----------------------------------------CLASIFICADOR----------------------------------------------------
#esta funcion permite a partir del caracter obtener su columna dentro de la matriz de transiciones declarada en la variable TABLA_TEXTO
def columna(c):
    if c is None:
        return 19                        # EOF, se pone al principio porque si avanza a alguna de las otras condiciones siendo None, dara error
    if c.isascii() and c.isalpha():
        return 0                         # letra
    if c.isascii() and c.isdigit():
        return 1                         # dígito
    if c in ' \t\r':
        return 18                        # blanco
    return SIMBOLOS.get(c, 20)           # símbolo conocido u "otro", aqui si no se cumple ninguna de las anteriores entonces se va a la tabla de simbolos y busca el numero del que corresponde a 'c', si no existe, le da 20 que representa cualquiera otro caracter no identificado
#nuestro codigo nesecita conocer la matriz de transiciones, la mejor forma de representar una tabla en python es con una lista de listas como en la siguiente, aunque no son listas, son cadenas, en el siguiente comentario esta la explicacion de como se convierten esas cadenas en listas
TABLA_TEXTO = [
    "1 2 500 5 6 7 8 9 10 114 113 115 116 117 118 130 131 104 0 119 500",   # q0
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
#esta linea que sigue esta diciendo que por cada fila de TABLA_TEXTO es decir por cada cadena que hay, se creara una lista separando entre espacios vacios la cadane, si la cadena tuviera "2 3 4" la lista que crearia seria: ["2","3","4"]
TABLA = [fila.split() for fila in TABLA_TEXTO]
#esto siguiente linea es para evitar errores, es decir, recorre la tabla que anterior mente creamos y se asegura de que no haya ni mas ni menos columnas que las que tiene nuestra tabla, que son 21, si son diferente a 21 se detiene y arroja el aviso
assert all(len(fila) == 21 for fila in TABLA), "Una fila no tiene 21 columnas"

def decodificar(celda):
    return int(celda.rstrip('*')), celda.endswith('*')
#nesecitamos que el scanner recuerde y nada de lo que hicimos anteriormente sirve para eso, son solo datos que nuestro scanner va a usar, pero necesitamos que recuerde donde se quedo, es por eso que una clase es lo que necesitamos
#una clase es un plano, que dice que es lo que debe de llevar el objeto y que es lo que debe saber hacer
class Scanner:
    #el __init__ es el constructor, es como si tuvieras una mochila, el constructor dice "mi mochila va a guardar estas cosas" self.texto guarda el texto que le pasemos, es decir, el que el scanner va a utilziar, suposicion de inicio por default es 0 y ademas crea una lista donde guardara los errores que se presenten
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.errores = []
    #este es la funcion que le permite al scanner leer caracter por caracter, primero toma el texto y la posicion guardada en pos y accede a ese caracter y lo devuelve, si pos es mas grande que la longitud del texto, regresa None, es decir EOF
    def leer(self):
        c = self.texto[self.pos] if self.pos < len(self.texto) else None
        self.pos += 1
        return c
    #en caso de que el scanner requiera retroceder como cuando recibe un "100*" se usa esta funcion
    def retroceder(self):
        self.pos -= 1
    #es lo que permite devolver en donde esta ubicada nuestro scanner
    def posicion(self, indice):
        linea = self.texto.count('\n', 0, indice) + 1 #cuenta cuantos saltos de linea hay desde que empezamos, si hay 0, entonces estas en la linea 1
        inicio_linea = self.texto.rfind('\n', 0, indice) + 1 
        return linea, indice - inicio_linea + 1
    # Es el método que usará el parser: cada llamada lee los caracteres
    # necesarios para formar UN token y lo entrega. La posición queda
    # guardada en self.pos, así que la siguiente llamada continúa donde se quedó.
    def siguiente_token(self):
        # Variables locales (sin self): solo sirven mientras se arma ESTE token
        # y está bien que se pierdan al terminar.
        estado = 0        # todo token empieza en q0
        lexema = ""       # todavía no hemos juntado ningún carácter
        inicio = self.pos # copia del índice donde empieza el token, para calcular su línea y columna

        # Se repite hasta que haya un token que entregar (el return termina el ciclo).
        while True:
            # El corazón del autómata: leer un carácter, clasificarlo en su
            # columna, consultar la celda y separarla en número y retroceso.
            c = self.leer()
            sig, retro = decodificar(TABLA[estado][columna(c)])

            # ---- CASO 1: la celda es un estado (0 a 10): el token no ha terminado ----
            if sig <= 10:
                if sig == 0:
                    # Blanco en q0: no pertenece a ningún token. Se salta y el
                    # inicio se mueve, porque el token empezará después del espacio.
                    inicio = self.pos
                else:
                    # El carácter es parte del token que se está armando.
                    lexema += c
                estado = sig  # cambiamos de fila en la tabla
                continue      # volvemos al inicio del ciclo a leer el siguiente carácter

            # A partir de aquí, sig es un token (1xx) o un error (5xx).

            # ---- ¿El último carácter pertenece al token? ----
            if retro:
                # La celda tenía *: el carácter es del siguiente token.
                # Se regresa para que la próxima lectura lo vuelva a entregar.
                self.retroceder()
            elif c is not None:
                # No tenía *: el carácter sí pertenece (como el = de <=).
                # Se excluye el EOF porque None no se puede agregar a un texto.
                lexema += c

            # Línea y columna donde EMPEZÓ el token; sirve para tokens y errores.
            linea, col = self.posicion(inicio)

            # ---- CASO 2: error (500 o más) ----
            if sig >= 500:
                # Se anota en la lista de errores y se reinicia todo para seguir
                # buscando un token válido. El parser nunca recibe errores.
                self.errores.append(f"Error {sig} en línea {linea}, columna {col}: {ERRORES[sig]} ({lexema!r})")
                estado, lexema, inicio = 0, "", self.pos
                continue

            # ---- CASO 3: token ----
            if sig == 105:
                # Comentario: el parser no lo necesita. Se descarta como un
                # error, pero sin anotarlo, y se sigue buscando.
                estado, lexema, inicio = 0, "", self.pos
                continue

            if sig == 100:
                # Identificador: se revisa la lista de palabras reservadas.
                # Si está, cambia a su código; si no, se queda en 100.
                sig = RESERVADAS.get(lexema, 100)

            if sig == 119:
                # EOF: se regresa el separador para que las siguientes
                # llamadas sigan encontrando el EOF.
                self.retroceder()
                if self.ultimo not in (None, 104, 119):
                    # La última instrucción no tenía SALTO: se entrega uno
                    # implícito (lexema vacío) y el EOF saldrá en la siguiente llamada.
                    sig, lexema = 104, ""

            self.ultimo = sig  # se anota en la mochila qué token salió, para la próxima llamada
            return Token(sig, lexema, linea, col)