from urllib.parse import urlparse

x = urlparse("https://docs.streamlit.io/develop/api-reference")
print(x.netloc)
print(x.scheme)