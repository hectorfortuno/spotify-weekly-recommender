import mariadb
from db_utils import get_config

# connection for MariaDB
conn = mariadb.connect(**get_config())
# create a connection cursor
cur = conn.cursor()
cur.execute("USE recommender;")

cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS features;")

cur.execute("CREATE TABLE users(userid VARCHAR(100), name VARCHAR(100), access_token VARCHAR(300), playlistid VARCHAR(100), PRIMARY KEY (userid));")
cur.execute("CREATE TABLE features(songid VARCHAR(100), features JSON, PRIMARY KEY (songid));")
