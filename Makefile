.PHONY: test check
check: test
	python3 scripts/check.py

test:
	python3 -m unittest discover -s tests -v
