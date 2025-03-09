import sampling_freq as sf
import csv

def test_create_sampling_report():
    in_json_filename = r'data\water_stn.json'
    out_csv_filename = r'data\water_stn.csv'
    sf.create_sampling_report(in_json_filename,out_csv_filename)
    with open (out_csv_filename) as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            if row[0] == 'Yearly':
                actual = row[1]
    expected = '682'
    assert actual == expected
