import instaloader
import pandas as pd
import time
from time import sleep
import random
import os

# crear instancia
L = instaloader.Instaloader()

# Login or load session
USERNAME =  ''#cuenta usuario
PASSWORD =   ''#password usuario
L.login(USERNAME, PASSWORD)


ruta = os.getcwd()+ '/comentariospost'
os.mkdir(ruta)

idpostt = pd.read_csv('listado_id_comentarios.csv')
idpostt =  idpostt['shortcode'].to_list()


def scrape_comentario(idpost):
    post = instaloader.Post.from_shortcode(L.context, idpost)
    comments_from_loop_including_answers = []
    user = []
    fecha = []
    
    for comment in post.get_comments():
        comments_from_loop_including_answers.append(comment.text)
        user.append(comment.owner)
        fecha.append(comment.created_at_utc)
        for answer in comment.answers:
            comments_from_loop_including_answers.append(answer.text)
            user.append(answer.owner)
            fecha.append(answer.created_at_utc)
            
    df = pd.DataFrame({'usuario':user,
                       'comentario':comments_from_loop_including_answers,
                       'fecha':fecha,
                       'idpost':idpost})

    print(df)
    df.to_csv(ruta +'/'+f'comentarios_post_{idpost}.csv')
    sleep(random.randrange(0,30))

 
for idpost in idpostt:
    print(idpost)
    scrape_comentario(idpost)