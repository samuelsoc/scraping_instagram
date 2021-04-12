#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuelrg

Instalar libreria instaloader:
pip3 install --upgrade instaloader
"""
# librerias necesarias
import instaloader
import time
from time import sleep
import random
import pandas as pd
from datetime import datetime
import sys
from tqdm import tqdm

# crear instancia
L = instaloader.Instaloader()

# traer lista de usuarios
# editar nombrearchivo con el nombre del archivo
# en caso de que sea un .txt
#data = pd.read_csv('archivomuestras.txt',sep =' ',names=['cuenta'])

data = pd.read_csv('nombrearchivo.csv')
# editar nombre de la columna que tiene los usuarios, de ser necesario
user_list = list(data['cuenta'])
# ultima posicion de la lista
maxlen = len(user_list)
# crear nombre del archivo
# la extension sera .csv
nombrearchivo = ''

# lista con las cuentas a scrapear
# como es una lista puedes seleccionar el rango especifico ej: user_list[601:maxlen]
listacuentas = user_list
print('########## Iniciando Extraccion #########')
print ("Inicio Recolección: %s" % time.ctime())

# parametros rango segundos de espera, para delaySleep
# tiene un rango entre 5 y 20 segundos de espera random por cada iteracion
min = 5
max = 15
# loops de extraccion
for cuenta in tqdm(listacuentas):

    try:
       delaySleep = random.randrange(min,max)

       profile = instaloader.Profile.from_username(L.context, cuenta)

       username = profile.username
       followers = profile.followers
       followees = profile.followees
       publi = profile.mediacount
       fullname = profile.full_name
       privada = profile.is_private

       meta = {'usuario': username,
            'followers':followers,
            'followings':followees,
            'publicaciones':publi,
            'fullname':fullname,
            'privada':privada }

       metadata = pd.DataFrame([meta])

       with open(nombrearchivo + '.csv', 'a') as f:
            metadata.to_csv(f, header=f.tell()==0)

       #print(cuenta,'OK')
       sleep(delaySleep)

    except Exception as error:
           print("No existe:", cuenta)

print('########## Extracción Finalizada ########')
print ("Fin Recolección: %s" % time.ctime())
