# Data Modeling with PostgreSQL


## Introduction

This database is configured for a startup named **Sparkify**. This company wants to analyze the data they've been collecting to understand what songs users are listening to.

All the information is obtained from thier own app, they have a directory of JSON logs and user activity, as well as a directory of JSON metadata.


## Project Goals
**Sparkify** needs an easy way to query the data.

In this project, it'll be established the processes of *Data Modeling* and building an *ETL pipeline*.

> Data modeling process:
>
> - It'll be defined a fact and dimensional tables for a star schema using **Postgres**.

> ETL pipeline:
>
> - It'll transfer data from files in two local directories into tables using **Python** and **SQL**.

For this project it'll be loaded files from *data/log_data* and *data/song_data* directories, and both contains files in *JSON* format.

> i.e. song data:
>
> song_data/A/B/C/TRABCEI128F424C983.json
> song_data/A/A/B/TRAABJL12903CDCF1A.json

> i.e. log_data:
>
> - log_data/2018/11/2018-11-12-events.json
> - log_data/2018/11/2018-11-13-events.json


### Data Modeling

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

The project workspace includes five files: sql_query.py, test.ipynb, create_tables.py, etl.ipynb, and etl.py. 

> - sql_query.py contains all your sql queries.
>
> - create_tables.py drops and creates tables (this file resets tables).
>
> - test.ipynb confirms tables created, and records inserted into each table. 
>
> - etl.ipynb reads and processes a single file from *song_data* and *log_data* and load data into tables.
>
> - etl.py reads and processes files from *song_data* and *log_data* and loads them into tables 

**Process:**

1. Run create_tables.py to create the database and tables.

2. Run test.ipynb to confirm the creation of tables and validate the columns. 
> **Make sure to click "Restart Kernel" to close de connection to the data base after running this notebook**.

3. Run etl.ipynb to insert one record into each table. At the end of each table section, or at the end of the notebook, run again test.ipynb to confirm records were inserted correctly into tables.
> Rerun always create_tables.py before running etl.py

4. Run create_tables.py to reset the tables.
 
5. Run etl.py to process the entire datasets. After that, rerun test.ipynb to confirm the records were successfully inserted into each table. 


## References

[Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/series.html)

[postgres tutorial](https://www.postgresqltutorial.com/postgresql-upsert/)

Convert list into a dictionary [stackoverflow](https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary)