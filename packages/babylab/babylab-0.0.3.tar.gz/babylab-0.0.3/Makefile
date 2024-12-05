main:
	python -m main

venv:
	python -m venv .venv

serve:
	python -m flask --app babylab.main run

debug:
	python -m flask --app babylab.main run  --debug 

freeze:
	python -m pip freeze -l > requirements.txt 

install:
	python -m pip install -r requirements.txt
