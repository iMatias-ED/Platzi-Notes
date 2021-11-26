# Resumen del curso Componentes y Servicios

## Artefactos nucleo de Angular

- Componentes
- Pipes
- Directivas
- Servicios

## Componentes

### Que son los componentes?

Los utilizamos para abstraer cada funcionalidad de nuestra aplicacion en varios componentes con responsabilidades unicas.
Cada componente esta compuesto de 4 archivos:

- **component.html** -> Es la vista de nuestro componente. Comunmente llamado template
- **component.css** -> Los estilos de nuestro componente
- **component.spec.ts** -> Este archivo es generado para hacer pruebas (testing) a nuestro componente
- **component.ts** -> Es el archivo que tiene toda la logica. Este archivo tambien se encarga de unir al HTML y al CSS.

#### Comando para generar componentes en Angular

- Version Larga: `ng generate component nombre-componente`
- Version abreviada: `ng g c nombre-componente`

#### Organizacion del proyecto

Es buena practica dividir tus artefactos en carpetas. Por ejemplo; una carpeta especifica para los componentes, otra carpeta para los servicios, etc.

#### Algo que debes de tener muy en cuenta

Cada componente **solo puede pertenecer a un modulo**. Un componente no puede pertenecer a mas de un modulo

### Como funciona un componente?

Un componente esta conformado por varias partes.

- El decorador `@Component`: este decorador se encarga de enlazar el HTML y el CSS, ademas de darle un selector a nuestro componente. El selector es la forma en la que vamos a llamar al componente desde otros componentes.

## Los decoradores

Los decoradores son algo muy importante en Angular, por que le dicen al compilador (TypeScript) como debe comportarse esa clase en particular

## Inputs y Outputs

### @Input

Un input nos funciona para pasar informacion desde el padre hacia el hijo.

*Obs: para el ejemplo tendremos la siguiente estructura:*

```HTML
    <app-root> <!--Parent componente-->
        <app-img>
            <!--Child component-->
        </app-img>
    </app-root>
```

- Pasos a seguir:
  - Inicializar una variable en nuestro componente hijo con el decorador @Input()

   ```TypeScript
    export class ImgComponent{

        @Input() img!:string;

        constructor() { }
    }
   ```

  - Pasar el valor para la variable desde el HTML del componente padre

   ```HTML
        <app-img img='Image from parent'></app-img>
   ```
  
  - Para enviar el valor de forma dinamica, debemos de utilizar el property binding

   ```HTML
        <app-img [img]='imgParent'></app-img>
   ```

### @Output

Es la forma de pasar informacion del hijo al padre.

*Obs: para el ejemplo tendremos la siguiente estructura:*

```HTML
    <app-root> <!--Parent componente-->
        <app-img>
            <!--Child component-->
        </app-img>
    </app-root>
```

- Pasos para enviar el evento desde el componente hijo:
  - Inicializar una variable en nuestro componente hijo con el decorador @Output(), como instancia de **EventEmitter**

   ```TypeScript
    export class ImgComponent{

        @Output() loaded = new EventEmitter()

        constructor() { }
    }
   ```

  - Creamos un metodo *(en el componente hijo)* que se encargara de emitir el evento hacia el componente padre.

   ```TypeScript
        export class ImgComponent{
            @Output() loaded = new EventEmitter()

            imgLoaded():void{
                this.loaded.emit()
            }
        }
   ```
  
  - Capturamos un evento desde el HTML y lo conectamos al metodo que acabamos de crear. En este ejemplo capturaremos el evento **load**

   ```HTML
        <img 
            *ngIf="img; else elseImg" 
            [src]="img" 
            (load)="imgLoaded()"
        >
   ```

- Pasos para escuchar el evento desde el componente padre:

  - Creamos un metodo *(en el componente padre)* que se encargara de procesar el evento recibido.

   ```TypeScript
        export class AppComponent {
            title = '';

            onLoaded():void{
                console.log('Event Received')
            }

        }
   ```

  - Escuchamos el evento con ayuda de eventBinding y lo conectamos al metodo creado recientemente. *Obs: el evento tiene el mismo nombre que la variable creada como instancia de EventEmitter*

   ```HTML
        <app-img 
        [img]='title' 
        (loaded)="onLoaded()"
        >
        </app-img>
   ```
  
- Enviar datos a traves del output:
  - Declarar que tipo de dato va a retornar el EventEmitter al momento de su instanciacion

   ```TypeScript
    export class ImgComponent{

        @Output() loaded = new EventEmitter<string>()

        constructor() { }
    }
   ```

  - Al momento de emitir el mensaje, pasamos el dato a enviar como parametro

   ```TypeScript
        export class ImgComponent{
            @Output() loaded = new EventEmitter()

            imgLoaded():void{
                this.loaded.emit("The image was uploaded successfully.")
            }
        }
   ```
  
  - El resto del procedimiento es igual al anterior.

- Recibir los datos del evento desde el componente padre:

  - Creamos un metodo *(en el componente padre)* que se encargara de procesar el evento recibido, y declaramos que recibira como parametro un dato, en este caso, una string.

   ```TypeScript
        export class AppComponent {
            title = '';

            onLoaded(message:string):void{
                console.log('message')
            }

        }
   ```

  - Al escuchar el evento con ayuda de eventBinding, declaramos que se recibiran datos con ayuda de `$event`

   ```HTML
        <app-img 
        [img]='title' 
        (loaded)="onLoaded($event)"
        >
        </app-img>
   ```

### Ciclo de vida de los Componentes

- **constructor:** crea la instancia del componente. Corre antes del render. Es importante que **no corras cosas asincronas** en el constructor. El constructor se corre cada vez que se crea un componente.

- **ngOnChanges:** Corre antes y durante el render (cada vez que detecta un cambio en un `@Input`). Su objetivo es estar actualizando los **cambios en los @inputs**. Las veces que se actualice el valor de todos los @input que tengamos en el componente, lo vamos a recibir en el *ngOnChanges*

  - Los cambios que llegan son de tipo *SimpleChanges*, interfaz que podemos exportar de `@angular/core`. Estoy podemos utilizarlo para leer los cambios
  - Que pasa si tenemos varios inputs y solo queremos leer los cambios de un input en especifico?.
    - Esto podemos solucionarlo convirtiendo el `@input` en un set. Esto consiste en independizar la variable del input, y crear una funcion que se encargue de asignar el valor del input a nuestra variable. Ahora la diferencia es que podemos procesar el input dentro de esa funcion.

    ```TypeScript
        //Input tradicional
        export class ImgComponent implements OnInit {
            @Input() img!:string;
        }
    ```

    ```TypeScript
        //Utilizando set
        export class ImgComponent implements OnInit {
            img!:string;
            
            @Input() 
            set ChangeImg(src_img:string){
                this.img = src_img;
                // Code goes herek
            }
        }
    ```

    - Ahora deberiamos de cambiar el nombre del input por *ChangeImg* desde nuestro componente padre y listo.
    - Si no quieres cambiar el nombre del input, puedes personalizar el nombre del Input en su declaracion

    ```TypeScript
        //Utilizando set
        export class ImgComponent implements OnInit {
            img!:string;
            
            @Input('img') 
            set ChangeImg(src_img:string){
                this.img = src_img;
                // Code goes herek
            }
        }
    ```

- **ngOnInit:** Tambien corre antes del render. Aqui **si podemos correr cosas asincronas**. Corre una sola vez.

- **ngAfterViewInit:** Corre despues del render. Aqui podemos manejar los hijos (HTML), ya que los componentes ya deberian de estar pintados. Las directivas normalmente se corren en el *AfterViewInit*

- **ngOnDestroy:** Cuando se elimina el componente. *Dato interesante:* un *ngIf* en caso de ser verdadero,crea una instancia del componente, y en caso de ser falso, elimina la instancia del componente, llamando a *ngOnDestroy*.

  - **Dato importante:** algunos eventos siguen existiendo aun si se eliminan el componente. Por eso es importante utilizar el *ngOnDestroy* para limpiar los eventos que puedan quedar abiertos

## Servicios

Es la forma en que Angular nos permite hacer modular nuestra aplicación y apartar toda nuestra lógica de negocio, (todo lo que no tiene que ver con la UI, como manipular datos o hacer servicios compartidos).

Los servicios unicamente comunican 'Logica de negocio' hacia los componentes y estos pueden ser utilizados a traves de toda la aplicacion, por los todos componentes.

### Comando para generar un servicio

- Version Larga: `ng generate service nombre-service`
- Version abreviada: `ng g s nombre-service`

Es buena practica guardar todos nuestros servicios en una carpeta llamada *services*

Obs: Los servicios pueden utilizarse dentro de los componentes y/o tambien dentro de otros servicios

#### Archivos generados

Angular nos genera dos archivos, un archivo *.ts* donde estara la logica y, un archivo *.spec.ts*, que puede utilizarse para tests

### Como utilizar los servicios

Para utilizar un servicio debemos de seguir estos pasos:

1. Importar el servicio en el componente a ser utilizado

- `import { StoreService } from '../../services/store.service';`

2. Para incluir a este servicio dentro del componente, vamos a crear algo llamado `Inyeccion de dependencias`
  
- Dentro del constructor, instanciamos una variable, y le decimos que esta variable, del tipo de servicio que vayamos a utilizar
  
  ```TypeScript
    export class ProductsComponent implements OnInit {
        constructor(
            private storeService: StoreService 
        ) { }
    }
  ```

## Inyección de dependencias

### El decorador @Injectable

El decorador de un servicio es `@Injectable`, el cual permite que el servicio se pueda 'Inyectar' en otros componentes y servicios.

Dentro del decorador, esta declarado el Alcance o Scope del servicio

```TypeScript
    @Injectable{
        providedIn: 'root'
    }

```

El motor de inyeccion de dependencias de Angular funciona de la siguiente manera:

- Nuestro servicio es 'Inyectado' dentro de un componente 
  
  ```TypeScript
    export class ProductsComponent implements OnInit {
        constructor(
            private storeService: StoreService 
        ) { }
    }
  ```

  Aqui tipamos la variable al tipo de servicio que vayamos a utilizar, pero no la instanciamos, ya que el motor de Inyecciones hace esto por nosotros.

  Desde ahora, cuando nuestro componente llame a la variable tipada con el tipo de servicio, el motor de inyecciones se encargara de crear la instancia por nosotros.

  Pero, el motor de inyecciones tambien hace algo mas por nosotros.

### Patron Singleton

- Que pasa si hay dos componentes utilizando el mismo servicio. ¿Se crean dos instancias del servicio?

No. Aqui el motor de inyecciones de Angular emplea el patron Singleton

Esto lo que hace es, guardar en memoria la instancia creada, y devuelve la referencia a todos los componentes que la necesiten. Con eso no creamos instancias por cada componente que este requiriendo ese servicio

## Peticiones HTTP con servicios

Angular cuenta con un modulo especifico para las peticiones HTTP

1. Crear el servicion encargado de realizar las peticiones HTTP.
2. Importar el Modulo *HttpClientModule* en el app.module de nuestra aplicacion.
3. Agregar el *HttpClientModule* a la seccion de *imports*
4. Vamos a nuestro servicio e importamos el **SERVICIO** *HttpClient*
5. Como el *HttpClient* es un servicio, debemos de declararlo en el constructor, como cualquier otro servicio
6. Realizamos la peticion a nuestra url con ayuda de `HttpClient.get`

```TypeScript
    import { HttpClient } from '@angular/common/http'

    export class ProductsService{
        constructor(
            private http: HttpClient
        ){}

        getAllProducts(){
            return this.http.get('https://fakestoreapi.com/products')
        }
    }
```

7. Debemos ir a nuestro componente y crear la Inyeccion dependencias para poder utilizar el servicio. 

```TypeScript
    import { StoreService } from '../../services/store.service';
    import { ProductsService } from '../../services/products.service';

    export class ProductsComponent implements OnInit {

    constructor(
        private storeService: StoreService,
        private productsService: ProductsService
    ) {}
```

8. Como una peticion Http es una operacion asincrona, no podemos hacerla desde el constructor. Recordemos que un lugar apropiado para utilizar funcionalidades asincronas es en el `ngOnInit`

```TypeScript
    import { StoreService } from '../../services/store.service';
    import { ProductsService } from '../../services/products.service';

    export class ProductsComponent implements OnInit {

    constructor(
        private storeService: StoreService,
        private productsService: ProductsService
    ) {}

    ngOnInit(): void {
        this.productsService.getAllProducts()
        .subscribe(data => {
        this.products = data;
        });
    }
```

9. Angular maneja un formato por defecto para los resultados asincronos; un *Observable*. Podemos acceder a los datos de este Observable utilizando *.subscribe*

```TypeScript
    ngOnInit(): void {
        this.productsService.getAllProducts()
        .subscribe(data => {
        this.products = data;
        });
    }
```

### Tipar los datos que devuelve una peticion

Esto lo hacemos para asegurarnos que la peticion Http nos devuelve los datos con el formato que esperamos.

```TypeScript
    import { HttpClient } from '@angular/common/http'
    import { Product } from '../../models/product.model'

    export class ProductsService{
        constructor(
            private http: HttpClient
        ){}

        getAllProducts(){
            return this.http.get<Product[]>('https://fakestoreapi.com/products')
        }
    }
```

## Los Pipes

Los pipes funcionan como una tuberia, tienen una entrada, por donde entran los datos, posteriormente se procesan esos datos y nos produce una salida. Estos son utilizados desde el HTML

Una caracteristica de los pipes es que se pueden unir.

```HTML
    <p>
        Fecha: {{ date_var | date:'short' }}
    </p>
```

En este ejemplo, tenemos la manera de utilizar un pipe:

1. Nuestra variable `date_var` constituye la entrada del pipe.

- `<p> Fecha: {{ date_var }}</p>`

2. El simbolo `|` es el que utilizamos para 'decir' que vamos a utilizar un Pipe

- `<p> Fecha: {{ date_var | }}</p>`

3. Luego le sigue el nombre del Pipe.

- `<p> Fecha: {{ date_var | date }}</p>`

4. Y por ultimo tenemos el formato que queremos darle a nuestra salida

- `<p> Fecha: {{ date_var | date:'short' }}</p>`

### Construir un Pipe propio

#### Comando para generar un Pipe

- Version Larga: `ng generate pipe nombre-pipe`
- Version abreviada: `ng g p nombre-pipe`

Angular nos genera dos archivos, un archivo *.ts* donde estara la logica y, un archivo *.spec.ts*, que puede utilizarse para tests

### Estructura interna de un pipe

1. Simple

```TypeScript
    import { Pipe, PipeTransform } from '@angular/core';

    @Pipe({
    name: 'reverse'
    })
    export class ReversePipe implements PipeTransform {
        transform(value: string): string {
            return value.split('').reverse().join('');
        }
    }
```

- El parametro `value` constituye la entrada del Pipe.
- Luego simplement retornamos el valor con el cambio deseado.

2. Con argumentos

```TypeScript
    import { Pipe, PipeTransform } from '@angular/core';

    @Pipe({
    name: 'reverse'
    })
    export class ReversePipe implements PipeTransform {
        transform(value: string, ...args:string[] ): string {
            return value.split('').reverse().join('');
            //No se explica como utilizar los argumentos
        }
    }
```

## Directivas

Se utilizan para hacer modificaciones del DOM de forma directa y tambien, podemos modificar atributos.

Normalmente evitamos hacer modificaciones del DOM, porque los frameworks ya hacen esto por nosotros

### Comando para generar una Directiva

- Version Larga: `ng generate directive nombre-directive`
- Version abreviada: `ng g d nombre-directive`

Es buena practica guardar las directivas dentro de una carpeta llamada *directives*

Angular nos genera dos archivos, un archivo *.ts* donde estara la logica y, un archivo *.spec.ts*, que puede utilizarse para tests

### Estructura interna de una directiva

```TypeScript
    import { Directive, ElementRef, HostListener } from '@angular/core';

    @Directive({
    selector: '[appHighlight]'
    })
    export class HighlightDirective {
        constructor(
            private element: ElementRef
        ) {
            this.element.nativeElement.style.backgroundColor='red';
        }
    }
```

Con ayuda de el servicio ElementRef, nos traemos una referencia del elemento HTML y desde ahi podemos modificarlo

Para utilizar esta directiva simplemente debemos de ponerlo como un atributo dentro del elemento HTML que queremos modificar

```HTML
    <p appHighlight>{{ product.description }}</p>
```

*Dato: el elemento que implementa la directiva es llamado elemento `host`*

#### Como escuchar eventos del elemento 'host'

Para esto debemos importar el decorador `@HostListener`, desde angular core.

Luego simplemente ponemos cual es el evento que queremos escuchar

```TypeScript
  @HostListener('mouseenter') onMouseEnter() {
    this.element.nativeElement.style.backgroundColor = 'red';
  }
```

## Reactividad basica

### State management

Para esto, debemos de tener en cuenta que nuestros componentes forman un arbol por jerarquias. 

Por ejemplo: Si tenemos al componente *root*, que dentro tiene un componente *padre* y a su vez, este componente *padre* tiene un componente *hijo*

```HTML
    <root>
        <padre>
            <hijo></hijo>
        </padre>
    </root>
```

Que pasa si el componente hijo quiere comunicarse con el componente root? 

Si seguimos el estandar de Angular (@Inputs y @Outputs), cada componente tendria un @Output hasta llegar al root

```HTML
    <root><!-- Recibe el mensaje a <padre> -->
        <padre> 
            <!-- Recibe el mensaje de <hijo> y -->
            <!-- Envia el mensaje a <root> -->
            
            <hijo></hijo> <!-- Envia el mensaje a <padre> -->
        
        </padre>
    </root>
```

Para evitar tener que hacer este recorrido de componentes, se han creado estrategias para poder comunicarse de un componente a otro sin tener que hacer todo el recorrido

### De que trata esta teoria?

Se trata de tener un 'Store' o un estado global de la aplicacion, en donde, en lugar de recorrer cada componente para poder comunicarme, debo crear un 'Store' donde se almacenen los estados que se van a compartir.

De esta forma, los componentes que quieran ese estado, simplemente se suscriben

### Como Aplicarlo a codigo

Para esto, creamos un servicio, el cual utilizaremos como 'Store' y, como variable para almacenar los estados utilizaremos un BehaviorSubject de rxjs.

```TypeScript
    import { BehaviorSubject } from 'rxjs';
    export class StoreService {
        //declaramos el BehaviorSubject
        private myCart = new BehaviorSubject<Product[]>([]);
        
        //Lo convertimos a un observable para poder 
        //suscribirnos a sus cambios
        myCart$ = this.myCart.asObservable();

        constructor() { }

        addProduct(product: Product) {
            //Emitimos el nuevo 'estado' de myCart
            this.myCart.next(this.myShoppingCart);

            //la 'notificacion' solo le llega a los componentes 
            //suscritos
        }
    }
```

### Como escuchar los cambios desde el componente

1. Inyectamos el servicio en el componente
2. Nos suscribimos desde el ngOnInit o desde el constructor

```TypeScript
    import { StoreService } from '../../services/store.service'

    export class NavComponent implements OnInit {
        counter = 0;

        constructor(
            private storeService: StoreService
        ) { }

        ngOnInit(): void {
            this.storeService.myCart$.subscribe(products => {
            });
        }
    }
```

#### Buenas practicas para definir observables

A los observables, normalmente se les agrega un signo de pesos (\$) al final `myCart\$`

## Estilos y Linters en Angular

### Aplicar las buenas practicas de forma sistematizada

Antes que nada, angular cuenta con una Guia de buenas practicas oficial <https://angular.io/guide/styleguide#naming>

Para ver si cumples con estas buenas practicas puedes utilizar un Linter

#### Pasos

1. Configurar el linter
`ng add @angular-eslint/schematics`

2. Correr el linter
`ng lint`