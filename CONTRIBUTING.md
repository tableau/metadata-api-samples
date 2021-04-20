# Contributing Samples

This project is used to share samples of using the Metadata API. Contributions to this project are welcome and can include any of the following:
* Request for a new sample, task or scenario
* Fix for an issue/bug with a sample
* A new sample

Contributions will be approved via pull-request from a Tableau maintainer of this repository.

Note: Contributions must follow the guidelines outlined on the [Tableau Organization page](http://tableau.github.io/contributing.html), though filing an issue or requesting a new sample does not require the CLA.

## Sample formats
There are two main formats for samples in this project: simple and advanced. 

### Simple format
The simplest samples only include Metadata API queries. For those samples, add a file containing your sample queries under the `/samples` directory that meet the following guidelines: 
* **Descriptive file name:** The file name should be descriptive of the types of queries or tasks your sample includes.
* **Comment with server versions tested:** The file must include a comment at the top with the server version(s) the queries were tested against.

### Advanced format
If your sample involves additional scripts or steps beyond running queries directly against the Metadata API (e.g. Python scripts that process the results of a query), follow the format described below.
1. Add a new folder under the `/samples` directory with a descriptive name of your sample
2. Within `/samples/<your_sample_name>`, the following files should be included:
  * **`Readme.md`:** In the readme, describe the scenario or task this query addresses. The readme should include the Tableau Server version that the sample was written for and all versions you have verified it to work on. Optionally includes instructions for any other files or scripts included in this sample.
  * **`.graphql` file(s):** Include the GraphQL files containing all of the Metadata API queries used by this sample. These GraphQL query files should always include a comment in the top with the server version(s) they were tested against or used on when the sample was authored.
  * **(Optional) Other scripts:** If there are any other scripts you wish to share (e.g. Python scripts). Please share those in the project here.

## Feature requests
Share your feature requests on the [Tableau Ideas](https://community.tableau.com/community/ideas) forum using `metadata_api` tag.
