from ctransformers import AutoModelForCausalLM
import time
import re
import os
from dotenv import load_dotenv

nv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=nv_path)

# os.environ['HF_HOME'] = "path to your model..." # this is to download your model to specific location instead of "/users/{user}/.cache"
class llm:
    def __init__(self,model='',version=''):
        self.model = model
        self.version = version
        self.llm = ''
        self.template = '''[INST] You are a professional SQL developer. Understand the question asked and return the most suitable query
                            supported by SQLSERVER using the table : ""{schema}"". Always write sql server standard queries.
                            Always wrap your code answer using ```. question: {prompt} [/INST]'''
    def load_model(self):
        try:
            if self.model and self.version:
                llm_model = AutoModelForCausalLM.from_pretrained(os.environ['MODEL_PATH'],local_files_only=True)
            elif self.model:
                llm_model = AutoModelForCausalLM.from_pretrained(self.model,local_files_only=True)
            else:
                raise Exception("You don't have a local model")
            self.llm = llm_model
            return llm_model
        except Exception as e:
            try:
                if self.model and self.version:
                    llm_model = AutoModelForCausalLM.from_pretrained(self.model,model_file=self.version)
                elif self.model:
                    llm_model = AutoModelForCausalLM.from_pretrained(self.model)
                self.llm = llm_model
            except Exception as e:
                return f'Unable to find a local model. When tried to install, below error occurred\n{e}'
    def response_capturer(self,schema,prompt):
        try:
            start_time=time.time()
            template = self.template.replace("{schema}",schema).replace("{prompt}",prompt)
            if self.llm:
                model = self.llm
                print(model)
            else:
                 model = self.load_model()
                 print(model)
                 if type(model)==str:
                     raise Exception(model)
            sql_query = model(template)
            try:
                sql_query = re.findall(r'```([\s\S]*?)```',sql_query, re.DOTALL)[0]
            except:
                pass
            end_time = time.time()
            return sql_query, (end_time-start_time)
        except Exception as e:
            return f'Error in loading the response\n {e}',0


    
            


