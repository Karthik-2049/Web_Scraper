import requests
import io
from bs4 import BeautifulSoup as bs
from PyPDF2 import PdfReader
from sqlite_db import *
from pdf_extraction import *
import aiohttp
import asyncio
from datetime import datetime, timedelta

# Generate dates and URLs
def formatDate(x):
    temp = x.split('-')
    return "-".join(temp[::-1])

start_date = datetime(2023, 4, 5)
end_date = datetime(2024, 9, 17)
date_list = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range((end_date - start_date).days + 1)]
res = [[f"https://registry.in/system/files/domain-creates_{formatDate(i)}.pdf", i] for i in date_list]

# Asynchronous function for fetching PDFs and extracting data
async def fetch_pdf(session, url,num):
    try:
        async with session.get(url[0]) as response:
            if response.status != 200:
                print(f"Failed to retrieve {url[0]}, Status Code: {response.status}")
                return []

            data = io.BytesIO(await response.read())
            reader = PdfReader(data)
            entries = []

            for i in range(len(reader.pages)):
                text = reader.pages[i].extract_text()
                temp = text.split()
                start = 3 if i == 0 else 0
                for j in range(start, len(temp) // 2):
                    entries.append((url[1], temp[2 * j], temp[2 * j + 1]))
            
            # Print the date of the PDF after processing is complete
            print(f"{num}. Date: {url[1]}")
            return entries

    except Exception as e:
        print(f"Error processing {url[0]}: {e}")
        return []

# Main async function to handle multiple PDFs
async def exec(domain_list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pdf(session, domain_list[i],i) for i in range(len(domain_list))]
        results = await asyncio.gather(*tasks)
        
        # Flatten the list of entries
        all_entries = [entry for result in results for entry in result if result]

    # Batch URLs for status check and database insertion
    urls = [f"https://{elem[1]}" for elem in all_entries]
    statuses = await giveStatus(urls)

    # Prepare modified entries with statuses
    modified_entries = [(all_entries[i][0], all_entries[i][1], all_entries[i][2], statuses[i]) for i in range(len(urls))]
    insertEntries(modified_entries)
    print(f"Processed {len(domain_list)} PDFs successfully")

# Run the exec function for a subset of domains (adjust limit for testing)
asyncio.run(exec(res))
