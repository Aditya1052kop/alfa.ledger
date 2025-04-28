import streamlit as st
import time
import hashlib

# Initialize session state to persist blockchain across interactions
if "blockchain" not in st.session_state:
    st.session_state.blockchain = []

# Function to create a block
def create_block(index, data, previous_hash):
    block = {
        "index": index,
        "data": data,
        "timestamp": time.time(),
        "previous_hash": previous_hash
    }
    return block

# Function to generate hash for a block
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to add a block
def add_block(data):
    previous_block = st.session_state.blockchain[-1]
    new_index = previous_block["index"] + 1
    new_hash = generate_hash(previous_block)
    new_block = create_block(new_index, data, new_hash)
    st.session_state.blockchain.append(new_block)

# Create genesis block if blockchain is empty
if not st.session_state.blockchain:
    genesis_block = create_block(1, "First Ticket Booking", "0")
    st.session_state.blockchain.append(genesis_block)

# Title
st.title("🚌 Bus Ticket Booking Blockchain")

# Input form to add a new ticket
st.subheader("📥 Add a New Ticket Booking")
with st.form("booking_form", clear_on_submit=True):
    ticket_id = st.number_input("Ticket ID", step=1, min_value=1)
    customer_name = st.text_input("Customer Name")
    bus_route = st.text_input("Bus Route")
    departure_time = st.text_input("Departure Time (e.g., 2025-05-01 08:00)")
    seat_number = st.text_input("Seat Number")
    submitted = st.form_submit_button("Add Booking")

    if submitted:
        if customer_name and bus_route and departure_time and seat_number:
            new_data = {
                "ticket_id": ticket_id,
                "customer_name": customer_name,
                "bus_route": bus_route,
                "departure_time": departure_time,
                "seat_number": seat_number
            }
            add_block(new_data)
            st.success("✅ Booking added to blockchain.")
        else:
            st.error("❗Please fill in all fields.")

# Show the blockchain
st.subheader("🔗 Blockchain Ledger")

for block in st.session_state.blockchain:
    st.write(f"**Block Index:** {block['index']}")
    st.json(block["data"])
    st.write(f"Timestamp: {block['timestamp']}")
    st.write(f"Previous Hash: {block['previous_hash']}")
    st.write(f"Current Hash: {generate_hash(block)}")
    st.markdown("---")
