# Aplicación de la programación lineal para optimizar la producción de Dulce Trigo

## 1. Introducción

La Investigación de Operaciones proporciona modelos matemáticos para apoyar la toma de decisiones cuando existen recursos limitados. Una de sus herramientas principales es la programación lineal, que permite determinar la mejor combinación de actividades cuando la relación entre los recursos y las decisiones puede expresarse mediante ecuaciones o desigualdades lineales.

Este proyecto presenta un caso de producción para la empresa Dulce Trigo. Se analizan dos productos y tres recursos limitados. El modelo se resuelve mediante el método gráfico y se acompaña con una aplicación web que permite modificar los datos y observar el efecto sobre la solución.

## 2. Planteamiento del problema

Dulce Trigo produce semanalmente lotes de galletas y cupcakes. Cada producto requiere una cantidad determinada de harina, mano de obra y capacidad de producción. La empresa necesita definir cuántos lotes de cada producto debe fabricar para obtener el mayor margen de contribución sin superar los recursos disponibles.

La decisión se representa con dos variables:

- `x`: lotes de galletas por semana.
- `y`: lotes de cupcakes por semana.

La pregunta central es:

> ¿Cuál es la combinación de lotes de galletas y cupcakes que maximiza el margen semanal de Dulce Trigo?

## 3. Justificación

Resolver el problema mediante programación lineal permite sustituir una decisión intuitiva por un procedimiento cuantitativo. El análisis identifica la combinación más conveniente, muestra qué recursos se utilizan por completo y determina qué capacidad permanece disponible.

La aplicación web facilita la demostración del modelo porque permite ingresar los valores, observar la región factible, revisar los puntos extremos y comprobar la solución óptima.

## 4. Objetivos

### 4.1 Objetivo general

Aplicar la programación lineal y el método gráfico para determinar la combinación de productos que maximiza el margen semanal de Dulce Trigo.

### 4.2 Objetivos específicos

1. Definir las variables de decisión del problema.
2. Identificar el margen y el consumo de recursos de cada producto.
3. Formular la función objetivo y las restricciones.
4. Representar gráficamente la región factible.
5. Evaluar los puntos extremos y seleccionar la solución óptima.
6. Desarrollar una aplicación web para demostrar el modelo y sus resultados.

## 5. Marco teórico

### 5.1 Investigación de Operaciones

La Investigación de Operaciones utiliza modelos matemáticos, datos y métodos analíticos para apoyar decisiones en sistemas que tienen objetivos y restricciones.

### 5.2 Programación lineal

La programación lineal busca maximizar o minimizar una función lineal sujeta a restricciones lineales y condiciones de no negatividad.

### 5.3 Elementos del modelo

- **Variables de decisión:** representan las cantidades que deben determinarse.
- **Función objetivo:** expresa el margen que se desea maximizar.
- **Restricciones:** representan los límites de los recursos.
- **Región factible:** conjunto de combinaciones que cumplen todas las restricciones.
- **Puntos extremos:** intersecciones que se evalúan para encontrar la solución óptima.
- **Holgura:** diferencia entre el recurso disponible y el recurso utilizado.

### 5.4 Método gráfico

El método gráfico permite resolver modelos de programación lineal con dos variables. Primero se representan las rectas de las restricciones, luego se identifica la región factible y finalmente se evalúa la función objetivo en sus puntos extremos.

## 6. Metodología

1. Definir los productos y las unidades de decisión.
2. Establecer el margen de contribución por lote.
3. Registrar el consumo de cada recurso por producto.
4. Formular la función objetivo y las restricciones.
5. Calcular las intersecciones de las rectas.
6. Verificar cuáles puntos cumplen todas las restricciones.
7. Evaluar el margen en cada punto extremo.
8. Interpretar la solución y el uso de los recursos.
9. Comprobar los cálculos mediante la aplicación web.

## 7. Datos del caso

| Recurso | Galletas `x` | Cupcakes `y` | Disponibilidad semanal |
|---|---:|---:|---:|
| Harina | 2 kg | 3 kg | 120 kg |
| Mano de obra | 3 horas | 2 horas | 120 horas |
| Capacidad de producción | 1 lote | 1 lote | 45 lotes |

| Producto | Margen por lote |
|---|---:|
| Galletas | Q40 |
| Cupcakes | Q50 |

## 8. Formulación del modelo

### 8.1 Función objetivo

\[
\text{Maximizar } Z = 40x + 50y
\]

### 8.2 Restricciones

Harina:

\[
2x + 3y \leq 120
\]

Mano de obra:

\[
3x + 2y \leq 120
\]

Capacidad:

\[
x + y \leq 45
\]

Condiciones de no negatividad:

\[
x \geq 0, \qquad y \geq 0
\]

## 9. Solución mediante el método gráfico

### 9.1 Interceptos

| Restricción | Intercepto en `x` | Intercepto en `y` |
|---|---:|---:|
| `2x + 3y = 120` | `(60, 0)` | `(0, 40)` |
| `3x + 2y = 120` | `(40, 0)` | `(0, 60)` |
| `x + y = 45` | `(45, 0)` | `(0, 45)` |

### 9.2 Puntos extremos factibles

| Punto | Cálculo del margen | Margen |
|---|---|---:|
| `(0, 0)` | `40(0) + 50(0)` | Q0 |
| `(40, 0)` | `40(40) + 50(0)` | Q1,600 |
| `(30, 15)` | `40(30) + 50(15)` | Q1,950 |
| `(15, 30)` | `40(15) + 50(30)` | **Q2,100** |
| `(0, 40)` | `40(0) + 50(40)` | Q2,000 |

La intersección entre las restricciones de harina y mano de obra es `(24, 24)`, pero no es factible porque `24 + 24 = 48` supera la capacidad máxima de 45 lotes.

## 10. Resultado óptimo

La combinación que produce el mayor margen es:

- `x = 15` lotes de galletas.
- `y = 30` lotes de cupcakes.

El margen máximo es:

\[
Z = 40(15) + 50(30) = Q2,100
\]

### Uso de recursos

| Recurso | Utilizado | Disponible | Holgura |
|---|---:|---:|---:|
| Harina | 120 kg | 120 kg | 0 kg |
| Mano de obra | 105 horas | 120 horas | 15 horas |
| Capacidad | 45 lotes | 45 lotes | 0 lotes |

La harina y la capacidad son recursos totalmente utilizados. La mano de obra conserva una holgura de 15 horas.

## 11. Aplicación web

La aplicación **Dulce Trigo Optimizer** fue desarrollada en Python con Streamlit. Su función es demostrar el modelo de forma interactiva.

La aplicación permite:

- Ingresar el margen de cada producto.
- Modificar el consumo de recursos.
- Modificar la disponibilidad.
- Generar el modelo matemático.
- Calcular las intersecciones.
- Separar los puntos factibles de los no factibles.
- Evaluar los puntos extremos.
- Mostrar la región factible.
- Presentar la solución óptima y las holguras.

El código fuente y las instrucciones de ejecución se encuentran en el repositorio del proyecto. La versión publicada se compartirá mediante una URL de Streamlit Community Cloud.

## 12. Evaluación de resultados

El modelo determina que la producción combinada de 15 lotes de galletas y 30 lotes de cupcakes es superior a las demás combinaciones evaluadas. La solución utiliza completamente la harina y la capacidad de producción, mientras que aún existe disponibilidad de mano de obra.

La aplicación permite modificar los valores para observar cómo cambia la región factible y verificar que la solución depende de los márgenes y de la disponibilidad de los recursos.

## 13. Conclusiones

1. La programación lineal permite representar la decisión de producción mediante variables, una función objetivo y restricciones.
2. El método gráfico permite identificar visualmente las combinaciones factibles y seleccionar el punto con mayor margen.
3. La solución óptima del caso es producir 15 lotes de galletas y 30 lotes de cupcakes.
4. El margen máximo obtenido es de Q2,100 por semana.
5. La harina y la capacidad de producción son los recursos limitantes del modelo.
6. La aplicación web facilita la comprobación y demostración del procedimiento.

## 14. Recomendaciones

1. Mantener la producción dentro de la combinación óptima mientras se conserven los mismos valores del modelo.
2. Evaluar primero un aumento de harina o capacidad, porque ambos recursos se utilizan completamente.
3. No asignar más mano de obra sin revisar antes si aumentan la demanda o los demás recursos.
4. Utilizar la aplicación para probar escenarios alternativos antes de modificar la planificación.

## 15. Video demostrativo

El video presentará, en este orden:

1. El problema de Dulce Trigo.
2. Las variables y los datos.
3. La función objetivo y las restricciones.
4. La aplicación web.
5. La solución gráfica.
6. Los puntos extremos y el margen de cada uno.
7. La solución óptima y el uso de los recursos.

## 16. Preguntas del proyecto

Esta sección se completará con las preguntas 11.1 a 11.10 en cuanto se incorpore su texto exacto.

## 17. Bibliografía

Se incorporarán los materiales de clase proporcionados para Investigación de Operaciones, programación lineal, método gráfico y método Simplex, utilizando los datos bibliográficos que aparecen en sus portadas.
