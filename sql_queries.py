import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS events_staging"
staging_songs_table_drop = "DROP TABLE IF EXISTS songs_staging"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
   CREATE TABLE IF NOT EXISTS staging_events (
       artist varchar,
       auth varchar  not null,
       firstName varchar,
       gender char(1),
       itemInSession int not null,
       lastName varchar,
       length numeric,
       level varchar not null,
       location varchar,
       method varchar not null,
       page varchar not null,
       registration numeric,
       sessionId int not null,
       song varchar,
       status int not null,
       ts numeric not null,
       userAgent varchar,
       userId int
   )

""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs int not null,
        artist_id char(20) not null,
        artist_latitude varchar,
        artist_longitude varchar,
        artist_location varchar,
        artist_name varchar not null,
        song_id char(20) not null,
        title varchar not null,
        duration numeric not null,
        year int not null
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id int identity(0,1) PRIMARY KEY,
        start_time timestamp not null,
        user_id int not null,
        level varchar not null,
        song_id char(20),
        artist_id char(20),
        session_id int,
        location varchar,
        user_agent varchar not null
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id int PRIMARY KEY,
        first_name varchar not null,
        last_name varchar not null,
        gender char(1) not null,
        level varchar not null
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id char(20) PRIMARY KEY,
        title varchar not null,
        artist_id char(20) not null,
        year int not null,
        duration numeric not null
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id char(20) PRIMARY KEY,
        name varchar not null,
        location varchar,
        latitude numeric,
        longitude numeric
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS times (
        start_time timestamp PRIMARY KEY,
        hour int not null,
        day int not null,
        week int not null,
        month int not null,
        year int not null,
        weekday int not null
    )
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
