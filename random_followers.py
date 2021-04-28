"""
autor: samuelrg

1. Este codigo toma el archivo con la extraccion de followers.
2. Genera un muestreo tomando en cuenta el total de followers recolectados
3. Al muestreo les scrapea sus perfiles
4. De todos los perfiles deja solo los publicos con menos de 5K followings
5. Guarda un archivo final con los followers publicos para aplciar extraccion
 de followings
6. No es necesario logearse con una cuenta fake 
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
import os
# crear instancia
L = instaloader.Instaloader()

print('cargando archivo')

namefile = 'followers_muletdechile.csv'
nombrefinal = 'pub_mulet.csv' # archivo final con los perfiles publicos, usar para extraccion de followings

folder = os.getcwd() # carpeta donde esta el archivo con todos los followers
ruta = os.path.join(folder,namefile) # ruta completa del archivo con followers
ruta
# lectura archivo con los followers
dt_follow = pd.read_csv(ruta, index_col=0)
# semilla estabiliza random al repetir
random.seed(21)
# largo  df
maxlen= len(dt_follow)

print('Realizando muestreo')

# controlar el amaño de la muestra cuando hay menos de 3k followers
if maxlen >= 1500 & maxlen <= 3000:
    muestra_followers = 1500
    sample_followers = dt_follow.sample(muestra_followers)
    print('Tamaño muestra:{}'.format(muestra_followers))
elif maxlen > 3000:
    muestra_followers = 2500
    sample_followers = dt_follow.sample(muestra_followers)
    print('Tamaño muestra:{}'.format(muestra_followers))

# extraer muestra de followers
# df con la muestra de followers
len(sample_followers)

# lista con las cuentas obtenidas del muestreo, para extraer metadata perfiles
listacuentas = sample_followers['followers'] #[2697:maxlen]
print('########## Iniciando Extraccion Perfiles #########')
print ("Inicio Recolección: %s" % time.ctime())

# parametros rango segundos de espera, para delaySleep
# tiene un rango entre 5 y 20 segundos de espera random por cada iteracion
min = 2
max = 8
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


       sleep(delaySleep)

    except Exception as error:
           print("No existe:", cuenta)

print('########## Extracción Finalizada ########')
print ("Fin Recolección: %s" % time.ctime())
print("---------------------------------------------------")

print("Filtrando perfiles publicos")
# filtro para dejar solo perfiles publicos
df_pub = metadata[metadata['privada']==False]
# filtro dejar solo cuentas con menos de 5k followings
df_pub=df_pub[df_pub['followings']<5000]
print("Publicos con menos de 5k followings:{}".format(len(df_pub)))
#tamaño muestra perfiles publicaciones
if len(df_pub) >= 500:
    muestra_perfiles = 500
    print("Tamaño muestra perfiles:{}".format(muestra_perfiles))
elif len(df_pub) <= 500:
    muestra_perfiles = len(df_pub)
    print("Tamaño muestra perfiles:{}".format(muestra_perfiles))
else:
    print("No se cumplen todos los criterios")

# tamaño muestra
data_pub = df_pub.sample(muestra_perfiles)
# guardar perfiles publicos
archivofinal = os.path.join(folder,nombrefinal)

data_pub.to_csv(archivofinal)
print("Archivo guardado en: {}".format(archivofinal))
