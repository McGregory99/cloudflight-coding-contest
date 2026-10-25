

def leer_lineas_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        primera_linea = archivo.readline().strip()
        lineas_restantes = archivo.readlines()
    return primera_linea, lineas_restantes

# Ejemplo de uso
ruta = 'level1/data/level1-2/level1_example.in'
n_cases, lineas_restantes = leer_lineas_archivo(ruta)

print("N_cases:", n_cases)
for linea in lineas_restantes:
    x, y = linea.split(" ")
    print(f"x: {x}, y: {y}")

