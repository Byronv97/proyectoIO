# Sistema de Optimización de Producción

Aplicacion web educativa para demostrar programacion lineal mediante el metodo grafico.

## Alcance

La aplicacion trabaja con dos variables de decision y hasta tres restricciones de tipo menor o igual. Calcula las intersecciones de las fronteras, conserva los puntos factibles, evalua la funcion objetivo en cada vertice y muestra la region factible.

El caso inicial corresponde a la produccion semanal de dos productos:

- `x`: lotes de galletas.
- `y`: lotes de cupcakes.

Con los valores precargados, la solucion esperada es:

- `x = 15` lotes de galletas.
- `y = 30` lotes de cupcakes.
- Margen maximo: `Q2,100`.
- Holgura de mano de obra: `15` horas.

## Ejecucion local

Requiere Python 3.11 o una version posterior soportada por Streamlit.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

La aplicacion se abrira en la direccion local que indique Streamlit.

## Pruebas del calculo

```powershell
python -m unittest -v
```

## Despliegue en Streamlit Community Cloud

1. Crear un repositorio en GitHub y subir `app.py`, `lp_solver.py`, `requirements.txt` y `README.md`.
2. Iniciar sesion en Streamlit Community Cloud con GitHub.
3. Seleccionar el repositorio y el archivo `app.py` como punto de entrada.
4. Publicar la aplicacion.
5. Compartir la URL `*.streamlit.app` con el docente.

## Relacion con el proyecto

La aplicacion es el complemento practico del informe. La explicacion academica debe incluir las variables, la funcion objetivo, las restricciones, la region factible, los vertices y la interpretacion de la solucion. Dulce Trigo es el caso de estudio utilizado por el sistema.

## Informe

El borrador del informe académico se encuentra en `PROJECT_DRAFT.md`. Incluye el planteamiento, la formulación matemática, la solución, la evaluación, el cronograma y las respuestas a los cuestionamientos del proyecto.
