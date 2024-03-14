import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the SQLite database file
my_path = 'C:\\Users\\barte\\Desktop\\Oreln16.db'

# Connect to the SQLite database
conn = sqlite3.connect(my_path)

def add_labels(years, row_data):
    for i in range(len(years)):
        plt.text(i, row_data[i], row_data[i], ha='center')

# Retrieve the list of unique "Nazwa_Pozycji" from the database
query = "SELECT DISTINCT Nazwa_Pozycji FROM Orlen"
unique_positions = [row[0] for row in conn.execute(query)]

# Specify the values you want to retrieve for each position
for row_value in unique_positions:
    # Define the SQL query to select all columns for the specified row
    sql = f"""SELECT *
    FROM Orlen
    WHERE "Nazwa_Pozycji" = '{row_value}'
    """

    # Execute the SQL query and store the results in a DataFrame
    data = pd.read_sql(sql, conn)

    # Extract the values of the selected row (excluding non-year columns)
    row_data = data.iloc[:, 1:].values[0]

    # Check for None values and ensure all values are greater than 0
    if row_data is not None and all(value is not None for value in row_data):
        # Create a bar chart for the row data
        years = [str(year) for year in range(2013, 2023)]

        plt.figure(figsize=(10, 6))
        plt.bar(years, row_data)
        add_labels(years, row_data)

        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.title(f'Bar Chart for Position: {row_value}')

        plt.xticks(rotation=45)

        # Construct a unique file path for each plot
        file_path = f'C:\\Users\\barte\\PycharmProjects\\HelloWorld\\orlen\\static\\images\\{row_value}.png'

        # Save the plot using the constructed file path
        plt.savefig(file_path)

        # Close the plot
        plt.close()

