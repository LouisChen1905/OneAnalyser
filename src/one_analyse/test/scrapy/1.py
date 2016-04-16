# Number of datasets currently listed on data.gov
import requests
from lxml import html

response = requests.get('http://www.data.gov/')
doc = html.fromstring(response.text)
link = doc.cssselect('small a')[0]
print(link.text)