####
# This script demonstrates how to query the Metadata API using the Tableau
# Server Client.
#
# To run the script, you must have installed Python 2.7.9 or later.
####


import argparse
import getpass
import logging
import requests

from datetime import time

import tableauserverclient as TSC


def main():
    #Set the query https://help.tableau.com/current/api/metadata_api/en-us/docs/meta_api_examples.html
    query = """
    {
        databases{
            id
            name
        }
    }
    """

    parser = argparse.ArgumentParser(description='Creates sample schedules for each type of frequency.')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')
    parser.add_argument('--sitename', '-n', help='fghdhr')
    args = parser.parse_args()
    

    password = getpass.getpass("Password: ")

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    tableau_auth = TSC.TableauAuth(args.username, password, args.sitename)
    server = TSC.Server(args.server)
    server.version = '3.3'

    with server.auth.sign_in(tableau_auth):
        #Query the Metadata API and store the response in resp
        resp = server.metadata.query(query)
        datasources = resp['data']
        
        
        

            

if __name__ == '__main__':
    main()
    