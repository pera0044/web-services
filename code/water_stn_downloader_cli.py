# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:        water_stn_downloader_cli.py
#
# Purpose:     Client to water_stn_downloader module.  This script sets the
#              attributes and calls the method to download and save a
#              response to a RESTful request to a file
#
# Author:      Brigitte and Lizan
#
# Created:     dd/mm/yyyy
# ------------------------------------------------------------------------------

import os
import sys
import water_stn_downloader as wsd

# Path to folder containing this script and make it the current folder
#
_script_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(_script_folder)

def main():
    # TODO: Check for command line parameter containing output JSON file name
    # If no file is specified, print 
    # Usage:  water_stn_downloader_cli.py <out_json_file>
    # and exit the script (i.e. sys.exit(0))
    if len(sys.argv) < 2:
        print('Usage:  water_stn_downloader_cli.py <out_json_file>')
        sys.exit(0)

    # TODO: set wsd.out_json_filename to the command-line argument
    wsd.out_json_filename = sys.argv[1]

    # TODO: Set the wsd.url to the RESTful API endpoint.  
    # That is http:// to the last character before the parameters 
    # (i.e. the "?")
    # For long urls, use string concatenation or line continuation to limit
    # statement length to 80 char or less
    #
    wsd.url = 'https://maps-cartes.ec.gc.ca/arcgis/rest/services/CESI_FGP_All_Layers/MapServer/6/query'

    # TODO: Set the wsd.params argument where
    # key = name of the string query parameter and
    # value = content assigned to the query parameter
    #
    wsd.params = {'f':'json', 'where': 'OBJECTID>0', 'outFields': '*'}

    # TODO: Call wsd.download_to_file()
    #       and set the return value to a variable named status
    #
    status = wsd.download_to_file()

    # TODO:  Print a message to inform the user what as happened
    # Based on the value of status, if the file downloaded successfully,
    # print "Download successful to wsd.out_json_filename"
    # If the file did not download successfully, print the status value
    if status == 'OK':
        print("Download successful to wsd.out_json_filename")
    else:
        print(status)

if __name__ == '__main__':
    main()