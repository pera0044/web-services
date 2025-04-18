# Example Web Services
water_stn_downloader_cli.py 
- Sends a RESTful request to the maps-cartes.ec.gc.ca server and save the response to a local JSON file.

water_stn_converter.py 
- Has a method to load a JSON file as Python dictionary (load_json_file_to_dict), and to extract relevant values from each feature in that JSON file (get_values_from_feature).
- The function called get_sampling_frequencies returns a list of tuples.  Each tuple will contain the sampling frequency and the count from the JSON file.

sampling_freq.py
- Creates a report in CSV format. The report includes two columns: “Sampling Frequency” and “Station Count” where “Sampling Frequency” contains a list of unique values from “Sampling_Frequency” attribute in the API response (e.g. Yearly, Seasonal, etc.)
