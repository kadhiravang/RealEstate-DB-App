🏠 Real Estate Management Application

A Streamlit-based web application for managing real estate listings, agents, renters, bookings, and payments — powered by PostgreSQL for robust database handling.
This project was developed as part of the Database Organization (CS425) coursework and demonstrates practical application of relational database concepts in a real-world domain.

🚀 Features
👥 User Management

    - Separate login/registration for Agents and Renters
    - Secure session-based access using Streamlit session state
    - Automatic user-type detection and role-based interface

🏡 Property Management (Agents)

    - Add, edit, and delete property listings
    - Include detailed info like type, price, size, availability, and description
    - Automatically updates property status when booked

🔍 Property Search (Renters)

    - Search by location, price, rooms, and type
    - Filter and sort results dynamically
    - View detailed property data including agent and price info

🧾 Booking System

    - Renters and agents can make bookings with start/end dates
    - Automated total cost computation
    - Booking cancellation updates availability in real time

💳 Payment and Address Management

    - Add, edit, or delete billing addresses and credit cards
    - Agents can make bookings on behalf of renters using default cards
    - Integrated card–address relationship integrity checks

🗄️ Database Schema

    - The system uses PostgreSQL with multiple relational tables:

Table	Description
Users	Stores basic user details and user type
Agents	Contains agent-specific data (agency, job title, contact)
Prospective_Renters	Contains renter budget and preferences
Property	Main property listings table
Booking	Tracks all bookings and rental periods
Addresses	Stores user addresses for billing
Credit_cards	Stores encrypted card data linked to addresses
User_type, prop_type	Lookup tables ensuring referential integrity

⚙️ Tech Stack
Layer	Technology
Frontend/UI	Streamlit

Backend Logic	Python
Database	PostgreSQL
ORM/DB Access	psycopg2
Hosting (Optional)	Streamlit Cloud / Localhost

🧰 Installation & Setup

1️⃣ Clone the Repository

`git clone https://github.com/kadhiravang/RealEstate-Management.git
cd RealEstate-Management`

2️⃣ Configure PostgreSQL
Create a new PostgreSQL database named Real-Estate-Management
Update credentials inside the script:

`def get_connection():
    return psycopg2.connect(
        host='localhost',
        dbname='Real-Estate-Management',
        user='postgres',
        password='test@123',
        port='5432'
    )`

3️⃣ Install Dependencies

`pip install requirements.txt`

4️⃣ Run the Application

`streamlit run Real_Estate_Management.py`


Then open http://localhost:8501
 in your browser.
🧩 Future Enhancements
🔐 Implement user authentication with hashed passwords
📊 Add admin dashboards for property analytics
🖼️ Support property image uploads
📅 Introduce calendar-based rental period selection
☁️ Deploy using Docker + AWS RDS

🧑‍💻 Author
Kadhiravan Gopal
M.S. Artificial Intelligence – Illinois Institute of Technology
https://kadhiravang.github.io
