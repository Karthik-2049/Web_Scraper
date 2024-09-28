
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlparse

def get_title(soup):
    title = soup.find('title')
    return title.text if title else "No Title Found"

def get_meta_description(soup):
    description = soup.find('meta', attrs={'name': 'description'})
    return description['content'] if description else "No Meta Description Found"

def get_open_graph(soup):
    og_title = soup.find('meta', property='og:title')
    og_description = soup.find('meta', property='og:description')
    og_image = soup.find('meta', property='og:image')

    return {
        'og_title': og_title['content'] if og_title else "No OG Title",
        'og_description': og_description['content'] if og_description else "No OG Description",
        'og_image': og_image['content'] if og_image else "No OG Image"
    }


def get_headings(soup):
    h1_tags = [h1.text.strip() for h1 in soup.find_all('h1')]
    h2_tags = [h2.text.strip() for h2 in soup.find_all('h2')]

    return {
        'h1': h1_tags if h1_tags else ["No H1 Tags Found"],
        'h2': h2_tags if h2_tags else ["No H2 Tags Found"]
    }

def get_images(soup):
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    return images if images else ["No Images Found"]


def get_links(soup, domain):
    parsed_domain = urlparse(domain).netloc

    internal_links = []
    external_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if parsed_domain in href:
            internal_links.append(href)
        else:
            external_links.append(href)

    return {
        'internal_links': internal_links if internal_links else ["No Internal Links Found"],
        'external_links': external_links if external_links else ["No External Links Found"]
    }


def get_social_media_links(soup):
    social_links = []
    social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']


    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(social in href for social in social_domains):
            social_links.append(href)

    return social_links if social_links else ["No Social Media Links Found"]

import re

def get_contact_info(soup):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d[\d -]{8,12}\d'

    emails = re.findall(email_pattern, soup.text)
    phones = re.findall(phone_pattern, soup.text)

    return {
        'emails': emails if emails else ["No Emails Found"],
        'phone_numbers': phones if phones else ["No Phone Numbers Found"]
    }

def get_seo_keywords(soup):
    keywords = soup.find_all('meta', attrs={'name': 'keywords'})
    return keywords if keywords else ["No Keywords Found"]



