import streamlit as st
import psycopg2
import pandas as pd
from config import load_config

from datetime import datetime

#fetch daily collection data for todays date
def fetch_todays_collection_data():
    """ Retrieve today's daily collection data """
    today = datetime.now().strftime("%Y-%m-%d")
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM collectiondata WHERE collectiondate = %s", (today,))
                rows = cur.fetchall()
                return rows
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_dailycollectiondata():
    """ Retrieve data from the daily collection table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM collectiondata")
                rows = cur.fetchall()
                return rows
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_dailycollectiondata(collectiondataid,collectiondate,customerid,agentid,weight,collectiontime,rate,quality,amount,waterpercent):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
#insert into collectiondata table with the given parameterscollectiondataid,collectiondate,customerid,agentid,weight,collectiontime,rate,quality,amount,waterpercent
                cur.execute("INSERT INTO collectiondata (collectiondataid,collectiondate,customerid,agentid,weight,collectiontime,rate,quality,amount,waterpercent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (collectiondataid, collectiondate, customerid, agentid, weight, collectiontime, rate, quality, amount, waterpercent))
                conn.commit()
                print("Customer inserted successfully")
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)