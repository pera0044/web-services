import water_stn_converter as wsc
import csv


def create_sampling_report(in_json_filename, out_csv_filename):
    wsc.in_json_filename = in_json_filename
    wsc.out_csv_filename = out_csv_filename 
    list_of_tuples_sampling_freq = wsc.get_sampling_frequencies()
    rows = []
    header = ['Sampling Frequency', 'Station Count']
    for element in list_of_tuples_sampling_freq:
        rows.append(list(element))
    with open(out_csv_filename, 'w', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)