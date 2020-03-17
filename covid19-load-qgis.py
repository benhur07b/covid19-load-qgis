"""
This script should be run from the Python Console inside QGIS (CTRL + ALT + P).

It adds COVID-19 confirmed cases and deaths data from
https://github.com/CSSEGISandData/COVID-19 provided by Johns Hopkins University CSSE.

Script by Ben Hur Pintor
License: GPLv3
"""

import requests
import os
import csv
from qgis.core import QgsVectorLayer, QgsProject

# Links to CSSEGISandData
CASES_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
DEATHS_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

# Path where CSVs will be downloaded and saved (can be changed)
FPATH = os.getcwd()

# Get and Save most recent CSVs
cases_r = requests.get(CASES_URL)
deaths_r = requests.get(DEATHS_URL)
cases = "{}/cases.csv".format(FPATH)
deaths = "{}/deaths.csv".format(FPATH)

with open(cases, "w") as f1:
    f1.write(cases_r.text)

with open(deaths, "w") as f2:
    f2.write(deaths_r.text)

# Load Confirmed Cases CSV to QGIS
cases_latest = next(csv.reader(open(cases)))[-1].replace("/","-")
cases_local = "file://{uri}?delimiter={delimiter}&crs=epsg:4326&xField={x}&yField={y}".format(uri=cases, delimiter=",", x="Long", y="Lat")
cases_layer = QgsVectorLayer(cases_local, "covid19-cases-as-of-{latest}".format(latest=cases_latest), "delimitedtext")
QgsProject.instance().addMapLayer(cases_layer)

#Load Deaths CSV to QGIS
deaths_latest = next(csv.reader(open(deaths)))[-1].replace("/","-")
deaths_local = "file://{uri}?delimiter={delimiter}&crs=epsg:4326&xField={x}&yField={y}".format(uri=deaths, delimiter=",", x="Long", y="Lat")
deaths_layer = QgsVectorLayer(deaths_local, "covid19-deaths-as-of-{latest}".format(latest=deaths_latest), "delimitedtext")
QgsProject.instance().addMapLayer(deaths_layer)
