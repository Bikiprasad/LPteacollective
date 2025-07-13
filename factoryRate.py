import streamlit as st
import psycopg2
import pandas as pd
from config import load_config

from datetime import datetime

#fetch daily collection data for todays date
def fetch_factory_rate():
    """ Retrieve today's daily collection data """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM factoryrate")
                rows = cur.fetchall()
                return rows
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_factory_rate(factoryrateid,factoryid,ratedate,factoryrate,totalamount,agentid,quality):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("Insert INTO factoryrate (factoryrateid, factoryid, ratedate, factoryrate, totalamount, agentid, quality) VALUES (%s, %s, %s, %s, %s, %s, %s)", (factoryrateid, factoryid, ratedate, factoryrate, totalamount, agentid, quality))
                conn.commit()
                print("Customer inserted successfully")
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update_collection_rate(rate, collectiondate, agentid, quality):
    """ Update the collection rate for a specific date and agent """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE collectiondata SET rate = %s WHERE collectiondate = %s AND agentid = %s AND quality = %s", (rate, collectiondate, agentid, quality))
                conn.commit()
                print("Collection rate updated successfully")
        conn.close()
        print("Connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)