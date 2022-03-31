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

# Parse XML from a file object
# with open("./xml/FHRS900en-GB.xml") as file:
#    soup = BeautifulSoup(file, features="lxml-xml")
#    print(type(soup))

# with open('./xml/FHRS900en-GB.xml', 'r') as myfile:
#     obj = xmltodict.parse(myfile.read())
# print(json.dumps(obj))

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

    # for region in ni_data:
    #     for business in region:
    #         print(type(business['BusinessName']))



    # ni_data(json.dumps(obj))
    # <FHRSEstablishment xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    # <EstablishmentCollection>
    # <EstablishmentDetail>
    # ....<FHRSID>1153550</FHRSID>

    # i = 0
    # ni_combined = {}
    # for dictionary in ni_data:
    #     for l in list:
    #         ni_combined[i] = l
    #         i += 1

    # ni_json = json.dumps(ni_combined)

    # f = open("ni_combined.json", "w")
    # f.write(ni_json)
    # f.close()

# with open('ni_combined.json', 'r') as f:
#   ni_json = json.load(f)

# for key, value in ni_json.items():
#     print(key, '->', value)