import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")

# Check if there is a connection to the MongoDB server
try:
    # Try to get the list of databases 
    database_list = client.list_database_names()
    print("Connection to MongoDB established successfully.")
    print("Available databases:", database_list)
except Exception as e:
    print("Error establishing a connection to MongoDB:", str(e))
finally:
    
    client.close()

