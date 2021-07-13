#!/usr/bin/env python3

import pandas as pd
import urllib.request

source_url = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv'
svg_url = 'https://upload.wikimedia.org/wikipedia/commons/0/05/Blank_map_of_Europe_%28without_disputed_regions%29.svg'
days = 7

def get_population(country):
    if country == 'AT':
        return 8932664
    elif country == 'BE':
        return 11492641
    elif country == 'BG':
        return 6951482
    elif country == 'CY':
        return 848300
    elif country == 'CZ':
        return 10700000
    elif country == 'DE':
        return 83155031
    elif country == 'DK':
        return 5840045
    elif country == 'EE':
        return 1300000
    elif country == 'EL':
        return 10718565
    elif country == 'ES':
        return 47100000
    elif country == 'FI':
        return 5536146
    elif country == 'FR':
        return 67422000
    elif country == 'HR':
        return 4058165
    elif country == 'HU':
        return 9769526
    elif country == 'IE':
        return 4900000
    elif country == 'IS':
        return 361000
    elif country == 'IT':
        return 60026546
    elif country == 'LI':
        return 38650
    elif country == 'LT':
        return 3029118
    elif country == 'LU':
        return 626108
    elif country == 'LV':
        return 1900000
    elif country == 'MT':
        return 520700
    elif country == 'NL':
        return 17474693
    elif country == 'NO':
        return 5391369
    elif country == 'PL':
        return 37798655
    elif country == 'PT':
        return 10295909
    elif country == 'RO':
        return 19400000
    elif country == 'SE':
        return 10327589
    elif country == 'SI':
        return 2081912
    elif country == 'SK':
        return 5457873
    else:
        return 0

def get_cases(data, country, backlook):
    temp = data.query('geoId == "{0}"'.format(country))
    temp = temp.head(7 + backlook).tail(7)
    
    return temp.cases.sum()

def get_countries_in_dataset(data):
    list = data.geoId.drop_duplicates().to_list()
    list.sort()
    
    return list

def calc_incidence(cases, pop):
    return cases / pop * 100000

# urllib.request.urlretrieve(source_url, "data.csv")
urllib.request.urlretrieve(svg_url, "map.svg")

data = pd.read_csv('data.csv')

countries = get_countries_in_dataset(data)
changes = {}

for country in countries:
    pop = get_population(country)
    last_cases = []
    for backlook in range(0, days):
        cases = get_cases(data, country, backlook)
        last_cases.append(calc_incidence(cases, pop))
    last_cases.reverse()
    
    first = last_cases[0]
    average = sum(last_cases) / days
    percent = average / first * 100 - 100
    
    changes[country] = percent
    
changes = sorted(changes.items(), key=lambda x: x[1])
    
for country, change in changes:
    print('Country: {0} change {1:+.0f} %'.format(country, change))
