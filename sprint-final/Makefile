# setup dev
pre-commit:
	@pre-commit install

# serverless utils
deployfunc:
	@cd $(D) && sls deploy function -f $(F)
info:
	@cd $(D) && sls info

# api
api-deps:
	@cd chatbot/backend && pip install --no-cache-dir -r requirements.txt
run-api:
	@cd serverless && sls offline
deploy-api:
	@cd serverless && sls deploy

# lex chatbot
chatbot-deps:
	@cd serverless && pip install --no-cache-dir -r requirements.txt
deploy-chatbot:
	@cd chatbot/backend && sls deploy

# django website
run-website:
	@cd website && python manage.py runserver
