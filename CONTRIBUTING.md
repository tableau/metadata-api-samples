# Contributing Samples

This project is used to share samples of using the Metadata API. Contributions to this project are welcome and can include any of the following:
* Request a new sample for a new task or scenario
* Fix an Issue/Bug with a sample
* Add a new sample

Contributions will be approved via pull-request from a Tableau maintainer of this repository.

Contributions must follow the guidelines outlined on the [Tableau Organization page](http://tableau.github.io/contributing.html), though filing an issue or requesting a new sample do not require the CLA.

## Sample Formats
There are two main formats for samples in this project. 
### Simple Format
The simplest samples only include Metadata API queries. For those, please add a file containing your sample queries under the `/samples` directory with the following guidelines.
* The file name should be descriptive of the types of queries or tasks your sample includes.
* The file must include a comment at the top with the server version(s) the queries were tested against.

### Advanced Format
If your sample involves additional scripts or steps beyond running queries directly against the Metadata API (e.g. Python scripts that process the results of a query), please follow the below format.
1. Add a new folder under the `/samples` directory with a descriptive name of your sample
2. Within `/samples/<your_sample_name>` the following files should be included:
  * `Readme.md`: To describe the scenario or task this query helps. A readme should include the Tableau Server version that the sample was written for and all versions you have verified it to work on. Optionally includes instructions for any other files or scripts included in this sample.
  * `.graphql` file(s) containing all of the Metadata API queries used for this sample. GraphQL query files should always include a comment in the top with the server version they were used on when the sample was authored.
  * <em>Optional</em> If there are any other scripts you wish to share (e.g. Python scripts). Please share those in the project here.


## Feature Requests
Please share feature requests on the [Tableau Ideas forum](https://community.tableau.com/community/ideas) using `metadata_api` tag. 

