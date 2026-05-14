.PHONY: build check test clean

build:
	python -m scripts.build

check:
	python -m scripts.check

test:
	pytest -v

# Note: no `bump` target — bell-labs is an original synthesis, not a port,
# so there is no upstream SHA to bump.
clean:
	rm -rf COMPANY.md teams/ agents/ images/
