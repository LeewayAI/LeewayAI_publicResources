import mysql.connector
import requests
import json

# This File helps you automate the process to find all the table names and all the columns 
# and their data types in each table.
# The file can be run locally and even be modified to be Pipelines to
# regenrate the entire schemas if there are any changes (Yes! We are migration friendly :))

# The file would require database connection information and schema name. 
# The output of the script would be a json file namely "tablesInformation.json" by default
# which contains data in the format that our API's tablesSchema parameter requires
# which is all the tables in a Schema with their attributes and data types

# Add database instance details for making a connection
host_value = "<Database Endpoint>"
port_value = "<Port Number>"
database_value = "<Databse Name>"
user_value = "<Username>"
password_value = "<Password for that username>"
schema_name = "<Schema Name>"

Database = {}
tableSchemas = []

# Establish a connection to the Databse instance
connection = mysql.connector.connect(
    host=host_value,
    user=user_value,
    password=password_value,
    database=database_value
)

cursor = connection.cursor()

Query = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema_name}'"
cursor.execute(Query)

# Fetch all rows from the result set
rows = cursor.fetchall()
for row in rows:
    if row[2] in Database:
        Database[row[2]][row[3]]=row[7]
    else:
        Database[row[2]] = {}
        Database[row[2]][row[3]]=row[7]

for eachKey in Database:
    tableSchemas.append({"tableName":eachKey,"attributes":Database[eachKey]})

# Creates a file in the same directory named - tablesInformation.json which has the json for
# the tablesSchema parameter that has to be passed in the body of the request to our API. 
with open("tablesInformation.json","w") as outfile:
    outfile.write(json.dumps(tableSchemas))

    
    




