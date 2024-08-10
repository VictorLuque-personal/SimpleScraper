import sqlite3
import os.path as path
import uuid
from datetime import datetime

def create_db():
  """ The creation of the database if it does not exist """
  
  # The OS sensible path of the current file + ../Storage/storage.db 
  db_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'Storage', 'storage.db')
  
  if not path.exists(db_path):
    # Conection (that creates if not existing file) and cursor to interact
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Create the necessary tables for the project
    # I always prefer to use GUID as ids and save them as binary objects.
    # Also I allow the column for the filter criteria to be null for non-
    # filtered queries and I will not do a CHECK() to bound the vaues to allow
    # the application grow easily. The score and the number of comments can not
    # be null because if there are not is set to zero
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS Queries (
        ID BLOB PRIMARY KEY,
        TimeStamp DATETIME NOT NULL,
        FilterCriteria INT,
        NumEntries INT NOT NULL
      )
    ''')
    
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS QueryEntries (
        ID BLOB PRIMARY KEY,
        Rank INT NOT NULL,
        Title varchar(500) NOT NULL,
        Score INT,
        Comments INT,
        QueryID BLOB,
        FOREIGN KEY (QueryID) REFERENCES Queries(ID)
      );
    ''')
    
    # Save changes & close connection
    connection.commit()
    connection.close()

class StorageManager:
  
  def __init__(self, db_path):
    """ Connection and cursor to interact """
    self.connection = sqlite3.connect(db_path)
    self.cursor = self.connection.cursor()
    
  def guid_generator(self):
    return uuid.uuid4().bytes
  
  def save(self, data: dict, criteria: int):
    """ Saves a query, filtered or not with its entries and the timestamp """
    
    # The query info
    queryID = self.guid_generator()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    self.cursor.execute('''
      INSERT INTO Queries (ID, TimeStamp, FilterCriteria, NumEntries) VALUES (?, ?, ?, ?)
    ''', (queryID, timestamp, criteria, len(data)))
    
    entries = [(self.guid_generator(), rank, values[0], values[1], values[2], queryID) for rank, values in data.items()]
    
    self.cursor.executemany('''
      INSERT INTO QueryEntries (ID, Rank, Title, Score, Comments, QueryID) VALUES (?, ?, ?, ?, ?, ?)
    ''', entries)
    
    self.connection.commit()
  
  def close_connection(self):
    self.connection.close()
