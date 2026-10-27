# Actividad 4. Pruebas del algoritmo genético

**Integrante:** Ponce Valle Xóchitl Kumary  
**Proyecto:** Algoritmo genético para el problema de la mochila

## Objetivo

Comparar los resultados del algoritmo genético al cambiar el tamaño de la población y las probabilidades de cruce y mutación.

## Pruebas realizadas

Para esta actividad ejecuté el programa `experimentos.py` en Visual Studio Code. Se probaron cuatro configuraciones y cada una se ejecutó cinco veces con las semillas 11, 22, 33, 44 y 55. En total fueron 20 ejecuciones de 40 generaciones cada una.

El programa registró la mejor aptitud encontrada, la generación en la que apareció por primera vez, el tiempo de ejecución y la diversidad al final de cada prueba. En este problema, el valor óptimo calculado por fuerza bruta es 40.

| Configuración | Población | Cruce | Mutación | Generaciones |
|---|---:|---:|---:|---:|
| A | 10 | 60% | 1% | 40 |
| B | 40 | 60% | 1% | 40 |
| C | 10 | 60% | 10% | 40 |
| D | 10 | 90% | 1% | 40 |

## Resultados obtenidos

| Configuración | Semilla | Mejor aptitud | Generación | Tiempo (s) | Diversidad final |
|---|---:|---:|---:|---:|---:|
| A | 11 | 40 | 13 | 0.01153 | 20.0% |
| A | 22 | 38 | 0 | 0.01336 | 20.0% |
| A | 33 | 38 | 0 | 0.01179 | 20.0% |
| A | 44 | 37 | 0 | 0.01097 | 20.0% |
| A | 55 | 37 | 6 | 0.01021 | 30.0% |
| B | 11 | 40 | 2 | 0.13796 | 12.5% |
| B | 22 | 40 | 1 | 0.13845 | 20.0% |
| B | 33 | 40 | 18 | 0.13638 | 27.5% |
| B | 44 | 39 | 3 | 0.14204 | 15.0% |
| B | 55 | 39 | 0 | 0.16349 | 22.5% |
| C | 11 | 39 | 40 | 0.01070 | 90.0% |
| C | 22 | 40 | 19 | 0.01488 | 100.0% |
| C | 33 | 39 | 6 | 0.01784 | 80.0% |
| C | 44 | 40 | 10 | 0.01445 | 80.0% |
| C | 55 | 39 | 1 | 0.01168 | 100.0% |
| D | 11 | 40 | 2 | 0.01179 | 20.0% |
| D | 22 | 39 | 3 | 0.01396 | 30.0% |
| D | 33 | 38 | 0 | 0.01193 | 20.0% |
| D | 44 | 38 | 10 | 0.01078 | 40.0% |
| D | 55 | 37 | 15 | 0.01237 | 50.0% |

En la siguiente tabla se muestran los promedios de las cinco pruebas de cada configuración. La desviación estándar indica qué tanto cambiaron las mejores aptitudes entre las ejecuciones.

| Configuración | Aptitud promedio | Desviación estándar | Veces que llegó a 40 | Tiempo promedio (s) | Diversidad promedio |
|---|---:|---:|---:|---:|---:|
| A | 38.00 | 1.23 | 1 de 5 | 0.01157 | 22.0% |
| B | 39.60 | 0.55 | 3 de 5 | 0.14366 | 19.5% |
| C | 39.40 | 0.55 | 2 de 5 | 0.01391 | 90.0% |
| D | 38.40 | 1.14 | 1 de 5 | 0.01217 | 32.0% |

## Observaciones

La configuración B fue la que obtuvo los mejores resultados, ya que tuvo un promedio de 39.60 y llegó al valor óptimo de 40 en tres de las cinco pruebas. Al aumentar la población de 10 a 40 individuos, el resultado fue mejor que en A, pero también tardó más en ejecutarse.

La configuración C tuvo una diversidad final promedio del 90%, mucho mayor que las demás. Esto ocurrió al utilizar una mutación del 10%. Aunque mantuvo más soluciones diferentes, solo encontró el valor óptimo en dos pruebas. Por otro lado, la configuración D aumentó el cruce al 90%, pero no logró superar los resultados de B ni de C.

También observé que algunas ejecuciones encontraron su mejor resultado desde la generación 0 y ya no mejoraron. Por ejemplo, esto pasó con A en las semillas 22, 33 y 44. Esto muestra un estancamiento del mejor valor durante esas pruebas, aunque no significa necesariamente que todos los individuos fueran iguales.

## Conclusión

Después de realizar las 20 ejecuciones, el algoritmo encontró el valor óptimo de 40 en siete ocasiones. En estas pruebas, la configuración B fue la que dio mejores resultados en promedio, mientras que C conservó mayor diversidad. Con esto pude observar que cambiar la población, el cruce y la mutación influye en los resultados, y que usar valores más altos no siempre significa obtener una mejor solución.