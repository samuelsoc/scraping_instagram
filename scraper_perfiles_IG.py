#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuelrg
"""

#scraper_IG

# librerias
import instaloader
import time
from time import sleep
import random
import pandas as pd
from datetime import datetime
import sys




# crear instancia
L = instaloader.Instaloader()

# Login or load session
USERNAME =  'samuelrg.sna'#'literaturaemprende'#'chileentuojo'#'freedata_univ'#cuenta usuario
PASSWORD =   'mU9drgY9eZGBR5B'#'89648685rr'#'89648685ee'#'.-_qJA$m2rZh57+'#password usuario
L.login(USERNAME, PASSWORD)

# traer lista de usuarios
# editar nombrearchivo con el nombre del archivo
data = pd.read_csv('~/scrapIG/meta_followings_connie/ig_user_5.csv', sep =' ')
# editar nombre de la columna que tine los usuarios
user_list = data['cuentas']
maxlen = len(user_list)


# crar nombre del archivo
nombrearchivo = 'listaMuna'


# lista con las cuentas a scrapear
listacuentas = user_list[601:maxlen]
#listacuentas
print('########## Iniciando Extraccion #########')
print ("Inicio Recolección: %s" % time.ctime())

# loops de extraccion
for cuenta in listacuentas:

    try:
       delaySleep = random.randrange(5,20)

       profile = instaloader.Profile.from_username(L.context, cuenta)

       username = profile.username
       followers = profile.followers
       followees = profile.followees

       meta = {'usuario': username,
            'followers':followers,
            'followings':followees}

       metadata = pd.DataFrame([meta])

       with open(nombrearchivo + '.csv', 'a') as f:
            metadata.to_csv(f, header=f.tell()==0)

       print(cuenta,'OK')
       sleep(delaySleep)

    except Exception as error:
           print("No existe:", cuenta)

print('########## Extracción Finalizada ########')
print ("Fin Recolección: %s" % time.ctime())
