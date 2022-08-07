fmt:
	black .
	isort .

lint:
	isort . --check-only
	black . --check

build: pptx-templates
	poetry build

pptx-templates:
	./utils/dopptx.sh templates
	mkdir -p ./presentpy/templates
	cp ./templates/*.pptx ./presentpy/templates/

unpack-pptx:
	./utils/unpptx.sh templates

patch:
	bumpversion patch

minor:
	bumpversion minor

major:
	bumpversion major

clean:
	rm -rf dist
	rm -rf .ipynb_checkpoints
