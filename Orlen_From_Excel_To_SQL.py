from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import functools
import operator
import sqlite3
import xlrd

#połączenie z SQL
my_path='C:\\Users\\barte\\Desktop\\Oreln16.db' # update path
my_conn = create_engine("sqlite:///"+ my_path) # connection object
connection_obj = sqlite3.connect(my_path)
cursor_obj = connection_obj.cursor()

excel_name = [2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]
column_name_index = 1
column_index = 3
row_index = 1
sheet = "RZiS"

connection_obj = sqlite3.connect(my_path)
cursor_obj = connection_obj.cursor()

# Create a table in the database to store the data
cursor_obj.execute(f'''
     CREATE TABLE IF NOT EXISTS Orlen (
         Nazwa_Pozycji TEXT,
         "2022" INTEGER,
         "2021" INTEGER,
         "2020" INTEGER,
         "2019" INTEGER,
         "2018" INTEGER,
         "2017" INTEGER,
         "2016" INTEGER,
         "2015" INTEGER,
         "2014" INTEGER,
         "2013" INTEGER
     );
 ''')

for x in excel_name:
    i = str(x)
    # Use reduce() to convert tuple to string so the path will be usable as a path
    tuples = ("C:\\Users\\barte\\Desktop\\Orlen_Skon_Roczny_EXCEL\\", (i), ".xls")
    string = functools.reduce(operator.add, (tuples))

    path = (string)
    df = pd.read_excel (path , sheet_name= sheet)  # create DataFrame by reading Excel

#Telling program from were to take data , and converting data to list
    name_column = df.iloc[row_index :, column_name_index]
    data_column = df.iloc[row_index :, column_index]
    name_list = name_column.astype(str).tolist()
    data_list = data_column.astype(float).tolist()

    name_list_LOW = [elem.strip().lower().replace("/"," ") for elem in name_list]


    for name, data in zip(name_list_LOW, data_list):
            # Check if the 'Nazwa_Pozycji' already exists in the database
            cursor_obj.execute("SELECT COUNT(*) FROM Orlen WHERE Nazwa_Pozycji = ?", (name,))
            count = cursor_obj.fetchone()[0]

            if count == 0:
                # If 'Nazwa_Pozycji' doesn't exist, insert it
                cursor_obj.execute("INSERT INTO Orlen (Nazwa_Pozycji) VALUES (?)", (name,))

            # Now, update the corresponding year's column with the data
            cursor_obj.execute(f'''
                   UPDATE Orlen
                   SET "{i}" = ?
                   WHERE Nazwa_Pozycji = ?
               ''', (data, name))

connection_obj.commit()
connection_obj.close()

print("Done")