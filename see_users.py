import mariadb
from db_utils import get_users, get_config

conn = mariadb.connect(**get_config())
cur = conn.cursor()
cur.execute("USE recommender;")

users = get_users(cur)

conn.close()

if users is not None:
    for user in users:
        print(user)
else:
    print('There are no users!')