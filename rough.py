# from urllib.parse import urlparse

# x = urlparse("https://docs.streamlit.io/develop/api-reference")
# print(x.netloc)
# print(x.scheme)


# x = [
#     ('2024-09-29', 'raeon.in', 'in', 'Not Working'),
# ('2024-09-29', 'dotwaveshop.in', 'in', 'Not Working'),
# ('2024-09-29', 'contemplations02.in', 'in', 'Not Working'),
# ('2024-09-29', 'contemplations02.in', 'in', 'Not Working'),
# ('2024-09-29', 'doublegk.in', 'in', 'Not Working')
# ]

# for i in x:
#     i.append("dkj")
# print(x)

# import sqlite3 as sq

# conn = sq.connect('web_scraper.db')
# cur = conn.cursor()
# query = f"select * from DOMAIN_LINKS limit 10"
# data = list(cur.execute(query))
# # print(data)
# date = [i[0] for i in data]
# domain_link = [f'https://{i[1]}' for i in data]
# tld = [i[2] for i in data]
# status = [i[3] for i in data]

# print(type(data[0][3]))

import random

x = int(random.random()*10000)
print(x)