import instaloader
import time
from time import sleep
import random

L = instaloader.Instaloader()

posts = instaloader.Profile.from_username(L.context, "sebastiansichel").get_posts()


min1 = 2
max1 = 10

for post in posts:
    print(post)
    L.download_post(post,"sebastiansichel")
    timeDelay1 = random.randrange(min1,max1)
    sleep(timeDelay1)
