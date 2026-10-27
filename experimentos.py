"""Actividad 4: experimentos reproducibles con el algoritmo genético de mochila.

Colocar este archivo junto a algoritmo_genetico.py y ejecutar:
    python experimentos.py
"""

import csv
import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from algoritmo_genetico import (
    aptitud,
    crear_individuo,
    cruzar,
    fuerza_bruta,
    mutar,
    seleccion_ruleta,
)

# En cada pareja solo se modifica un parámetro respecto de A.
CONFIGURACIONES = [
    ("A", 10, 0.60, 0.01),
    ("B", 40, 0.60, 0.01),
    ("C", 10, 0.60, 0.10),
    ("D", 10, 0.90, 0.01),
]
SEMILLAS = [11, 22, 33, 44, 55]
GENERACIONES = 40
CARPETA = Path(__file__).resolve().parent


def ejecutar_experimento(tamano, prob_cruce, prob_mutacion, semilla):
    """Mismo algoritmo de la Actividad 3, registrando además diversidad."""
    random.seed(semilla)
    inicio = time.perf_counter()
    poblacion = [crear_individuo() for _ in range(tamano)]
    mejor = max(poblacion, key=aptitud)[:]
    historial = [aptitud(mejor)]
    diversidades = [len({tuple(i) for i in poblacion}) / tamano]

    for _ in range(GENERACIONES):
        nueva = [mejor[:]]  # Elitismo
        while len(nueva) < tamano:
            padre1 = seleccion_ruleta(poblacion)
            padre2 = seleccion_ruleta(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2, prob_cruce)
            nueva.append(mutar(hijo1, prob_mutacion))
            if len(nueva) < tamano:
                nueva.append(mutar(hijo2, prob_mutacion))
        poblacion = nueva
        mejor_de_generacion = max(poblacion, key=aptitud)
        if aptitud(mejor_de_generacion) > aptitud(mejor):
            mejor = mejor_de_generacion[:]
        historial.append(aptitud(mejor))
        diversidades.append(len({tuple(i) for i in poblacion}) / tamano)

    tiempo = time.perf_counter() - inicio  # No incluye generar las gráficas
    primera = historial.index(historial[-1])
    return {
        "aptitud": aptitud(mejor),
        "primera_generacion": primera,
        "meseta_final": GENERACIONES - primera,
        "tiempo_segundos": tiempo,
        "historial": historial,
        "diversidad_inicial": diversidades[0],
        "diversidad_final": diversidades[-1],
        "diversidades": diversidades,
    }


def guardar_csv(ruta, filas, columnas):
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    optimo = aptitud(fuerza_bruta())
    ejecuciones = []
    resumen = []
    historiales_por_config = {}

    print(f"Óptimo exacto (fuerza bruta): {optimo}")
    print("Config  Semilla  Mejor  Generación  Tiempo(s)  Diversidad final")
    for nombre, tamano, pc, pm in CONFIGURACIONES:
        resultados = []
        for semilla in SEMILLAS:
            r = ejecutar_experimento(tamano, pc, pm, semilla)
            resultados.append(r)
            ejecuciones.append({
                "configuracion": nombre,
                "semilla": semilla,
                "poblacion": tamano,
                "probabilidad_cruce": pc,
                "probabilidad_mutacion": pm,
                "generaciones": GENERACIONES,
                "mejor_aptitud": r["aptitud"],
                "primera_generacion_mejor_final": r["primera_generacion"],
                "generaciones_sin_mejora_al_final": r["meseta_final"],
                "tiempo_segundos": round(r["tiempo_segundos"], 6),
                "diversidad_inicial_porcentaje": round(100*r["diversidad_inicial"], 2),
                "diversidad_final_porcentaje": round(100*r["diversidad_final"], 2),
                "alcanzo_optimo": "Sí" if r["aptitud"] == optimo else "No",
            })
            print(f"{nombre:>4} {semilla:>8} {r['aptitud']:>6} "
                  f"{r['primera_generacion']:>10} "
                  f"{r['tiempo_segundos']:>10.5f} "
                  f"{r['diversidad_final']*100:>10.1f}%")

        valores = [r["aptitud"] for r in resultados]
        resumen.append({
            "configuracion": nombre,
            "poblacion": tamano,
            "probabilidad_cruce": pc,
            "probabilidad_mutacion": pm,
            "ejecuciones": len(resultados),
            "promedio_mejor_aptitud": round(statistics.mean(valores), 3),
            "desviacion_estandar_muestral": round(statistics.stdev(valores), 3),
            "mejor_valor": max(valores),
            "peor_valor": min(valores),
            "optimos_encontrados": sum(v == optimo for v in valores),
            "tiempo_promedio_segundos": round(statistics.mean(r["tiempo_segundos"] for r in resultados), 6),
            "diversidad_final_promedio_porcentaje": round(
                statistics.mean(r["diversidad_final"] for r in resultados) * 100, 2),
        })
        historiales_por_config[nombre] = [r["historial"] for r in resultados]

    guardar_csv(CARPETA / "resultados_20_ejecuciones.csv", ejecuciones, list(ejecuciones[0]))
    guardar_csv(CARPETA / "resumen_configuraciones.csv", resumen, list(resumen[0]))

    # Figura 1: aptitud media por configuración (barras de error = desviación estándar muestral).
    nombres = [r["configuracion"] for r in resumen]
    medias = [r["promedio_mejor_aptitud"] for r in resumen]
    desviaciones = [r["desviacion_estandar_muestral"] for r in resumen]
    plt.figure(figsize=(8, 4.5))
    plt.bar(nombres, medias, yerr=desviaciones, capsize=5)
    plt.ylim(0, max(medias)+5)
    plt.xlabel("Configuración")
    plt.ylabel("Mejor aptitud promedio")
    plt.title("Aptitud promedio de 5 ejecuciones por configuración")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(CARPETA / "comparacion_configuraciones.png", dpi=200)
    plt.close()

    # Figura 2: evolución media del mejor valor (promedio de cinco semillas).
    plt.figure(figsize=(8, 4.5))
    for nombre, historiales in historiales_por_config.items():
        promedio_generacion = [statistics.mean(r[i] for r in historiales)
                               for i in range(GENERACIONES + 1)]
        plt.plot(range(GENERACIONES + 1), promedio_generacion, label=f"Config. {nombre}")
    plt.xlabel("Generación")
    plt.ylabel("Mejor aptitud acumulada promedio")
    plt.title("Convergencia promedio por configuración")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(CARPETA / "convergencia_comparativa.png", dpi=200)
    plt.close()

    print("\nRESUMEN POR CONFIGURACIÓN")
    for r in resumen:
        print(f"{r['configuracion']}: media={r['promedio_mejor_aptitud']:.2f}, "
              f"s={r['desviacion_estandar_muestral']:.2f}, "
              f"óptimos={r['optimos_encontrados']}/5, "
              f"diversidad final={r['diversidad_final_promedio_porcentaje']:.1f}%")
    print("\nSe guardaron 2 archivos CSV y 2 gráficas PNG en esta carpeta.")
    print("Nota: la generación reportada es cuando se alcanza el mejor valor observado;")
    print("no demuestra por sí sola convergencia completa de la población.")


if __name__ == "__main__":
    main()
