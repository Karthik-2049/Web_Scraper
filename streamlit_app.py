from scraper import *
import streamlit as st
from bs4 import BeautifulSoup as bs
import requests
import time

st.session_state['domain'] = ""


def stream_data(data):
    for letter in list(data):
        yield letter + ""
        time.sleep(0.005)

st.title("WEB :blue[SCRAPER]")
domain = st.text_input("Paste the url", value = st.session_state['domain'])



if(st.button("Scrape")):
    try:
        if(domain==""):
            st.write("No url provided")
        else:
            if("https://" not in domain):
                domain = "https://"+domain
            Info = requests.get(domain)
            soup = bs(Info.text, 'html.parser')
            # print(soup)

            if(soup):  
                #Title
                st.markdown("<h2 style='color:#78a0e1;'>Title</h2>", unsafe_allow_html=True)
                st.write_stream(stream_data(get_title(soup)))
                ## Headings
                headings = get_headings(soup)
                col1, col2 = st.columns(2)
                col1.markdown("<h2 style='color:#78a0e1;'>H1 Tags</h2>", unsafe_allow_html=True)
                col2.markdown("<h2 style='color:#78a0e1;'>H2 Tags</h2>", unsafe_allow_html=True)
                f1 = col1.container(height = 300)
                f2 = col2.container(height = 300)
                for i in headings['h1']:
                    f1.write_stream(stream_data(i))
                for i in headings['h2']:
                    f2.write_stream(stream_data(i))

                ##Open Graph data
                st.markdown("<h2 style='color:#78a0e1;'>Open Graph Data</h2>", unsafe_allow_html=True)
                og_data = get_open_graph(soup)
                st.write_stream(stream_data(f"Title : {og_data['og_title']}"))
                st.write_stream(stream_data(f"Description : {og_data['og_description']}"))
                st.write_stream(stream_data(f"Image_URL : {og_data["og_image"]}")
                )

                ## Images
                st.markdown("<h2 style='color:#78a0e1;'>Images</h2>", unsafe_allow_html=True)
                Image_container = st.container(height = 400)
                x1, x2, x3 = Image_container.columns(3)
                images = get_images(soup)
                if images == ["No Images Found"]:
                    Image_container.write_stream(stream_data(images[0]))
                else:
                    parsed_url = urlparse(domain)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
                    # print(images)
                    images_new = []
                    for i in images:
                        if i.find('https')==-1:
                            images_new.append(base_url+i)
                        else:
                            images_new.append(i)

                    n = len(images_new)
                    for i in range(0,n,3):
                        x1.image(images_new[i], width = 200)
                        if(i+1<n) : x2.image(images_new[i+1], width = 200)
                        if(i+2<n) :x3.image(images_new[i+2], width = 200)
                        

                ##LINKS 
                col1, col2 = st.columns(2)
                col1.markdown("<h2 style='color:#78a0e1;'>Internal Links</h2>", unsafe_allow_html=True)
                col2.markdown("<h2 style='color:#78a0e1;'>External Links</h2>", unsafe_allow_html=True)
                f1 = col1.container(height = 400)
                f2 = col2.container(height = 400)
                links = get_links(soup,domain)
                for i in set(links['internal_links']):
                    f1.write_stream(stream_data(i))
                for i in set(links['external_links']):
                    f2.write_stream(stream_data(i))

                ##Social Media Links
                st.markdown("<h2 style='color:#78a0e1;'>Social Media Links</h2>", unsafe_allow_html=True)
                s_m_links = get_social_media_links(soup)
                for i in s_m_links:
                    st.write_stream(stream_data(i))
                
                ##SEO Keywords
                st.markdown("<h2 style='color:#78a0e1;'>SEO Keywords</h2>", unsafe_allow_html=True)
                key = get_seo_keywords(soup)
                if(key==["No Keywords Found"]):
                    st.write_stream(stream_data(key[0]))
                else:
                    for i in key:
                        st.write_stream(stream_data(i['content']))

                ##Contact Info
                col1, col2 = st.columns(2)
                col1.markdown("<h2 style='color:#78a0e1;'>Emails</h2>", unsafe_allow_html=True)
                col2.markdown("<h2 style='color:#78a0e1;'>Phone Numbers</h2>", unsafe_allow_html=True)
                contact = get_contact_info(soup)
                for i in contact['emails']:
                    col1.write_stream(stream_data(i))
                for i in contact['phone_numbers']:
                    col2.write_stream(stream_data(i))

   

    except Exception as e:
        print(e)
        st.write("Connection timed out for the provided url")







