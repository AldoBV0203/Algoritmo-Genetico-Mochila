
import json
import random
import time
from itertools import product

import matplotlib.pyplot as plt


# Diez objetos: (nombre, peso, valor).
OBJETOS = [
    ("Agua", 2, 6),
    ("Comida", 3, 8),
    ("Botiquín", 4, 11),
    ("Linterna", 2, 6),
    ("Batería", 3, 7),
    ("Radio", 4, 9),
    ("Ropa", 5, 12),
    ("Herramientas", 6, 14),
    ("Manta", 3, 6),
    ("Cuerda", 2, 5),
]
CAPACIDAD = 15


def peso_y_valor(individuo):
    #Calcula peso y valor de una solución binaria.
    peso = sum(bit * obj[1] for bit, obj in zip(individuo, OBJETOS))
    valor = sum(bit * obj[2] for bit, obj in zip(individuo, OBJETOS))
    return peso, valor


def aptitud(individuo):
    #Soluciones que exceden la capacidad reciben aptitud cero.
    peso, valor = peso_y_valor(individuo)
    return valor if peso <= CAPACIDAD else 0


def crear_individuo():
    #Crea una posible solución con 10 bits aleatorios.
    return [random.randint(0, 1) for _ in OBJETOS]


def seleccion_ruleta(poblacion):
    #Elige un padre; más aptitud implica más probabilidad.
    pesos = [aptitud(individuo) for individuo in poblacion]
    if sum(pesos) == 0:
        return random.choice(poblacion)[:]
    return random.choices(poblacion, weights=pesos, k=1)[0][:]


def cruzar(padre1, padre2, probabilidad):
    #Cruce en un punto, con probabilidad configurable.
    if random.random() < probabilidad:
        punto = random.randint(1, len(OBJETOS) - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1[:], padre2[:]


def mutar(individuo, probabilidad):
    #Invierte cada bit con la probabilidad indicada.
    for i in range(len(individuo)):
        if random.random() < probabilidad:
            individuo[i] = 1 - individuo[i]
    return individuo


def ejecutar(config):
    #Devuelve la mejor solución, su historial y datos de ejecución.
    random.seed(config["semilla"])
    tamano = config["tamano_poblacion"]
    generaciones = config["generaciones"]
    prob_cruce = config["probabilidad_cruce"]
    prob_mutacion = config["probabilidad_mutacion"]

    if tamano < 2 or generaciones < 1:
        raise ValueError("La población debe ser >= 2 y las generaciones >= 1.")
    if not (0 <= prob_cruce <= 1 and 0 <= prob_mutacion <= 1):
        raise ValueError("Las probabilidades deben estar entre 0 y 1.")

    inicio = time.perf_counter()
    poblacion = [crear_individuo() for _ in range(tamano)]
    mejor = max(poblacion, key=aptitud)[:]
    historial = [aptitud(mejor)]  # Generación 0: población inicial.

    for _ in range(generaciones):
        # Elitismo: conservamos el mejor individuo de la generación anterior.
        nueva_poblacion = [mejor[:]]
        while len(nueva_poblacion) < tamano:
            padre1 = seleccion_ruleta(poblacion)
            padre2 = seleccion_ruleta(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2, prob_cruce)
            nueva_poblacion.append(mutar(hijo1, prob_mutacion))
            if len(nueva_poblacion) < tamano:
                nueva_poblacion.append(mutar(hijo2, prob_mutacion))
        poblacion = nueva_poblacion
        mejor_generacion = max(poblacion, key=aptitud)
        if aptitud(mejor_generacion) > aptitud(mejor):
            mejor = mejor_generacion[:]
        historial.append(aptitud(mejor))

    tiempo = time.perf_counter() - inicio
    # Con elitismo, historial es no decreciente. Esta es la primera vez
    # que se alcanzó el mejor valor final, no una prueba de convergencia global.
    primera_generacion_mejor_final = historial.index(historial[-1])
    return mejor, historial, tiempo, primera_generacion_mejor_final


def fuerza_bruta():
    #Busca la mejor solución exacta entre las 2^10 combinaciones.
    posibilidades = product([0, 1], repeat=len(OBJETOS))
    return list(max(posibilidades, key=aptitud))


def guardar_grafica(historial):
    plt.figure(figsize=(8, 4.5))
    plt.plot(range(len(historial)), historial, marker="o", markersize=2)
    plt.xlabel("Generación")
    plt.ylabel("Mejor aptitud acumulada")
    plt.title("Convergencia del algoritmo genético")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("convergencia.png", dpi=180)
    plt.close()


def main():
    with open("config.json", "r", encoding="utf-8") as archivo:
        config = json.load(archivo)

    mejor, historial, tiempo, primera = ejecutar(config)
    exacto = fuerza_bruta()
    peso, valor = peso_y_valor(mejor)

    print("\n=== ALGORITMO GENÉTICO: PROBLEMA DE LA MOCHILA ===")
    print("Semilla:", config["semilla"])
    print("Generaciones:", config["generaciones"])
    print("Mejor cromosoma:", "".join(map(str, mejor)))
    print("Objetos seleccionados:", ", ".join(
        obj[0] for bit, obj in zip(mejor, OBJETOS) if bit
    ) or "Ninguno")
    print("Peso:", peso, "/", CAPACIDAD)
    print("Valor / aptitud:", valor)
    print("Primera generación con el mejor valor final:", primera)
    print("Tiempo de ejecución (sin gráfica):", f"{tiempo:.5f}", "segundos")
    print("Valor óptimo por fuerza bruta:", aptitud(exacto))
    print("Diferencia con el óptimo:", aptitud(exacto) - aptitud(mejor))

    guardar_grafica(historial)
    print("Gráfica guardada como: convergencia.png")


if __name__ == "__main__":
    main()
