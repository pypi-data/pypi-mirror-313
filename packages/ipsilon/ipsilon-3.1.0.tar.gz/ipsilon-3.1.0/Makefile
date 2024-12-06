.PHONY: tests

RPMBUILD = $(PWD)/dist/rpmbuild
VERSION := $(shell python setup.py --version)
MANPAGES = man/ipsilon.7 man/ipsilon-client-install.1 man/ipsilon.conf.5 man/ipsilon-server-install.1

all: testdeps lint flake8 test security
	echo "All tests passed"

testdeps:
	# Determine if test deps are installed
	# First, some binaries
	which flake8
	which httpd
	which postgres
	which openssl
	which slapd
	# Now, python libraries
	python -c 'import argparse'
	python -c 'import requests_kerberos'
	python -c 'import openid'
	python -c 'import openid_teams'
	python -c 'import openid_cla'
	python -c 'import cherrypy'
	python -c 'import lasso'
	python -c 'import importlib.metadata; assert tuple(int(n) for n in importlib.metadata.version("sqlalchemy").split(".")[:2]) >= (1, 4)'
	python -c 'import ldap'
	python -c 'import pam'
	python -c 'import fedora'
	python -c 'import jinja2'
	python -c 'import psycopg2'
	# And now everything else
	ls /usr/lib*/security/pam_sss.so
	ls /usr/lib*/httpd/modules/mod_wsgi_python3.so
	ls /usr/libexec/mod_auth_mellon

lint:
	# Analyze code
	# don't show recommendations, info, comments, report
        # W0613 - unused argument
	# Ignore cherrypy class members as they are dynamically added
	# Ignore IPA API class members as they are dynamically added
	pylint-3 -d c,r,i,W0613,W0707 -r n -f colorized \
		   --notes= \
		   --ignored-classes=cherrypy,API \
		   --disable=star-args \
		   --extension-pkg-whitelist _ldap \
		   ./ipsilon

flake8:
	# Check style consistency
	flake8 ipsilon

security:
	# Run a static analyzer aimed at security (OpenStack Bandit)
	# Level MEDIUM and above are blocking
	bandit -r ipsilon -ll

# Requires NodeJS less and clear-css packages
ui/css/patternfly.css: less/patternfly/patternfly.less
	lessc $< $@
ui/css/%.css: less/%.less
	# Create and minify CSS
	# FIXME: temporarily disable clean-css for development
	# lessc --clean-css $< $@
	lessc $< $@

ui-node: ui/css/ipsilon.css ui/css/admin.css ui/css/styles.css ui/css/patternfly.css


man/%: man/%.in setup.py
	sed -e "s/_VERSION_/$(VERSION)/g" $< > $@

manpages: $(MANPAGES)

clean:
	rm -fr testdir cscope.out
	find ./ -name '*.pyc' -exec rm -f {} \;
	rm -f $(MANPAGES)

cscope:
	git ls-files | xargs pycscope

lp-test:
	pylint-3 -d c,r,i,W0613 -r n -f colorized \
		   --notes= \
		   --ignored-classes=cherrypy \
		   --disable=star-args \
		   --extension-pkg-whitelist _ldap \
		   ./tests
	flake8 --ignore=E121,E123,E126,E226,E24,E704,E402 tests

TESTDIR := $(shell mktemp --directory /tmp/ipsilon-testdir.XXXXXXXX)

tests:
	echo "Testdir: $(TESTDIR)"
	./runtests --path=$(TESTDIR) -vvvv

test: unittests tests

unittests:
	which python && PYTHONPATH=./ python ./ipsilon/tools/saml2metadata.py || PYTHONPATH=./ python3 ./ipsilon/tools/saml2metadata.py
	which python && PYTHONPATH=./ python ./ipsilon/util/policy.py || PYTHONPATH=./ python3 ./ipsilon/util/policy.py

sdist: manpages ui-node
	python setup.py sdist

rpmroot:
	rm -rf $(RPMBUILD)
	mkdir -p $(RPMBUILD)/BUILD
	mkdir -p $(RPMBUILD)/RPMS
	mkdir -p $(RPMBUILD)/SOURCES
	mkdir -p $(RPMBUILD)/SPECS
	mkdir -p $(RPMBUILD)/SRPMS

rpmdistdir:
	mkdir -p dist/rpms
	mkdir -p dist/srpms

rpms: rpmroot rpmdistdir sdist
	cp dist/ipsilon*.tar.gz $(RPMBUILD)/SOURCES/
	rpmbuild --define "gittag .git`git rev-parse --short HEAD`" --define "builddate .`date +%Y%m%d%H%M`" --define "_topdir $(RPMBUILD)" -ba contrib/fedora/ipsilon.spec
	mv $(RPMBUILD)/RPMS/*/ipsilon-*.rpm dist/rpms/
	mv $(RPMBUILD)/SRPMS/ipsilon-*.src.rpm dist/srpms/
	rm -rf $(RPMBUILD)

releaserpms: rpmroot rpmdistdir sdist
	cp dist/ipsilon*.tar.gz $(RPMBUILD)/SOURCES/
	rpmbuild --define "_topdir $(RPMBUILD)" -ba contrib/fedora/ipsilon.spec
	mv $(RPMBUILD)/RPMS/*/ipsilon-*.rpm dist/rpms/
	mv $(RPMBUILD)/SRPMS/ipsilon-*.src.rpm dist/srpms/
	rm -rf $(RPMBUILD)

# Running within containers
container-quickrun:
	echo "Building quickrun container ..."
	(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-dev tests/containers/Dockerfile-fedora tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/fedora:latest/' | podman build -f - -t ipsilon-quickrun .
	echo "quickrun container built"

quickrun: container-quickrun
	echo "Starting Quickrun ..."
	podman run -v `pwd`:/code:z -t --rm -it -p 8080 ipsilon-quickrun

# Testing within containers
container-centos8-stream:
	@echo "Building CentOS 8 Stream container ..."
	@(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-centos8 tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/centos:stream8/' | podman build -f - -q -t ipsilon-centos8-stream .
	@echo "CentOS 8 Stream container built"

container-centos9-stream:
	@echo "Building CentOS 9 Stream container ..."
	@(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-centos9 tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/centos:stream9/' | podman build -f - -q -t ipsilon-centos9-stream .
	@echo "CentOS 9 Stream container built"

container-fedora39:
	@echo "Building Fedora 39 container ..."
	@(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-fedora tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/fedora:39/' | podman build -f - -t ipsilon-fedora39 .
	@echo "Fedora 39 container built"

container-fedora40:
	@echo "Building Fedora 40 container ..."
	@(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-fedora tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/fedora:40/' | podman build -f - -t ipsilon-fedora40 .
	@echo "Fedora 40 container built"

container-fedora41:
	@echo "Building Fedora 41 container ..."
	@(cat tests/containers/Dockerfile-base tests/containers/Dockerfile-fedora tests/containers/Dockerfile-rpm tests/containers/Dockerfile-rpm-py3; echo "USER testuser") | sed -e 's/BASE/fedora:41/' | podman build -f - -t ipsilon-fedora41 .
	@echo "Fedora 41 container built"

containers: container-centos9-stream container-fedora39 container-fedora40 container-fedora41
	@echo "Containers built"

containertest-centos8-stream: container-centos8-stream
	@echo "Starting CentOS 8 Stream tests ..."
	@podman run -v `pwd`:/code:z -t --rm ipsilon-centos8-stream
	@echo "CentOS 8 Stream passed"

containertest-centos9-stream: container-centos9-stream
	@echo "Starting CentOS 9 Stream tests ..."
	@podman run -v `pwd`:/code:z -t --rm ipsilon-centos9-stream
	@echo "CentOS 9 Stream passed"

containertest-fedora39: container-fedora39
	@echo "Starting Fedora 39 tests ..."
	@podman run -v `pwd`:/code:z -t --rm ipsilon-fedora39
	@echo "Fedora 39 passed"

# This containertest is failing on lasso library randomly
# Removing it from containertest till new version of lasso library is available
# https://src.fedoraproject.org/rpms/lasso
containertest-fedora40: container-fedora40
	@echo "Starting Fedora 40 tests ..."
	@podman run -v `pwd`:/code:z -t --rm ipsilon-fedora40
	@echo "Fedora 40 passed"

containertest-fedora41: container-fedora41
	@echo "Starting Fedora 41 tests ..."
	@podman run -v `pwd`:/code:z -t --rm ipsilon-fedora41
	@echo "Fedora 41 passed"

containertest-lint: container-fedora41
	@echo "Starting code lint tests ..."
	@podman run -v `pwd`:/code:z -t --rm --entrypoint /usr/bin/make ipsilon-fedora39 lint security
	@echo "Code lint tests passed"

containertest: containertest-lint containertest-centos9-stream containertest-centos8-stream containertest-fedora39 containertest-fedora40 containertest-fedora41
	@echo "Container tests passed"
