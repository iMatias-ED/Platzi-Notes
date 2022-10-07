## Tipos de errores

### Cuando Python si nos avisa

- Syntax Error: 
    Un error al escribir una palabra clave. En estos casos Python **ni siquiera ejecuta el programa**.
- Exceptions: 
    Estas si suceden **durante la ejecucion del programa**

*Palabra clave: elevar* 
Cuando una excepcion ocurre, lo hace dentro de un lugar en especifico, por ejemplo una funcion.

Si el error en esa funcion no fue capturado, lo que hace Python es *elevar* esa excepcion a una funcion superior esperando que esta la maneje.

Si el error no es manejado en ningun lugar, la ejecucion del programa se corta y Python nos arroja un *Traceback*

### Como leer un Traceback

Lo correcto es leer desde el final hacia el principio

## Manejo de Excepciones

- **TRY**: En el try se coloca código que esperamos que pueda lanzar algún error.
- **EXCEPT**: En el except se maneja el error, es decir, si ocurre un error dentro del bloque de código del try, se deja de ejecutar el código del try y se ejecuta lo que se haya definido en el Except.
- **ELSE**: El else se ejecuta sólo si no hubo ninguna excepción lanzada desde el try
- **FINALLY**: Se ejecuta SIEMPRE, haya sido lanzada la excepción o no haya sido lanzada.

### Como imprimir un error

```Python
    def function():
        try:
            # Code...
        except Exception as error:
            print( 'Imprime la descripcion del error', error )
```

### Raise *(significa elevar)*

Esta instrucción nos permite generar errores, es decir crear nuestros propios errores cuando detectemos que nuestro programa no actúa como debería con cierto tipo de datos
Su sintaxis es: `raise <NombreError>("<descripcion del error>")`

## Assert Statements \<afirmaciones\>

Afirmo que esta condicion es verdadera, si no, imprime este mensaje de error

- Notacion
```Python
    assert condicion, mensaje de error
```

- Ejemplo
```Python
    assert len(text) > 0, "El texto ingresado esta vacio"
```

## Archivos en Python

`with open(<ruta>, <modo_apertura>) as <nombre>`

*Palabra clave **with***: En python es lo que se denomina un manejador contextual.
Esta palabra clave controla el flujo de nuestro archivo, haciendo que, si el programa se detiene de forma inesperada, el archivo no se dañe.

*Bonus **|***: este operador suma diccionarios de la misma manera que `+` suma listas.
*Useful **enumerate***

- r -> Solo lectura
- r+ -> Lectura y escritura
- w -> Solo escritura. Sobre escribe el archivo si existe. Crea el archivo si no existe
- w+ -> Escritura y lectura. Sobre escribe el archivo si existe. Crea el archivo si no existe
- a -> Añadido (agregar contenido). Crea el archivo si éste no existe
- a+ -> Añadido (agregar contenido) y lectura. Crea el archivo si éste no existe.