#!/usr/bin/env python3

"""A small script to display the SARS-CoV-2 incidence change in the EU.
It uses data provided by the EU. This data is © ECDC [2005-2021].
The map used is from Wikimedia Commons and is © Nordwestern, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0

Copyright: (C) 2021 Michael Bemmerl
License: MIT License (see COPYING)
SPDX-License-Identifier: MIT

Requirements:
- Python >= 3.8
- pandas
For viewing the results:
- a webbrowser with JavaScript enabled and SVG support

Tested with Python 3.8.2 & pandas 1.2.0
"""

import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import os.path
from datetime import datetime

# https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country
data_url = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv'
svg_url = 'https://upload.wikimedia.org/wikipedia/commons/0/05/Blank_map_of_Europe_%28without_disputed_regions%29.svg'
days = 7            # Number of days used for the calculation of the average incidence
red = '#c00000'     # Color code for red
green = '#00c000'   # Color code for green


def get_cases(country, backlook):
    """Returns the sum of all cases for the specified country and number of days in the past.
    This is always done for the period of seven days."""
    
    # The country code of Greece is 'EL' in the data.
    if country == 'GR':
        country = 'EL'
    temp = data.query('geoId == "{0}"'.format(country))
    temp = temp.head(7 + backlook).tail(7)
    
    return temp.cases.sum()


def get_countries_in_dataset():
    """"Returns all countries available in the data."""
    
    list = data.geoId.drop_duplicates().to_list()
    
    # The country code of Greece is 'EL' in the data.
    if 'EL' in list:
        list.remove('EL')
        list.append('GR')
    
    list.sort()
    
    return list


def calc_incidence(cases, pop):
    """Calculates the incidence value with the population and cases specified."""
    return cases / pop * 100000


# Retrieve the data published for the EU
urllib.request.urlretrieve(data_url, "data.csv")

# Retrieve the map SVG if not already downloaded
if not os.path.isfile("map.svg"):
    urllib.request.urlretrieve(svg_url, "map.svg")

# Read the cases and the population data
data = pd.read_csv('data.csv')
pop_data = pd.read_csv('countries.csv')

countries = get_countries_in_dataset()

# Initialize XML element tree
svg = ET.parse('map.svg')
root_node = svg.getroot()

# Start with generating the HTML file with the results...
html = open('results.html', 'w')
html.write('<!doctype html>\n')
html.write('<html lang="en">\n')
html.write('<head><title>Incidence change in the EU</title><script src="sorttable.js"></script>')
html.write('<style>td { border: 1px solid #a2a9b1; }</style></head>\n')
html.write('<body>\n')
html.write('<img src="map-edited.svg" alt="Map" />\n')
html.write('<table class="sortable" style="border-collapse: collapse; width: 680px;">\n')
html.write('<tr><th>Country</th><th>Name</th><th>Latest incidence</th><th>Average incidence<br />')
html.write('in the last {0} days</th><th>Change in<br />the last {0} days</th></tr>\n'.format(days))

# Iterate through all available countries
for country in countries:
    # Get the population
    pop = pop_data.query('Code == "{0}"'.format(country)).iloc[0]['Population']
    last_cases = []
    
    # Calculate the incidence for the last n days
    for backlook in range(0, days):
        cases = get_cases(country, backlook)
        last_cases.append(calc_incidence(cases, pop))
    last_cases.reverse()
    
    oldest = last_cases[0]
    latest = last_cases[-1]
    average = sum(last_cases) / days
    change = average / oldest * 100 - 100    # Percentage of change between the oldest and average incidence
    
    print('country {0}; average {2:.1f}; change {1:+.0f} %'.format(country, change, average))
    
    # Get the XML element corresponding to the country
    country_node = root_node.findall('.//*[@id="{0}"]'.format(country.lower()))[0]
    style = country_node.attrib['style']
    
    # Replace the gray color regarding to the sign of the percentaged change
    if change > 0:
        country_node.attrib['style'] = style.replace('#c0c0c0', red)
    elif change < 0:
        country_node.attrib['style'] = style.replace('#c0c0c0', green)
    
    name = pop_data.query('Code == "{0}"'.format(country)).iloc[0]['Name']
    html.write('<tr><td>{0}</td><td>{1}</td><td>{2:.1f}</td><td>{3:.1f}</td>'.format(country, name, latest, average))
    html.write('<td sorttable_customkey="{0:.0f}">{0:+.0f} %</td></tr>\n'.format(change))

# Finish editing the SVG and the HTML.
svg.write('map-edited.svg')

html.write('</table>')
html.write('<p>Report created at {0}.</p>'.format(datetime.now()))
html.write('</body></html>\n')
html.close()
