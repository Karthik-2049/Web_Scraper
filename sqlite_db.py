


import sqlite3 as sq
def insertEntries(entries_list):
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS DOMAIN_LINKS
                 (date TEXT, domain_name TEXT, tld TEXT)''')
    conn.executemany('''INSERT INTO DOMAIN_LINKS (date,domain_name,tld, status) VALUES (?,?,?,?)''',entries_list)
    conn.commit()
    cur.close()
    conn.close()

def displayFirstNEntries(table_name,n):
    print(f"\nFirst {n} Entries : ")
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY DATE ASC LIMIT {n}"
    data = cur.execute(query)
    for row in data:
        print(row)
    cur.close()
    conn.close()

def displayLastNEntries(table_name,n):
    print(f"\nLast {n} Entries : ")
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY DATE DESC LIMIT {n}"
    data = list(cur.execute(query))
    for row in data[::-1]:
        print(row)
    cur.close()
    conn.close()

def lastEntryDate(table_name):
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT 1;"
    data = list(cur.execute(query))
    cur.close()
    conn.close()
    return data[0][0]

def numberOfRegisteredDomains(table_name, date):
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    query = f"Select Count(*) AS entry_count from {table_name} where date = '{date}'"
    registered_number = list(cur.execute(query))
    print(f"Number of registered domain users : {registered_number[0][0]}")

def numberOfDomains(table_name):
    conn = sq.connect('web_scraper.db')
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cur.fetchone()[0]
    conn.close()
    return row_count
