import earthquake_report as er
import os

def test_get_earthquake_data():
    expected = True
    known_file_name = 'data\earthquake_data.atom'
    if os.path.exists(known_file_name) == True:
        actual = os.path.exists(known_file_name) 
    else:
        er.get_earthquake_data(known_file_name)
        actual = os.path.exists(known_file_name)
    assert expected == actual

def test_parse_earthquake_data():
    atom_file = 'data\earthquake_data.atom'
    actual = er.parse_earthquake_data(atom_file)[0][1]
    expected = '68 km NE of Barcelona, Philippines'
    assert expected == actual

def test_create_earthquake_report():
    expected = ['Magnitude,Count\n','<1.0,2886\n','>1.0-2.5,4940\n','>2.5-4.5,1111\n','>4.5+,466\n']
    in_atom_file = r'data\\earthquake_data.atom'
    out_csv_file = r'data\\magnitude_count.csv'
    if os.path.exists(in_atom_file) == True:
        er.create_earthquake_report(in_atom_file, out_csv_file)
    else:
        er.get_earthquake_data(in_atom_file)
        er.create_earthquake_report(in_atom_file, out_csv_file)
    with open(out_csv_file) as outfile:
      actual = outfile.readlines()
    assert expected == actual

def test_write_kml():
    expected = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Placemark>
    <name>Magnitude: 5.2</name>
    <description>Location: 68 km NE of Barcelona, Philippines
Latitude: 8.5186
Longitude: 126.946</description>
    <Point>
      <coordinates>126.946,8.5186,0</coordinates>
    </Point>
  </Placemark>"""
    in_atom_filename = 'data\earthquake_data.atom'
    out_kml_filename = 'data\earthquake_data.kml'
    er.write_kml(in_atom_filename, out_kml_filename)
    with open(out_kml_filename) as infile:
        kml = infile.read()
        actual = kml[:kml.find('/Placemark') + 11]
    assert actual == expected
    
    script_folder = os.path.dirname(os.path.abspath(__file__))
    earthquake_data_kml = os.path.join(script_folder, out_kml_filename)
    # os.startfile(earthquake_data_kml)
    