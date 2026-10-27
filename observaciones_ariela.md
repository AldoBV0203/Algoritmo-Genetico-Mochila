# Observaciones de las pruebas del algoritmo genético

**Responsable:** Ariela Hernández Zermeño

## Objetivo

Comprobar el funcionamiento del algoritmo genético para el problema de la mochila mediante tres pruebas, modificando el tamaño de la población y el número de generaciones.

## Prueba 1. Configuración original

- Población: 20 individuos.
- Generaciones: 40.
- Mejor valor obtenido: 40.
- Peso obtenido: 15.
- Tiempo de ejecución: 0.07821 segundos.
- Diferencia con el valor óptimo: 0.

## Prueba 2. Población reducida

- Población: 10 individuos.
- Generaciones: 40.
- Mejor valor obtenido: 40.
- Peso obtenido: 15.
- Tiempo de ejecución: 0.01843 segundos.
- Diferencia con el valor óptimo: 0.

## Prueba 3. Más generaciones

- Población: 20 individuos.
- Generaciones: 100.
- Mejor valor obtenido: 40.
- Peso obtenido: 15.
- Tiempo de ejecución: 0.16240 segundos.
- Diferencia con el valor óptimo: 0.

## Conclusión

Al realizar las tres pruebas observé que el algoritmo genético encontró el mismo valor óptimo de 40 en todas las configuraciones, sin superar la capacidad máxima de la mochila. También pude observar que la prueba con menor población tuvo el tiempo de ejecución más corto, mientras que al aumentar las generaciones el programa tardó más. Con esta actividad comprobé que el algoritmo funciona correctamente con las configuraciones utilizadas y que cambiar sus parámetros puede influir en el tiempo de ejecución.