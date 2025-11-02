import re
from typing import List, Dict, Union, Tuple

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

#funcion para validar el placement

def expandir_fila(fila: str) -> List[str]:
    resultado = []
    for caracter in fila:
        if caracter.isdigit():
            resultado.extend('.' * int(caracter))
        else:
            resultado.append(caracter)
    return resultado

def validar_fen_placement(placement: str) -> Dict:
    respuesta = {
        "valid": True,
        "board": [],
        "errors": [],
        "rows": []
    }

    # Validar número de filas
    filas = placement.split('/')
    if len(filas) != 8:
        respuesta["valid"] = False
        respuesta["errors"].append(f"Se esperaban 8 filas, hay {len(filas)}.")
        return respuesta

    # Validar cada fila
    board_temp = []
    for i, fila in enumerate(filas, 1):
        num_fila = 9 - i  # Para mensajes de error (8 -> 1)
        row_data = {"rank": fila, "sum": 0, "ok": False}

        # Validar caracteres permitidos
        if not REGEX_RANK.match(fila):
            invalid_chars = set(fila) - set("PNBRQKpnbrqk12345678")
            if invalid_chars:
                respuesta["valid"] = False
                respuesta["errors"].append(f"Fila {num_fila} contiene símbolo inválido '{next(iter(invalid_chars))}'.")
                row_data["sum"] = None
                respuesta["rows"].append(row_data)
                return respuesta

        # Calcular suma de casillas
        suma = 0
        for c in fila:
            if c.isdigit():
                suma += int(c)
            else:
                suma += 1

        row_data["sum"] = suma

        if suma != 8:
            respuesta["valid"] = False
            respuesta["errors"].append(f"Fila {num_fila} suma {suma} casillas, debe ser 8.")
            row_data["ok"] = False
            respuesta["rows"].append(row_data)
            return respuesta

        row_data["ok"] = True
        respuesta["rows"].append(row_data)

        # Expandir fila para el tablero
        board_temp.append(expandir_fila(fila))

    if respuesta["valid"]:
        respuesta["board"] = board_temp

    return respuesta
