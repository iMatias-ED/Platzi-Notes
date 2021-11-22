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
