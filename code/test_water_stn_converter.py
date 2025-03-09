# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        test_water_stn_converter.py
#
# Purpose:     Tests for functions in water_stn_converter.py
#
# Author:      David Viljoen
#
# Created:     09/11/2021
#-------------------------------------------------------------------------------

import csv
import water_stn_converter as wsc
import os
import water_stn_downloader as wsd

wsc.in_json_filename = r'data\water_stn.json'
wsc.out_kml_filename = r'data\water_stn.kml'
wsc.out_csv_filename = r'data\water_stn.csv'

def test_load_json_file_to_dict():
    expected = 'Station_Name'
    data = wsc.load_json_file_to_dict()
    actual = data['displayFieldName']
    assert actual == expected


def test_get_values_from_feature():
    expected = ('01AD002', 'Saint John River at Fort Kent', '-68.59583', '47.25806')
    data =wsc.load_json_file_to_dict()
    features = data['features']
    feature = features[0]
    stn_no, stn_name, longitude, latitude = wsc.get_values_from_feature(feature)
    actual = stn_no, stn_name, longitude, latitude
    assert expected == actual


def test_json_to_csv():
    expected = ('01AD002', 'Saint John River at Fort Kent', '-68.59583', '47.25806')
    wsc.json_to_csv()
    with open(wsc.out_csv_filename) as infile:
        reader = csv.reader(infile)
        next(reader)
        actual = next(reader)
    assert expected == tuple(actual)


def test_get_placemark():
    expected = """<Placemark>
        <name>Saint John River at Fort Kent</name>
        <description>
            https://wateroffice.ec.gc.ca/report/real_time_e.html?stn=01AD002
        </description>
        <Point>
            <coordinates>-68.59583,47.25806,0</coordinates>
        </Point></Placemark>"""
    actual = wsc.get_placemark('Saint John River at Fort Kent',
                               -68.59583, 47.25806,
                               wsc._get_wateroffice_link('01AD002') )
    assert expected == actual


def test_json_to_kml():
    expected = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document><Placemark>
        <name>Saint John River at Fort Kent</name>
        <description>
            https://wateroffice.ec.gc.ca/report/real_time_e.html?stn=01AD002
        </description>
        <Point>
            <coordinates>-68.59583,47.25806,0</coordinates>
        </Point></Placemark>"""
    wsc.json_to_kml()
    with open(wsc.out_kml_filename) as infile:
        kml = infile.read()
        actual = kml[:kml.find('/Placemark') + 11]
    assert expected == actual
    # os.startfile(wsc.out_kml_filename)


def test_json_to_kmz():
    wsc.json_to_kmz()
    kmz_size = os.path.getsize(wsc.out_kml_filename.replace('.kml', '.kmz'))
    kml_size = os.path.getsize(wsc.out_kml_filename)
    assert kmz_size < kml_size
    assert kmz_size > 10000
    # os.startfile(wsc.out_kml_filename.replace('kml', 'kmz'))

def test_get_sampling_frequencies():
    expected = 682
    known_file_name = 'data\water_stn.json'
    if os.path.exists(known_file_name) == True:
        actual = wsc.get_sampling_frequencies()[0][1]
    else:
        wsd.out_json_filename = known_file_name
        wsd.url = 'https://maps-cartes.ec.gc.ca/arcgis/rest/services/CESI_FGP_All_Layers/MapServer/6/query'
        wsd.params = {'f':'json', 'where': 'OBJECTID>0', 'outFields': '*'}
        wsd.download_to_file()
        actual = wsc.get_sampling_frequencies()[0][1]  
    assert expected == actual