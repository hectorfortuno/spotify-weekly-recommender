"""

"""
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
    return False if cur[0] == 0 else True


def add_user(cur, userid, username, access_token, playlistid):
    """
    """

    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (userid, username, access_token, playlistid))


def delete_user(cur, userid):
    """
    """

    if user_exists(cur, userid):
        cur.execute("DELETE FROM users WHERE userid=?;",(userid,))
        return None
    else:
        return -1
    

def get_user_info(cur, userid):
    """
    """

    if user_exists(cur, userid):
        cur.execute("SELECT * FROM users WHERE userid=?;"(userid,))
        return cur[0]
    else:
        return -1
    

def get_users(cur):
    """
    """
    return cur.execute("SELECT * FROM users;")


def song_processed(cur, songid):
    """
    """

    cur.execute("SELECT COUNT(*) FROM features WHERE songid=?;",(songid,))
    return False if cur[0] == 0 else True


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
        result.append([songid, features])
    return result
    


