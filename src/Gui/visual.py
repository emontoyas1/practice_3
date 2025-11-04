import tkinter as tk
from tkinter import messagebox
from src.parse.CadenaFEN import parse_fen

# aqui ponemos como se ven las piezas
PIEZAS_UNICODE = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    '.': ''
}

class InterfazAjedrez:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Validador FEN")

        # marco principal para todo
        marco_principal = tk.Frame(ventana, padx=10, pady=10)
        marco_principal.pack(expand=True, fill='both')

        # donde se escribe el fen
        marco_entrada = tk.Frame(marco_principal)
        marco_entrada.pack(fill='x', pady=(0, 10))

        tk.Label(marco_entrada, text="FEN:").pack(side='left')
        self.entrada_fen = tk.Entry(marco_entrada, width=50)
        self.entrada_fen.pack(side='left', padx=5, fill='x', expand=True)

        # boton para validar
        tk.Button(marco_entrada, text="Validar y pintar", command=self.validar_y_pintar).pack(side='left', padx=5)

        # Marco para información del juego
        marco_info = tk.Frame(marco_principal)
        marco_info.pack(fill='x', pady=(0, 10))

        # Labels para mostrar información
        self.enroque_label = tk.Label(marco_info, text="Enroque: —")
        self.enroque_label.pack(side='left', padx=5)

        self.media_jugada_label = tk.Label(marco_info, text="Media jugada: —")
        self.media_jugada_label.pack(side='left', padx=5)

        self.jugada_completa_label = tk.Label(marco_info, text="Jugada completa: —")
        self.jugada_completa_label.pack(side='left', padx=5)

        # donde se dibuja el tablero
        self.lienzo = tk.Canvas(marco_principal, width=400, height=400)
        self.lienzo.pack()

        # hacer el tablero vacio
        self.dibujar_tablero_vacio()

        # ejemplo de fen para que el usuario vea
        fen_ejemplo = "2r3k1/p3bqp1/Q2p3p/3Pp3/P3N3/8/5PPP/5RK1 b - - 1 27"
        self.entrada_fen.insert(0, fen_ejemplo)

    def dibujar_tablero_vacio(self):
        """
        dibuja el tablero con cuadros blancos y grises
        """
        self.lienzo.delete('all')
        tamano_casilla = min(self.lienzo.winfo_width(), self.lienzo.winfo_height()) // 8

        for fila in range(8):
            for columna in range(8):
                x1 = columna * tamano_casilla
                y1 = fila * tamano_casilla
                x2 = x1 + tamano_casilla
                y2 = y1 + tamano_casilla

                # poner color a los cuadros
                color = '#FFFFFF' if (fila + columna) % 2 == 0 else '#808080'
                self.lienzo.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

    def dibujar_piezas(self, tablero):
        """
        pone las piezas en el tablero usando los dibujitos
        """
        tamano_casilla = min(self.lienzo.winfo_width(), self.lienzo.winfo_height()) // 8

        for fila in range(8):
            for columna in range(8):
                pieza = tablero[fila][columna]
                if pieza in PIEZAS_UNICODE and PIEZAS_UNICODE[pieza]:
                    x = columna * tamano_casilla + tamano_casilla//2
                    y = fila * tamano_casilla + tamano_casilla//2
                    self.lienzo.create_text(
                        x, y,
                        text=PIEZAS_UNICODE[pieza],
                        font=('Arial', tamano_casilla//2),
                        fill='black' if pieza.isupper() else '#303030'
                    )

    def validar_y_pintar(self):
        """
        revisa si el fen esta bien y dibuja el tablero
        """
        fen = self.entrada_fen.get().strip()
        resultado = parse_fen(fen)

        if resultado["valid"]:
            self.dibujar_tablero_vacio()
            self.dibujar_piezas(resultado["board"])

            # Actualizar la información del juego
            meta = resultado["meta"]
            self.enroque_label.config(text=f"Enroque: {meta['castling']}")
            self.media_jugada_label.config(text=f"Media jugada: {meta['halfmove']}")
            self.jugada_completa_label.config(text=f"Jugada completa: {meta['fullmove']}")
        else:
            messagebox.showerror("Cadena FEN invalida", "\n".join(resultado["errors"]))


def main():
    ventana_principal = tk.Tk()
    app = InterfazAjedrez(ventana_principal)
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()
