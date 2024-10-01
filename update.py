import sqlite3
import aiohttp
import asyncio

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Function to add the 'status' column to the DOMAIN_LINKS table
def add_status_column(conn):
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE DOMAIN_LINKS ADD COLUMN status TEXT")
    conn.commit()

# Asynchronous function to check if a website is working
async def is_website_working(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return "Working"
            else:
                return "Not Working"
    except:
        return "Not Working"

# Function to gather status for a list of domain links
async def giveStatus(domain_links):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        status = await asyncio.gather(*(is_website_working(url, session) for url in domain_links))
        return status

# Function to update the status in the DOMAIN_LINKS table
def update_status(conn, domain_names, statuses):
    cursor = conn.cursor()
    for domain_name, status in zip(domain_names, statuses):
        cursor.execute("UPDATE DOMAIN_LINKS SET status = ? WHERE domain_name = ?", (status, domain_name))
    conn.commit()

# Main function to run the script
async def main():
    database = "web_scraper.db"  # Replace with your database path

    # Create a connection to the SQLite database
    conn = create_connection(database)

    # Add the 'status' column to the DOMAIN_LINKS table
    # add_status_column(conn)

    # Fetch domain names from the DOMAIN_LINKS table
    cursor = conn.cursor()
    cursor.execute("SELECT domain_name FROM DOMAIN_LINKS")
    domain_names = [row[0] for row in cursor.fetchall()]

    # Prepare domain links for checking status
    domain_links = [f"https://{domain}" for domain in domain_names]  # Assuming HTTP, adjust if needed

    # Get statuses for the domain links
    statuses = await giveStatus(domain_links)

    # Update the status in the database
    update_status(conn, domain_names, statuses)

    # Close the database connection
    conn.close()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
