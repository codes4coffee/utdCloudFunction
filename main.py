from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from flask import Response
import json
import os
import unicodedata


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def get_name_from_email(email):
    page = urlopen(Request('https://www.utdallas.edu/directory/includes/directories.class.php?dirType=displayname&dirSearch='+email+'&dirAffil=All&dirDept=All&dirMajor=All&dirSchool=All',
                        headers={'User-Agent': 'Mozilla'}))
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.find('h3')
    print(name)
    if name is None:
        name = ''
    else:
        name = name.get_text()
    return name

outFile = open('emails-w-names.csv', 'w')
outFile.write('email, name\n')
with open('subscriber-emails.txt', 'r') as file:
    for line in file:
        outLine = remove_control_characters(line) + ',"' + get_name_from_email(remove_control_characters(line)) + '"\n'
        outFile.write(outLine)
outFile.close()
print("Finished :)")