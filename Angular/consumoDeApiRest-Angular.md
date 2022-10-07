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
## Url Parameters y paginacion.
    
Son datos que enviamos en la URL, los cuales el Backend recibe. Uno de sus usos más clásicos es hacer filtros o paginación.

### Paginación con Limit y Offset

- **Limit**: Indica cuantos elementos quiero obtener

- **Offset**: Indica cuantos elementos quiero 'escapar'. Es decir, cuantos elementos quiero que se omitan antes de traerme los resultados.

### HttpParams

Nos sirve para enviar o no enviar parametros en un request de forma dinámica.

Es decir, enviar ciertos parametros solo si una condición se cumple. Si no se cumple la condición, hacemos el pedido simplemente sin parámetros.

```TypeScript
    //products.service.ts
    import { HttpParams } from '@angular/common/http';

    getAllProducts(limit?: number, offset?: number) {
        // tenemos dos parametros opcionales. limit y number

        let params = new HttpParams();
        // declaramos una instancia de los parametros

        if (limit && offset) {
        // en caso de recibir ambos parametros
        // configuramos los parametros a ser enviados

        //params.set('nombre_parametro', valor)
        params = params.set('limit', limit);
        params = params.set('offset', offset);
        }
        return this.http.get<Product[]>(this.apiUrl, { params });
    }
```

## Observable vs Promise

- **Observable**: con un Observable nosotros creamos un stream constante de datos. Datos que se van a ir comunicando.
  Con un observable puedo emitir varios valores, y cada vez que un valor nuevo sea emitido, este se comunicará a los observadores como eventos

- **Promise**: Con la promesa no podemos emitir varios valores como en un observable. Podemos resolver solo una vez la promesa, por lo tanto solo podemos emitir un valor.
  
Una Promesa se ejecuta una sola vez y me entrega un valor único.
Un Observable me entrega un flujo constante de datos

### Ventajas de un Observable

- Capacidad de emitir muchos datos
- Cancelar el Observable en cuando ya no lo necesite: Cuando nosotros enviamos una promesa no la podemos cancelar. Con un Observador si podemos hacer esto
- Se pueden utilizar Pipes para aplicar ciertas transformaciones o filtros al resultado

``` JavaScript
    const { Observable } = require('rxjs')
    const { filter } = require('rxjs/operators')

    anObservable
        .pipe( 
            filter( value => value !== null )
            // Solo se reciben los valores diferentes 
            // a null
         )
        .subscribe( response => console.log(response))

```

## Reintentar una petición 

Gracias a los Observadores, esta tarea se hace sencilla.
Para esto utilizamos un operador llamado *retry*

```TypeScript
    //products.service.ts
    import { retry } from 'rxjs/operators'

    var wrongURL = "www.platzo.com/api/products"

    getAllProducts(){
        http.get( wrongURL )
            .pipe(
                retry(3)
                // Reintenta la peticion 3 veces en caso
                // de que esta falle
            )
    }

```

También contamos con `retryWhen`, para reintentar la petición dependiendo de una condición

## CORS - Cross Origin Resourse Sharing

Para solucionar este problema necesitamos que el backend acepte pedidos desde otros dominios especificos. O tal vez de cualquier dominio

Pero, ¿Qué pasa si no tenemos control en el backend?

Hay una forma de crear un proxy desde Angular para que el origen se modifique al mismo que el api, y así no tengamos un problema de cors. Pero esto **solo funciona en modo de desarrollo**

### Como crear el proxy en Angular

1. Creamos un archivo llamado *proxy.config.json* en el root de nuestro proyecto
   
2. Ahí especificamos que cualquier petición que vaya a un *api* aplique unas reglas específicas

```Json
    {
        "/api/*": {
            "target": "https://api_url.com",
            "secure":   true,
            "logLevel": "debug",
            "changeOrigin": true
        }
    }
```

3. Ahora cambiamos el Endpoint de nuestros pedidos. Quitamos la url y simplemente dejamos el path 

```TypeScript
    
    //before
    var apiUrl = "https://api_url.com/api/products"
    http.get(apiUrl)

    //after
    var apiUrl = "/api/products"
    http.get(apiUrl)

```

De esta forma, Angular hará que el pedido salga desde el dominio de la api ( `https://api_url.com` ) en lugar de nuestro dominio de desarrollo ( `http://localhost:4200` )

### Ejecutar la aplicacion utilizando el proxy 

` ng serve --proxy-config <file_path>`

Ejemplo

` ng serve --proxy-config ./proxy.config.json `

## Manejo de ambientes

Angular por defecto nos da dos ambientes. Uno de produccion y uno de desarrollo

```TypeScript
    //Produccion
    export const environment = {
        production: false,
        apiUrl: "https://api_url.com"
    };
```

```TypeScript
    //Desarrollo
    export const environment = {
        production: true,
        apiUrl: ""
    };
```

Angular se encarga de tomar un valor u otro dependiendo de si estamos en produccion o en desarrollo.

De la siguiente manera, podemos utilizar las variables de entorno en nuestra aplicacion.

```TypeScript
    //products.service.ts
    import { environment } from "../../environments/environment"
    /* IMPORTANTE
     Siempre importar el environment.ts, no el environment.prod.ts
    */

   var apiUrl = `${environment.apiUrl}/api/products`

```

De esta forma conseguimos que nuestra URL se modifique dependiendo de si estamos en un entorno de desarrollo o en produccion

## Manejo de errores

Como manejar los errores de las peticiones con los *Observables*

**IMPORTANTE: los errores utilizan la interfaz `HttpErrorResponse`**

### Manejo de errores en el subscribe

Para manejar los errores en el subscribe, agregamos un nuevo "parametro", en el cual recibiremos el error en caso de que este ocurra

```TypeScript

  //products.component.ts
  onShowDetail(id: string) {
    this.productsService.getProduct(id)
    .subscribe(data => { //parametro1

        /* Aqui se reciben los datos si el pedido fue 
        exitoso
        */
    },
    response => { //parametro2

      /* Aqui recibimos el error en caso de que este 
      ocurra
      */
    })
  }

```

### Manejo de errores en el pedido \<service\>

Para esto utilizaremos el operador `catchError` de `rxjs/operators` y `throwError` de `rxjs`

1. Hacemos el pedido, le agregamos un *pipe* y utilizamos *catchError* para capturar los errores que se presenten. 

2. Con ayuda de *throwError* también podemos emitir **errores personalizados** dependiendo del código de error *\<status>*

``` TypeScript
//products.service.ts 
import { catchError } from 'rxjs/operators'
import { throwError } from 'rxjs'

  getProduct(id: string) {
    return this.http.get<Product>(`${this.apiUrl}/${id}`)
    
    .pipe(
      catchError( (response: HttpErrorResponse) => {
        // se hace catch del error
        if (response.status === 404){
            return throwError('El producto no existe')
            // retornamos un error personalizado
        }
        return throwError('Ups algo salio mal')
      })
    )
  }

```

#### HttpStatusCode

Es una herramienta que nos provee angular para detectar el status de los errores, en caso de que no tengamos conocimiento de que significa cada status de error.

```TypeScript
    //products.service.ts
    import { HttpStatusCode } from '@angular/common/http';

    getProduct(id: string) {
        return this.http.get<Product>(`${this.apiUrl}/${id}`)
        
        .pipe(
        catchError( (response: HttpErrorResponse) => {
            if (response.status === HttpStatusCode.NotFound){
                return throwError('El producto no existe')
            }
            if (response.status === HttpStatusCode.Unauthorized){
                return throwError('No estas autorizado')
            }
            return throwError('Ups algo salio mal')
        })
        )
    }

```

## Transformar peticiones

Podemos manipular la respuesta del backend y tranformarla. Por ejemplo, insertar más informacion.

Normalmente queremos que todo venga calculado desde el backend, pero pueden darse estos casos.

Para esto utilizaremos el operador `map` de `rxjs/operators`

El operador `map` nos permite evaluar cada uno de los valores que llegan en el Observable, y nos permite aplicar una transformacion.

Recuerda: `map` es para transformar los valores que lleguen en el observable

```TypeScript
    //products.service.ts
    
    import { map } from 'rxjs/operators'

    getAllProducts() {
        return this.http.get<Product[]>(this.apiUrl)

        .pipe(

            /* map recibe todos los datos del subscribe,
            en este caso lo llamamos <products> */
            map( products => products.map(item => {
                
                /*como <products> es un array, podemos 
                aplicar la funcion nativa de JavaScript 
                <map>*/
                    return {
                    ...item,
                    taxes: .10 * item.price
                
                    /* Agregamos un nuevo elemento <taxes>
                    a cada item dentro del array <products>
                    */
                    }
                }))
        )
    }

```

Luego, podemos utilizar este valor en el template del componente.

```TypeScript
    <p>{{ product.taxes | currency:'COP'}}</p>
```

Si el atributo es opcional en la interfaz, podria darnos errores al no estar definido.

Esto lo podemos solucionar de esta manera

```TypeScript
    <p>{{ product?.taxes | currency:'COP'}}</p>
    /* De esta forma le decimos a Angular que esto es opcional. Y angular lo tratara de manera que no de errores en caso de que no exista*/
```

## Como Evitar el CallbackHell

Esto se da cuando tenemos varias peticiones donde cada una de ellas depende de la otra; Por lo que empezamos a anidar varias veces haciendo que el codigo sea dificil de leer y de mantener.

### Ejemplo de CallbackHell con dependencia

Supongamos que queremos leer un producto y actualizarlo al instante.

*con dependencia:* indica que necesitamos del primer resultado para poder ejecutar la segunda operacion.

``` TypeScript
  readAndUpdate(id: string){
    this.productsService.getProduct(id)
    //Lectura del producto
    .subscribe(data => {
    //primer subscribe

      this.productsService.update(data.id, {title: 'change'})
      //Actualizacion
      .subscribe( updateResponse => {
          //segundo subscribe
        console.log(updateResponse)
      })
    })
  } 
```

Como vemos, aqui tenemos dos subscribes anidados.

## Como solucionar esto con observables

En los observables, lo solucionamos con ayuda del operador `switchMap`

```TypeScript

  readAndUpdate(id: string){
    this.productsService.getProduct(id)
      .pipe(
        switchMap(product => {
          return this.productsService.update(product.id, {title: 'change'})
        }),
        switchMap(updateResponse => {
          //another action with the update response
          return updateResponse.title
        })
      )
      .subscribe( data => {
        // Respuesta final luego de los switchMaps
        // En este caso recibe el titulo del producto actualizado
      })
    
  }

```

## Como solucionar esto con promesas

En las promesas, esto lo solucionamos con ayuda de `.then`

``` TypeScript
  readAndUpdate(id: string){
    this.productsService.getProduct(id)
    //Lectura del producto
    .then(
        //Primera accion
    )
    .then(
        //Segunda accion
    )
  } 
```

## Varios request sin dependencia

Por ejemplo, cuando queremos ejecutar dos pedidos, que no dependen el uno del otro, al mismo tiempo.

*ejemplo con promesas*

```TypeScript
    Promise.all(promesa_1(), promesa_2())
```

Con promesas, utilizamos esto para ejecutar ambas en paralelo y recibir el resultado al mismo tiempo

## Como hacer esto con Observables

Para esto, utilizamos `zip` de `rxjs`, el cual nos permite adjuntar dos observables y recibir la respuesta de los dos al mismo tiempo

```TypeScript
    zip(
      this.productsService.getProduct(id),
      this.productsService.update(id, {title: 'zip title'})
    )
    .subscribe( response => {
        // zip nos devuelve ambos resultados en forma de array.
        // El orden depende exclusivamente de como lo ubicamos en el zip

      const product = response [0]
      const update = response [1]
    } )
```

### Cierre de modulo

De este modulo, resaltamos varias buenas practicas sobre como manejar los errores, evitar callbackHells, manejar problemas de CORS, entre otras cosas

Es importante tener en cuenta que toda la logica de los pedidos debemos ubicarlas en los servicios, y utilizar los componentes solamente para lo que realmente son: **mostrar la informacion y manipular la interaccion con el usuario.**

## Login y manejo de Auth

Como hacemos un Login con una API y como esta mantiene nuestra sesion.

En este caso, la API a la que nos vamos a conectar tiene un modo de autenticación por JWT.

Asi que aqui aprenderemos como loguearse con este sistema de autenticacion.

### Servicios

Para lograr esto utilizaremos 3 servicios.

- auth: se encarga del la autenticacion del login y la autenticacion para ver los datos del perfil \<profile>
- users: se encarga de la creacion y lectura de usuarios.
- token: se encarga de guardar y obtener el token de donde sea que lo hayamos guardado

### Manejo de Headers

Es en las cabeceras del pedido donde enviamos nuestro Token

Lo importante al utilizar autenticaciones es seguir este esquema

`Authorization: <type> <credentials>`

El espacio entre \<type> y \<credentials> es necesario.

Ejemplo: `Authorization: Bearer 10348108245r10jasijdf09u1q20893`

```TypeScript
  profile(token: string) {
    return this.http.get<User>(`${this.apiUrl}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      }
    })
  }
```
enviamos los headers simplemente despues de la url

Si necesitamos que los headers sean dinamicos, utilizamos HttpHeaders

```TypeScript
  profile(token: string) {
    let headers = new HttpHeaders()
    headers.set('Authorization', `Bearer ${token}`)
    
    return this.http.get<User>(`${this.apiUrl}/profile`, {
      headers
    })
  }
```

## Interceptores

Sirven para interceptar cada peticion que hacemos y asi poder agregar informacion. Por ejemplo agregar el token por medio de interceptores

### Como crear interceptores

`ng g interceptor interceptors/time` 

```TypeScript

@Injectable()
export class TimeInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const start = performance.now()
    // guardamos el tiempo de inicio
    
    return next //next es un observable
    .handle(request)
    .pipe(
    
      tap( () => {
        // tap nos permite ejecutar una operacion luego de 
        // que la primera termine
        
        const time = performance.now() - start
        console.log(`${request.url}: ${time} ms`)
        //imprimimos la diferencia de tiempo
      })
    );
  }
}

```

### Injectar el Interceptor en nuestro app.module.ts

```TypeScript
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { TimeInterceptor } from './interceptors/time.interceptor';

@NgModule({
  providers: [
    { 
        provide: HTTP_INTERCEPTORS, 
        useClass: TimeInterceptor, 
        multi: true 
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

## Donde guardar el token

- Memory storage -> una variable. Se pierde el valor al cerrar el navegador, la pestaña o al recargar
  
- Session storage -> memoria de la sesion. Se pierde el valor al cerrar el navegador o la pestaña
  
- Local Storage -> Nos mantendria el token guardado hasta que el usuario cierre sesion

- Cookie storage -> Tambien tiene una persistencia y es mas seguro que el local storage

## Agregar autorizacion mediante un interceptor

Para esto, necesitamos un interceptor que nos intercepte todos los pedidos que realizamos y agregue la autorizacion en los headers del pedido.

```TypeScript

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(
    private tokenService: TokenService
  ) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    request = this.addToken(request)
    //sobreescribimos el request original

    return next.handle(request);
    //realizamos el pedido
  }

  private addToken(request: HttpRequest<unknown>){
    const token = this.tokenService.getToken()
    if (token){
      const authRequest = request.clone({
        //Necesitamos clonar el request para modificarlo

        headers: request.headers.set(
          'Authorization', 
          `Bearer ${token}`
        )
        // Añadimos un nuevo header
      })
      return authRequest
      //Retornamos el request ya con la autorizacion
    }
    return request
  }
}

```

## Agregando contexto a los Interceptores

Con esto, podemos evitar que los interceptores que creamos intercepten todos nuestros pedidos. Solo haremos que intercepten los pedidos especificos que nosotros queremos

1. Importamos `HttpContext` y `HttpContextToken`
2. Creamos una constante que nos indicara si el pedido debe o no ser interceptado por defecto

```TypeScript

import {
  HttpContext,
  HttpContextToken
} from '@angular/common/http';

const CHECK_TIME = new HttpContextToken<boolean>(() => false)
//Los pedidos NO se interceptan por defecto

```

3. Creamos un método EXPORTABLE que se encargará de hacer un toggle de la variable que creamos anteriormente

```TypeScript
export function checkTime(){
  return new HttpContext().set(CHECK_TIME, true)
  //Si esta funcion se llama, el pedido sera interceptado.
  //Ya que agregamos al request el contexto necesario 
  //para que sea interceptado
}
```

4. Creamos una condición dentro del interceptor, que verifica si el pedido "tiene" el contexto para ser interceptado

```TypeScript
@Injectable()
export class TimeInterceptor implements HttpInterceptor {


  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    if (request.context.get(CHECK_TIME)){
      //Preguntamos si tiene el contexto

      //Logica 
      const start = performance.now()

      return next
      .handle(request)
      .pipe(
        tap( () => {
          const time = performance.now() - start
          console.log(`${request.url}: ${time} ms`)
        })
      );
    }
    
    return next.handle(request)
    // Si no tiene el contexto, lo dejamos pasar
  }
}
```

Ahora, para agregar el contexto a los pedidos que SI queremos que sean interceptados, lo hacemos de la siguiente manera:

1. Importamos la funcion que activa el contexto *(funcion que creamos dentro del interceptor)*
2. Configuramos el contexto al realizar el pedido

```TypeScript

import { checkTime } from '../interceptors/time.interceptor';

export class ProductsService {

  getProductsByPage(limit: number, offset: number) {
    return this.http.get<Product[]>(`${environment.API_URL}`, {
      params: { limit, offset },
      context: checkTime()
      //Aqui configuramos el contexto
    })
  }

}

```

## Descarga de Archivos 

Cuando ya tengamos un archivo estatico y queremos solamente un boton de descarga, podemos utilizar solo HTML.

Especificamente una etiqueta \<a>, que apunte al archivo. A esta etiqueta debemos agregarle el atributo especial `download`

`<a href="../assets/files/texto.txt" download>descargar</a>`

### Descarga de Archivos con Http

Para esto, necesitamos descargar la dependencia `file-saver`, la cual nos permite hacer descargas por http.
Tambien necesitamos descargar el tipado de esta libreria

1. `npm i file-saver`
2. `npm install @types/file-saver --save-dev`

3. Creamos un metodo que recibe
  - El nombre con el que se va a descargar el archivo
  - La url del archivo
  - El tipo de archivo

4. Hacemos un pedido `get` a la url del archivo, y agregamos como `responseType` "blob"

5. Con ayuda de un pipe, tap y file-saver, hacemos que se guarde el archivo luego de que se reciba la respuesta del pedido.

6. Con ayuda de map, hacemos que solo se devuelva un Booleano en el observable. Ya que ya no necesitamos el contenido del archivo ( ya fue descargado )

```TypeScript
import { saveAs } from 'file-saver';
import { tap, map } from 'rxjs/operators';

export class FilesService {
  getFile(name:string, url:string, type:string){
    return this.http
    .get(
      url, 
      {responseType: 'blob'}
    )
    .pipe(
      tap( content => {
        const blob = new Blob([content], {type})
        saveAs(blob, name)
      }),
      map( () => true)
    )
  }
}
```

## Subida de archivos con HTTP

1. Creamos un metodo, que se encargara de recibir el archivo y hacer el pedido de creacion al fondo

```TypeScript
  uploadFile(file: Blob){
    const dto = new FormData()
    // formato estandar de HTML para este tipo de request

    dto.append('file', file)
    //Agregamos el key (solicitado por el back, en este caso 'file')
    //Y adjuntamos el archivo como valor

    return this.http.post<File>(`${this.apiUrl}/upload`, dto, {
      // headers: {
      //   'Content-type': "multipart/form-data"
      // }
    })
    // Hay veces que es necesario enviar estos headers. 
    // Eso depende exclusivamente de si el back los necesita o no
  }
```

2. En el HTML, creamos un Input para que el usuario pueda seleccionar el archivo.

```HTML
    <input type="file" (change)="onUpload($event)">
    <!-- En este ejemplo, el archivo se subirá cada vez que sea seleccionado -->
```

3. En el metodo, necesitamos acceder al archivo adjunto al input, y enviarlo al metodo del servicio, para que se encargue de subirlo

```TypeScript
  onUpload(event: Event){
    const element = event.target as HTMLInputElement
    
    const file = element.files?.item(0)
    //Comprueba si tiene archivos adjuntos y trae el primero
    //[0] por que se pueden seleccionar varios archivos

    if (file){
      this.fileService.uploadFile(file)
      .subscribe()
    }
  }
```