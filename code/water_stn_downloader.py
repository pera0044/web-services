# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:        water_stn_downloader_client.py
#
# Purpose:     Client to water_stn_downloader module.  This script sets the
#              attributes and calls the method to download and save a
#              response to a RESTful request to a file
#
# Author:      Brigitte and Lizan
#
# Created:     dd/mm/yyyy
# ------------------------------------------------------------------------------

import requests
from requests import HTTPError

url = ''
params = {}
out_json_filename = ''

def download_to_file():
    """Save the response of a RESTful request to a file.  The following global
    attributes are used:
        url = The base URL to the RESTful service
        params = Python dictionary of key value pairs for query parameters
        out_json_filename = file where response to RESTful request will be
                            saved. """

    try:
        response = requests.get(url, params, stream=True, timeout=30)
        response.raise_for_status()
        with open(out_json_filename, 'wb') as out_file:
            # Iterate through the response in 1 MB chunks
            #
            for chunk in response.iter_content(chunk_size=1024*1024):
                # Write each chunk out to the .json file ...
                #
                out_file.write(chunk)
    except HTTPError as http_err:
        return 'HTTPError: {}'.format(http_err)
    except Exception as err:
        return 'Error:'.format(err.message)
    else:
        return 'OK'

if __name__ == '__main__':
    main()