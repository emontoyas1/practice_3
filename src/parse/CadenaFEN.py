import re
from typing import List, Dict, Union, Tuple

# esto es para validar el fen
PATRON_FILA = re.compile(r'^(?:[PNBRQKpnbrqk]|[1-8])+$')  # para revisar las piezas y numeros
PATRON_LADO = re.compile(r'^[wb]$')  # w es blanco y b es negro
PATRON_ENROQUE = re.compile(r'^-$|^[KQkq]{1,4}$')  # para ver si puede enrocar
PATRON_ALPASO = re.compile(r'^-$|^[a-h][36]$')  # para el movimiento al paso
PATRON_MEDIO = re.compile(r'^\d+$')  # para los medio movimientos
PATRON_COMPLETO = re.compile(r'^[1-9]\d*$')  # para los movimientos completos


def validar_fila_fen(fila: str) -> bool:
    """
    esto checa que la fila este bien
    """
    if not isinstance(fila, str) or not PATRON_FILA.match(fila):
        return False

    total_casillas = 0
    for letra in fila:
        if letra.isdigit():
            numero = int(letra)
            if numero < 1 or numero > 8:  # los numeros tienen que ser del 1 al 8
                return False
            total_casillas += numero
        else:
            total_casillas += 1

        if total_casillas > 8:
            return False

    return total_casillas == 8


def expandir_fila(fila: str) -> List[str]:
    """
    convierte los numeros en puntos
    """
    lista_expandida = []
    for letra in fila:
        if letra.isdigit():
            lista_expandida.extend(['.'] * int(letra))
        else:
            lista_expandida.append(letra)
    return lista_expandida


def validar_fen_placement(posicion: str) -> Dict:
    """
    revisa que el tablero este bien puesto
    """
    respuesta = {
        "valid": True,
        "board": [],
        "errors": [],
        "rows": []
    }

    # ver si hay 8 filas
    filas = posicion.split('/')
    if len(filas) != 8:
        respuesta["valid"] = False
        respuesta["errors"].append(f"Se esperaban 8 filas, hay {len(filas)}.")
        return respuesta

    # revisar cada fila
    tablero_temporal = []
    for i, fila in enumerate(filas):
        num_fila = 8 - i  # para los errores
        datos_fila = {"rank": fila, "sum": 0, "ok": False}

        # ver que solo tenga letras buenas
        if not PATRON_FILA.match(fila):
            letras_malas = [c for c in fila if c not in "PNBRQKpnbrqk12345678"]
            if letras_malas:
                respuesta["valid"] = False
                respuesta["errors"].append(f"Fila {num_fila} contiene simbolo invalido '{letras_malas[0]}'.")
                datos_fila["sum"] = None
                respuesta["rows"].append(datos_fila)
                return respuesta

        # sumar las casillas
        suma = sum(int(c) if c.isdigit() else 1 for c in fila)
        datos_fila["sum"] = suma

        if suma != 8:
            respuesta["valid"] = False
            respuesta["errors"].append(f"Fila {num_fila} suma {suma} casillas, debe ser 8.")
            datos_fila["ok"] = False
            respuesta["rows"].append(datos_fila)
            return respuesta

        datos_fila["ok"] = True
        respuesta["rows"].append(datos_fila)

        # poner los puntos en vez de numeros
        tablero_temporal.append(expandir_fila(fila))

    if respuesta["valid"]:
        respuesta["board"] = tablero_temporal

    return respuesta



def parse_fen(cadena_fen: str) -> Dict:
    """
    revisa toda la cadena fen
    """
    resultado = {
        "valid": False,
        "board": [],
        "errors": [],
        "meta": {}
    }

    # ver si tiene 6 partes
    partes = cadena_fen.strip().split()
    if len(partes) != 6:
        resultado["errors"].append(f"Se esperaban 6 campos, hay {len(partes)}.")
        return resultado

    # revisar el tablero
    revision_tablero = validar_fen_placement(partes[0])
    if not revision_tablero["valid"]:
        resultado["errors"].extend(revision_tablero["errors"])
        return resultado

    resultado["board"] = revision_tablero["board"]

    # ver quien juega
    if not PATRON_LADO.match(partes[1]):
        resultado["errors"].append("Side invalido: use 'w' o 'b'.")
        return resultado

    # ver si puede enrocar
    if not PATRON_ENROQUE.match(partes[2]):
        resultado["errors"].append("Enroque invalido: use '-' o combinacion de KQkq (sin repetidos).")
        return resultado
    if partes[2] != '-' and len(set(partes[2])) != len(partes[2]):
        resultado["errors"].append("Enroque invalido: use '-' o combinacion de KQkq (sin repetidos).")
        return resultado

    # ver el movimiento al paso
    if not PATRON_ALPASO.match(partes[3]):
        resultado["errors"].append("En-passant invalido: use '-' o a-h con fila 3/6 (ej. e3, c6).")
        return resultado

    # ver movimientos medios
    if not PATRON_MEDIO.match(partes[4]):
        resultado["errors"].append("Halfmove clock invalido: entero ≥ 0.")
        return resultado
    movimientos_medios = int(partes[4])
    if movimientos_medios < 0:
        resultado["errors"].append("Halfmove clock invalido: entero ≥ 0.")
        return resultado

    # ver movimientos completos
    if not PATRON_COMPLETO.match(partes[5]):
        resultado["errors"].append("Fullmove number invalido: entero ≥ 1.")
        return resultado
    movimientos_completos = int(partes[5])
    if movimientos_completos < 1:
        resultado["errors"].append("Fullmove number invalido: entero ≥ 1.")
        return resultado

    # si llega aca todo esta bien
    resultado["valid"] = True
    resultado["meta"] = {
        "side": partes[1],
        "castling": partes[2],
        "en_passant": partes[3],
        "halfmove": movimientos_medios,
        "fullmove": movimientos_completos
    }

    return resultado