# Curso de fundamentos de Angular. Platzi

## Estructura de un proyecto

- El nucleo de la aplicacion se encuentra #  la carpet src*
- Los componentes se encuentran en el directorio *app*

## Archivos internos

- .browserslistrc:
Indica a angular en que versiones tiene que ser compatible tu aplicacion

- .editorconfig
Tiene mas que ver con trabajar en equipo.
Sirve para configurar las reglas de desarrollo del equipo.
Por ejemplo la indentacion, etc.
*Para que este archivo funcione* debes de instalar en VsCode un plugin llamado *EditorConfig for VS Code*

- tsconfig.json
Tiene que ve con la configuracion que tiene Angular con TypeScript

- angular.json
Es donde podemos manejar diferentes ambientes.
Por ejemplo: podemos tener un ambiente de staging y un ambiente de QA (testing).
En la seccion de *budgets* podemos configurar cual es el tamaño que deberia tener normalmente nuestra aplicacion

- karma.conf.js
Es para correr unit testing

- package.json
Las versiones que estamos utilizando

- .nvmrc
Sirve para especificar la version de node en la cual corre nuestro proyecto.
Si no esta creada simplemente podemos crearla

## Property Binding

Su uso es para configurar propiedades en un elemento html
`<button [disabled]="btnDisabled"> Click me </button>`

## Event Binding

Con parentesis, encerramos el evento que queremos capturar
`<button (click)="onClick()"> Click me </button>`

## Data Binding

Es una fusion entre escuchar un evento (*Event Binding*) y escuchar una propiedad (*Property Binding*)
En angular tenemos algo especial para esto, que es el:

- [(ngModel)]: ngModel siempre esta pendiente del estado del input. Chequea si ese campo es valido o no y ademas sincroniza el valor

## Estructuras de control

- NgIf

```HTML
    <div *ngIf="condition; else elseBlock">
        Content to render when condition is true.
    </div>
    <ng-template #elseBlock>
        Content to render when condition is false.
    </ng-template>

```

- NgFor

```HTML
    <li *ngFor="let item of items; index as i; trackBy: trackByFn">...</li>
```

- NgSwitch

```HTML
    <container-element [ngSwitch]="switch_expression">
        <!-- the same view can be shown in more than one case -->
        <some-element *ngSwitchCase="match_expression_1">...</some-element>
        <some-element *ngSwitchCase="match_expression_2">...</some-element>
        <some-other-element *ngSwitchCase="match_expression_3">...</some-other-element>
        <!--default case when there are no matches -->
        <some-element *ngSwitchDefault>...</some-element>
    </container-element>
```

## Template reference variables

Es una referencia a un elemento de nuestra aplicacion. Podemos acceder a esta referencia tanto desde nuestro typescript como desde el html.
Las referencias pueden ser utilizadas *en el TS* recien desde el afterViewInit
*en el HTML* solo podemos acceder a la variable despues de declararla, no antes.
**Pasos para utilizar template variables**

1. Agregar el template variable en el html

```HTML
    <p #text>
        Random text
    </p>
```

1. Agregar la referencia al elemento HTML en el *TS* con *@ViewChild*
` @ViewChild('text') text!:ElementRef; `

1. Utilizar la refencia al elemento dentro *afterViewInit*, o en cualquier metodo que se ejecute luego de *afterViewInit*

```TYPESCRIPT
  ngAfterViewInit(){
    console.log(this.text)
    this.text.nativeElement.innerHTML += "Hola desde TS"
  }
```

## Estilos dinamicos dependiedo del estado de un elemento

### Agregar clases dinamicas

Nos permite activar o desactivar una clase CSS, en un elemento, dependiendo de una condicion.
Su sintaxis es la siguiente:

```HTML
    <p #text class='simple-text' [class.nameClass]='condition goes here'>
        Random text
    </p>
    <!--por ejemplo-->
    <p #text class='simple-text' [class.active]=' 1 == 1 '>
        Random text
    </p>

```

#### Como verificar que un elemento tiene uno o mas estilos concatenados

Con verificar que un elemento tiene estilos concatenados, me refiero a esto:

```HTML
    <p #text class='simple-text active' >
        Random text
    </p>
```

Esto podemos verificarlo en el *CSS* de esta forma:

```CSS
.simple-text {
    background: red;
    color: white;
    opacity: 0; //Hace que sea invisible

    &.active{
        opacity: 1;
    }
}
```

Esto hace que, cuando nuestro elemento cuente con las clases simple-text y active al mismo tiempo, nuestra opacidad cambie a 1, es decir, que se muestre el elemento

### Modificar estilos dinamicamente

Esto nos permite modificar un estilo especifico en el html, dependiendo de una condicion.

```HTML
    <p #text [style.font-style]="condicion ? 'true-value' : 'false-value'">
        Random text
    </p>
```

Por ejemplo

```HTML
    <p #text [style.font-style]="condicion ? 'bold' : 'normal'">
        Random text
    </p>
```

## NgClass & NgStyle

Nos permite agregar *varias* clases y/o estilos *de forma dinamica.*

- NgClass

```HTML
    <p #text class='simple-text' [ngClass]="{
        'class-name-1': condition1,
        'class-name-2': condition2
    }">
        Random text
    </p>
    <!--por ejemplo-->
    <p #text class='simple-text' [ngClass]="{
        'valid-class': input.lenght > 0,
        'invalid-class': input.lenght == 0
    }">
        Random text
    </p>

```

- NgStyle

```HTML
    <p #text class='simple-text' [ngStyle]="{
        'color': pStyles.color,
        'background': pStyles.background
    }">
        Random text
    </p>
```

En este ejemplo, *pStyles* es un objeto declarado en el TS del componente.

## Creacion de un formulario desde HTML

```HTML

<!-- Aqui se declara que es un formulario 'reactivo'.
Esto nos sirve para comprobar que todos los campos esten completados -->
<form #myForm="ngForm">
    <input name="name" type="text">
    <input name="lastname" type="text">
    <input name="password" type="password">

    <button 
        type="submit" 
        [disabled]=myForm.invalid>
        Enviar
    </button>
</form>

```

## Datos interesantes sobre Estilos

- *40em* es una ancho estandar para tablets en adelante. A utilizarlo en las *@media queries*
- *62em* parece un ancho estandar para desktops. Tambien para las *@media queries*

## Compilar nuestra aplicacion para producccion

`ng build`
