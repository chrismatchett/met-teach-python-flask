import os
import xmltodict, json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
import re

download = False

if download:

    req = Request("https://ratings.food.gov.uk/open-data/en-gb")
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, "html.parser")

    links = []

    for item in soup.select('a[href^="http://ratings.food.gov.uk/OpenDataFiles"]'):
        links.append(item.get('href'))

    print(links)

    os.chdir('./xml')

    for link in links:
        filename = link.rsplit('/', 1)[-1]
        print("Downloading %s to %s..." % (link, filename) )
        urlretrieve(link, filename)
        print("Done")

combine = True

if combine:
    ni_data = []

    for f in os.listdir('./xml/NI'):
        with open('./xml/NI/' + f, 'r') as myfile:
            obj = xmltodict.parse(myfile.read())
            ni_data.append(obj['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail'])

    ni_json = json.dumps(ni_data)

    f = open("ni_combined.json", "w")
    f.write(ni_json)
    f.close()

    with open('ni_combined.json', 'r') as f:
      ni_json = json.load(f)

    for region in ni_json:
        for business in region:
            print(business["BusinessName"])
