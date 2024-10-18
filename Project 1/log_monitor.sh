#!/bin/bash

# Example logs
# 2024-10-16 00:19:25 [ERROR] Payment gateway timeout for transaction ID 87654.
# 2024-10-16 00:20:37 [FATAL] Disk failure detected on /dev/sdb. Immediate replacement required.

# Filter the log file for only logs containing the FATAL or ERROR  logs
logbuffer=$(grep -E "FATAL|ERROR" "/home/danny/Revature/Project1/log/app.log")

# Truncates the log file as to prevent duplicates from being read again
> /home/danny/Revature/Project1/log/app.log

# Loop through each line in the log buffer, and separate the values

while ISF= read -r line; do

	error_type=$(echo "$line" | grep -oP "FATAL|ERROR")
	time_stamp=$(echo "$line" | grep -oP "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
	error_text=$(echo "$line" | grep -oP "\[\w+\]\s+(.*)" | sed 's/^\[\w\+\]\s*//' | sed "s/'/''/g")

#	echo $error_type
#	echo $time_stamp
#	echo $error_text

	# Connect details
	DB_NAME="logs"
	DB_USER="danny"
	DB_PASSWORD=$logs_db_pass #environment variable
	DB_HOST="/var/run/postgresql"
	DB_PORT="5432"

	# INSERT statement to be generated.
	INSERT="INSERT INTO severelogs(timestamp, impact, message) VALUES ('$time_stamp','$error_type','$error_text');"


	psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$INSERT"


done <<< "$logbuffer"


