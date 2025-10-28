import streamlit as st
import psycopg2
import datetime

# Database connection setup
def get_connection():
    return psycopg2.connect(
        host='localhost',
        dbname='Real-Estate-Management',
        user='postgres',
        password='test@123',
        port='5432'
    )

def execute_query(query, params=None, fetch=False):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall() if fetch else None
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def get_dropdown_data(query):
    result = execute_query(query, fetch=True)
    return [row[0] for row in result] if result else []

# Session management
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

st.title("Real Estate Management Application")

# Login or Register Page
if st.session_state.user_type is None:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        user_type = st.selectbox("Login As", ["Agent", "Renter"], key="login_type")
        if st.button("Login"):
            table = "Agents" if user_type == "Agent" else "Prospective_Renters"
            key = "Agent" if user_type == "Agent" else "Renter"
            result = execute_query(f"SELECT * FROM {table} WHERE {key}_Email = %s;", (email,), fetch=True)
            if result:
                st.session_state.user_email = email
                st.session_state.user_type = user_type
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials. Please register first.")

    with tab2:
        st.subheader("User Registration")
        user_type = st.selectbox("Select User Type", ["Agent", "Renter"], key="register_type")
        email = st.text_input("Email", key="register_email")
        name = st.text_input("Name", key="register_name")

        if user_type == "Agent":
            job_title = st.text_input("Job Title")
            agency = st.text_input("Agency")
            phone = st.text_input("Phone")
        else:
            budget = st.number_input("Budget", min_value=0)
            preferred_location = st.text_input("Preferred Location")
            move_in_date = st.date_input("Move-in Date")

        if st.button("Register"):
            execute_query("INSERT INTO User_type (type) VALUES (%s) ON CONFLICT DO NOTHING;", (user_type,))
            execute_query("INSERT INTO Users (Email, Name, User_type) VALUES (%s, %s, %s);", (email, name, user_type))

            if user_type == "Agent":
                execute_query("INSERT INTO Agents (Agent_Email, job_title, Agency, phone) VALUES (%s, %s, %s, %s);",
                              (email, job_title, agency, phone))
                st.success("Agent registered successfully. Please login.")
            else:
                execute_query("INSERT INTO Prospective_Renters (Renter_Email, Budget, preferred_location, move_in_date) VALUES (%s, %s, %s, %s);",
                              (email, budget, preferred_location, move_in_date))
                st.success("Renter registered successfully. Please login.")

    st.stop()

# Sidebar and Logout Option
menu = ["Search Properties", "Book Property", "View Bookings"]
if st.session_state.user_type == "Agent":
    menu.insert(0, "Add Property")
    menu.insert(1, "Modify/Delete Property")
if st.session_state.user_type == "Renter":
    menu.insert(0, "Manage Payment/Address")

menu.append("Logout")
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Logout":
    st.session_state.user_type = None
    st.session_state.user_email = None
    st.success("You have been logged out.")
    st.rerun()

# Register
if choice == "Register":
    st.subheader("User Registration")

    user_type = st.selectbox("Select User Type", ["Agent", "Renter"])
    email = st.text_input("Email")
    name = st.text_input("Name")

    if user_type == "Agent":
        job_title = st.text_input("Job Title")
        agency = st.text_input("Agency")
        phone = st.text_input("Phone")
    else:
        budget = st.number_input("Budget", min_value=0)
        preferred_location = st.text_input("Preferred Location")
        move_in_date = st.date_input("Move-in Date")

    if st.button("Register"):
        execute_query("INSERT INTO User_type (type) VALUES (%s) ON CONFLICT DO NOTHING;", (user_type,))
        execute_query("INSERT INTO Users (Email, Name, User_type) VALUES (%s, %s, %s);", (email, name, user_type))

        if user_type == "Agent":
            execute_query("INSERT INTO Agents (Agent_Email, job_title, Agency, phone) VALUES (%s, %s, %s, %s);",
                          (email, job_title, agency, phone))
            st.success("Agent registered successfully.")
        else:
            execute_query("INSERT INTO Prospective_Renters (Renter_Email, Budget, preferred_location, move_in_date) VALUES (%s, %s, %s, %s);",
                          (email, budget, preferred_location, move_in_date))
            st.success("Renter registered successfully.")

# Add property
elif choice == "Add Property":
    st.subheader("Add New Property")

    agent_email = st.session_state.user_email

    property_type = st.selectbox("Property Type", ["House", "Apartment", "Commercial"])
    location = st.text_input("Location")
    description = st.text_area("Description")
    city = st.text_input("City")
    state = st.text_input("State")
    price = st.number_input("Price", min_value=0)
    availability = st.text_input("Availability")
    sqft = st.number_input("Square Footage", min_value=0)
    no_of_rooms = st.number_input("Number of Rooms", min_value=0)
    neighborhood_id = st.number_input("Neighborhood ID", min_value=0)

    if st.button("Add Property"):
        execute_query("INSERT INTO prop_type (type) VALUES (%s) ON CONFLICT DO NOTHING;", (property_type,))
        execute_query("""
            INSERT INTO Property (property_type, location, description, city, state, price, availability, sqft, no_of_rooms, neighborhood_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (property_type, location, description, city, state, price, availability, sqft, no_of_rooms, neighborhood_id))
        st.success("Property added successfully.")

# Modify/Delete property
elif choice == "Modify/Delete Property":
    st.subheader("Modify or Delete Your Property Listings")
    agent_email = st.session_state.user_email
    properties = execute_query("SELECT property_id, description FROM Property;", (agent_email,), fetch=True)

    if properties:
        selected_id = st.selectbox("Select Property ID to Edit/Delete", [f"{p[0]} - {p[1][:30]}..." for p in properties])
        property_id = int(selected_id.split(" - ")[0])
        action = st.radio("Action", ["Edit", "Delete"])

        if action == "Edit":
            fields = execute_query("SELECT location, description, city, state, price, availability, sqft, no_of_rooms FROM Property WHERE property_id = %s", (property_id,), fetch=True)[0]
            location = st.text_input("Location", fields[0])
            description = st.text_area("Description", fields[1])
            city = st.text_input("City", fields[2])
            state = st.text_input("State", fields[3])
            price = st.number_input("Price", min_value=0, value=fields[4])
            availability = st.text_input("Availability", fields[5])
            sqft = st.number_input("Square Footage", min_value=0, value=fields[6])
            rooms = st.number_input("Number of Rooms", min_value=0, value=fields[7])

            if st.button("Update Property"):
                execute_query("""
                    UPDATE Property SET location=%s, description=%s, city=%s, state=%s, price=%s, availability=%s, sqft=%s, no_of_rooms=%s
                    WHERE property_id = %s
                """, (location, description, city, state, price, availability, sqft, rooms, property_id))
                st.success("Property updated successfully.")

        elif action == "Delete":
            if st.button("Delete Property"):
                execute_query("DELETE FROM Property WHERE property_id = %s", (property_id,))
                st.success("Property deleted successfully.")
    else:
        st.info("You don't have any properties to modify or delete.")

# Search properties
elif choice == "Search Properties":
    st.subheader("Search Available Properties")

    location = st.text_input("Location")
    min_price = st.number_input("Minimum Price", min_value=0, value=0)
    max_price = st.number_input("Maximum Price", min_value=0, value=1000000)
    min_rooms = st.number_input("Minimum Bedrooms", min_value=0, value=0)
    max_rooms = st.number_input("Maximum Bedrooms", min_value=0, value=10)
    property_type = st.selectbox("Property Type", ["Any", "House", "Apartment", "Commercial"])
    order_by = st.radio("Order Results By", ["Price", "Number of Rooms"])

    if st.button("Search"):
        query = """
            SELECT Property_id, property_type, location, description, city, state, price, availability, sqft, no_of_rooms
            FROM Property
            WHERE location ILIKE %s AND price BETWEEN %s AND %s AND no_of_rooms BETWEEN %s AND %s
            AND property_type ILIKE %s
        """
        order_column = "price" if order_by == "Price" else "no_of_rooms"
        query += f" ORDER BY {order_column}"

        property_type_filter = "%" if property_type == "Any" else property_type
        params = (f"%{location}%", min_price, max_price, min_rooms, max_rooms, property_type_filter)

        results = execute_query(query, params, fetch=True)

        if results:
            for row in results:
                st.write(f"Property ID: {row[0]} | Type: {row[1]} | Location: {row[2]}")
                st.write(f"Description: {row[3]}")
                st.write(f"City: {row[4]}, State: {row[5]}")
                st.write(f"Price: {row[6]} | Availability: {row[7]} | Sqft: {row[8]} | Rooms: {row[9]}")
                st.markdown("---")
        else:
            st.info("No matching properties found.")

# Book property
elif choice == "Book Property":
    st.subheader("Book a Property")

    renter_email = st.session_state.user_email
    user_type = st.session_state.user_type

    property_ids = get_dropdown_data("SELECT property_id FROM Property WHERE availability = 'Available';")
    property_id = st.selectbox("Select Property ID", property_ids)

    agent_emails = get_dropdown_data("SELECT Agent_Email FROM Agents;")
    agent_email = st.selectbox("Agent Email", agent_emails)

    start_date = st.date_input("Rental Start Date", datetime.date.today())
    end_date = st.date_input("Rental End Date", datetime.date.today())

    if user_type == "Agent":
        st.info("As an agent, you can book properties for renters using a default card.")
        renter_email_for_agent = st.text_input("Enter Renter Email")
        if st.button("Book for Renter"):
            if start_date >= end_date:
                st.warning("Start date must be before end date.")
            else:
                duration_days = (end_date - start_date).days
                price = execute_query("SELECT price FROM Property WHERE property_id = %s", (property_id,), fetch=True)[0][0]
                total_cost = duration_days * price

                default_card_number = 9999888877776666
                existing_card = execute_query("SELECT card_number FROM Credit_cards WHERE card_number = %s", (default_card_number,), fetch=True)
                if not existing_card:
                    address_id = execute_query("SELECT Address_id FROM Addresses WHERE User_email = %s LIMIT 1", (renter_email_for_agent,), fetch=True)
                    if not address_id:
                        st.error("No billing address found for the renter. Please add one before proceeding.")
                    else:
                        address_id = address_id[0][0]
                        execute_query("INSERT INTO Credit_cards (card_number, expiry_date, cvv, billing_address_id) VALUES (%s, %s, %s, %s);", (default_card_number, '01/30', '000', address_id))

                execute_query("""
                    INSERT INTO Booking (property_id, booking_date, card_number, agent_id, renter_id, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (property_id, datetime.date.today(), default_card_number, agent_email, renter_email_for_agent, start_date, end_date))

                execute_query("UPDATE Property SET availability = 'Occupied' WHERE property_id = %s", (property_id,))
                st.success(f"Booking successful for {renter_email_for_agent}. Total Cost: ${total_cost}")

    elif user_type == "Renter":
        address_result = execute_query("SELECT Address_id FROM Addresses WHERE User_email = %s;", (renter_email,), fetch=True)
        card_numbers = execute_query("SELECT card_number FROM Credit_cards WHERE billing_address_id IN (SELECT Address_id FROM Addresses WHERE User_email = %s);", (renter_email,), fetch=True) if address_result else []

        if address_result and card_numbers:
            card_number_list = [row[0] for row in card_numbers]
            card_number = st.selectbox("Select Credit Card", card_number_list)

            if st.button("Book Property"):
                if start_date >= end_date:
                    st.warning("Start date must be before end date.")
                else:
                    duration_days = (end_date - start_date).days
                    price = execute_query("SELECT price FROM Property WHERE property_id = %s", (property_id,), fetch=True)[0][0]
                    total_cost = duration_days * price

                    execute_query("""
                        INSERT INTO Booking (property_id, booking_date, card_number, agent_id, renter_id, start_date, end_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (property_id, datetime.date.today(), card_number, agent_email, renter_email, start_date, end_date))

                    execute_query("UPDATE Property SET availability = 'Occupied' WHERE property_id = %s", (property_id,))
                    st.success(f"Booking successful! Total Cost: ${total_cost}")
        else:
            st.warning("Please add a billing address and a credit card before booking.")

# Cancel booking for renters and agents
elif choice == "View Bookings":
    st.subheader("View Your Bookings")
    user_email = st.session_state.user_email
    user_type = st.session_state.user_type

    if user_type == "Renter":
        bookings = execute_query("""
            SELECT b.booking_id, p.property_id, p.location, p.price, b.booking_date, b.agent_id, b.start_date, b.end_date
            FROM Booking b
            JOIN Property p ON b.property_id = p.property_id
            WHERE b.renter_id = %s;
        """, (user_email,), fetch=True)

        if bookings:
            for book in bookings:
                st.write(f"Booking ID: {book[0]} | Property ID: {book[1]} | Location: {book[2]} | Price: {book[3]}")
                st.write(f"Booking Date: {book[4]} | Agent: {book[5]} | Rental Period: {book[6]} to {book[7]}")
                if st.button(f"Cancel Booking {book[0]}"):
                    execute_query("DELETE FROM Booking WHERE booking_id = %s", (book[0],))
                    execute_query("UPDATE Property SET availability = 'Available' WHERE property_id = %s", (book[1],))
                    st.success("Booking canceled and refund initiated to your saved payment method.")
                st.markdown("---")
        else:
            st.info("No bookings found.")

    elif user_type == "Agent":
        bookings = execute_query("""
            SELECT b.booking_id, p.property_id, p.location, b.renter_id, b.booking_date, b.card_number, b.start_date, b.end_date
            FROM Booking b
            JOIN Property p ON b.property_id = p.property_id
            WHERE b.agent_id = %s;
        """, (user_email,), fetch=True)

        if bookings:
            for book in bookings:
                st.write(f"Booking ID: {book[0]} | Property ID: {book[1]} | Location: {book[2]}")
                st.write(f"Renter: {book[3]} | Date: {book[4]} | Card: {book[5]} | Rental Period: {book[6]} to {book[7]}")
                if st.button(f"Cancel Booking {book[0]}"):
                    execute_query("DELETE FROM Booking WHERE booking_id = %s", (book[0],))
                    execute_query("UPDATE Property SET availability = 'Available' WHERE property_id = %s", (book[1],))
                    st.success("Booking canceled and refund issued to the renter.")
                st.markdown("---")
        else:
            st.info("No bookings found.")
            
# Manage payment and address
elif choice == "Manage Payment/Address":
    st.subheader("Manage Payment and Address Information")
    renter_email = st.session_state.user_email

    action = st.radio("Action", ["Add Address", "Delete Address", "Add Card", "Delete Card", "View Saved Addresses & Cards"])

    if action == "Add Address":
        st.subheader("Add New Billing Address")
        street = st.text_input("Street")
        city = st.text_input("City")
        state = st.text_input("State")
        zip_code = st.number_input("ZIP Code", min_value=10000, max_value=99999)
        if st.button("Add Address"):
            execute_query("""
                INSERT INTO Addresses (street, city, state, zip_code, User_email)
                VALUES (%s, %s, %s, %s, %s);
            """, (street, city, state, zip_code, renter_email))
            st.success("Address added successfully.")

    elif action == "Delete Address":
        addresses = execute_query("SELECT Address_id FROM Addresses WHERE User_email = %s", (renter_email,), fetch=True)
        if addresses:
            address_ids = [str(addr[0]) for addr in addresses]
            selected = st.selectbox("Select Address ID to Delete", address_ids)
            card_check = execute_query("SELECT card_number FROM Credit_cards WHERE billing_address_id = %s", (selected,), fetch=True)
            if card_check:
                st.warning("Cannot delete this address as it is linked to a credit card. Please delete the card first.")
            elif st.button("Delete Address"):
                execute_query("DELETE FROM Addresses WHERE Address_id = %s", (selected,))
                st.success("Address deleted successfully.")
        else:
            st.info("No address found to delete.")

    elif action == "Add Card":
        address_result = execute_query("SELECT Address_id FROM Addresses WHERE User_email = %s", (renter_email,), fetch=True)
        if address_result:
            address_ids = [addr[0] for addr in address_result]
            address_id = st.selectbox("Select Billing Address", address_ids)
        else:
            st.subheader("Enter Billing Address (Required)")
            street = st.text_input("Street")
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.number_input("ZIP Code", min_value=10000, max_value=99999)

        card_number = st.text_input("Card Number")
        expiry_date = st.text_input("Expiry Date (MM/YYYY)")
        cvv = st.text_input("CVV")

        if st.button("Add Card"):
            if not address_result:
                # Insert new address first
                execute_query("""
                    INSERT INTO Addresses (street, city, state, zip_code, User_email)
                    VALUES (%s, %s, %s, %s, %s);
                """, (street, city, state, zip_code, renter_email))
                address_id = execute_query("SELECT Address_id FROM Addresses WHERE street = %s AND city = %s AND state = %s AND zip_code = %s AND User_email = %s ORDER BY Address_id DESC LIMIT 1", (street, city, state, zip_code, renter_email), fetch=True)[0][0]

            execute_query("""
                INSERT INTO Credit_cards (card_number, expiry_date, cvv, billing_address_id)
                VALUES (%s, %s, %s, %s);
            """, (card_number, expiry_date, cvv, address_id))
            st.success("Card and billing address added successfully.")

    elif action == "Delete Card":
        cards = execute_query("SELECT card_number FROM Credit_cards c JOIN Addresses a ON c.billing_address_id = a.Address_id WHERE a.User_email = %s", (renter_email,), fetch=True)
        if cards:
            card_numbers = [str(c[0]) for c in cards]
            selected_card = st.selectbox("Select Card Number to Delete", card_numbers)
            if st.button("Delete Card"):
                execute_query("DELETE FROM Credit_cards WHERE card_number = %s", (selected_card,))
                st.success("Card deleted successfully.")
        else:
            st.info("No credit card found to delete.")

    elif action == "View Saved Addresses & Cards":
        st.subheader("Your Saved Addresses")
        addresses = execute_query("SELECT Address_id, street, city, state, zip_code FROM Addresses WHERE User_email = %s", (renter_email,), fetch=True)
        if addresses:
            for addr in addresses:
                st.write(f"ID: {addr[0]} | {addr[1]}, {addr[2]}, {addr[3]} - {addr[4]}")
        else:
            st.info("No saved addresses found.")

        st.subheader("Your Saved Credit Cards")
        cards = execute_query("SELECT card_number, expiry_date FROM Credit_cards c JOIN Addresses a ON c.billing_address_id = a.Address_id WHERE a.User_email = %s", (renter_email,), fetch=True)
        if cards:
            for card in cards:
                st.write(f"Card: {card[0]} | Expiry: {card[1]}")
        else:
            st.info("No saved credit cards found.")