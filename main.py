import pandas as pd
import math
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
tabla1_path = os.path.join(current_dir, "data", "Distancias sin h(n).csv")
tabla2_path = os.path.join(current_dir, "data", "Distancias DLR.csv") #CVS de los Destinos 

# Cargar los datos desde los archivos CSV
tabla1 = pd.read_csv(tabla1_path)
tabla2 = pd.read_csv(tabla2_path)

# Convertir el tiempo recorrido a minutos para facilitar los cálculos
def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

tabla1['TiempoRecorridoMin'] = tabla1['TiempoRecorrido'].apply(time_to_minutes)

# Función heurística para A*
def heuristic_cost_estimate(node, goal):
    dlr = tabla2[(tabla2['Origen'] == node) & (tabla2['Destino'] == goal)]['DLR']
    if len(dlr) > 0:
        return dlr.values[0]
    else:
        return math.inf

# Implementación del algoritmo A*
def a_star(start, goal):
    open_set = set([start])
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, goal)}
    came_from = {}
    time_score = {start: 0}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, math.inf))

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal], time_score[goal]

        open_set.remove(current)
        closed_set.add(current)

        for idx, row in tabla1[tabla1['Origen'] == current].iterrows():
            neighbor = row['Destino']
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + row['g(n)']
            tentative_time_score = time_score[current] + row['TiempoRecorridoMin']

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score.get(neighbor, math.inf):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            time_score[neighbor] = tentative_time_score
            f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal)

    return None, None, None

# Convertir minutos a horas y minutos para mostrar el tiempo
def minutes_to_time(minutes):
    h = minutes // 60
    m = minutes % 60
    return f"{h}:{m:02d}"

# Ejemplo de uso
def inicio():
  start = input('Origen: ')
  start = start.title()
  goal = input('Destino: ')
  goal = goal.title()
  path, distance, time = a_star(start, goal)

  if path:
      print("Ruta óptima:", path)
      print("Distancia a recorrer:", distance)
      print("Tiempo estimado:", minutes_to_time(time))
      con = input('Desea continuar (s/n): ')
      if(con == 's'):
        inicio()
  else:
      print("No se encontró una ruta válida.")
      inicio()

if __name__ == '__main__':
    inicio()
