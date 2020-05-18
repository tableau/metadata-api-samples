####
# This script can be used for getting more information about CustomSQL prevelance on a Tableau Server/Site.
#
# This script was written on Python 3.7.6 and was not tested to work on other versions of Python.
# This script 
####


import argparse
import getpass
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import csv

from datetime import time

import tableauserverclient as TSC

#See more examples here https://help.tableau.com/current/api/metadata_api/en-us/docs/meta_api_examples.html



def main():
    parser = argparse.ArgumentParser(description='Reports on CustomSQL statistics in the Catalog graph. Outputs data into CSV files for reporting.')
    parser.add_argument('--server', '-s', required=True, help='server address (include "http(s)://")')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')
    parser.add_argument('--sitename', '-n', help='Sitename to process CustomSQL Statistics for. This is optional and defaults to the `Default` site')

    args = parser.parse_args()

    password = getpass.getpass("Password: ")


    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    
    tableau_auth = TSC.TableauAuth(args.username, password, args.sitename)
    server = TSC.Server(args.server)
    server.add_http_options({"verify": False})
    server.use_server_version()

    with server.auth.sign_in(tableau_auth):
        logging.debug("Signed into Server")

        # resp = server.metadata.query(query)
        #Query the Metadata API and store the response in resp
        
        query = """
{ 
customSQLTablesConnection(first: 20, after: AFTER_TOKEN_SIGNAL) {
    nodes {
      id
      
      database {
        connectionType
      }

      tables {
            id
      }

      query

      columns {
        workbooks_directly_connected: referencedByFields {
          datasource {
            ... on EmbeddedDatasource {
              workbook {
                name
                id
              }
            }
          }
        }
        datasources_directly_connected: referencedByFields {
          datasource {
            ... on PublishedDatasource {
              name
              id
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""
        print("--------------------------\nBeginning to query information about CustomSQLTables on this site...")
        resp = server.metadata.query(query.replace('AFTER_TOKEN_SIGNAL', 'null'))
        workbooks = {}
        datasources = {}
        table_stats = {'num_skipped': 0, 'num_tables_seen': 0, 'num_failed_parse': 0}
        while True:
            process_page(resp, workbooks, datasources, table_stats)

            page_info = resp['data']['customSQLTablesConnection']['pageInfo']

            print("--------------------------\n Processing update:")
            print(table_stats)
            if page_info['hasNextPage']:
                resp = server.metadata.query(query.replace('AFTER_TOKEN_SIGNAL', '"' + page_info['endCursor'] + '"'))
            else:
                break

        logging.debug("{} CustomSQLTables were skipped due to unexpected data".format(table_stats['num_skipped']))
        totalCountsQuery = """
        {
        total_workbooks_count: workbooksConnection { totalCount }
        total_datasources_count: publishedDatasourcesConnection { totalCount }
        }
        """
        resp = server.metadata.query(totalCountsQuery)
        total_workbooks = resp['data']['total_workbooks_count']['totalCount']
        total_datasources = resp['data']['total_datasources_count']['totalCount']


        print("--------------------------\nFinished processing CustomSQLTables on this site... Writing to results files now")

        ## Outputting summary to customSQL-stats-summary.txt file
        with open("./customSQL-stats-summary.txt", 'w', newline='') as file:
            
            print("Total # of CustomSQLTables on site={} and {} of them ({:.2f}%) were not parsed by Catalog".format(table_stats['num_tables_seen'], table_stats['num_failed_parse'], percentify(safe_divide(table_stats['num_failed_parse'], table_stats['num_tables_seen']))), file=file)
            print("Total # of Workbooks on Site={}".format(total_workbooks), file=file)
            print("# of Workbooks using CustomSQL={} ({:.2f}% of total)".format(len(workbooks), percentify(safe_divide(len(workbooks), total_workbooks))), file=file)

            print("Total # of Published Data Sources on Site={}".format(total_datasources), file=file)
            print("# of Published Data Sources using CustomSQL={} ({:.2f}% of total)".format(len(datasources), percentify(safe_divide(len(datasources), total_datasources))), file=file)


        ## Outputting detaield data to CSV file
        filename='./customSQL-stats.csv'
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)

            columnHeaders = ['parent_content_type', 'parent_content_graph_id', 'custom_sql_graph_id', 'sql_failed_to_parse', 'query_string', 'database_type']
            csv_writer.writerow(columnHeaders)

            serialize_to_csv(csv_writer, workbooks, 'workbook')
            serialize_to_csv(csv_writer, datasources, 'published datasource') 


def safe_divide(num, denom):
    return num / denom if denom else 0

# Serializes info to a CSV file 
def serialize_to_csv(writer, collection, content_type):    
    ## Create a row per each customSQL table in each worbkook or data source
    for content_item_id in collection.keys():
        for cust_sql_table_id in collection[content_item_id]['customSQLTables'].keys():
            cust_sql_table = collection[content_item_id]['customSQLTables'][cust_sql_table_id]
            
            new_row = [content_type]
            new_row.append(content_item_id)
            new_row.append(cust_sql_table_id)
            new_row.append(cust_sql_table['sql_failed_to_parse'])
            new_row.append(cust_sql_table['query_string'])
            new_row.append(cust_sql_table['database_type'])

            writer.writerow(new_row)



def percentify(decimal):
    return decimal * 100


def process_page(response, workbooks, datasources, table_stats):
    customSQLTables = response['data']['customSQLTablesConnection']['nodes']

    for table in customSQLTables: 
        table_stats['num_tables_seen'] += 1
        table_stats['num_failed_parse'] += 1 if has_failed_sql(table) else 0

        if len(table['columns']) == 0:
            logging.debug("Table {} has no columns and will be skipped".format(table['id']))
            table_stats['num_skipped'] += 1
            continue

        if len(table['columns'][0]['workbooks_directly_connected']) == 0:
            logging.debug("Table {} has nothing in `workbooks_directly_connected` and will be skipped".format(table['id']))
            table_stats['num_skipped'] += 1
            continue

        ## this is CustomSQLTable connecting to a WB
        if bool(table['columns'][0]['workbooks_directly_connected'][0]['datasource']):
            object_id = table['columns'][0]['workbooks_directly_connected'][0]['datasource']['workbook']['id']
            process_table_for_collection(table, object_id, workbooks)

        ## This is a CustomSQLTable connecting to a PDS
        else:
            object_id = table['columns'][0]['datasources_directly_connected'][0]['datasource']['id']
            process_table_for_collection(table, object_id, datasources)


def process_table_for_collection(table, object_id, collection):
    
    ## This is first time we've seen this workbook
    if object_id not in collection:
        collection[object_id] = {}
        collection[object_id]['customSQLTables'] = {}
        collection[object_id]['customSQLTables'][table['id']] = {}
        extract_sql_table_info(table, collection[object_id]['customSQLTables'][table['id']])
    else:
        if table['id'] in collection[object_id]['customSQLTables']:
            logging.debug('Seeing same CustomSQLTable twice. Skipping adding to dictionary. Table ID: {}'.format(table['id']))
        else:
            collection[object_id]['customSQLTables'][table['id']] = {}
            extract_sql_table_info(table, collection[object_id]['customSQLTables'][table['id']])

    logging.info("Processed table id={} and added to collection".format(table['id']))


def extract_sql_table_info(source_table_dict, dest_table_dict):
    dest_table_dict['sql_failed_to_parse'] = has_failed_sql(source_table_dict)
    dest_table_dict['query_string'] = source_table_dict['query']
    dest_table_dict['database_type'] = source_table_dict['database']['connectionType']


def has_failed_sql(table):
    return False if len(table['tables']) > 0 else True            

if __name__ == '__main__':
    main()
    