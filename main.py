from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from flask import Response
import json
import os

if os.environ['TESTING'] == 'true':
    soup = BeautifulSoup(open('testPage.html'), 'html.parser')
else:
    page = urlopen(Request('https://www.utdallas.edu/services/transit/garages/_code.php',
                           headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page, 'html.parser')

parkingStructures = ['Parking Structure 1', 'Parking Structure 3', 'Parking Structure 4']

def getParkingSpaces(request):
    finalList = []
    # List the amount of spots for every parking structure 1 - 4
    for structure in parkingStructures:
        jsonObj = {'structure': structure}
        jsonObj['hasInfo'] = True; # Sometimes garage isn't available. Consumers need to know this
        jsonObj['green'] = 0;
        jsonObj['gold'] = 0;
        jsonObj['orange'] = 0;
        jsonObj['purple'] = 0;
        jsonObj['pay_by_space'] = 0;
        parkingTable = soup.find('table', attrs={'summary':structure})

        if parkingTable is None:
            jsonObj['hasInfo'] = False # Needed to add this in because sometimes all the garage info isn't available
            continue;

        tableData = parkingTable.tbody # The sub-table for a single parking structure
        for child in tableData:
            if hasattr(child,'attrs'):
                color = str(child.td.next_sibling.next_sibling)[11:] # Get the permit type of the space and strip out the type from the html tag
                color = color[:color.find('"')]
                color = color[8:]
                numSpace = str(child.td.next_sibling.next_sibling.next_sibling.next_sibling.contents[0])
                if numSpace[0] != '<':
                    jsonObj[color] = jsonObj[color] + int(numSpace)
        finalList.append(jsonObj)
    resp = Response(json.dumps(finalList), mimetype='application/json')
    return resp
