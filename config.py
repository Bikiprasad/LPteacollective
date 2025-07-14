from configparser import ConfigParser
import streamlit as st

host = st.secrets["host"]
database = st.secrets["database"]   
user = st.secrets["user"]
password = st.secrets["password"]

def load_config():
    config = {}
    config['host'] = host
    config['database'] = database
    config['user'] = user
    config['password'] = password
    
    return config

if __name__ == '__main__':
    config = load_config()
    print(config)
