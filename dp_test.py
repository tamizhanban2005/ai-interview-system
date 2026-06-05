import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ai_interview_system"
)

print("Database Connected Successfully")