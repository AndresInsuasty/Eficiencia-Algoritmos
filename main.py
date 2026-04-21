import time
from algoritmos.numeros import es_par_impar

tiempo_inicio = time.time()

####################################
### función a evaluar
respuesta = es_par_impar()

####################################

tiempo_fin = time.time()
tiempo_ejecucion = tiempo_fin - tiempo_inicio



print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos = {tiempo_ejecucion * 1e6:.2f} microsegundos")  
print(f"El número es {respuesta}")