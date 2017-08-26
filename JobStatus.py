import ast
import urllib2
import base64
import sys
import argparse

import sqlite3
from sqlite3 import Error

def queryJobStatus(url, username, password,dbFile):

    hostURL = str(url + "/api/python?depth=1&tree=jobs[displayName,lastBuild[result]]")

    #assert False

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request = urllib2.Request(hostURL)
    request.add_header("Authorization", "Basic %s" % base64string)

    try:
        result = urllib2.urlopen(request)

    except Error as e:
        print("Error opening url: "+ e.message)
        sys.exit(1)


    timestamp = result.info()['Date']
    jobsObject= ast.literal_eval(result.read())
    jobsList = jobsObject['jobs']

    updateDB(dbFile,jobsList,timestamp)


def updateDB(dbFile,jobsList, timestamp):

    try:
        conn = sqlite3.connect(dbFile)

    except Error as e:
        print("DB Conn error: "+ e.message)
        sys.exit(1)


    #create new db table if none exist
    createTabel(conn)


    for (index, item) in enumerate(jobsList):

        displayName = item['displayName']
        lastBuild =  item['lastBuild']
        classType = item['_class']

        if not lastBuild == None:
            lastBuildResult = item['lastBuild']['result']
        else:
            lastBuildResult = "None"

        newRow = ( displayName , classType, lastBuildResult, timestamp)
        with conn:
            row_id = createRows(conn,newRow)

    conn.close()







def createTabel(conn):

    sql_create_jobStatus_table = """ CREATE TABLE IF NOT EXISTS jobstatus (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                class text NOT NULL,
                                                last_build_result text, 
                                                time_stamp text


                                            ); """

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_jobStatus_table)
        except Error as e:
            print("Error creating table: " + e.message)
            sys.exit(1)
    else:
        print("Error! cannot create the database connection.")
        sys.exit(1)




def createRows(conn,row):
    """
    Create a new rows into the jobstatus table
    :param conn:
    :param row:
    """
    sql = ''' INSERT INTO jobstatus (name,class,last_build_result, time_stamp)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, row)
    return cur.lastrowid




def main():


    url = raw_input('Enter jenkins server URL: ')
    dbFile = raw_input('Enter path to database file: ')
    username = raw_input('Enter Jenkins server username: ')
    password = raw_input('Enter jenkins server account password: ')

    if url == None or len(url) < 1:
        print ('invalid url input!')
        exit(1)

    if dbFile == None or len(dbFile) < 1:
        print ('invalid dbFile location')


    queryJobStatus( url,  str(username), str(password), dbFile )
    #queryJobStatus( "http://localhost:8080", "hero4barca", "password", "C:\\sqlite\db\pythonsqlite.db" )
    print ("Db successfully updated")

if __name__=="__main__":
    main()


