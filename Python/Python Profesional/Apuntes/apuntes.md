## Funcionamiento Interno de Python

### Python es un lenguaje interpretado
Lo que significa que tu código es transformado por el intérprete (máquina virtual de Python) a bytecode antes de ser ejecutado por un ordenador con x sistema operativo. 
El bytecode es un lenguaje de programación de más bajo nivel.

### Garbage collector
Recuerda que el *garbage collector* toma los objetos y variables que **no están en uso** y los **elimina.**

**Interesante**:
Puedes verificar los objetos recolectados por el garbage collector con el módulo gc:

```Python
#Importa el módulo
import gc

#Retorna el número de objetos colectados y liberados
collected = gc.collect()

#Imprime los objetos en el garbage collector
print("Objetos dentro de Garbage collector: ", collected)
```

### \_\_pycache\_\_

Es el directorio que contiene el bytecode que crea Python para que lo pueda leer la máquina virtual.

## Organización de archivos

Es importante conocer dos conceptos:

- ### Módulos: 
Es cualquier archivo de Python. Generalmente, contiene código que puedes reutilizar.
- ### Paquetes: 
Un paquete es un conjunto de módulos. Siempre posee el archivo `__init__.py`.

**Interesante:** 
`__init__` is pronounced “dunder init”: dunder is short for “double-underscore”.

## ¿Qué son los tipados?

💻 Los tipados es una clasificación de los lenguajes de programación, tenemos cuatro tipos:

- Estático
- Dinámico
- Débil
- Fuerte

El tipado del lenguaje **depende de cómo trata a los tipos de datos.**

### El tipado estático es el que **levanta un error en el tiempo de compilación**, ejemplo en JAVA:

```JAVA
String str = "Hello" // Variable tipo String
str = 5 // ERROR: no se puede convertir un tipo de dato en otro de esta forma.
```

### El tipado dinámico **levantan el error en tiempo de ejecución**, ejemplo en Python:

```Python
str = "Hello" # Variable tipo String
str = 5 # La variable ahora es de tipo Entero, no hay error

## TIPADO FUERTE
x = 1
y = "2"
z = x + y # ERROR: no podemos hacer estas operaciones con tipos de datos distintos entre sí
```
El tipado débil es el que hace un cambio en un tipo de dato para poder operar con el, como lo hace JavaScript y PHP.

🐍 Python es un lenguaje de tipado 👾 Dinámico y 💪 Fuerte.

## Tipado Estático en Python

<https://docs.python.org/3/library/typing.html>

Para hacer que Python sea de tipado estático es necesario agregar algo de sintaxis adicional a lo aprendido, además, esta característica solo se puede aplicar a partir de la versión 3.6.

`<variable> : <tipo_de_dato> = <valor_asignado>`

```Python
a: int = 5
print(a)

b: str = "Hola"
print(b)

c: bool = True
print(c)
```

Del mismo modo se puede usar esta metodología de tipado en Python a funciones adicionando el signo menos a continuación del signo mayor que para determinar el tipo de dato. Ejemplo:

```Python
def suma(a: int, b: int) -> int :
	return a + b

print(suma(1,2))
```

## *Typing*
Existe una librería de fabrica que viene preinstalada con Python que se llama typing, que es de gran utilidad para trabajar con tipado con estructuras de datos entre la versión 3.6 y 3.9, entonces:

```Python
from typing import Dict, List

positives: List [int] = [1,2,3,4,5]

users: Dict [str, int] = {
	"argentina": 1.
	"mexico": 34,
	"colombia": 45,
}

countries: List[Dict[str, str]] = [
	{
		"name" : "Argentina",
		"people" : "45000",
	},
	{
		"name" : "México",
		"people" : "9000000",
	},
	{
		"name" : "Colombia",
		"people" : "99999999999",
	}
]

# Tambien se pueden guardar los tipos de datos para utilizarlos posteriormente
from typing import Tuple, Dict, List

# Se crea el tipo de dato <CoordinatesType>
CoordinatesType = List[Dict[str, Tuple[int, int]]]

coordinates: CoordinatesType = [
	{
		"coord1": (1,2),
		"coord2": (3,5)
	},
	{
		"coord1": (0,1),
		"coord2": (2,5)
	}
]
```

## Modulo mypy

El modulo mypy se complementa con el modulo typing ya que permitirá mostrar los errores de tipado debil en Python.

Para revisar si algún archivo contiene errores de tipado ejecutamos en la línea de comandos lo siguiente: `mypy archivo.py --check-untyped-defs`

*Interesante:* Crear tipos de datos con clases en python `('creacion-tipo-datos-con-clases-python.png')`

*Interesante:* Usar Optional[], de la libreria typing para cuando ocupamos retornar None u otra variable

```Python
def foo() -> Optional[List]:
  if b: return []
  else: None
```

## Conceptos avanzados sobre funciones

## Scopes
El scope es el alcance que tienen las variables. Depende de donde declares o inicialices una variable para saber si tienes acceso. Regla de oro:

Una variable solo esta disponible dentro de la region donde fue creada

- ### Local Scope
Es la región que corresponde el ámbito de una función, donde podremos tener una o mas variables, las variables van a ser accesibles únicamente en esta region y no serán visibles para otras regiones

- ### Global Scope
Al escribir una o mas variables en esta region, estas podrán ser accesibles desde cualquier parte del código.

- Tambien tenemos keywords como `global` y `nonlocal`.
Mas aqui: <https://stackabuse.com/how-to-use-global-and-nonlocal-variables-in-python>

## Closures

Es básicamente cuando una variable de un scope superior es recordada por una función de scope inferior (aunque luego se elimine la de scope superior).

- ### Ejemplo 1

```Python
def main():
	a = 1
	def nested():
		print(a)
	return nested

my_func = main()
my_func()
```

- ### Ejemplo 2

```Python
def main():
	a = 1
	def nested():
		print(a)
	return nested

my_func = main()
my_func()
# 1

# Se elimina la funcion de scope superior
del(main)
my_func()
# 1 -> Sigue funcionando
```

- ### Reglas para encontrar un Closure
  - Debemos tener una nested function
  - La nested function debe referenciar un valor de un scope superior
  - La función que envuelve a la nested function debe retornarla también

## Decoradores 

Un decorador es una función que recibe como parámetro otra función, le añade cosas y retorna una función diferente. Tienen la misma estructura que los Closures pero en vez de variables lo que se envía es una función. Ejemplo:

```Python
def decorador(func):
    def envoltura():
        print("Esto se añade a mi función original.")
        func()
    return envoltura

def saludo():
    print("¡Hola!")

saludo()
# Salida:
# ¡Hola!

saludo = decorador(saludo) # Se guarda la función decorada en la variable saludo
saludo()                   # La función saludo está ahora decorada
# Salida:
# Esto se añade a mi función original.
# ¡Hola!
```

Se puede hacer de manera mas sencilla, con azúcar sintáctica (sugar syntax): Cuando tenemos un código que está embellecido para que nosotros lo veamos de una manera más estática, ayudando a entender de manera mas sencilla el código. De esta manera, tenemos el código anterior:

```Python
def decorador(func):
    def envoltura():
        print("Esto se añade a mi función original.")
        func()
    return envoltura

# De esta manera se decora la función saludo (equivale a saludo = decorador(saludo) de la última línea, quedando ahora en la línea inmediata superior ):
@decorador                
def saludo():
    print("¡Hola!")

saludo() 

```

## Estructuras de datos avanzadas

### Iteradores

Antes de entender qué son los iteradores, primero debemos entender a los iterables.

Son todos aquellos objetos que podemos recorrer en un ciclo. Son aquellas estructuras de datos divisibles en elementos únicos que yo puedo recorrer en un ciclo.

**Pero** en Python las cosas no son así. Los iterables se convierten en iteradores.

```Python 
	# Creando un iterador
	my_list = [1,2,3,4,5]
	my_iter = iter(my_list)

	# Iterando un iterador
	print(next(my_iter))

	# Cuando no quedan datos, la excepción StopIteration es elevada
```
```Python 
	# Creando un iterador
	my_list = [1,2,3,4,5]
	my_iter = iter(my_list)

	# Funcionamiento interno del bucle for
	while True: 
	try:
		element = next(my_iter)
		print(element)
	except StopIteration:
		break
```

*Momento impactante:* El ciclo “for” dentro de Python, no existe. Es un while con StopIteration. 🤯🤯🤯

my_list = [1,2,3,4,5]

#### Como counstruir iteradores

Para ello es necesario utilizar clases y metodos, ademas de conocer el protocolo de los iteradores.
Este protocolo nos dice que, para construir un *iterador* necesitamos una clase que tenga dos metodos importantes: `__iter__` y `__next__`

```Python 
class EvenNumbers:
  """Clase que implementa un iterador de todos los números pares,
  o los números pares hasta un máximo
  """

  #* Constructor de la clase
  def __init__(self, max = None):
    self.max = max


  # Método para tener elementos o atributos que voy a necesitar para que el iterador funcione
  def __iter__(self):
    self.num = 0;
    #* Convertir un iterable en un iterador
    return self

  # Método para tener la función "next" de Python
  def __next__(self):
    if not self.max or self.num <= self.max:
      result = self.num
      self.num += 2
      return result
    else:
      raise StopIteration
```

#### Ventajas de usar iteradores:
- Nos ahorra recursos.
- Ocupan poca memoria.

### Generadores 
Generadores
Sugar syntax de los iteradores. Los generadores son funciones que guardan un estado. Es un iterador escrito de forma más simple.

```Python
	def my_gen():

	"""un ejemplo de generadores"""

	print('Hello world!')
	n = 0
	yield n # es exactamente lo mismo que return pero detiene la función, cuando se vuelva a llamar a la función, seguirá desde donde se quedó

	print('Hello heaven!')
	n = 1
	yield n

	print('Hello hell!')
	n = 2
	yield n


	a = my_gen()
	print(next(a)) # Hello world!
	print(next(a)) # Hello heaven!
	print(next(a)) # Hello hell!
	print(next(a)) StopIteration
```
Ahora veremos un generator expression (es como list comprehension pero mucho mejor, porque podemos manejar mucha cantidad de información sin tener problemas de rendimiento):

```Python
	#Generator expression

	my_list = [0,1,4,7,9,10]

	my_second_list = [x*2 for x in my_list] #List comprehension
	my_second_gen = (x*2 for x in my_list) #Generator expression
```

### Sets

#### Un pequeño resumen:

Los sets son una estructura de datos muy similares a las listas en cuanto a su forma, pero presentan ciertas características particulares:

**Los elementos de los sets son inmutables**
- Cada elemento del set es único, esto es que no se admiten duplicados, aun si durante la definición del set se agregan elementos repetidos python solo guarda un elemento
- los sets guardan los elementos en desorden
- Para declararlos se utilizan los {} parecido a los diccionarios solo que carece de la composición de conjunto {a:b, c:d}

```Python
	# declarar un set vacío
	empty_set = set()

	# set de enteros
	print(my_set)
	my_set = {1, 3, 5}

	# set de diferentes tipos de datos
	my_set = {1.0, "Hi", (1, 4, 7)}
	print(my_set)
```
Los sets no pueden ser leídos como las listas utilizando indices o slices, esto debido a que no tienen un criterio de orden. Sin embargo si podemos agregar o eliminar items de los sets utilizando métodos:

- add(): nos permite agregar elementos al set, si se intenta agregar un elemento existente simplemente python los ignorara
- update(): nos permite agregar múltiples elementos al set
- remove(): permite eliminar un elemento del set, en el caso en que no se encuentre presente dicho elemento, Python elevará un error
- discard(): permite eliminar un elemento del set, en el caso en que no se encuentre presente dicho elemento, Python dejará el set intacto, sin elevar ningún error.
- pop(): permite eliminar un elemento del set, pero lo hará de forma aleatoria.
- clear(): Limpia completamente el set, dejándolo vació.


#### Operaciones con Sets (Unión, Intersección, Diferencia y Diferencia Simétrica)

- Unión: Es el resultado de combinar todos los elementos de los conjuntos. En caso de haber elementos repetidos, estos se eliminan..

```Python
	my_set3 = my_set1 | my_set2;
	# o tambien
	set1.union(set2)
```

- Intersección: Esta operación nos da como resultados los elementos en común de los conjuntos.

```Python
	my_set3 = my_set1 & my_set2
	# O tambien
	set1.intersection(set2)
```

- Diferencia: Tomar dos sets, y de uno quitar todos los elementos que contiene el otro.

```Python
	my_set3 = my_set1 - my_set2
	# O tambien
	set1.difference(set2)
```

- Diferencia Simétrica: Es la operación opuesta a la Intersección, es decir, obtenemos todos los elementos de ambos sets, menos los que se comparten.

```Python
	my_set3 = my_set1 ^ my_set2 
	# O tambien
	set1.symmetric_difference(set2)
```

### Manejo de fechas

```Python
	import datetime

	my_time = datetime.datetime.now() # hora local de mi PC u hora universal
	my_date = datetime.date.today() # fecha actual
	print(f'Year: {my_day.year}')
	print(f'Month: {my_day.month}')
	print(f'Day: {my_day.day}')


	#Tabla de códigos de formato para fechas y horas(los más importantes):

	# Formato	Código
	# Año		%Y
	# Mes		%m
	# Día		%d
	# Hora		%H
	# Minutos	%M
	# Segundos	%S

	from datetime import datetime

	latam = my_datetime.strftime('%d/%m/%Y')
	print(f'Formato LATAM: {latam}')

	usa = my_datetime.strftime('%m/%d/%Y')
	print(f'Formato USA: {usa}')

	random_format = my_datetime.strftime('año %Y mes %m día %d')
	print(f'Formato random: {random_format}')

	formato_utc = datetime.utcnow()
	print(f'Formato UTC: {formato_utc}')
```

#### TimeZone

El módulo que me permite trabajar con zonas horarias es el pytz y lo debemos instalar

```Python 
	from datetime import datetime
	import pytz


	def timezones(clave: str, nombre: str):
		time_zone = pytz.timezone(clave)
		date = datetime.now(time_zone)
		return nombre + ' ' + date.strftime('%d/%m/%Y, %H:%M:%S')


	if __name__ == '__main__':
		print(timezones('America/Bogota', 'Bogotá'))
		print(timezones('America/Mexico_City', 'México'))
		print(timezones('America/Caracas', 'Caracas'))
```
