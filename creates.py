import mariadb

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Password123!',
    'database': 'recommender'
}


# connection for MariaDB
conn = mariadb.connect(**config)
# create a connection cursor
cur = conn.cursor()
cur.execute("USE recommender;")

cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS features;")

cur.execute("CREATE TABLE users(userid VARCHAR(100), username VARCHAR(100), access_token VARCHAR(100), playlistid VARCHAR(100), PRIMARY KEY (userid));")
cur.execute("CREATE TABLE features(songid VARCHAR(100), genre VARCHAR(100), vector VARCHAR(100), trendy DATETIME, PRIMARY KEY (songid));")
