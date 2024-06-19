import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.excute("""
CREATE TABLE IF NOT EXISTS userdata
	id INTEGER PRIMARY KEY
	username VARCHAR(255) NOT NULL
	password VARCHAR(255) NOT NULL
)
""")

useraname1 , password 1 = "Paschal123", hashlib.sha256("Paschalpassword".encode()).hexdigest()
username2 , password 2 = "John", hashlib.sha256("Iam good".encode()).hexdigest()
username3 , password 3 = "Paschal", hashlib.sha256("feeling".encode()).hexdigest()
username4 , password 4 = "Sea123", hashlib.sha256("Godlyin person".encode()).hexdigest()
username5 , password 5 = "neye123", hashlib.sha256("rideonme".encode()).hexdigest()
cur.excute("INSERT INTO userdata(username, password) VALUES (?, ?)", (username1,password1) )
cur.excute("INSERT INTO userdata(username, password) VALUES (?, ?)", (username2,password2) 
cur.excute("INSERT INTO userdata(username, password) VALUES (?, ?)", (username3,password3) 
cur.excute("INSERT INTO userdata(username, password) VALUES (?, ?)", (username4,password4) 
cur.excute("INSERT INTO userdata(username, password) VALUES (?, ?)", (username5,password5) 


conn.commit()


