all: typecheck test style flake8

export PROJECT := tuxpkg
include tuxpkg/data/tuxpkg.mk

doc: docs/index.md
	mkdocs build

docs/index.md: README.md scripts/readme2index.sh
	scripts/readme2index.sh $@

doc-serve:
	mkdocs serve
