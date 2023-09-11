from pymongo import MongoClient

def get_mongodb_connection(database_name='news', host='localhost', port=27017):
    """
    Create and return a MongoDB connection using pymongo.
    
    Args:
        database_name (str): The name of the database to connect to (default: 'news').
        host (str): The MongoDB host address (default: 'localhost').
        port (int): The MongoDB port (default: 27017).
    
    Returns:
        pymongo.MongoClient: The MongoClient object for the MongoDB connection.
    """
    client = MongoClient(host, port)
    db = client[database_name]
    
    return db


