########### Para crear un entorno virtual
# Es buena practica agregar el entorno virtual al .gitignore
'''py -m venv <nombre entorno virtual>'''

# Para guardar los requerimientos de un proyecto puedes hacerlo con
'''pip freeze > requirements.txt'''

example_list = [ 0, 3, 5, 6, 8, 10 ]

########### List comprehensions
l = [ i for i in range(0, 11) ]
print("\n\nLIST COMPREHENSIONS", l) 


########### Dictionary comprehensions
d = { i: i**2 for i in range(0, 11) }
print("\n\nDICTIONARY COMPREHENSIONS", d)


########### Lambda functions
es_par = lambda number: number % 2 == 0;
print( "\n\nLAMBDA FUNCTIONS", es_par(6) )


########### Filter 
'''Recibe como parametro una lambda function y un iterable.
Devuelve un iterador que puedes guardar en otro iterable
'''
print( "\n\nFILTER" )

# Using comprehensions
impares_comprehensions = [ i for i in example_list if i % 2 != 0 ]
print( "Using Comprehensions", impares_comprehensions )

# Using Filter function
impares_filter = list( filter( lambda i: i % 2 != 0, example_list ) )
print( "Using Filter", impares_filter )


########### Map
'''Manipula los datos de una lista'''
print( "\n\nMAP" )

# Using Comprehensions
squares_comprehensions = [ i**2 for i in example_list ]
print( "Using Comprehensions", squares_comprehensions )

# Using Filter function
squares_filter = list( map( lambda i: i**2, example_list ) )
print( "Using Filter", squares_filter )


########### Reduce 
from functools import reduce
'''Se necesita usar el modulo functools (integrado en python) para poderlo usar.
Hace que todos los numeros dentro de una lista hagan las operaciones, indicadas en la funcion, entre si y DEVUELVE 1 SOLO VALOR
'''
print( "\n\nREDUCE" )

suma_reduce = reduce( lambda a, b: a + b, example_list )
print( "suma usando reduce", suma_reduce )

mult_reduce = reduce( lambda a, b: a * b, example_list )
print( "multiplicacion usando reduce", mult_reduce )


########### MANEJO DE ERRORES
print( '\n\nMANEJO DE ERRORES' )

try: 
    if ( 2 > 3 ): raise ValueError("el numero es mayor que 3")
    print(" todo bien xd ")
except:
    print( 'ups, tuvimos un error' )
else:
    print( 'no tuvimos ningun error asi que imprimo esto.' )
finally: 
    print( 'El bloque /try/ ha finalizado' )

# Asserts. Una alternativa a try (tambien se pueden combinar)
print( '\nAsserts' )

assert 3 > 2, "Este error ocurre por que la afirmacion es falsa"
print('El primer assert fue pasado xd')

assert 1 > 2, "Parece que 1 no es mayor que 2"


########### Manejo de archivos
'''Los apuntes se encuentran en anotaciones.md'''
'''La practica se encuentra en el juego del ahorcado'''