import sqlite3
import os
import json
import pandas as pd

def get_file_path(name:str, format:str):
     file = name + '.' + format
     path = os.path.join("data", file)

     return file, path



table_country = 'country_cd'
table_language = 'language_cd'
table_upp = 'upp_dataset'
conn = sqlite3.connect('epo.db')
cursor = conn.cursor()
def main():
     table = table_upp.split('_')[0]
     upp_file, upp_path = get_file_path(table_upp, "json")
     country_file, country_path = get_file_path(table_country, 'csv')
     language_file, language_path = get_file_path(table_language, 'csv')

     # Create upp dataframe
     df_upp = pd.read_json(upp_path)

     # Create country dataframe
     df_country = pd.read_csv(country_path)
     df_country['Code'] = df_country['Code'].str.lower()

     # Create language dataframe
     df_language = pd.read_csv(language_path)

     df = pd.merge(df_upp, df_country, left_on='Country proprietor', right_on='Code', how='left')
     df = pd.merge(df, df_language, left_on='Procedural language', right_on='LanguageCode', how='left')
     df = pd.merge(df, df_language, left_on='Translation language', right_on='LanguageCode', how='left', suffixes=(' Procedural', ' Translation'))

     df.to_sql(table, conn, if_exists = 'replace')
     conn.commit()

     #conn.close()

main()





