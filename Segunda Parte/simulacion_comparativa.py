import simpy
import random
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt

# Parámetros base
RANDOM_SEED = 10
SIM_TIME = 100  # minutos simulados
NUM_ENFERMERAS = 2
NUM_DOCTORES = 2
NUM_LABORATORIOS = 1
NUM_RAYOS_X = 1

# Diccionario para guardar resultados por escenario
resultados_por_escenario = {}

# Función principal de cada paciente
def triage(env, paciente_id, enfermeras, doctor, laboratorio, rayos_x, tiempos_totales, escenario):
    llegada = env.now
    print(f"[{env.now:.1f}] ({escenario}) Paciente {paciente_id} llega.")

    with enfermeras.request() as req:
        yield req
        yield env.timeout(10)
        severidad = random.randint(1, 5)
        print(f"[{env.now:.1f}] ({escenario}) Paciente {paciente_id} evaluado con severidad {severidad}.")

    with doctor.request(priority=severidad) as req_doc:
        yield req_doc
        yield env.timeout(15)

    if severidad <= 2:
        with laboratorio.request(priority=severidad) as req_lab:
            yield req_lab
            yield env.timeout(20)

        with rayos_x.request(priority=severidad) as req_rx:
            yield req_rx
            yield env.timeout(25)

    elif severidad == 3:
        if random.choice([True, False]):
            with laboratorio.request(priority=severidad) as req_lab:
                yield req_lab
                yield env.timeout(20)
        else:
            with rayos_x.request(priority=severidad) as req_rx:
                yield req_rx
                yield env.timeout(25)

    salida = env.now
    print(f"[{env.now:.1f}] ({escenario}) Paciente {paciente_id} sale del sistema.")
    tiempos_totales.append(salida - llegada)

# Generador de pacientes
def generar_pacientes(env, enfermeras, doctor, laboratorio, rayos_x, tasa_llegada, tiempos_totales, escenario):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / tasa_llegada))
        env.process(triage(env, i, enfermeras, doctor, laboratorio, rayos_x, tiempos_totales, escenario))
        i += 1

# Simulación por escenario
def simular_escenario(nombre, tasa_llegada):
    print(f"\n=== Simulando: {nombre} ===\n")
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    enfermeras = simpy.Resource(env, capacity=NUM_ENFERMERAS)
    doctor = simpy.PriorityResource(env, capacity=NUM_DOCTORES)
    laboratorio = simpy.PriorityResource(env, capacity=NUM_LABORATORIOS)
    rayos_x = simpy.PriorityResource(env, capacity=NUM_RAYOS_X)

    tiempos = []
    env.process(generar_pacientes(env, enfermeras, doctor, laboratorio, rayos_x, tasa_llegada, tiempos, nombre))
    env.run(until=SIM_TIME)

    promedio = sum(tiempos) / len(tiempos) if tiempos else 0
    resultados_por_escenario[nombre] = {
        "tiempos": tiempos,
        "promedio": promedio
    }

# Ejecutar los 3 escenarios
simular_escenario("Día normal", tasa_llegada=6)
simular_escenario("Fin de semana", tasa_llegada=3.5)
simular_escenario("Feriado", tasa_llegada=2)

# Mostrar gráfica comparativa
nombres = list(resultados_por_escenario.keys())
promedios = [resultados_por_escenario[n]["promedio"] for n in nombres]

plt.figure(figsize=(9, 5))
plt.bar(nombres, promedios, color=["green", "orange", "red"])
plt.title("Comparación de tiempo promedio por paciente en diferentes días")
plt.ylabel("Minutos")
plt.grid(axis="y")
plt.tight_layout()
plt.show()
