import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('workouts.db')

# Fetch data from the database
df = pd.read_sql_query("SELECT * FROM workout", conn)

# Perform data analysis
summary = df.describe()

# Print the summary statistics
print(summary)