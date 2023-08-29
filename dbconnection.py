import os
import sys
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
import json

nv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=nv_path)

class dbactivities:
    ### Write down all the SQL related queries here ###
    def __init__(self):
        # Connection parameters
        self.host = os.environ['HOST']
        self.port = os.environ['PORT']
        self.database = os.environ['DB']
        self.username = os.environ['USER']
        self.password = os.environ['PASSWORD']
        # Establishing a connection with SQL Server
        try:
            connection_string = f'mssql+pymssql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
            # Create the SQLAlchemy engine
            self.engine = create_engine(connection_string)
            print(f'Connection String :: {connection_string}')
        except Exception as e:
            print(f'Unable to establish a connection because of the below reason\n{e}')
            sys.exit(1)
        self.tables = []
        self.columns = []
        self.datatypes = []
    def get_databases(self):
        query = f"""
                SELECT name FROM sys.databases WHERE database_id > 4;
                """
        # Execute the query using the engine
        with self.engine.connect() as connection:
            result = connection.execute(query)
            dbs = [row['name'] for row in result] # fetch all the tables
        return dbs
    def switch_db(self,db):
        self.database = db
        try:
            connection_string = f'mssql+pymssql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
            # Create the SQLAlchemy engine
            self.engine = create_engine(connection_string)
            print(f'Connection String :: {connection_string}')
        except Exception as e:
            print(f'Unable to establish a connection because of the below reason\n{e}')
            sys.exit(1)
    def get_tables(self):
        ### Get list of all tables ###
        # SQL query to fetch all table names from the database
        query = f"""
            SELECT *
            FROM {self.database}.INFORMATION_SCHEMA.TABLES
            ORDER BY TABLE_SCHEMA;
        """
        # Execute the query using the engine
        with self.engine.connect() as connection:
            result = connection.execute(query)
            dbtables = [f'{row[0]}.{row[1]}.{row[2]}' for row in result if 'BASE TABLE'==row[3]] # fetch all the tables
            self.tables = dbtables
        return dbtables
    def get_columns(self, table):
        ### Get list of all columns in a table ###
        query = f"""
            SELECT TABLE_NAME,COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            where TABLE_NAME='{table}'
        """
        df=pd.read_sql_query(query,self.engine)
        tblcolumns = df['COLUMN_NAME'].values # fetch all the columns
        tbltype = df['DATA_TYPE'].values
        self.columns = tblcolumns
        self.datatypes = tbltype
        return tblcolumns, tbltype
    
    def query_outputs(self, query):
        df = pd.read_sql(query, self.engine)
        def is_overflow(value):
            try:
                json.dumps(value)
                return False
            except:
                return True
        def convert_overflow_values(df):
            for col in df.columns:
                for i in df.index:
                    if is_overflow(df.loc[i, col]):
                        df.loc[i, col] = str(df.loc[i, col])
        convert_overflow_values(df)
        return df.to_json(date_format='iso') #default_handler=str
    
    def index(self):
        json_data = {}
        tables = self.get_tables()
        databases = self.get_databases()
        for table in tables:
            schema = table.split('.')[1]
            table = table.split('.')[2]
            columns, datatypes = self.get_columns(table)
            json_data[table] = []
            json_data[table].append({'schema':schema, 'name':','.join(columns),'dtypes':','.join(datatypes),'selected':True})
        return json_data