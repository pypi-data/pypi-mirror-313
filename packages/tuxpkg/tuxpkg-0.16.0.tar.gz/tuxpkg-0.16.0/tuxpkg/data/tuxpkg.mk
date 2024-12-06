.PHONY: test

export MODULE ?= $(shell echo $(PROJECT) | sed -e 's/-/_/g')
TUXPKG_MIN_COVERAGE ?= 100
ifneq ($(NUM_WORKERS),)
WORKERS="--workers=$(NUM_WORKERS)"
endif

test:
	python3 -m pytest $(WORKERS) --cov=$(MODULE) --cov-report=term-missing --cov-report=html --cov-report=xml:coverage.xml --cov-fail-under=$(TUXPKG_MIN_COVERAGE) $(TUXPKG_PYTEST_OPTIONS)

style:
	black --check --diff $(TUXPKG_BLACK_OPTIONS) .

flake8:
	flake8 --exclude=dist/ --ignore=E501,W503 $(TUXPKG_FLAKE8_OPTIONS) .

typecheck:
	mypy --exclude=dist/ $(TUXPKG_MYPY_OPTIONS) .

version ?= $(shell sed -e '/^__version__/ !d; s/"\s*$$//; s/.*"//' $(MODULE)/__init__.py)

CLEAN += dist

rpm: dist/$(PROJECT)-$(version)-0$(MODULE).noarch.rpm

RPMBUILD = rpmbuild
dist/$(PROJECT)-$(version)-0$(MODULE).noarch.rpm: dist/$(PROJECT)-$(version).tar.gz dist/$(PROJECT).spec
	cd dist && \
	$(RPMBUILD) -ta --define "dist $(MODULE)" --define "_rpmdir $$(pwd)" $(PROJECT)-$(version).tar.gz
	mv $(patsubst dist/%, dist/noarch/%, $@) $@
	rmdir dist/noarch

rpmsrc: dist dist/$(PROJECT).spec

dist/$(PROJECT).spec: $(PROJECT).spec
	cp $(PROJECT).spec dist/

dist: dist/$(PROJECT)-$(version).tar.gz

dist/$(PROJECT)-$(version).tar.gz:
	flit build
	find dist/ -type f
	if [ ! -f $@ ]; then git archive --prefix=$(PROJECT)-$(version)/ --output=$@ HEAD; fi

deb: debsrc dist/$(PROJECT)_$(version)-1_all.deb

dist/$(PROJECT)_$(version)-1_all.deb: dist/$(PROJECT)_$(version)-1.dsc
	cd dist/$(PROJECT)-$(version) && dpkg-buildpackage -b -us -uc

debsrc: dist dist/$(PROJECT)_$(version)-1.dsc dist/$(PROJECT)_$(version).orig.tar.gz

dist/$(PROJECT)_$(version).orig.tar.gz: dist/$(PROJECT)-$(version).tar.gz
	ln -f $< $@

dist/$(PROJECT)_$(version)-1.dsc: debian dist/$(PROJECT)_$(version).orig.tar.gz $(wildcard debian/*)
	cd dist && tar xaf $(PROJECT)_$(version).orig.tar.gz
	cp -r debian/ dist/$(PROJECT)-$(version)
	cd dist/$(PROJECT)-$(version)/ && dpkg-buildpackage -S -d -us -uc

CLEAN += run
run:
	echo "#!/bin/sh" > $@
	echo "set -eu" >> $@
	echo 'realfile="$$(readlink -f "$$0")"' >> $@
	echo 'export PYTHONPATH="$$(dirname "$$realfile")"' >> $@
	echo 'exec python3 -m $(MODULE) "$$@"' >> $@
	chmod +x run

release:
	python3 -m tuxpkg release

clean::
	$(RM) -r $(CLEAN)
