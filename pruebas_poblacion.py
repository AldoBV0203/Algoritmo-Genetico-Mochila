# Pruebas de población y generaciones
# Actividad de Ariela Hernández Zermeño

import csv
import json
from pathlib import Path

from algoritmo_genetico import (
    CAPACIDAD,
    aptitud,
    ejecutar,
    fuerza_bruta,
    peso_y_valor,
)

# Ubicacion de los archivos del proyecto
carpeta = Path(__file__).resolve().parent

# Leer la configuracion original
with open(carpeta / "config.json", "r", encoding="utf-8") as archivo:
    configuracion = json.load(archivo)

# Configuraciones que se van a probar
pruebas = [
    ("Original", 20, 40),
    ("Poblacion_reducida", 10, 40),
    ("Mas_generaciones", 20, 100),
]

# Obtener el valor optimo para comparar
solucion_optima = fuerza_bruta()
valor_optimo = aptitud(solucion_optima)

resultados = []

print("PRUEBAS DEL ALGORITMO GENETICO")
print("Responsable: Ariela Hernandez Zermeno")
print("-----------------------------------")

# Ejecutar cada prueba
for nombre, poblacion, generaciones in pruebas:

    config = configuracion.copy()

    config["tamano_poblacion"] = poblacion
    config["generaciones"] = generaciones

    mejor, historial, tiempo, primera = ejecutar(config)

    peso, valor = peso_y_valor(mejor)

    # Verificar que la solucion sea valida
    if peso <= CAPACIDAD:
        estado = "Valida"
    else:
        estado = "No valida"

    assert peso <= CAPACIDAD, "La mochila excede la capacidad"
    assert len(historial) == generaciones + 1

    diferencia = valor_optimo - aptitud(mejor)

    # Mostrar resultados en pantalla
    print("\nPrueba:", nombre)
    print("Poblacion:", poblacion)
    print("Generaciones:", generaciones)
    print("Semilla:", config["semilla"])
    print("Peso:", peso)
    print("Capacidad:", CAPACIDAD)
    print("Mejor valor:", valor)
    print("Valor optimo:", valor_optimo)
    print("Diferencia con el optimo:", diferencia)
    print("Estado:", estado)
    print("Tiempo:", round(tiempo, 5), "segundos")

    # Guardar los datos de la prueba
    resultados.append({
        "prueba": nombre,
        "poblacion": poblacion,
        "generaciones": generaciones,
        "semilla": config["semilla"],
        "peso": peso,
        "capacidad": CAPACIDAD,
        "mejor_valor": valor,
        "valor_optimo": valor_optimo,
        "diferencia": diferencia,
        "estado": estado,
        "tiempo_segundos": round(tiempo, 5)
    })

# Guardar los resultados en un archivo CSV
ruta = carpeta / "resultados_ariela.csv"

with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.DictWriter(
        archivo,
        fieldnames=resultados[0].keys()
    )

    escritor.writeheader()
    escritor.writerows(resultados)

print("\nTodas las pruebas terminaron correctamente.")
print("Archivo generado: resultados_ariela.csv")