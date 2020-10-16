import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek, date_format
import pandas as pd


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Create a Spark Session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    This function loads data from song_data folder, 
    extracts columns to create songs_table and artists_table, 
    and finally, creates the .parquet files to upload into S3.
    """
    # get filepath to song data file
    #song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
    song_data = os.path.join(input_data, "song-data/A/A/A/*.json")
    
    # read song data file
    df = spark.read.json(song_data)
    
    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "year", "duration").dropDuplicates()
    print(songs_table.printSchema())
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(os.path.join(output_data, "songs.parquet"), "overwrite")

    # extract columns to create artists table
    artists_table = df.select("artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude").dropDuplicates()
    print(artists_table.printSchema())
    
    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, "artist.parquet"), "overwrite")


def process_log_data(spark, input_data, output_data):
    """
    This function loads data from log_data folder,
    extracts columns to create users_table, time_table and songplays_table,
    and finally, creates the .parquet files to upload into S3.
    """
    # get filepath to log data file
    log_data = os.path.join(input_data,"log_data/*/*/*.json")
    
    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == "NextSong")

    # extract columns for users table    
    users_table = df.select("userId", "firstName", "lastName", "gender", "level").dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, "users.parquet"), "overwrite")
    print(users_table.printSchema)
    
    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: int((int(x)/1000)))
    df = df.withColumn("timestamp", get_timestamp(df.ts))
        
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x))
    df = df.withColumn("start_time", get_datetime(df.timestamp))
    
    # extract columns to create time table
    time_table = df.select("ts", "timestamp", "start_time") \
                      .withColumn("hour", hour("start_time")) \
                      .withColumn("day", dayofmonth("start_time")) \
                      .withColumn("week", weekofyear("start_time")) \
                      .withColumn("month", month("start_time")) \
                      .withColumn("year", year("start_time")) \
                      .withColumn("weekday", dayofweek("start_time"))
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(os.path.join(output_data, "time.parquet"), "overwrite")
    print(time_table.printSchema())
    
    # read in song data to use for songplays table
    #song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
    song_data = os.path.join(input_data, "song-data/A/A/A/*.json")
    
    song_df = spark.read.json(song_data)
    
    # extract columns from joined song and log datasets to create songplays table    
    df_joined = df.join(song_df, (song_df.title == df.song) & (song_df.artist_name == df.artist))
    #print(df_joined.printSchema())
    
    songplays_table = df_joined.select(
                                col("start_time"),
                                col("userId").alias("user_id"),
                                col("level").alias("level"),
                                col("song_id").alias("song_id"),
                                col("artist_id").alias("artist_id"),
                                col("sessionId").alias("session_id"),
                                col("location").alias("location"),
                                col("userAgent").alias("user_agent")) \
                                .withColumn("year", year("start_time")) \
                                .withColumn("month", month("start_time")) \
                                .withColumn("songplay_id", monotonically_increasing_id())
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(os.path.join(output_data, "songplays.parquet"), "overwrite")
    print(songplays_table.printSchema())

def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    #output_data = ""
    
    #local testing
    #input_data = "data/"
    output_data = "data_transformed/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
