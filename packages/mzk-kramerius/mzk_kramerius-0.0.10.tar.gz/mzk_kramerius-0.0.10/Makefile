.PHONY: create-env rm-env publish

create-env:
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

rm-env:
	rm -r .venv/

publish:
	python setup.py sdist bdist_wheel && twine upload dist/*
