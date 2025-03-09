import requests
from requests import HTTPError
import os
import feedparser
import water_stn_converter as wsc
import csv

def get_earthquake_data(out_atom_filename):
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.atom'
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(out_atom_filename, 'wb') as out_file:
            # Iterate through the response in 1 MB chunks
            #
            for chunk in response.iter_content(chunk_size=1024*1024):
                # Write each chunk out to the .csv file ...
                #
                out_file.write(chunk)
    except HTTPError as http_err:
        return 'HTTPError: {}'.format(http_err)
    except Exception as err:
        return 'Error:'.format(err.message)
    else:
        return 'OK'

def parse_earthquake_data(atom_file):
    parsed_dict = feedparser.parse(atom_file)
    list_of_earthquakes = []
    # Extracting the values of lat, long, magnitude, and description from the parsed distionary
    for entry in parsed_dict.entries:
        latitude = entry['where']['coordinates'][1]
        longitude = entry['where']['coordinates'][0]
        title = entry['title']
        list_title = title.split(' - ')
        list_magnitude_earthquake = list_title[0].split()
        magnitude_earthquake = float(list_magnitude_earthquake[1])
        description_of_location = list_title[1]
        tuple_earthquakes_data = (magnitude_earthquake, description_of_location, latitude, longitude)
        # List of tuples with the information of each earthquake!!!
        list_of_earthquakes.append(tuple_earthquakes_data)

    return list_of_earthquakes


def create_earthquake_report(in_atom_file, out_csv_file):
    # Creating a list of magnitudes for each earthquake in atom_file using parse_earthquake_report_function
    list_of_earthquakes = list(parse_earthquake_data(in_atom_file))
    list_magnitude_earthquakes = []
    count = 0
    for magnitude in list_of_earthquakes:
        magnitude = list_of_earthquakes[count][0]
        list_magnitude_earthquakes.append(magnitude)
        count += 1

    # Creating 4 empty lists for each magnitude condition 
    magnitude_less_1 = []
    magnitude_between_1_and_2_5 = []
    magnitude_between_2_5_and_4_5 = []
    magnitude_greater_4_5 = []

    # Looping through each magnitude in the list of magnitudes and appending the magnitude values that meet a condition to the list for that condition
    for magnitude in list_magnitude_earthquakes:
        if magnitude <= 1.0:
            magnitude_less_1.append(magnitude)
        elif 1.0 < magnitude <= 2.5:
            magnitude_between_1_and_2_5.append(magnitude)
        elif 2.5 < magnitude <= 4.5:
            magnitude_between_2_5_and_4_5.append(magnitude)
        elif magnitude > 4.5:
            magnitude_greater_4_5.append(magnitude)
    
    # Measuring the unique count of the number of earthquakes in each classification bin
    count_magnitude_less_1 = len(magnitude_less_1)
    count_magnitude_between_1_and_2_5 = len(magnitude_between_1_and_2_5)
    count_magnitude_between_2_5_and_4_5 = len(magnitude_between_2_5_and_4_5)
    count_magnitude_greater_4_5 = len(magnitude_greater_4_5)

    # Creating a dictionary that will serve as a basis for the csv file
    dict_count_earthquakes = {'<1.0':count_magnitude_less_1, '>1.0-2.5':count_magnitude_between_1_and_2_5, '>2.5-4.5':count_magnitude_between_2_5_and_4_5, '>4.5+':count_magnitude_greater_4_5}

    # Creating the magnitude count csv
    with open(out_csv_file, 'w', newline = '') as outfile:
        writer = csv.writer(outfile)
        header = ['Magnitude', 'Count']
        writer.writerow(header)
        for element in dict_count_earthquakes.items():
            writer.writerow(element)

def write_kml(in_atom_filename, out_kml_filename):
    list_of_tuples_earthquakes = parse_earthquake_data(in_atom_filename)
    with open (out_kml_filename, 'w') as kml_file:
        kml_file.write(wsc.get_kml_header())
        for earthquake_event in list_of_tuples_earthquakes:
            magnitude_earthquake = earthquake_event[0]
            description_location = earthquake_event[1]
            latitude = earthquake_event[2]
            longitude = earthquake_event[3]
            kml_file.write(get_placemark(magnitude_earthquake, description_location, longitude, latitude))
        kml_file.write(wsc.get_kml_footer())
        kml_file.close

# Placemark format string for KML Placemark elements
pm_fmt = u"""
  <Placemark>
    <name>Magnitude: {}</name>
    <description>Location: {}\nLatitude: {}\nLongitude: {}</description>
    <Point>
      <coordinates>{},{},0</coordinates>
    </Point>
  </Placemark>"""

def get_placemark(magnitude, description, longitude, latitude):
    """Return the KML Placemark element including start and end tags.
    """
    kml = pm_fmt.format(magnitude, description, latitude, longitude, longitude, latitude)
    return kml
