# Resumen del curso Consumo de APIs REST con Angular

Angular nos provee un modulo especifico para estos casos, el cual es Angular Http.

Este modulo maneja *Observables*

## Utilizar Modulo HTTP

* Para empezar a utilizar peticiones HTTP, debemos de importar el modulo correspondiente en nuestro *app.module.ts*

    `Import { HttpClientModule } from '@angular/common/http';`

    Este debemos agregarlo a la seccion de *imports*

* Como siguiente paso, debemos ir al servicio o componente que realizara la peticion, e importar el **Servicio** HttpClient

    `Import { HttpClient } from '@angular/common/http';`

    Como *HttpClient* es un servicio, debemos declararlo en el *constructor*

    ```TypeScript
        export class ProductService{
            constructor(
                private http: HttpClient;
            ){}
        }
    ```

## Tipos de peticiones

### Get

Las peticiones de tipo *GET* nos permiten obtener informacion

* Para realizar una peticion de tipo GET debemos de utilizar el metodo *get()* del servicio *HttpClient*.

Esto nos devolvera un observable con lo que retorne la API

```TypeScript
        export class ProductService{
            constructor(
                private http: HttpClient;
            ){}
            getAllProducts(){
                return this.http.get<Product[]>('https://young-sands-07814.herokuapp.com/api/products')
            }
        }
```

### POST

Sirve para insertar datos, por ejemplo, crear un producto

`http.post(apiUrl, body)`

* En el *apiUrl*, le pasamos la url de nuestra API
* En el *body*, podemos enviar el objeto que contiene los datos necesarios para poder insertar en el API. Por ejemplo, los datos de nuestro producto

    ```TypeScript
        export class ProductService{
            constructor(
                private http: HttpClient;
            ){}

            create(){
                let product_data = {
                    title: 'new Product',
                    price: 5000
                }

                return this.http.post<Product>(
                    `https://young-sands-07814.herokuapp.com/api/products`,
                    product_data
                )
            }
        }
    ```

### Data Transfer Object

Estos se conocen como objetos que tienen la informacion de transferencia, en este caso, a una API.

Por ejemplo, al insertar un producto, no necesitamos enviar el *id*; pero nuestra interfaz *Product*, requiere el campo *id*. En este caso, la informacion que necesitamos enviar difiere, solo un poco, de nuestra interfaz

Para solucionar esto, creamos una nueva interfaz especifica, que herede la estructura anterior, pero omita los datos que no necesita. Esto lo hacemos con **Omit**

Es buena practica terminar el nombre de la interfaz con *DTO* (Data Transfer Object)

```TypeScript
    export interface Product {
        id: string;
        title: string;
        price: number;
        image: string;
        description: string;
        category: string;
    }

    //Estructura de Omit:
    //Omit< Interfaz, 'propiedad1' | 'propiedad2'>
    export interface createProductDTO extends Omit<Product, 'id'> {
        /*
        Hereda todos los atributos de product
        (title, price, image, ...) pero omite el id
        */
    }
```

### PUT y PATCH

Ambos sirven para hacer actualizaciones de informacion.
Generalmente la *URL* es la misma que cuando hacemos una creacion con *POST*, aunque tambien debemos de pasarle el *id* del (en este ejemplo) 'producto' a actualizar. 
- `http.put(apiUrl/id, body)`
- `http.patch(apiUrl/id, body)`

#### Diferencias entre PUT y PATCH

Esto depende de como este configurado el *Backend*, pero, si somos puristas:
- PUT: requiere todos los datos del objeto, aun cuando un solo dato vaya a ser actualizado.
  - Ejemplo: Quiero actualizar el nombre de un usuario, pero, obligatoriamente, debo enviarle al backend todos los datos del usuario (nombre, apellido, edad, direccion, ...)
- PATCH: requiere solo los datos a ser actualizados.
  - Ejemplo: Quiero actualizar el nombre de un usuario, y solo necesito enviarle al backend   el nombre del usuario

Una vez mas, esto simplemente **depende de como este configurado el backend**, por ejemplo, tambien se puede configurar PUT de tal manera que reciba todos los datos o solo los datos necesarios

```TypeScript
    export class ProductService{
        constructor(
            private http: HttpClient;
        ){}

        update(id:string, dto:updateProductDTO){

            return this.http.put<Product>(
                `https://young-sands-07814.herokuapp.com/api/products/${id}`,
                dto //objeto con los datos para la actualizacion
            )
        }
    }
```

En este caso, necesitamos los enviar los mismos datos que enviamos en una creacion (title, image, price, description, category). Entonces, por que no reutilizar la misma interfaz?

#### Implements *Partial<>*

No podemos reutilizar la interfaz *createProductDTO* porque en esta **todos los datos son obligatorios**; sin embargo nosotros, solo queremos enviar los datos que necesitamos actualizar.

##### Como Podemos solucionar este problema?

Para hacerlo de forma manual, debemos de crear una nueva interfaz y especificar que cada atributo es opcional

```TypeScript
    export interface updateProductDTO {
        title?: string;
        price?: number;
        image?: string;
        description?: string;
        category?: string;
    }
```

Sin embargo, esta no es la mejor manera de realizarlo, ya que estamos repitiendo codigo. 

Para evitar repetir codigo, podemos hacer uso de *Partial<>*

```TypeScript
    export interface updateProductDTO implements Partial<createProductDTO>{
        /*
            Trae todos los atributos de createProductDTO, pero
            indica que cada atributo es opcional.
            De esta forma no repetimos codigo, gracias a Partial<>
        */
    }
```

### DELETE

Nos sirve para eliminar informacion. Solamente debemos de enviar el id del objeto a eliminar

- `http.delete(apiUrl/id)`

```TypeScript
    export class ProductService{
        constructor(
            private http: HttpClient;
        ){}

        update(id:string){

            return this.http.delete<Product>(
                `https://young-sands-07814.herokuapp.com/api/products/${id}`
                )
        }
    }
```