# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:04:00 2018

@author: Alessandro Gianfelici
"""

__version__ = '0.1.0'

import bs4
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

myDict = {}

def getNumPages(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser') 
    tmp = html_soup.find_all('span', class_ = 'headline__review-count')
    NrevTot = int(tmp[0].text)
    Nrec1pag = len(html_soup.find_all('div', class_ = 'review-card'))
    return NrevTot//Nrec1pag + 1

def trustPilotParser(input_url : str):
    """
    This function take the url of the trustpilot page of the company you are interested in 
    and return as output a pandas dataframe containing the following columns:

     - company_name
     - review_title
     - review_text
     - review_stars

    :param input_url: The url of the trustpilot page of the company you are interested in.
    :type input_url: str
    :return: reviews
    :rtype: pd.DataFrame
    """   
    titolo = []
    testo = []
    stelle = []
    nPages = getNumPages(input_url)
    for page in range(1,nPages):
        print(f"Processing page {page} of {nPages-1}...")
        url = f'{input_url}&page={page}'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        recensioni = html_soup.find_all('div', class_ = 'review-card')
        for recensione in recensioni:
            exec(f"global myDict; myDict = {recensione.script.contents[0][1:-1]}")
            titolo.append(myDict['reviewHeader'])
            testo.append(myDict['reviewBody'])
            stelle.append(myDict['stars'])
    data = {'company_name' : myDict['businessUnitDisplayName'],
            'review_title' : titolo,
            'review_text' : testo,
            'review_stars' : stelle}
    return pd.DataFrame(data).drop_duplicates()