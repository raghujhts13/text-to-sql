from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os
import sys
import json
import openai
from dotenv import load_dotenv
from dbconnection import dbactivities
import pygwalker as pyg
import pandas as pd
from llama import llm
import time

nv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=nv_path)
openai.api_key = os.environ['OPENAI_KEY']

app = Flask(__name__, template_folder='templates',static_folder='static')
app.secret_key = os.environ['FLASK_KEY']

# Initiate the DB Handling Script
dbcon = dbactivities()
llm_model = llm('TheBloke/CodeLlama-7B-Instruct-GGUF','codellama-7b-instruct.Q5_K_M.gguf')
db_schema = dbcon.index()
print('SQL data fetched successfully')

connectionstring = {'Database':os.environ['DB'],
                'user':os.environ['USER'],
                'host':os.environ['HOST'],
                'port':os.environ['PORT']}

# ==================================FOR OPENAI GPT===========================================
# prompt_template = '''You are a professional SQL developer. Given an input question, respond only with syntactically correct sqlserver 
#                     query using the provided schema.\n\nSchema:""schema""\n\nInstrcutions:""instruction""'''
# ==================================FOR OPENAI GPT===========================================

current_query = 'select * from SalesLT.Address'
current_table = 'nothing'
tokens_consumed = 0
time_difference=0

def query_generator(question):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        max_tokens=500,
        temperature=0.8,
        messages=[  
            {'role':'user','content': question}
        ]
    )
    return response["choices"][0]["message"]["content"], response['usage']['total_tokens']

# FLASK APPLICATION
@app.get('/')
def index():
    normalized_data = json.dumps(db_schema)
    normalized_data = json.loads(normalized_data)
    return render_template('index.html',json_data=normalized_data, db_data=connectionstring)

# Keep the below function for openAI
'''
@app.route('/process_textarea', methods=['POST'])
def process_textarea():
    start_time = time.time()
    content = request.get_json()
    prompt = prompt_template.replace('""schema""',content['schema']).replace('""instruction""',content['query'])
    global current_query 
    current_query = "SELECT * FROM SalesLT.Customer;"
    # global tokens_consumed
    # current_query, tokens_consumed = query_generator(prompt)
    # global time_difference
    # time_difference = round((time.time() - start_time) * 1000)
    return current_query
'''

# function for llama
@app.route('/process_textarea', methods=['POST'])
def process_textarea():
    content = request.get_json()
    global current_query 
    # current_query = "SELECT * FROM SalesLT.Customer;"
    current_query, time_taken = llm_model.response_capturer(content['schema'],content['query'])
    global time_difference
    time_difference = time_taken
    return {'query':current_query, 'time':time_taken}

# function to clean the response
@app.route('/clean_query', methods=['POST'])
def clean_query():
    content = request.get_json()
    global current_query
    current_query = content['query']
    return 'done'

@app.route('/output_page')
def output_page():
    table = json.loads(dbcon.query_outputs(current_query))
    global current_table
    current_table = table
    columns = list(table.keys())
    indices = list(table[columns[0]].keys())
    return render_template('output.html', db_data=current_query, positions=indices, output=table, gpt_metadata={'tokens':tokens_consumed,'time_taken':time_difference})

@app.route('/render_dashboard')
def render_dashboard():
    if isinstance(current_table,pd.DataFrame):
        df=current_table
    else:
        df = pd.DataFrame(current_table)
    walker = pyg.walk(df,hideDataSourceConfig=True)
    walker_html = walker.to_html()
    return walker_html
if __name__ == '__main__':
    app.run(debug=True)