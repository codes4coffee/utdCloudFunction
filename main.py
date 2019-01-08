from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from flask import Response
import json
import os

print (os.environ['TESTING'])
if os.environ['TESTING'] == 'true':
    soup = BeautifulSoup(open('testPage.html'), 'html.parser')
else:
    page = urlopen(Request('https://www.utdallas.edu/services/transit/garages/_code.php',
                           headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page, 'html.parser')

parkingStructures = ['Parking Structure 1', 'Parking Structure 3', 'Parking Structure 4']

def getParkingSpaces(request):
    final_list = []
    # List the amount of spots for every parking structure 1 - 4
    for structure in parkingStructures:
        jsonObj = {'structure': structure}
        parkingTable = soup.find('table', attrs={'summary':structure})
        tableData = parkingTable.tbody  # the sub-table for a single parking structure
        for child in tableData:
            if hasattr(child, 'attrs'):

                # Get the permit type of the space and strip out the type from the html tag
                color = str(child.td.next_sibling.next_sibling)[11:]
                print(color)
                level = str(child.td)[19:]
                color = color[:color.find('"')]
                level = level[:level.find('<')]
                color = color + '-' + level

                numSpace = str(child.td.next_sibling.next_sibling.next_sibling.next_sibling.contents[0])
                if numSpace[0] == '<':
                    jsonObj[color] = 0
                else:
                    jsonObj[color] = int(numSpace)
        final_list.append(jsonObj)
        resp = Response(json.dumps(final_list), mimetype='application/json')
    return resp
