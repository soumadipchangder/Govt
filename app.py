import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()
firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
os.environ['FIREBASE_CREDENTIALS'] = firebase_credentials
if firebase_credentials:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set.")

# Streamlit UI
st.title("Food Distribution Management")

menu = ["Data Entry", "Admin Panel"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Data Entry":
    st.subheader("Enter Food Distribution Data")
    with st.form(key="food_form"):
        rice = st.text_input("Rice")
        musur_dal = st.text_input("Musur Dal")
        mustard_oil = st.text_input("Mustard Oil")
        iodised_salt = st.text_input("Iodised Salt")
        rte_packet = st.text_input("RTE Packet")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        food_data = {
            "Rice": rice,
            "Musur Dal": musur_dal,
            "Mustard Oil": mustard_oil,
            "Iodised Salt": iodised_salt,
            "RTE Packet": rte_packet,
            "timestamp": datetime.utcnow()
        }
        db.collection("food_distribution").add(food_data)
        st.success("Data submitted successfully!")

elif choice == "Admin Panel":
    st.subheader("Admin Panel - View Food Distribution Data")
    docs = db.collection("food_distribution").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    food_data = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    
    if food_data:
        for data in food_data:
            st.write(f"**ID:** {data['id']}")
            st.write(f"Rice: {data['Rice']}")
            st.write(f"Musur Dal: {data['Musur Dal']}")
            st.write(f"Mustard Oil: {data['Mustard Oil']}")
            st.write(f"Iodised Salt: {data['Iodised Salt']}")
            st.write(f"RTE Packet: {data['RTE Packet']}")
            st.write(f"Timestamp: {data['timestamp']}")
            st.write("---")
    else:
        st.write("No data available.")
