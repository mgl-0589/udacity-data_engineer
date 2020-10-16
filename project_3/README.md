# Data Warehouse


## Introduction

This data warehouse will be configured for a startup named **Sparkify**. This company wants to analyze the data they've been collecting to understand what songs users are listening to.

All the information is obtained from thier own app. All their data resides in S3, in a directory of logs on user activity on the app, as well as a directory with metadata on the songs in their app.


## Project Goals
**Sparkify** wants to transform their data into a set of dimensional tables.

In this project, it'll be established the processes of *Data Modeling* and building an *ETL pipeline*.

> Data modeling:
>
> - It'll be defined two staging tables, as well as fact and dimensional tables for a star schema using **Postgres**.

> ETL pipeline:
>
> - It'll extracts their data from **S3**, stages them in **Redshift**, and transforms data into a set of fact and dimensional tables

For this project it'll be loaded files from *data/log_data* and *data/song_data* directories, both contains files in *JSON* format.

> Song data: s3://udacity-dend/song_data

> i.e. song data:

> - song_data/A/B/C/TRABCEI128F424C983.json
> - song_data/A/A/B/TRAABJL12903CDCF1A.json

> Log data json path: s3://udacity-dend/log_json_path.json
> Log data: s3://udacity-dend/log_data

> i.e. log_data:

> - log_data/2018/11/2018-11-12-events.json
> - log_data/2018/11/2018-11-13-events.json

### Data Modeling

**Staging Tables:**
- staging_events (Log data from **S3**)
   - event_id,
   - artist,
   - auth,
   - first_name,
   - gender,
   - item_in_session,
   - last_name,
   - lenght,
   - level,
   - location,
   - method,
   - page, 
   - registration,
   - session_id,
   - song_title,
   - status,
   - ts,
   - user_agent,
   - user_id

- staging_songs (songs data from **S3**)
   - num_songs,
   - artist_id,
   - artist_latitude,
   - artist_longitude,
   - artist_location,
   - artist_name,
   - song_id,
   - title,
   - duration,
   - year

**Fact Table:**
- songplays (records in log data associated with song plays) 
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
- users (users in the app)
   - user_id, 
   - first_name, 
   - last_name, 
   - gender, 
   - level

- songs (songs in music database)
   - song_id, 
   - title, 
   - artist_id, 
   - year, 
   - duration
    
- artists (artists in music database)
    - artist_id, 
    - name, 
    - location, 
    - latitude, 
    - longitude
    
- time (timestamps of records in songplays broken down into specific units)
    - start_time, 
    - hour, 
    - day, 
    - week, 
    - month, 
    - year, 
    - weekday


### ETL pipeline

The project workspace includes four files: dwh.cfg, sql_queries.py, create_tables.py, and etl.py. 

> - dwh.cfg must be filled in with the credentials to access AWS Redshift
>
> - sql_query.py contains all the sql queries.
>
> - create_tables.py drops and creates tables (this file resets tables).
>
> - etl.py reads and processes files from *song_data* and *log_data* and loads them into tables 

**Process:**

> **Before running the create_tables.py**

> - Create an *IAM Role* that makes **Redshift** able to access **S3** bucket
>
> - Create a **RedShift** Cluster
>
> - Edit the dwh.cfg file with the corresponding values
>   - HOST --> Endpoint
>   - DB_NAME --> Database Name
>   - DB_USER --> Database User Name
>   - DB_PASSWORD --> Database User Password
>   - DB_PORT --> Database Port
>   - ARN

1. Run create_tables.py to reset the tables. After that, use Query Editor in the **AWS Redshift** console to confirm all tables were succesfully created.
 
2. Run etl.py to process the entire datasets. After that, use Query Editor in the **AWS Redshift** to confirm the records were successfully inserted into each table. 


## References

[IDENTITY (0,1)](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html)

[Data types](https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html)

[convert timestamp](https://stackoverflow.com/questions/39815425/how-to-convert-epoch-to-datetime-redshift)

[Extract](https://docs.aws.amazon.com/es_es/redshift/latest/dg/r_EXTRACT_function.html)

[COPY](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)

[NOT NULL CONSTRAINT](https://dwgeek.com/redshift-not-null-constraint-syntax-and-examples.html/)