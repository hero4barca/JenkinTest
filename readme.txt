A python script for querying jobs on a specified Jenkin server
The script queries all existing jobs on a Jenkins server and stores the details in a specified database.

jenkins server url, path-to-databasefile and server login parameters are provided as input into the script

Assumptions:
database file location will be given as input into the script
jobstatus is captured by : job name, job class and lastbuild status
jenkins server account details i.e. username and password will be provided as input into script.
In the database table, each row does not represent a unique job but unique status checks - only the id is unique 
