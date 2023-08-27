# text-to-sql
llama + SQL + PyGWalker + Flask

**TO DO**
- [x] basic functioning flask application to load model, get text and convert to SQL
- [x] Search database based on schema and tables
- [x] Added manual verification process before executing the SQL query
- [x] change GPT to llama for sql generation
- [X] create a select all and unselect all functionality based on schema and tables
- [ ] added few validations and preloader (WIP)
- [ ] fine-tune code-llama-instruct model with custom SQL datasets
- [ ] Replace the standard code-llama-instruct-7B with fine-tuned model
- [ ] Edit the llama.py to add more configurations to model selection and training
- [ ] change the db creds to come from UI instead of .env
- [ ] store the response history for current session ( testing feasibility )
