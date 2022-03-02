import glob
import pathlib
import sqlite3

import pandas as pd

songs = []
sql_create_songs_table = """ CREATE TABLE IF NOT EXISTS songs 
                        (id integer PRIMARY KEY, title TEXT NOT NULL, 
                        language TEXT, content TEXT ); """

sql_insert_song_query = """INSERT INTO songs (title, language, content) VALUES (?, ?, ?);"""

db_file_path = pathlib.Path("songs.db")
db_file_path.unlink(missing_ok=True)

for song_path in glob.glob("./txt/**"):
    with open(song_path) as song:
        title = song.name.split("/")[-1].split(".")[0].lower()
        content = "".join([l for l in song.readlines()]).strip()
        title = title[0].upper() + title[1:]
        songs.append((title, "fr", content))

with sqlite3.connect(db_file_path) as con:
    cur = con.cursor()
    cur.execute(sql_create_songs_table)
    cur.executemany(sql_insert_song_query, songs)

songs_df = pd.DataFrame(songs)
songs_df.columns = ["Title", "Language", "Content"]
songs_df.to_excel("songs.xlsx")

