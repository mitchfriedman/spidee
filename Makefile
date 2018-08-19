nopyc:
	find . -name '*.pyc' | xargs rm -f || true

install: venv
	. venv/bin/activate; \
	pip install -r requirements.txt

test: nopyc
	. venv/bin/activate; \
	python -m unittest

venv:
	virtualenv --python=python3 venv

clean:
	rm -rf venv

