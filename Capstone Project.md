# Project Title
### Data Engineering Capstone Project

#### Project Summary
A team of Data Scientists has asked the following question: could the number of crimes committed in a city correlated to the average temperature and the immigration rates?

**NOTE:** Not considering psychological or socioeconomic factors.

To develop a pilot test, the Data Science team decided to take as a sample from one of the main cities in the United States, the city of Los Angeles California.

To help this team of researchers, the Data Engineering team has been asked to be in charge of obtaining and preparing the data to carry out this analysis.

This project was designed to execute the process to pull and transform the data needed for the Data Science team.

The project follows the next steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up


### Step 1: Scope the Project and Gather Data

#### Scope
For this project the main idea is to create a ETL process to make sure Immigration, crime and temperature data match. This process will allow the Data Science team to test its hypothesis about the correlation between immigration, crime and temperature data.


#### Describe and Gather Data

* #### Immigrtion Data
Each report contains international visitor arrival statistics by world regions and select countries (including top 20), type of visa, mode of transportation, age groups, states visited (first intended address only), and the top ports of entry (for select countries).

    Data and description retrieved from: 
    [Immigration data source](https://travel.trade.gov/research/reports/i94/historical/2016.html)
    
* #### LA Crime Data
This dataset reflects incidents of crime in the City of Los Angeles from 2010 to 2019. This data is transcribed from original crime reports that are typed on paper and therefore there may be some inaccuracies within the data. Some location fields with missing data are noted as (0°, 0°). Address fields are only provided to the nearest hundred block in order to maintain privacy.

    Data and description retrieved from:
    [LA Crime data source](https://www.kaggle.com/chaitanyakck/crime-data-from-2020-to-present?select=Crime_Data_from_2020_to_Present.csv)
    
* #### World Temperature Data

    Daily temperature data from ERA5 reanalysis data from Copernicus Climate Service. It's time-series value in degrees Celsius, for 1000 most populous cities in the world, from Jan-01-1980 to Sept-30-2020.

    Data and description retreived from:
    [Temperature data source](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
    

### Step 2: Explore and Assess the Data

#### Explore and Clean the Data 
In this step the objective is to identify data quality issues, like missing values, duplicate data, etc. The data types most be consitent to make sure the Data Science Team will be able to use all data

To clean the data sets the Data Engineering Team should drop duplicate records and make sure there is no missing values in columns that contain dates because this columns will be used to create the relations between data sets.

The general process consists of 3 steps
1. Exploring the data and counting records
2. Dropping duplicates and missing values
3. Changing data type if needed


### Step 3: Define the Data Model

#### 3.1 Conceptual Data Model
In this step the main idea is to configure a set of attributes (in this case immigration rates and temperature) to validate if they have an influence on the number of crimes committed.

That's the reason why Data Engineering and Data Science teams select the Immigration data and LA temperature data to create the dimensional tables and LA Crimes data to create the fact table.


**Dimension tables**:

- immigration_table
    - date_arr
    - date_dep
    - id_imm
    - year_arr
    - month_arr
    - port_arr
    - trans_mode
    - state_arr
    - visa_code
    - visa_type
    - visa_issued
    - imm_age
    - imm_gender
    - imm_city_birth
    - imm_city_res
    
    
- LA_temp_table
    - date
    - avg_temp
    
    
- time_table
    - date
    - year
    - month
    - week
    - weekday
    - day
    
**Fact table**:

- LA_crime_table
    - id_LA_crime
    - date_occ
    - date_rep
    - time_occ
    - area_name
    - crime_com_desc
    - modus_op_code
    - vict_age
    - vict_gender
    - vict_descent
    - crime_place_desc
    - weapon_used_desc
    - status_case_desc
    - latitude
    - longitude
    

#### 3.2 Mapping Out Data Pipelines

This pipeline should:
1. Load the datasets cleaned
2. Filter values in the immigration dataset to include only California info.
3. Create the dimension tables (immigration_dim_table, LA_temp_dim_table and time_dim_table)
4. Create fact table (LA_crime_fact_table)


### Step 4: Run Pipelines to Model the Data

#### 4.1 Create the data model
This step creates the data model previously defined.


#### 4.2 Data Quality Checks
The data quality ensures the pipeline ran as expected:
 * Integrity constraints on the relational database (unique key)
 * Source/Count checks to ensure completeness
 
 
 #### 4.3 Data dictionary 
The data dictionary provides a brief description of data used in the data model.
 
immigration_dim_table

| Value | Description |
| --- | --- |
|date_arr | Date when immigrant arrived (yyyy-mmdd) |
date_dep | Date when immigrant departured (yyyy-mmdd) |
id_imm | Number to identify the record |
year_arr | Year when immigrant arrived |
month_arr | Month when immigrant arrived (numeric) |
port_arr | Port where immigrant arrived |
trans_mode | Transport mode (1 = "Air"; 2 = "Sea"; 3 = "Land"; 4 = "Not Reported") |
state_arr | State where immigrant arrived |
visa_code | Visa codes (1 = "Business"; 2 = "Pleasure"; 3 = "Student" |
visa_type | Class of admission legally admitting the non-immigrant to temporarily stayed in U.S. |
visa_issued | Department of State where Visa was issued |
imm_age | Immigrant age |
imm_gender | Immigrant gender |
imm_city_birth | Immigrant city of birth in code |
imm_city_res | Immigrant city of residence in code |


LA_temperature_dim_table

| Value | Description |
| --- | --- |
| date | Date of temperature recorded |
| avg_temp| Average of temperatures |


time_dim_table

| Value | Description |
| --- | --- |
| year | Year |
| month | Month (numeric) |
| week | Week of year (numeric) |
| weekday | Day of the week (numeric) |
| day | Day of month (numeric) |


LA_crimes_fact_table

| Value | Description |
| --- | --- |
| id_crime | Number to identify the record |
| date_rptd | Date when the crime reported (yyyy-mm-dd) |
| date_occ | Date when the crime occurred (yyyy-mm-dd) |
| hour_occ | Hour when the crime occurred |
| area_name | The 21 Geographic Areas or Patrol Divisions |
| crime_com_desc | Description of the crime commited |
| modus_op_code | Modus Operandi code |
| vict_age | Victim age |
| vict_gender | Victim gender (F = "Female"; M = "Male"; X = "Unknown") |
| vict_descent_code | Victim descent (A = "Other Asian"; B = "Black"; C = "Chinese"; D = "Cambodian"; F = "Filipino"; G = "Guamanian"; H = "Hispanic/Latin/Mexican"; I = "American Indian/Alaskan Native"; J = "Japanese"; K = "Korean"; L = "Laotian"; O = "Other"; P = "Pacific Islander"; S = "Samoan"; U = "Hawaiian"; V = "Vietnamese"; W = "White"; X = "Unknown"; Z = "Asian Indian") |
| crime_place_desc | The type of structure, vehicle, or location where the crime occurred |
| weapon_used_desc | The type of weapon used in the crime |
| status_case_desc | Status of the case. (IC is the default) |
| latitude | Latiude coordinates |
| longitude | Longitude coordinates |
| year_occ | Year when the crime occurred |
| month_occ | Month when the crime occurred (numeric) |


#### Step 5: Complete Project Write Up

This project uses Apache Spark because it is a technology built and optimized for processing huge amounts of data within a fast way, it manages easily data formats (SAS, CSV, JSON, parquet), it can read in data from other sources as well (such as Amazon S3). 

Considering this project is not intended to show data in real-time, and Immigration/Crime data sources were built on a monthly basis, the Data Engineering team decided that data will be refreshed by month.

#### The data was increased by 100x.

There are many big data frameworks that could handle huge amounts of data; selecting one will depend on many factors.
For this particular project Apache Spark could be a good solution because we are not working with stream data and Spark is faster than Hadoop.
Also, it can be mentioned that there are options that allow us to manage in an easy way the increments of data; one of these platforms is AWS EMR among others.

#### The data populates a dashboard that must be updated on a daily basis by 7 am every day.

One of the most popular technologies for running pipelines on a schedule is Apache Airflow. 
This tool provides a control dashboard for users and maintainers. Also, it comes with many Hooks that can be integrated with common systems (HttpHook, PostgresHook, MySqlHook, SlackHook, PrestoHook, etc.)
For this particular project implementing Apache Airflow could handle tasks scheduled.

#### The database needed to be accessed by 100+ people.

Data warehouse in cloud is one of the best options for accessing databases simultaneously by a lot of people. Technologies like Redshift, BigQuery, Teradata, Aster, Oracle ExaData or Azure, paralellize the execution of one query on multiple CPU/machines.


## References

[convert dates from SAS files](https://knowledge.udacity.com/questions/66798)

[cast string into date type](https://sparkbyexamples.com/spark/spark-convert-timestamp-to-date/#:~:text=Spark%20to_date()%20%E2%80%93%20Convert%20timestamp%20to%20date&text=Spark%20Timestamp%20consists%20of%20value,date%20on%20Spark%20DataFrame%20column.)

[filter or include based on list](https://stackoverflow.com/questions/40421845/pyspark-dataframe-filter-or-include-based-on-list)

Udacity nanodegree program