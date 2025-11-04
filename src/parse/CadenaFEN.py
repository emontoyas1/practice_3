import re
from typing import List, Dict

# Expresión regular simplificada solo para validar piezas y números
PATRON_FILA = re.compile(r'^(?:[PNBRQKpnbrqk]|[1-8])+$')

def expandir_fila(fila: str) -> List[str]:
    """Convierte números en puntos para espacios vacíos"""
    lista_expandida = []
    for letra in fila:
        if letra.isdigit():
            lista_expandida.extend(['.'] * int(letra))
        else:
            lista_expandida.append(letra)
    return lista_expandida

def parse_fen(cadena_fen: str) -> Dict:
    """
    Validador simplificado de FEN que solo revisa lo básico y retorna la información necesaria
    para la interfaz gráfica
    """
    resultado = {
        "valid": False,
        "board": [],
        "errors": [],
        "meta": {"castling": "-", "halfmove": "0", "fullmove": "1"}
    }

    # Separar la cadena FEN en sus componentes
    partes = cadena_fen.strip().split()
    if len(partes) != 6:
        resultado["errors"].append(f"Se esperaban 6 campos, hay {len(partes)}.")
        return resultado

    # Validar el tablero (primera parte del FEN)
    filas = partes[0].split('/')
    if len(filas) != 8:
        resultado["errors"].append(f"Se esperaban 8 filas, hay {len(filas)}.")
        return resultado

    # Revisar cada fila
    tablero = []
    for i, fila in enumerate(filas):
        # Validar caracteres permitidos
        if not PATRON_FILA.match(fila):
            resultado["errors"].append(f"Fila {8-i} contiene símbolos inválidos.")
            return resultado

        # Validar que la fila sume 8 casillas
        suma = sum(int(c) if c.isdigit() else 1 for c in fila)
        if suma != 8:
            resultado["errors"].append(f"Fila {8-i} debe tener 8 casillas.")
            return resultado

        tablero.append(expandir_fila(fila))

    # Si llegamos aquí, el tablero es válido
    resultado["valid"] = True
    resultado["board"] = tablero

    # Guardar meta información simplificada
    resultado["meta"].update({
        "castling": partes[2],  # No validamos, solo mostramos
        "halfmove": partes[4],  # No validamos, solo mostramos
        "fullmove": partes[5]   # No validamos, solo mostramos
    })

    return resultado
