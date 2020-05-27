# Overview  

The custom-sql-statistics python script uses the Metadata API to find how much Custom SQL is used on a Tableau Site. It will report statistics of what percentage of Workbooks and Data Sources are using Custom SQL. It also tracks how many Custom SQL queries were not accepted/supported by the Catalog lineage parser. Please refer to the [official documentation for Catalog's support for Custom SQL](https://help.tableau.com/current/pro/desktop/en-us/customsql.htm#tableau-catalog-support-for-custom-sql) for more information on what SQL is intended to be supported by Catalog.

This script reports its statistics in two ways:
1. Outputs a brief summary of how much Custom SQL is on the site and how much was supported. This will be outputted to `customSQL-stats-summary.txt`.
2. Outputs data to `customSQL-stats.csv` that can be used for deeper analysis. **Note:** This format includes the actual SQL queries text included in the Data Source or Workbook (it does not include any data returned by the query, just the SQL used.)

## Instructions for use
To call the script, please use the latest version of python3 and call the script like so:
```
	python3 custom-sql-statistics.py --server <http://example.com> --username <your server/site username> --sitename <only needed for non-default sites>
```
The scripts results will be outputted to two files `customSQL-stats-summary.txt` which is summary of the data, and `customSQL-stats.csv` which gives row-level data on the results. The latter can be used in Tableau for more thorough analysis.

For best results, run this script as a site or server admin so that full query data can be returned. If run as a non-admin, the `query_string` examples may be blank due to permissions.

Note that for a large server with a lot of CustomSQL usage, this script may take a long time to run since it needs to iterate through all content in the server through the Metadata API.


## Requirements
* Tableau Server version must be 2020.1 or greater.
* Metadata Services must be enabled on the server: [Enable Metadata Services](https://help.tableau.com/current/server/en-us/dm_catalog_enable.htm#step6)
* This script uses Python 3 and was tested on Python 3.7
* This script relies on the [Tableau Server Client python library](https://github.com/tableau/server-client-python)


### Known limitations
This script does not include Custom SQL used from Prep flows.
