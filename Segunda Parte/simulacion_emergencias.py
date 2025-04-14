import simpy
import random
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

# Parámetros
RANDOM_SEED = 10
SIM_TIME = 200

# Recursos
NUM_ENFERMERAS = 2
NUM_DOCTORES = 2
NUM_LABORATORIOS = 1
NUM_RAYOS_X = 1

# Métricas
tiempos_totales = []
esperas_triage = []
esperas_doctor = []
esperas_lab = []
esperas_rayos_x = []

def triage(env, paciente_id, enfermeras, doctor, laboratorio, rayos_x):
    llegada = env.now
    print(f"[{env.now:.1f}] Paciente {paciente_id} llega a la emergencia.")

    with enfermeras.request() as req:
        yield req
        yield env.timeout(10)
        severidad = random.randint(1, 5)
        print(f"[{env.now:.1f}] Paciente {paciente_id} triage completado con severidad {severidad}.")

    esperas_triage.append(env.now - llegada)

    with doctor.request(priority=severidad) as req_doc:
        yield req_doc
        yield env.timeout(15)
        print(f"[{env.now:.1f}] Paciente {paciente_id} atendido por doctor.")

    esperas_doctor.append(env.now - llegada)

    if severidad <= 2:
        with laboratorio.request(priority=severidad) as req_lab:
            yield req_lab
            yield env.timeout(20)
            print(f"[{env.now:.1f}] Paciente {paciente_id} pasó por laboratorio.")
        esperas_lab.append(env.now - llegada)

        with rayos_x.request(priority=severidad) as req_rx:
            yield req_rx
            yield env.timeout(25)
            print(f"[{env.now:.1f}] Paciente {paciente_id} pasó por Rayos X.")
        esperas_rayos_x.append(env.now - llegada)

    elif severidad == 3:
        if random.choice([True, False]):
            with laboratorio.request(priority=severidad) as req_lab:
                yield req_lab
                yield env.timeout(20)
                print(f"[{env.now:.1f}] Paciente {paciente_id} pasó por laboratorio.")
            esperas_lab.append(env.now - llegada)
        else:
            with rayos_x.request(priority=severidad) as req_rx:
                yield req_rx
                yield env.timeout(25)
                print(f"[{env.now:.1f}] Paciente {paciente_id} pasó por Rayos X.")
            esperas_rayos_x.append(env.now - llegada)

    print(f"[{env.now:.1f}] Paciente {paciente_id} sale del sistema.")
    tiempos_totales.append(env.now - llegada)

def generar_pacientes(env, enfermeras, doctor, laboratorio, rayos_x, tasa_llegada):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / tasa_llegada))
        env.process(triage(env, i, enfermeras, doctor, laboratorio, rayos_x))
        i += 1

def simular(tasa_llegada=6):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    enfermeras = simpy.Resource(env, capacity=NUM_ENFERMERAS)
    doctor = simpy.PriorityResource(env, capacity=NUM_DOCTORES)
    laboratorio = simpy.PriorityResource(env, capacity=NUM_LABORATORIOS)
    rayos_x = simpy.PriorityResource(env, capacity=NUM_RAYOS_X)
    env.process(generar_pacientes(env, enfermeras, doctor, laboratorio, rayos_x, tasa_llegada))
    env.run(until=SIM_TIME)

# Correr simulación
simular()

# Gráfica 1: Histograma del tiempo total
plt.figure(figsize=(10, 5))
plt.hist(tiempos_totales, bins=20, edgecolor='black')
plt.title("Distribución del tiempo total por paciente")
plt.xlabel("Minutos")
plt.ylabel("Pacientes")
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfica 2: Tiempo promedio por etapa
etapas = ['Triage', 'Doctor', 'Lab', 'Rayos X']
promedios = [
    sum(esperas_triage)/len(esperas_triage),
    sum(esperas_doctor)/len(esperas_doctor),
    sum(esperas_lab)/len(esperas_lab) if esperas_lab else 0,
    sum(esperas_rayos_x)/len(esperas_rayos_x) if esperas_rayos_x else 0,
]

plt.figure(figsize=(10, 5))
plt.bar(etapas, promedios, color='skyblue')
plt.title("Tiempo promedio de espera por etapa")
plt.ylabel("Minutos")
plt.grid(axis='y')
plt.tight_layout()
plt.show()
