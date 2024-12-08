build:
	make clean
	.venv/bin/python -m build

clean:
	rm dist/*

upload:
	make build
	.venv/bin/python -m twine upload --repository pypi dist/* $(flags)
