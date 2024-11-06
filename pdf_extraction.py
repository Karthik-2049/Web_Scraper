
import requests
import io
from bs4 import BeautifulSoup as bs
from PyPDF2 import PdfReader
from sqlite_db import *
import aiohttp
import asyncio

def formatDate(x):
  temp = x.split('-')
  return "-".join(temp[::-1])

async def is_website_working(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return "Working"
            else:
                return "Not Working"
    except:
        return "Not Working"

async def giveStatus(domain_links):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        status = await asyncio.gather(*(is_website_working(url, session) for url in domain_links))
        return status


async def pushEntries(domain_list):
  for domain in domain_list:
    response = requests.get(domain[0])
    data = io.BytesIO(response.content)
    entries = []
    reader = PdfReader(data)
    for i in range(len(reader.pages)):
      text = reader.pages[i].extract_text()
      temp = text.split()
      start = 0
      if(i==0): start = 3
      for j in range(start,len(temp)//2):
        entries.append((domain[1],temp[2*j],temp[2*j+1]))

    urls = [f"https://{elem[1]}" for elem in entries]
    statuses = await giveStatus(urls)
    modified_entries = [(entries[i][0],entries[i][1],entries[i][2],statuses[i]) for i in range(len(urls))]
    insertEntries(modified_entries)

def pdfExtractor():
  domain = "https://registry.in/domain-creates"
  Info = requests.get(domain)
  soup = bs(Info.text, 'html.parser')

  domain_list = []
  links = soup.find_all('a')
  for link in links:
      x = str(link.get('href'))
      if x.find('.pdf')!=-1 and x.find('domain-creates')!=-1: 
        domain_list.append([x,formatDate(x[-14:-4])])  
  if(len(domain_list)==0):
    print("There are no relevant pdfs")
    return

  lastDate = lastEntryDate('domain_links')
  new_domain_list = [domain for domain in domain_list if(lastDate<domain[1])]

  if(len(new_domain_list)==0):
    print(f"Data is upto date, The last entry is at {lastDate}")
    print(numberOfDomains('DOMAIN_LINKS'))
    
    displayLastNEntries('DOMAIN_LINKS',5)
    # numberOfRegisteredDomains('DOMAIN_LINKS','2024-09-22')
    return
  pushEntries(new_domain_list)
  displayFirstNEntries('DOMAIN_LINKS',5)
  displayLastNEntries('DOMAIN_LINKS',5)


if __name__ == "__main__":
  pdfExtractor()





       
       

    



