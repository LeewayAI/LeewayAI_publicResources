# Below are all the packages that you will require to run the example
# This example demonstrates for MYSQL database type similarly POSTGRESQL connector package can be installed
import mysql.connector
import requests
import json


def lambda_handler(event, context):
    # Lambda handler function that takes query and any hard Appliedfilters as an event field
    # event["query"] has a string containing the query passed by user
    # event["filterApplied"] has a dictionary with key as some table attribute and its value for the filtering, for no filters let it be an empty dictionary
    url = "<Leeway_API_URL>"
    # for best practices the YOUR_API_KEY can be stored securely but for the scope of this example it is being hardcoded below in the headers.
    headers = {'Content-Type': 'application/json',
               'x-api-key': "<YOUR_API_KEY>"}

    # As referred in the documentation, payload for request body is made with tableSchemas, query, filterApplied and dbType attributes
    # where tableSchemas and dbType can be specified in the template whereas query and filterApplied can be variable and be retreived from the event
    # An example is given below for better understaning of how to make payload for request body.
    payload = {
        "tableSchemas": [
            {
                "tableName": "customers",
                "attributes": {
                    "customerNumber": "int PK",
                    "customerName": "varchar(50)",
                    "contactLastName": "varchar(50)",
                    "contactFirstName": "varchar(50)",
                    "phone": "varchar(50)",
                    "addressLine1": "varchar(50)",
                    "addressLine2": "varchar(50)",
                    "city": "varchar(50)",
                    "state": "varchar(50)",
                    "postalCode": "varchar(15)",
                    "country": "varchar(50)",
                    "salesRepEmployeeNumber": "int",
                    "creditLimit": "decimal(10,2)"
                }
            },
            {
                "tableName": "offices",
                "attributes": {
                    "officeCode": "varchar(10)",
                    "city": "varchar(50)",
                    "phone": "varchar(50)",
                    "addressLine1": "varchar(50)",
                    "addressLine2": "varchar(50)",
                    "state": "varchar(50)",
                    "country": "varchar(50)",
                    "postalCode": "varchar(15)",
                    "territory": "varchar(10)",
                }
            }
        ],
        "query": event["query"],
        "filtersApplied": event["filterApplied"],
        "dbType": "MYSQL"
    }

    # Convert the dictionary to JSON string
    bodyPayload = json.dumps(payload)

    # get the response from Leeway API endpoint
    response = requests.post(url, headers=headers, data=bodyPayload)

    # load the response as json object
    querySQLJson = json.loads(response.text)

    # get the value for result attribute of the above json object
    sqlQuery = querySQLJson["result"]

    # Now SQL query is ready! Time to establish connection with your Pre-Existing Database so that the query can be executed and results can be returned
    # Replace the placeholder values with your RDS or Pre-existing databse instance details.
    # Again for best practices they can be stored securely but for now its out of scope for this example
    host_value = "<Database Endpoint>"
    port_value = "<Port Number>"
    database_value = "<Databse Name>"
    user_value = "<Username>"
    password_value = "<Password for that username>"

    # Establish a connection to your Database using the connector
    # (this example only demonstrates for MYSQL and POSTGRESQL equivalent connector can be used)
    connection = mysql.connector.connect(
        host=host_value,
        user=user_value,
        password=password_value,
        database=database_value
    )

    # creating an object that represents a database cursor in the MySQL Connector/Python library.
    # A cursor is used to execute SQL statements and retrieve data from the MySQL database.
    cursor = connection.cursor()

    # Execute your Leeway returned query in your database
    cursor.execute(sqlQuery)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    #####################################################################
    # A very basic example of post processing would be to return the integer if the result obtained is
    # just a number for example with queries stated like "How many", "Number of ". Moreover, return entire rows of data
    # as a list of rows where each row is a tuple and print each row. Also, print "No result found" if no data matching
    # the query existed in DB.
    # Again post-processing could be done in a number of ways and the below code
    # is a basic example and might have its own limitations

    if "COUNT" in sqlQuery:
        finalResult = rows[0][0]
        print(finalResult)
    else:
        if len(rows) != 0:
            finalResult = rows
            for row in rows:
                print(row)
        else:
            finalResult = "No result found"
            print(finalResult)
    response = {
        'Status': "Sucessful",
        'message': finalResult
    }
    return response

    #####################################################################
    # Error Handling
    #
    # In the case of an API or database error, you'll want to show end users a standard message on the frontend instead 
    # of the error. A standard message may be "Sorry, we were unable to process your request at this time. Please try again later."
