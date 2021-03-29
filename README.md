# Redshift Data Warehouse Project

## Overview

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. 
Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project, I'm going to follow these steps:
1. Build an ETL pipeline that extracts the data from S3 
2. Stages them in Redshift
3. Transforms data into a set of dimensional tables for their analytics team to find what songs their users are listening to.

## How to Run Scripts

1. Clone `https://github.com/ArataKagan/redshift-data-warehouse`
2. Create `dwh.cfg` file and store in the project
3. Copy the following code into the `dwh.cfg` file:
```
[CLUSTER]
HOST=''

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

[IAM_ROLE]
ARN=''

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```
4. Fill in the necessary cluster information into the file
5. Execute `python create_table.py`
6. Execute `python etl.py`

## File Structure 
- etl.py : Reads and process S3 dataset and stored into Redshift 
- sql_queries.py : Contains all sql queries
- create_tables.py : Contains CREATE and DROP functions 

## Database Schema

### Staging Table:
**Staging Song Table**
 * num_songs INT
 * artist_id TEXT
 * artist_latitude DECIMAL
 * artist_longitude DECIMAL
 * artist_location TEXT
 * artist_name TEXT
 * song_id TEXT
 * title TEXT
 * duration DECIMAL
 * year INT
 
**Staging Event Table**
 * artist	TEXT	
 * auth	TEXT	
 * firstName	TEXT	
 * gender	TEXT		
 * itemInSession INT	
 * lastName	TEXT	
 * length	DECIMAL	
 * level	TEXT	
 * location	TEXT	
 * method	TEXT	
 * page	TEXT	
 * registration	TEXT	
 * sessionId	INT	
 * song	TEXT		
 * status	INT	
 * ts	TIMESTAMP	
 * userAgent	TEXT	
 * userId	INT

### Fact Table: 
**Songplays Table**
 * songplay_id INT PRIMARY KEY 
 * timestamp DATE : Time table's start time 
 * user_id INT : User ID 
 * level TEXT : User level 
 * song_id TEXT : Song ID 
 * artist_id TEXT : Artist ID 
 * session_id INT : Session ID 
 * location TEXT : User's location  
 * user_agent TEXT : User's agent to access the app 


### Dimention Tables: 
**Users Table**
 * user_id INT PRIMARY KEY
 * first_name TEXT 
 * last_name TEXT
 * gender TEXT
 * level TEXT 

**Songs Table**
 * song_id TEXT PRIMARY KEY 
 * title text NOT NULL
 * artist_id TEXT NOT NULL 
 * year INT
 * duration FLOAT NOT NULL

**Artists Table**
 * artist_id TEXT PRIMARY KEY
 * name TEXT NOT NULL
 * location TEXT
 * lattitude FLOAT
 * longitude FLOAT

**Times Table** 
 * start_time DATE PRIMARY KEY
 * hour INT 
 * day INT 
 * week INT 
 * month INT
 * year INT 
 * weekday text


