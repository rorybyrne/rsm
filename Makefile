.PHONY: test

unit-test:
	@echo "Running tests..."
	pip install tox
	tox

test:
	./test.sh

clean:
	rm -rf tmp
	rm -rf venv
