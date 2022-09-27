import math
from re import A
import numpy as np
import random

#Based on Sheldon Ross, Simulation, 5th Edition.
#Referencia: Miniproyecto 4 ambos grupos
"""
Universidad del Valle de Guatemala
Bryann Alfaro 19372
Diego Arredondo 19422
Raul Jimenez
Donaldo Garcia
Oscar Saravia

Proyecto 1
"""

#Servidores
capacity_supermarket = 10
clients_per_second_super = 6000/60
checkout_amount_super = 15

#Se utiliza distribucion Poisson para llegadas
def poisson_generation(t , lambda_value):
    u = random.random()
    return t - (1/lambda_value) * math.log(u)

#Inicializacion de variables
t = na = nd = n = 0
T0 = poisson_generation(t, clients_per_second_super)
ta = T0
arrival_time = {}
departure_time = {}

#Variable para almacenar el tiempo ocupado
occupied_time_list = []
#Fill occupied_time
for i in range(checkout_amount_super):
    occupied_time_list.append(0)


td = math.inf

#Customers en un servidor especifico
system_customers_servers = np.zeros(checkout_amount_super)

#Cantidad de clientes servidos por servidor
served_customers_servers = np.zeros(checkout_amount_super)

#Completition time by server
completition_time_departures = []
#Fill array with inf
for i in range(checkout_amount_super):
    completition_time_departures.append(math.inf)

#Tiempos en cola por cliente
queue_time = {}

#Fill queue_time with every server.
for i in range(checkout_amount_super):
    queue_time[i] = {}

#Salidas de cola por cliente
queue_departures = {}

#Fill queue_departures with every server.
for i in range(checkout_amount_super):
    queue_departures[i] = {}

T = 10 #Una hora de ejecucion
while t <= T or n>0:
    #Caso 1
    if ta <= min(completition_time_departures) and ta <= T:

        #Movernos en el tiempo
        t = ta
        na += 1
        n += 1
        ta = poisson_generation(t, clients_per_second_super) #Se genera la proxima llegada

        #Verificar en cada servidor cual esta libre
        flag = False
        for i in range(checkout_amount_super):
            if system_customers_servers[i] == 0:
                system_customers_servers[i] = na

                #Generar tiempo de servicio
                Y = random.expovariate(capacity_supermarket)
                completition_time_departures[i] = t + Y
                occupied_time_list[i] += Y
                flag = True
                break

        if flag == False:
            #Si no hay servidores libres
            #Se encola el cliente en el servidor con menor numero de clientes en cola
            #si hay empate, se hace random.
            min_queue = 0
            min_queue_size = len(queue_time[0])
            for i in range(checkout_amount_super):
                if len(queue_time[i]) < min_queue_size:
                    min_queue = i
                    min_queue_size = len(queue_time[i])
                if len(queue_time[i]) == min_queue_size:
                    if random.randint(0,1) == 1:
                        min_queue = i
                        min_queue_size = len(queue_time[i])
                    else:
                        continue

            #Se encola el cliente
            queue_time[min_queue][na] = t

    #Caso 2
    else:
        #Obtener el indice que tiene el minimo valor de la siguiente salida
        index = completition_time_departures.index(min(completition_time_departures))

        #Movernos en el tiempo
        t = completition_time_departures[index]
        nd += 1
        n -= 1

        #Se aumenta la cantidad de clientes servidos por este servidor (index)
        served_customers_servers[index] += 1

        #Guardar la salida
        departure_time[nd] = t

        #Verificar si hay clientes en cola
        if n >= checkout_amount_super:
            m_val = max(system_customers_servers)
            system_customers_servers[index] = m_val + 1

            #Generar tiempo de servicio
            Y = random.expovariate(capacity_supermarket)
            completition_time_departures[index] = t + Y
            occupied_time_list[index] += Y

            #Search for server of nd
            for i in range(checkout_amount_super):
                if nd in queue_time[i].keys():
                    queue_departures[i][nd] = t
                    break
        else:
            #Search for server of nd
            for i in range(checkout_amount_super):
                if nd in queue_time[i].keys():
                    queue_departures[i][nd] = t
                    break
            completition_time_departures[index] = math.inf
            system_customers_servers[index] = 0

#Cuestionamientos

#Tarea 1 Calcule el tiempo promedio de un cliente en cola (tiempo de espera)
total_global = 0

for i in range(checkout_amount_super):

    value_total = 0

    for j in queue_time[i]:
        value_total += (queue_departures[i][j] - queue_time[i][j])
    print('Tiempo total de solicitudes en cola del servidor', i+1, '> ',value_total)

    average_queue = 0
    if len(queue_time[i]) == 0:
        average_queue = 0
    else:
        average_queue = value_total / len(queue_time[i])

    print('Tiempo promedio de solicitudes en cola del servidor', i+1, '> ',average_queue,'\n')


# Tarea 2 Calcule el número de cliente en la cola

for i in range(checkout_amount_super):
    print('Cantidad de solicitudes en cola del servidor', i+1, '> ',len(queue_time[i]))

#Tarea 3 Para este punto considere los clientes atendidos por cada cajero dividido el número de clientes
#total
for i in range(checkout_amount_super):
    print('Porcentaje de solicitudes atendidas por el servidor', i+1, '> ',(served_customers_servers[i]/na)*100,'%')