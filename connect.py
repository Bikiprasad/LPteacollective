import random
import streamlit as st
import psycopg2
import pandas as pd
from customers import get_customers, insert_customer
from factoryRate import insert_factory_rate, fetch_factory_rate,update_collection_rate
from dailycollectiondata import get_dailycollectiondata, insert_dailycollectiondata, fetch_todays_collection_data
from datetime import datetime

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 10px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)   

#globalvariables
#quality types will be option of 3 : First Quality, Second Quality, General 
quality_types = ["First Quality", "Second Quality", "General"]
customers = get_customers()
#customer name will be displayed in the select box
#assuming the first column is Customer ID
customer_options = [customer[0] for customer in customers]  # Assuming the first column is Customer ID



st.sidebar.title('🍃 Navigation')
initial_sidebar_state="collapsed"   
page = st.sidebar.radio(
    "",
    ['🏠 Home', '➕ Add Customer', '📝 Daily Collection', '📊 Collection History', '📈 Statistics', '₹ Daily Rates']
)

if page == '🏠 Home':
    st.set_page_config(page_title="LP Green Leafs", page_icon="🍃",
    initial_sidebar_state="collapsed" )
    st.title("🍃 LP Green Leafs 🍃 ")

    #todays collection data
    todays_collection_data = fetch_todays_collection_data()
    todays_collection_data = pd.DataFrame(
        todays_collection_data,
        columns=[
            "Collection Data ID", "Collection Date", "Customer ID", "Agent ID",
            "Weight (kg)", "Collection Time", "Rate per kg", "Quality", "Amount", "Water Percentage"
        ]
    )

    todays_date = datetime.now().strftime("%d %B, %Y")
    st.subheader(f"Today's Date: {todays_date}")
    col1, col2, col3 = st.columns(3)

    # Add content to each column
    with col1:
        st.metric("Total Customers", len(customers),delta=0, delta_color="normal")

    with col2:
        st.metric("Total Collection Today", len(todays_collection_data),delta=-10, delta_color="normal")

    with col3:

        #sum of all weight of todays collection data
        total_weight = todays_collection_data["Weight (kg)"].sum()
        st.metric("Today's Total Weight", f"{total_weight:.2f}",delta=0, delta_color="normal")

    
    with st.expander("Today's Collection Data", expanded=False):
        todays_collection_data = pd.DataFrame(todays_collection_data, columns=["Collection Data ID", "Collection Date", "Customer ID", "Agent ID", "Weight (kg)", "Collection Time", "Rate per kg", "Quality", "Amount", "Water Percentage"])
        # Display only relevant columns
        display_columns = ["Collection Date", "Customer ID", "Weight (kg)", "Quality"]
        st.write("Today's Collection Data:")
        
        if todays_collection_data is not None:
            st.dataframe(todays_collection_data[display_columns])
        else:
            st.error("No collection data found for today .")
        


elif page == '➕ Add Customer':
    st.title("Customer Management") 
    st.write("Add a new customer to the database.")
    with st.form("Insert Customer", clear_on_submit=True):
        #customerid = st.text_input("Customer ID", value="", placeholder="Enter Customer ID")
        customerid= None
        customername = st.text_input("Customer Name", value="", placeholder="Enter Customer Name")
        customermobilenumber = st.text_input("Mobile Number", value="", placeholder="Enter Mobile Number")
        customeraddress = st.text_input("Address", value="", placeholder="Enter Address")
        advanceamount = st.number_input("Advance Amount (optional)", min_value=0.0, format="%.2f", value=0.0)
        dateofjoining = st.date_input("Date of Joining", value=None)
        agentid = st.number_input("Agent ID", min_value=1)

        if st.form_submit_button("Submit") and customername and dateofjoining and customeraddress:
            insert_customer(customername, customermobilenumber, customeraddress, advanceamount, dateofjoining, agentid)
            st.success("Customer inserted successfully")

    #loaded_data from the customers table will be displayed below
    with st.expander("Customers List", expanded=False):
        
        customer_data = get_customers()
        if customer_data is None:
            st.error("No customer data found or an error occurred.")
        else:
            customer_data = pd.DataFrame(customer_data, columns=["Customer ID", "Customer Name", "Mobile Number", "Address", "Advance Amount", "Date of Joining", "Agent ID"])
            st.dataframe(customer_data)

elif page == '📝 Daily Collection':

    
    st.title("Daily Collection Data")
    customersdata = pd.DataFrame(
        customers,
        columns=["Customer ID", "Customer Name", "Mobile Number", "Address", "Advance Amount", "Date of Joining", "Agent ID"]
    )
    customer_name = [customer[1] for customer in customers]
    customername1 = st.selectbox("Select Customer", options=customer_name, index=0)
    selected_df = customersdata[customersdata['Customer Name'] == customername1 ]
    extractedid = selected_df['Customer ID'].values[0]
    st.write(f"Customer ID: {extractedid}")
    customerid = int(extractedid)  # Use the extracted customer ID for insertion
    #insert daily collection data
    #generate a unique collectiondataid based on the current date
    collectiondataid = datetime.now().strftime("%Y%m%d")
        #random number generate
    collectiondataid += str(random.randint(1000, 9999))
    with st.form("Insert Daily Collection Data", clear_on_submit=True):
        
        #make collectiondataid read-only
        st.text_input("Collection Data ID", value=collectiondataid, disabled=True)
        #collectiondataid = st.text_input("Collection Data ID", value="", placeholder="Enter Collection Data ID")
        collectiondate = st.date_input("Collection Date", value=None)
        agentid = st.number_input("Agent ID", min_value=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f", value=0.0)
        collectiontime = datetime.now().time()
        rate = st.number_input("Rate per kg", min_value=0.0, format="%.2f", value=0.0)
        quality = st.selectbox("Quality", options=quality_types, index=0)
        amount = st.number_input("Amount", min_value=0.0, format="%.2f", value=0.0)
        waterpercent = st.number_input("Water Percentage (%)", min_value=0, max_value=100, value=0)

        if st.form_submit_button("Submit Collection Data"):
            insert_dailycollectiondata(collectiondataid, collectiondate, customerid, agentid, weight, collectiontime, rate, quality, amount, waterpercent)
            st.success("Daily collection data inserted successfully")
            collectiondataid = None  # Reset collectiondataid after submission

    #fetch daily collection data
    st.write("You can also retrieve daily collection data using the function get_dailycollectiondata()")
    dailycollectiondatabtn = st.button("Fetch Daily Collection Data")
    if dailycollectiondatabtn:
        st.write("Daily Collection Data:")
        daily_collection_data = get_dailycollectiondata()
        if daily_collection_data is None:
            st.error("No daily collection data found or an error occurred.")
        else:
            daily_collection_data = pd.DataFrame(daily_collection_data, columns=["Collection Data ID", "Collection Date", "Customer ID", "Agent ID", "Weight (kg)", "Collection Time", "Rate per kg", "Quality", "Amount", "Water Percentage"])
            st.dataframe(daily_collection_data)


elif page == '📊 Collection History':
    customersdata = pd.DataFrame(
        customers,
        columns=["Customer ID", "Customer Name", "Mobile Number", "Address", "Advance Amount", "Date of Joining", "Agent ID"]
    )
    customer_name = [customer[1] for customer in customers]
    # customername1 = st.selectbox("Select Customer", options=customer_name, index=0)
    # selected_df = customersdata[customersdata['Customer Name'] == customername1 ]
    # extractedid = selected_df['Customer ID'].values[0]
    # st.write(f"Selected Customer ID: {extractedid}")
    # customerid = int(extractedid) 
    # Layout with 3 columns
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        customer_filter = st.multiselect(
            'Filter by Customer',
            options=['All'] + customersdata['Customer Name'].tolist(),
            default='All'
        )

    with col2:
        date_filter_type = st.radio('Date Filter Type', ['Single Date', 'Date Range'], horizontal=True)

    with col3:
        st.write("")  # spacer

    # Date filter input
    if date_filter_type == 'Single Date':
        selected_date = st.date_input('Select Date', datetime.today().date())
    else:
        date_range = st.date_input('Select Date Range', [datetime.today().date(), datetime.today().date()])

    # --- Load and format collection data ---
    collection_df = get_dailycollectiondata()

    collection_df = pd.DataFrame(
        collection_df,
        columns=[
            "Collection Data ID", "Collection Date", "Customer ID", "Agent ID",
            "Weight (kg)", "Collection Time", "Rate per kg", "Quality", "Amount", "Water Percentage"
        ]
    )

    # Convert 'Collection Date' to date format
    collection_df['Collection Date'] = pd.to_datetime(collection_df['Collection Date']).dt.date

    # --- Apply Date Filter ---
    if date_filter_type == 'Single Date':
        collection_df = collection_df[collection_df['Collection Date'] == selected_date]
    else:
        start_date, end_date = date_range
        collection_df = collection_df[
            (collection_df['Collection Date'] >= start_date) &
            (collection_df['Collection Date'] <= end_date)
        ]

    # --- Apply Customer Filter ---
    if 'All' not in customer_filter:
        customer_ids = customersdata[customersdata['Customer Name'].isin(customer_filter)] 
        customer_ids = customer_ids['Customer ID'].tolist()
        collection_df = collection_df[collection_df['Customer ID'].isin(customer_ids)]

    # --- Display Filtered Data ---
    st.subheader("Filtered Collection Data")
    st.dataframe(collection_df)

    # --- Display Summary Statistics ---
    if not collection_df.empty:
        total_weight = collection_df['Weight (kg)'].sum()
        total_amount = collection_df['Amount'].sum()

        st.metric("Total Weight Collected", f"{total_weight:.2f} kg")
        collection_df["Weight (kg)"] = pd.to_numeric(collection_df["Weight (kg)"], errors='coerce')
        collection_df["Rate per kg"] = pd.to_numeric(collection_df["Rate per kg"], errors='coerce')

        # Calculate total amount collected
        total_amount = collection_df["Weight (kg)"] * collection_df["Rate per kg"]  # Assuming average rate for total amount
        amount = int(total_amount.sum())
        st.metric("Total Amount (₹)", int(amount))
    else:
        st.warning("No data available for the selected filters.")

elif page == '📈 Statistics':
    st.title("Statistics")
    st.write("This section will display various statistics related to the collection data.")
    
    # Fetch today's collection data
    todays_collection_data = fetch_todays_collection_data()
    if todays_collection_data is None:
        st.error("No collection data found for today.")
    else:
        todays_collection_data = pd.DataFrame(
            todays_collection_data,
            columns=["Collection Data ID", "Collection Date", "Customer ID", "Agent ID", "Weight (kg)", "Collection Time", "Rate per kg", "Quality", "Amount", "Water Percentage"]
        )

        # Calculate total weight
        total_weight = todays_collection_data["Weight (kg)"].sum()
        st.metric("Total Weight Collected Today (kg)", f"{total_weight:.2f}")

        todays_collection_data["Weight (kg)"] = pd.to_numeric(todays_collection_data["Weight (kg)"], errors='coerce')
        todays_collection_data["Rate per kg"] = pd.to_numeric(todays_collection_data["Rate per kg"], errors='coerce')

        # Calculate total amount collected
        total_amount = todays_collection_data["Weight (kg)"] * todays_collection_data["Rate per kg"]  # Assuming average rate for total amount
        amount = int(total_amount.sum())
        st.metric("Total Amount Collected Today (₹)", int(amount))


elif page == '₹ Daily Rates':
    #form to insert factory rate
    st.title("Factory Rate Management")
    with st.form("Insert Factory Rate", clear_on_submit=True):
        factoryrateid = datetime.now().strftime("%Y%m%d") + str(random.randint(1000, 9999))
        factoryid = st.number_input("Factory ID", min_value=1)
        ratedate = st.date_input("Rate Date", value=None)
        factoryrate = st.number_input("Factory Rate", min_value=0.0, format="%.2f", value=0.0)
        totalamount = 0
        agentid = st.number_input("Agent ID", min_value=1)
        quality = st.selectbox("Quality", options=quality_types, index=0)   
        if st.form_submit_button("Submit Factory Rate"):
            insert_factory_rate(factoryrateid, factoryid, ratedate, factoryrate, totalamount, agentid, quality)
            st.success("Factory rate inserted successfully")
            update_collection_rate(factoryrate, ratedate, agentid, quality)
            factoryrateid = None
