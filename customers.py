import streamlit as st
import psycopg2
import pandas as pd
from config import load_config
def get_customers():
    """ Retrieve data from the customers table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customer order by customername")
                rows = cur.fetchall()
                return rows
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_customer(customername,customermobilenumber,customeraddress,advanceamount,dateofjoining,agentid):
    """ Insert a new customer into the customers table """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO customer (customername, customermobilenumber, customeraddress, advanceamount, dateofjoining, agentid) VALUES (%s, %s, %s, %s, %s, %s)", (customername, customermobilenumber, customeraddress, advanceamount, dateofjoining, agentid))
                conn.commit()
                print("Customer inserted successfully")
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)