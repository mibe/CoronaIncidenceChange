A small script to display the SARS-CoV-2 incidence change in the EU.

# Data source
The data source for the daily cases is provided by the European Centre for Disease Prevention and Control, specifically the "[Data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)" is used. 

# Requirements
- Python 3
- [pandas](https://pandas.pydata.org/)

# Usage
## Command line
1. Install dependencies: `pip install -r requirements.txt`
2. Run the script, it will download all stuff necessary: `CoronaIncidenceChange.py`
3. Open the file `results.html` file in a webbrowser which supports SVG and has JavaScript enabled. So practically every reasonable modern one.

## Docker
```sh
docker build -t cic .
docker run --name cic_runner cic
docker cp cic_runner:/code/map-edited.svg .
docker cp cic_runner:/code/results.html .
docker rm cic_runner
```
Open the file `results.html` file in a webbrowser which supports SVG and has JavaScript enabled. So practically every reasonable modern one.

# License
This script is © 2021 Michael Bemmerl, available under the [MIT License](https://tldrlegal.com/license/mit-license). See COPYING for details.

## Third party copyright & licenses
- The cases data is © ECDC [2005-2021]
- The [map](https://commons.wikimedia.org/wiki/File:Blank_map_of_Europe_(without_disputed_regions).svg) is © Nordwestern, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- [sorttable.js](https://www.kryogenix.org/code/browser/sorttable/) is © Stuart Langridge, licensed under the [X11 license](https://tldrlegal.com/license/x11-license)
