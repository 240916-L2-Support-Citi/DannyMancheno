import psycopg # PSQL adapter for python
import os # Import OS so we can write to the file
import datetime

DB_NAME='logs'
DB_USER='danny'
DB_PASS=os.getenv('logs_db_pass')
DB_HOST='/var/run/postgresql'
DB_PORT="5432"

try: 
    # connect to psql db using psycopg library, create the conncetion object
    with psycopg.connect(
        f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}"
    ) as connection:
        # using the connection object, create a cursor object, used to send commands
        # queries to the connection object
        with connection.cursor() as my_cursor:
            # query the log database to only fetch the previous minute's logs. 
            my_cursor.execute("SELECT impact FROM severelogs WHERE timestamp >  NOW() - INTERVAL '1 minute';")
            
            # store all fetched rows, as a list of tuples
            records = my_cursor.fetchall()
            
            fatal_count=0
            error_count=0
            
            # loop through all tuples, in this case just the 'impact' column; 'FATAL' or 'ERROR' is needed.
            for row in records:
                if row[0] == 'ERROR':
                    error_count += 1
                else:
                    fatal_count += 1
                    
            # Catch the morning or evening for eye candy purposes 
            ampm='AM'
            if datetime.datetime.now().hour >= 12:
                ampm='PM'
            # Get the current timestamp if thresholds are reached
            time=datetime.datetime.now().strftime(f"%m-%d-%Y %H:%M {ampm}")
            # alert.txt file located for printing alerts
            filename='/home/danny/Revature/Project1/python/alert.txt'
            
            with open(filename, 'a') as file:
                
                # If any of the thresholds are reached, begin to alert.
                if fatal_count >= 1 or error_count >= 5:        
                    
                    file.write(f'\033[4m\033[31mThresholds reached\033[0m - {time}\033[0m\n')
                    # print(f'\033[4m\033[31mThresholds reached\033[0m - {time}\033[0m')
                    
                    if fatal_count >= 1:
                    
                        file.write(f'{fatal_count} fatals have been logged\n')
                        #print(f'{fatal_count} fatals have been logged')
                    
                    if error_count >= 5:
                    
                        file.write(f'{error_count} errors have been logged\n')
                        #print(f'{error_count} errors have been logged')
                    
                    # Used for padding between alert purposes.
                    file.write('\n')
                    # print('\n') 
                    
except Exception as e:
    print("Error connecting to db", e)