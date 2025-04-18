# Example Web Services
water_stn_downloader_cli.py sends a RESTful request to the maps-cartes.ec.gc.ca server and save the response to a local JSON file.

water_stn_converter.py has a method to load a JSON file as Python dictionary (load_json_file_to_dict), and to extract relevant values from each feature in that JSON file (get_values_from_feature).
