import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
ARN = config.get("IAM_ROLE", "ARN")

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
       auth varchar,
       firstName varchar,
       gender char(1),
       itemInSession int,
       lastName varchar,
       length numeric,
       level varchar,
       location varchar,
       method varchar,
       page varchar,
       registration numeric,
       sessionId int,
       song varchar,
       status int,
       ts numeric,
       userAgent varchar,
       userId int
   )

""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs int,
        artist_id char(20),
        artist_latitude varchar,
        artist_longitude varchar,
        artist_location varchar,
        artist_name varchar,
        song_id char(20),
        title varchar,
        duration numeric,
        year int 
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
 COPY staging_events FROM {}
    credentials 'aws_iam_role={}'
    format as json {}
    STATUPDATE ON
    region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
COPY staging_songs FROM {}
    credentials 'aws_iam_role={}'
    format as json 'auto'
    ACCEPTINVCHARS AS '^'
    STATUPDATE ON
    region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
        SELECT DISTINCT to_timestamp(to_char(se.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS'),
                        se.userId AS user_id, 
                        se.level AS level, 
                        ss.song_id AS song_id, 
                        ss.artist_id AS artist_id, 
                        se.sessionId AS session_id, 
                        se.location AS location, 
                        se.userAgent AS user_agent
        FROM staging_events se 
        INNER JOIN staging_songs ss 
            ON se.song = ss.title AND se.artist = ss.artist_name
        WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT  DISTINCT se.userId          AS user_id,
            se.firstName                AS first_name,
            se.lastName                 AS last_name,
            se.gender                   AS gender,
            se.level                    AS level
    FROM staging_events AS se
    WHERE se.page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT  DISTINCT ss.song_id         AS song_id,
            ss.title                    AS title,
            ss.artist_id                AS artist_id,
            ss.year                     AS year,
            ss.duration                 AS duration
    FROM staging_songs AS ss;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT  DISTINCT ss.artist_id       AS artist_id,
            ss.artist_name              AS name,
            ss.artist_location          AS location,
            ss.artist_latitude          AS latitude,
            ss.artist_longitude         AS longitude
    FROM staging_songs AS ss;
""")

time_table_insert = ("""
INSERT INTO times (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT to_timestamp(to_char(se.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS') AS start_time,
            EXTRACT(hour FROM start_time)    AS hour,
            EXTRACT(day FROM start_time)     AS day,
            EXTRACT(week FROM start_time)    AS week,
            EXTRACT(month FROM start_time)   AS month,
            EXTRACT(year FROM start_time)    AS year,
            EXTRACT(week FROM start_time)    AS weekday
    FROM    staging_events                   AS se
    WHERE se.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
