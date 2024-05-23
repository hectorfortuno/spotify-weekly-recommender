"""

"""
import mariadb

def get_config():
    """
    """

    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'Password123!',
        'database': 'recommender'
    }
    return config


def user_exists(cur, userid):
    """
    """

    cur.execute("SELECT COUNT(*) FROM users WHERE userid=?;",(userid,))
    result = cur.fetchone()

    return False if result[0] == 0 else True


def add_user(cur, userid, name, access_token, playlistid):
    """
    """

    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (userid, name, access_token, playlistid))


def delete_user(userid):
    """
    """
    conn = mariadb.connect(**get_config())
    cur = conn.cursor()
    cur.execute("USE recommender;")

    if user_exists(cur, userid):
        cur.execute("DELETE FROM users WHERE userid=?;",(userid,))
    conn.commit()
    conn.close()
    

def get_user_info(cur, userid):
    """
    """

    if user_exists(cur, userid):
        cur.execute("SELECT * FROM users WHERE userid=?;",(userid,))
        result = []
        for (userid, name, access_token, playlist_id) in cur:
            result.append([userid, name, access_token, playlist_id])
        return result[0]
    else:
        return -1
    

def get_users(cur):
    """
    """
    cur.execute("SELECT * FROM users;")
    result = []
    for (userid, name, access_token, playlist_id) in cur:
        result.append([userid, name, access_token, playlist_id])
    if len(result) == 0:
        return None
    return result


def song_processed(cur, songid):
    """
    """

    cur.execute("SELECT COUNT(*) FROM features WHERE songid=?;",(songid,))
    return False if cur.fetchone()[0] == 0 else True


def save_features(cur, songid, features):
    """
    """
    cur.execute("INSERT INTO features VALUES (?, ?);", (songid, features))


def delete_features(cur, save_songs):
    """
    """

    cur.execute("DELETE FROM features WHERE songid NOT IN ?;",(save_songs,))


def get_features(cur):
    """
    """

    cur.execute("SELECT * FROM features;")
    result = []
    for (songid, features) in cur:
        result.append([songid, eval(features)])
    return result
    


