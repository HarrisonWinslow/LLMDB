import sqlite3

import AIHelper

DB_PATH = '../NatLangDB.db'

def runPostQuery(queryString):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(queryString)

    connection.commit()
    connection.close()

    AIHelper.storeTableInfo()

def runGetQuery(queryString):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(queryString)
    rows = cursor.fetchall()

    connection.close()
    return rows

def dropTable(tableName):
    runPostQuery('DROP TABLE IF EXISTS ' + tableName + ';')

def clearDatabase():
    tableNames = ["Venue", "Band", "Attendee", "Concert", "BandPlaysConcert"]
    for tableName in tableNames:
        dropTable(tableName)

def getTableInfo():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    response = ""
    for table in tables:
        tableName = table[0]

        if tableName == 'sqlite_sequence': continue

        response += f'Table: {tableName}\n'

        # Get columns for the current table
        cursor.execute(f"PRAGMA table_info({tableName});")
        columns = cursor.fetchall()

        for column in columns:
            response += f'  Column: {column[1]} (Type: {column[2]})\n'

    # Close the connection
    conn.close()
    return response