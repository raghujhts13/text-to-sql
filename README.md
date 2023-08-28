# text-to-sql
llama + SQL + PyGWalker + Flask

**TO DO**
- [x] basic functioning flask application to load model, get text and convert to SQL
- [x] Search database based on schema and tables
- [x] Added manual verification process before executing the SQL query
- [x] change GPT to llama for sql generation
- [X] create a select all and unselect all functionality based on schema and tables
- [X] added few validations and preloader (WIP)
- [ ] fine-tune code-llama-instruct model with custom SQL datasets
    - [X] fetched dataset
    - [X] prepared the fine-tuning code and tested the functionality in colab (code concepts work)
    - [ ] insufficeint capacity in colab => test with SageMaker
    - [ ] test the updated model and based on results upload to huggingface and use the model
- [ ] Replace the standard code-llama-instruct-7B with fine-tuned model
- [ ] change the db creds to come from UI instead of .env
- [ ] store the response history for current session ( testing feasibility )
