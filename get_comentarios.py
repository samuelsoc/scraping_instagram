import instaloader
import pandas as pd

# crear instancia
L = instaloader.Instaloader()

# Login or load session
USERNAME =  'laura_duartemartin'#cuenta usuario
PASSWORD =   'Bots2020'#password usuario
L.login(USERNAME, PASSWORD)


idpost='CT0QjT_suhm'

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
        user.append(comment.owner)
        fecha.append(comment.created_at_utc)


df = pd.DataFrame({'usuario':user,
                   'comentario':comments_from_loop_including_answers,
                   'fecha':fecha,
                   'idpost':idpost})


print(df)
df.to_csv(f'comentarios_post_{idpost}.csv')