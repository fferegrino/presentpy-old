fmt:
	black .
	isort .

build: pptx-templates
	poetry build

pptx-templates:
	./utils/dopptx.sh templates
	mkdir -p ./presentpy/templates
	cp ./templates/*.pptx ./presentpy/templates/

unpack-pptx:
	./utils/unpptx.sh templates

clean:
	rm -rf dist
	rm -rf .ipynb_checkpoints
