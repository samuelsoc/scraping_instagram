#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuelrg

Instalar libreria instaloader:
pip3 install --upgrade instaloader

Con este script recolectamos los followings de varias cuentas
"""


# librerias
import instaloader
import time
from time import sleep
import random
import pandas as pd
from datetime import datetime
import sys
import os
from tqdm import tqdm


# crear instancia
L = instaloader.Instaloader()

# Login or load session
USERNAME =  '' #Escribir  usuario de IG
PASSWORD =  '' #Escribir contraaseña de IG
L.login(USERNAME, PASSWORD)


# crea carpeta nueva dentro del directorio para ir descarcango los resultados
ruta = os.getcwd()
nuevacarpeta = ruta + '/FOLLOWINGS'
os.mkdir(nuevacarpeta)

# cuenta a scrapear
usuarios = pd.read_csv('/ruta/archivo_muestra.csv')

# verificar el nombre de la columna que tiene las cuentas que seran scrapeadas
users = usuarios['usuario']
CUENTAS =  users.to_list()


# contador para controlar la cantidad de scrapeada
contador1 = 0
contador2 = 0
i = 1
data = []

# variable tiempo inicio recoleccion
starttime = time.ctime()

# parametros rango segundos de espera, para timeDelay
# timeDelay1 segundos entre cada extraccion
min1 = 2
max1 = 6
# timeDelay2 espera al llegar al descanso1
min2 = 15
max2 = 25
# timeDelay3 al llegar descanso2
min3 = 35
max3 = 45

# valores limites descansos
# si se cambian estos valores deben ser multiplos

descanso1 = 1000
descanso2 = 10000

# iterador sobre cada followers de la cuenta

for cuenta in tqdm(CUENTAS):
    try:
        print ("Inicio Recolección: %s" % time.ctime())
        print ("Cuenta:",cuenta)
        profile = instaloader.Profile.from_username(L.context, cuenta)
        for followee in profile.get_followees():
            timeDelay1 = random.randrange(min1,max1)
            username = followee.username
            data.append(username)
            contador1 = contador1 + 1
            contador2 = contador2 + 1
            sleep(timeDelay1)

            if contador1 == descanso1:
               timeDelay2 = random.randrange(min2,max2)
               print ("Reseteo contador1 a las: %s" % time.ctime())
               print('Van: ',i,' cuentas recolectadas')
               contador = 0
               print('Durmiendo ',timeDelay2,' minutos...')
               sleep(timeDelay2 * 60) # segundos multiplicados
               print ("Recolectando otra vez a las: %s" % time.ctime())

               if contador2 == descanso2:
                  timeDelay3 = random.randrange(min3,max3)
                  print ("Reseteo contador2 a las: %s" % time.ctime())
                  print('Van: ',i,' cuentas recolectadas')
                  contador2 = 0
                  print('Durmiendo',timeDelay3,'minutos...')
                  sleep(timeDelay3 * 60) # valor random multiplicado por minuto
                  print ("Recolectando otra vez a las: %s" % time.ctime())

            i = i + 1
            datos = pd.DataFrame(data, columns=['followings'])
            datos.to_csv(nuevacarpeta +'/' + cuenta + '.csv')
            data = []

    except Exception as error:
           print("No existe:", cuenta)


print("Inicio Recolección: %s" % starttime)
print("Fin Recolección: %s" % time.ctime())
print('Con',i,'cuentas recolectadas')
print('Archivos descargados en: ', nuevacarpeta)
