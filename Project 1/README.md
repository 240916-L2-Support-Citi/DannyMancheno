#### Project 1 ####

This project performs automates several scripts, and performs a log monitoring alert system.

# generate_logs.sh
- Will start by generating various level logs in a while loop to imitate a real world environment continuously between the INFO/WARNING/ERROR/FATAL levels
- The generated log <timestamp-level-message> messags will then be saved to the log/app.log

# log/app.log
- This log/app.log will serve as a bus for the logs between the ones generated from  generate_logs.sh, and the log monitor log_monitor.sh

# log_monitor.sh - cronjob 1
- The log monitor will at every minute:
    - Filter FATAL or ERROR log lines, generated in logs/app.log into a variable logbuffer.
    - Truncate logs/app.log, so that it will contain only new logs for the next minute interval
    - While loop through the logbuffer variable, and do the following
        - Variablize time / type / msg data from the log
        - Insert this data into a psql database in their respective columns

# psql logs table
- in psql, a simple severelogs table was created with the columns necessary mentioned above
___psql____
logs-# \d severelogs
                                        Table "public.severelogs"
  Column   |            Type            | Collation | Nullable | Default

id        | integer                     |           | not null | nextval
timestamp | timestamp without time zone |           |          |
impact    | character varying(10)       |           |          |
message   | character varying(300)      |           |          |

Indexes:
    "severelogs_pkey" PRIMARY KEY, btree (id)

# alert_system.py 
- This part of the project is written in python and does the following
    - It uses the psycopg package to connect to the psql database 
    - It creates a connection object, using it's .cursor.execute method to query the database
    - The query selects all logs from the severelogs table, but subtracts the first minute from now (to filter only the previous minute)
    - Once the tuples (rows) are extracted, a simple counter is made for each type of log FATAL or ERROR as each deserves it's own regard
        - If the counter thresholds are reached, an alert string is created, some beautified text is created to make the alert more readable. (eye candy)
        - The then beautified alert is echo'd into an alert.txt file.

# alert.txt
- This file contains minute by minute threshold alerts. 
    - If a minute reached thresholds, it's been recorded to this file
    - If not, it is skipped.
