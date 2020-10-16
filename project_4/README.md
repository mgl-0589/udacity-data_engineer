# Data Lake


## Introduction

A music streaming startup, **Sparkify**, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.


## Project Goals
**Sparkify** wants to transform their data into a set of dimensional tables.

In this project, it'll be established the processes of *Data Modeling* and building an *ETL pipeline* with **Apache Spark** framework.

> Data modeling:
>
> - It'll be defined fact and dimensional tables for a star schema.

> ETL pipeline:
>
> - It'll extracts data from **S3**, and transforms it into a set of fact and dimensional tables

For this project it'll be loaded files from *data/log_data* and *data/song_data* directories, both contains files in *JSON* format.

> Song data: s3://udacity-dend/song_data

> i.e. song data:

> - song_data/A/B/C/TRABCEI128F424C983.json
> - song_data/A/A/B/TRAABJL12903CDCF1A.json

> Log data: s3://udacity-dend/log_data

> i.e. log_data:

> - log_data/2018/11/2018-11-12-events.json
> - log_data/2018/11/2018-11-13-events.json

### Data Modeling

**Fact Table:**
- songplays_table (records in log data associated with song plays) 
   - songplay_id, 
   - start_time, 
   - user_id, 
   - level, 
   - song_id, 
   - artist_id, 
   - session_id, 
   - location, 
   - user_agent

**Dimensional Tables:**
- users_table (users in the app)
   - user_id, 
   - first_name, 
   - last_name, 
   - gender, 
   - level

- songs_table (songs in music database)
   - song_id, 
   - title, 
   - artist_id, 
   - year, 
   - duration
    
- artists_table (artists in music database)
    - artist_id, 
    - name, 
    - location, 
    - latitude, 
    - longitude
    
- time_table (timestamps of records in songplays broken down into specific units)
    - start_time, 
    - hour, 
    - day, 
    - week, 
    - month, 
    - year, 
    - weekday


### ETL pipeline

The project workspace includes four files: dwh.cfg and etl.py. 

> - dwh.cfg must be filled in with the credentials to access AWS
>
> - etl.py reads and processes files from *song_data* and *log_data* and loads them into tables as a .parquet file

**Process:**

> **Before running the create_tables.py**

> - Create the AWS *Access key ID* and *Secret access key* in the AWS portal
>
> - Create a **S3** Bucket to save all tables
>
> - Edit the dwh.cfg file with the corresponding values
>   - AWS_ACCESS_KEY_ID
>   - AWS_SECRET_ACCESS_KEY

1. Run etl.py and it'll read data from **S3**, process the entire datasets using Spark. Finally it'll write the *.parquet* files back to **S3**.


## References

[partitionBy()](https://stackoverflow.com/questions/50775870/pyspark-efficiently-have-partitionby-write-to-same-number-of-total-partitions-a)

[convert timestamp column](https://knowledge.udacity.com/questions/285538)

[.join](https://knowledge.udacity.com/questions/340141)