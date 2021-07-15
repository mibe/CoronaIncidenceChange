#!/usr/bin/env python3

import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import re

# https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country
data_url = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv'
svg_url = 'https://upload.wikimedia.org/wikipedia/commons/0/05/Blank_map_of_Europe_%28without_disputed_regions%29.svg'
days = 7
red = '#c00000'
green = '#00c000'

def get_cases(country, backlook):
    if country == 'GR':
        country = 'EL'
    temp = data.query('geoId == "{0}"'.format(country))
    temp = temp.head(7 + backlook).tail(7)
    
    return temp.cases.sum()

def get_countries_in_dataset():
    list = data.geoId.drop_duplicates().to_list()
    
    if 'EL' in list:
        list.remove('EL')
        list.append('GR')
    
    list.sort()
    
    return list

def calc_incidence(cases, pop):
    return cases / pop * 100000

#urllib.request.urlretrieve(data_url, "data.csv")
urllib.request.urlretrieve(svg_url, "map.svg")

data = pd.read_csv('data.csv')
pop_data = pd.read_csv('countries.csv')

countries = get_countries_in_dataset()

svg = ET.parse('map.svg')
root_node = svg.getroot()

html = open('results.html', 'w')
html.write('<!doctype html>\n')
html.write('<html lang="en">\n')
html.write('<head><title>Incidence change in the EU</title><script src="sorttable.js"></script><style>td { border: 1px solid #a2a9b1; }</style></head>\n')
html.write('<body>\n')
html.write('<img src="map-edited.svg" alt="Map" />\n')
html.write('<table class="sortable" style="border-collapse: collapse; width: 680px;">\n')
html.write('<tr><th>Country</th><th>Name</th><th>Average incidence<br />in the last {0} days</th><th>Change in<br />the last {0} days</th></tr>\n'.format(days))

for country in countries:
    pop = pop_data.query('Code == "{0}"'.format(country)).iloc[0]['Population']
    last_cases = []
    for backlook in range(0, days):
        cases = get_cases(country, backlook)
        last_cases.append(calc_incidence(cases, pop))
    last_cases.reverse()
    
    first = last_cases[0]
    average = sum(last_cases) / days
    change = average / first * 100 - 100
    
    print('country {0}; average {2:.1f}; change {1:+.0f} %'.format(country, change, average))
    country_node = root_node.findall('.//*[@id="{0}"]'.format(country.lower()))[0]
    style = country_node.attrib['style']
    
    if change > 0:
        country_node.attrib['style'] = style.replace('#c0c0c0', red)
    elif change < 0:
        country_node.attrib['style'] = style.replace('#c0c0c0', green)
    
    name = pop_data.query('Code == "{0}"'.format(country)).iloc[0]['Name']
    html.write('<tr><td>{0}</td><td>{1}</td><td>{2:.1f}</td><td sorttable_customkey="{3:.0f}">{3:+.0f} %</td></tr>\n'.format(country, name, average, change))

svg.write('map-edited.svg')

html.write('</table>')
html.write('</body></html>\n')
html.close()
