import streamlit as st
from views import supervisor, manager

st.set_page_config(page_title="LineTwin", layout="wide")
st.title("LineTwin: Spatiotemporal Digital Twin")

view = st.sidebar.radio("Select Persona", ["Floor Supervisor", "Plant Manager"])

if view == "Floor Supervisor":
    supervisor.show()
else:
    manager.show()
