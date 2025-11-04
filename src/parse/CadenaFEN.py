import re
from typing import List, Dict

# expresion regular simplificada solo para validar piezas y números
PATRON_FILA = re.compile(r'^(?:[PNBRQKpnbrqk]|[1-8])+$')

def expandir_fila(fila: str) -> List[str]:
    """cnvierte numeros en puntos para espacios vacíos"""
    lista_expandida = []
    for letra in fila:
        if letra.isdigit():
            lista_expandida.extend(['.'] * int(letra))
        else:
            lista_expandida.append(letra)
    return lista_expandida

#validador FEN para imprimir la cadena
def parse_fen(cadena_fen: str) -> Dict:

    resultado = {
        "valid": False,
        "board": [],
        "errors": [],
        "meta": {"castling": "-", "halfmove": "0", "fullmove": "1"}
    }

    # separa la cadena FEN en sus componentes
    partes = cadena_fen.strip().split()
    if len(partes) != 6:
        resultado["errors"].append(f"Se esperaban 6 campos, hay {len(partes)}.")
        return resultado

    # validar el tablero (primera parte del FEN)
    filas = partes[0].split('/')
    if len(filas) != 8:
        resultado["errors"].append(f"Se esperaban 8 filas, hay {len(filas)}.")
        return resultado

    # revisar cada fila
    tablero = []
    for i, fila in enumerate(filas):
        # validar caracteres
        if not PATRON_FILA.match(fila):
            resultado["errors"].append(f"Fila {8-i} contiene símbolos inválidos.")
            return resultado

        # validar que la fila sume 8 casillas
        suma = sum(int(c) if c.isdigit() else 1 for c in fila)
        if suma != 8:
            resultado["errors"].append(f"Fila {8-i} debe tener 8 casillas.")
            return resultado

        tablero.append(expandir_fila(fila))


    resultado["valid"] = True
    resultado["board"] = tablero

    # guardar info
    resultado["meta"].update({
        "castling": partes[2],  # no se valida solo se muestra
        "halfmove": partes[4],  # no se valida solo se muestra
        "fullmove": partes[5]   # no se valida solo se muestra
    })

    return resultado
