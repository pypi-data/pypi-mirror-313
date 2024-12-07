.PHONY: init
.PHONY: clean
.PHONY: build
.PHONY: install


init:
	make install

clean:
	python3 -m pip uninstall gitlabcis -y
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf build dist gitlabcis.egg-info .tox htmlcov .coverage coverage.xml .coverage.* results.* .pytest_cache

build:
	@echo "Removing previous builds..."
	make clean
	@echo "Building gitlabcis..."
	python3 -m pip install -q .[build]
	python3 -m build


install:
	@echo "Installing gitlabcis..."
	python3 -m pip install -q .
	python3 -m pip install -q .[test,build]
	pre-commit install
	pre-commit install --hook-type commit-msg
