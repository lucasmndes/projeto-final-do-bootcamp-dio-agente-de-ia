.PHONY: install run test

install:
	python -m pip install -r src/requirements.txt

run:
	python -m streamlit run src/app.py

test:
	python -m unittest discover -s tests -v
