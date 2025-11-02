import re
# Backend del parser

# expresion regular para validar caracteres permitidos en una fila FEN
REGEX_RANK = re.compile(r'^[PNBRQKpnbrqk1-8]+$')
##
#funcion que valida
def validar_fila_fen(fila: str) -> bool:
    if not isinstance(fila, str) or not REGEX_RANK.match(fila):
        return False

    total = 0
    for caracter in fila:
        if caracter.isdigit():
            total += int(caracter)
        else:
            total += 1

        if total > 8:
            return False

    return total == 8
