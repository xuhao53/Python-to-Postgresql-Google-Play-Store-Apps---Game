import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#read csv file and create a copy
data = pd.read_csv('google_play_store_dataset.csv')
df = data.copy()
#check dataframe types
df.info()

#check missing values
df.isna().sum()
#replace null value with 0 as its default value for 'Rating'
df.fillna({'Rating' : 0}, inplace=True)

#drop missing and not important columns
df = df.drop(columns=['Current Ver', 'Android Ver'])

#check the missing type row
df_type_null = df[df['Type'].isna()]
df['Type'] = df['Type'].fillna('Free')

df['Content Rating'].isna()
i= df[df['Content Rating'].isna()].index
df = df.drop(index = i)

df['Price'].value_counts()
df['Price'] = df['Price'].str.replace('$','')
df['Price'] = df['Price'].astype(float)

#convert Size column to float by removing the M, replace 'Varies with device' with mean()
# Define a function to convert all sizes to MB
def convert_to_mb(size):
    if pd.isna(size): 
        return size
    elif 'M' in size: 
        return round(float(size.replace('M', '')),1)
    elif 'K' in size:  # Convert KB to MB (1 KB = 1/1024 MB)
        return round(float(size.replace('K', '')) / 1024,1)
    elif 'G' in size:  # Convert GB to MB (1 GB = 1024 MB)
        return round(float(size.replace('G', '')) * 1024,1)
    return np.nan

df['Size'] = df['Size'].replace('Varies with device', np.nan)
df['Size'] = df['Size'].apply(convert_to_mb)
mean_size = round(df['Size'].mean(),1)
df['Size'].fillna(mean_size, inplace=True)

#convert Last Updated column to datatime type
df['Last Updated'] = pd.to_datetime(df['Last Updated'])
#drop duplicates
df.drop_duplicates(subset=['App','Category'],inplace=True)

#create a rough number of installs column
df['InstallCounts'] = df['Installs'].str.replace('+','').str.replace(',','').astype(int)

#change column names to lowercase, since it works better with PostgreSQL
df.columns = df.columns.str.lower()
# Database credentials
db_name = "google_play_store_app"
username = "postgres"
password = "passport"
host = "localhost"  
port = "5433"      

# Create the SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}')

# Convert the DataFrame to a SQL table
# Replace 'your_table_name' with the name of the table you want in the database
df.to_sql('googleplaystore_app', engine, if_exists='replace', index=False)

# Close the connection
engine.dispose()
print("Data has been successfully saved to PostgreSQL.")


