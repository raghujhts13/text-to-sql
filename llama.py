from ctransformers import AutoModelForCausalLM
import time
import re
import os
from dotenv import load_dotenv

nv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=nv_path)

class llm:
    def __init__(self,model='TheBloke/CodeLlama-7B-Instruct-GGUF',version='codellama-7b-instruct.Q5_K_M.gguf'):
        self.model = model
        self.version = version
        self.llm = ''
        self.template = '''[INST] You are a professional SQL developer. Understand the question asked and return the most suitable query
                            supported by SQLSERVER using the table schema : ""{schema}"". Always combine the schema name with table
                            name when writing the query. Always wrap your code answer using ```: {prompt} [/INST]'''
    def load_model(self):
        try:
            if self.model and self.version:
                llm_model = AutoModelForCausalLM.from_pretrained(os.environ['MODEL_PATH'],local_files_only=True)
                print(llm_model)
            elif self.model:
                llm_model = AutoModelForCausalLM.from_pretrained(self.model,local_files_only=True)
            self.llm = llm_model
            return llm_model
        except:
            return 'Error loading the model'
    def response_capturer(self,schema,prompt):
        try:
            start_time=time.time()
            template = self.template.replace("{schema}",schema).replace("{prompt}",prompt)
            if self.llm:
                model = self.llm
            else:
                 model = self.load_model()
                 if type(model)==str:
                     raise Exception(model)
            sql_query = model(template)
            # print(sql_query)
            # sql_query = re.findall(r'```([\s\S]*?)```',sql_query, re.DOTALL)[0]
            end_time = time.time()
            return sql_query, (end_time-start_time)
        except Exception as e:
            return f'Error in loading the response\n {e}',0


    
            


