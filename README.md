# Validador de Notación FEN 

Este proyecto implementa un validador y visualizador de notación FEN (Forsyth-Edwards Notation) para ajedrez.

## Lenguaje y Tecnologías 
- Python 3.6+ 
- -IDE PyCharm
- Regex (re) 

## Objetivo del Proyecto 
Este proyecto fue desarrollado como parte de la práctica final de la asignatura de Lenguajes de Programación. El objetivo principal es implementar un analizador sintáctico que valide la notación FEN utilizada en ajedrez, permitiendo:
- Validar la estructura correcta de las cadenas FEN
- Detectar y reportar errores específicos en la notación
- Visualizar el estado del tablero mediante una interfaz gráfica
- Proporcionar retroalimentación clara al usuario sobre errores de sintaxis

## Autores 
- Emmanuel Montoya
- Miguel Angel Alzate

## Funcionalidades 

- Validación completa de cadenas FEN según la gramática estándar
- Visualización del tablero usando caracteres Unicode
- Interfaz gráfica simple para validación y visualización
- Mensajes de error específicos para facilitar la corrección



## Ejemplos 

### FEN Válida 
```
2r3k1/p3bqp1/Q2p3p/3Pp3/P3N3/8/5PPP/5RK1 b - - 1 27
```

### FEN Inválida (con error en el placement) 
```
2r3k1/p3bqp1/Q2p3p/3Pp3/P3C3/8/5PPP/5RK1 b - - 1 27
```
el error esta en que 'C' no es un caracter valido para la cadena FEN de este progama


## Lista de FEN de prueba

```
8/8/8/8/8/8/8/8 w - e3 0 1

5rr/8/8/8/8/8/8/8 w - - 0 1

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

r3k2r/8/8/8/8/8/8/R3K2R w Kq - 0 10

8/8/8/8/8/8/8 w - - 0 1

2r3k1/p3bqp1/Q2p3p/3Pp3/P3C3/8/5PPP/5RK1 b - - 1 27

2r3k1/p3bqp1/Q2p3p/3Pp3/P3N3/8/5PPP/5RK1 b - - 1 27

3k4/8/8/8/8/8/8/4K3 b - - 7 42

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkk - 0 1

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1

```
