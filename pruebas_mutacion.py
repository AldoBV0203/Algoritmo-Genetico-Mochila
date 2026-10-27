
# Pruebas de probabilidad de mutacion
import csv
import json
from pathlib import Path

from algoritmo_genetico import (
    CAPACIDAD, aptitud, ejecutar,
    fuerza_bruta, peso_y_valor
)

carpeta = Path(__file__).resolve().parent

with open(carpeta / "config.json", encoding="utf-8") as archivo:
    configuracion = json.load(archivo)

pruebas = [
    ("Mutacion 1%", 0.01),
    ("Mutacion 5%", 0.05),
    ("Mutacion 10%", 0.10)
]

valor_optimo = aptitud(fuerza_bruta())
resultados = []

print("PRUEBAS DE MUTACION")

for nombre, mutacion in pruebas:
    config = configuracion.copy()
    config["probabilidad_mutacion"] = mutacion

    mejor, historial, tiempo, primera = ejecutar(config)
    peso, valor = peso_y_valor(mejor)

    assert peso <= CAPACIDAD, "Se excedio la capacidad"
    assert len(historial) == config["generaciones"] + 1

    print("\nPrueba:", nombre)
    print("Peso:", peso)
    print("Mejor valor:", valor)
    print("Valor optimo:", valor_optimo)
    print("Tiempo:", round(tiempo, 5), "segundos")

    resultados.append({
        "prueba": nombre,
        "mutacion": mutacion,
        "peso": peso,
        "mejor_valor": valor,
        "valor_optimo": valor_optimo,
        "tiempo": round(tiempo, 5)
    })

with open(carpeta / "resultados_mutacion_cecilia.csv",
          "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.DictWriter(
        archivo, fieldnames=resultados[0].keys()
    )
    escritor.writeheader()
    escritor.writerows(resultados)

print("\nLas tres pruebas terminaron correctamente.")
