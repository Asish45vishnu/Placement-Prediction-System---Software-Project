import mysql.connector
import streamlit as st

# Establish a connection to MySQL Server

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="seproj"


)
mycursor=mydb.cursor()
print("Connection Established")

st.write("Hello")
mycursor.execute("select * from demo")
result = mycursor.fetchall()
for row in result:
    st.write(row)
