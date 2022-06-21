# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] 

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

try:
  cursor.execute("""
    CREATE TABLE Owners (
      id                 integer  AUTO_INCREMENT PRIMARY KEY,
      first_name         VARCHAR(50) NOT NULL,
      last_name          VARCHAR(50) NOT NULL,
      user_name          VARCHAR(40) NOT NULL,
      email              VARCHAR(60) NOT NULL,
      password           VARCHAR(30) NOT NULL,
      payment_method     VARCHAR(60),
      collection_method  VARCHAR(60),
      created_at         TIMESTAMP default CURRENT_TIMESTAMP
    );
  """)
  print("OWNERS TABLE CREATED!!!!!!")
except:
  print("Owners table already exists. Not recreating it.")

'''
each toy will come with a unique id (toyID), this id will be part of manufacturing and it will be used to access
additional information about the toy, such as the image of that type of toy and the unique qr code assigned to 
that toy
'''
try:
  cursor.execute("""
    CREATE TABLE Toys (
      id              integer AUTO_INCREMENT PRIMARY KEY,
      toyID           integer NOT NULL,
      name            VARCHAR(30) NOT NULL,
      ownerPK         integer,
      link            VARCHAR(60),
      live            boolean default false,
      interact        boolean default false,
      donations       integer default 0,
      goal            integer default 0,
      created_at      TIMESTAMP default CURRENT_TIMESTAMP
    );
  """)
  print("TOYS TABLE CREATED!!!!!!")
except:
  print("Toys table already exists. Not recreating it.")

db.close()