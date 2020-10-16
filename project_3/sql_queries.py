import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        artist VARCHAR(255),
        auth VARCHAR(15),
        first_name VARCHAR(255),
        gender VARCHAR(1),
        item_in_session INTEGER,
        last_name VARCHAR(255),
        lenght REAL,
        level VARCHAR(15),
        location VARCHAR(255),
        method VARCHAR(5),
        page VARCHAR(50),
        registration REAL,
        session_id BIGINT,
        song_title VARCHAR(255),
        status INTEGER,
        ts VARCHAR(255),
        user_agent TEXT,
        user_id INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs INTEGER,
        artist_id VARCHAR(255),
        artist_latitude REAL,
        artist_longitude REAL,
        artist_location VARCHAR(255),
        artist_name VARCHAR(255),
        song_id VARCHAR(255),
        title VARCHAR(255),
        duration REAL,
        year INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL SORTKEY,
        user_id INTEGER NOT NULL DISTKEY,
        level VARCHAR(15),
        song_id VARCHAR(255) NOT NULL,
        artist_id VARCHAR(255) NOT NULL,
        session_id BIGINT NOT NULL,
        location VARCHAR(255),
        user_agent TEXT
    );
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        gender VARCHAR(1),
        level VARCHAR(15)
    )
    DISTSTYLE AUTO;
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        artist_id VARCHAR(255) NOT NULL,
        year INTEGER,
        duration REAL
    )
    DISTSTYLE AUTO;
""")

artist_table_create = ("""
    CREATE TABLE artists (
        artist_id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        location VARCHAR(255),
        latitude FLOAT,
        longitude FLOAT
    )
    DISTSTYLE AUTO;
""")

time_table_create = ("""
    CREATE TABLE time (
        start_time TIMESTAMP PRIMARY KEY SORTKEY,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER
    )
    DISTSTYLE AUTO;
""")

# STAGING TABLES

staging_events_copy = ("""
                          COPY staging_events FROM {}
                          CREDENTIALS 'aws_iam_role={}'
                          FORMAT AS JSON {} 
                          COMPUPDATE OFF REGION 'us-west-2';
""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
                         COPY staging_songs FROM {}
                         CREDENTIALS 'aws_iam_role={}'
                         FORMAT AS JSON 'auto'
                         COMPUPDATE OFF REGION 'us-west-2';
""").format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
                            INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT 
                                TIMESTAMP 'epoch' + events.ts/1000 * INTERVAL '1 second' AS start_time,
                                events.user_id,
                                events.level,
                                songs.song_id,
                                songs.artist_id,
                                events.session_id,
                                events.location,
                                events.user_agent
                            FROM
                                staging_events events
                            JOIN
                                staging_songs songs ON events.song_title = songs.title
                            WHERE
                                events.page = 'NextSong';
""")

user_table_insert = ("""
                        INSERT INTO users (user_id, first_name, last_name, gender, level)
                        SELECT DISTINCT
                            user_id,
                            first_name,
                            last_name,
                            gender,
                            level
                        FROM 
                            staging_events
                        WHERE
                            page = 'NextSong';
""")

song_table_insert = ("""
                        INSERT INTO songs (song_id, title, artist_id, year, duration)
                        SELECT DISTINCT
                            song_id,
                            title,
                            artist_id,
                            year,
                            duration
                        FROM
                            staging_songs;
""")

artist_table_insert = ("""
                          INSERT INTO artists (artist_id, name, location, latitude, longitude)
                          SELECT DISTINCT
                              artist_id,
                              artist_name,
                              artist_location,
                              artist_latitude,
                              artist_longitude
                            FROM
                                staging_songs;
""")

time_table_insert = ("""
                        INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                        SELECT DISTINCT
                            TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time,
                            EXTRACT(hour FROM start_time),
                            EXTRACT(day FROM start_time),
                            EXTRACT(week FROM start_time),
                            EXTRACT(month FROM start_time),
                            EXTRACT(year FROM start_time),
                            EXTRACT(weekday FROM start_time)
                        FROM
                            staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
