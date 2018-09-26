# clair-layer-issue

## Description

This repo is a demonstration of an issue with the Clair vulnerability scanner.
Clair reports vulnerabilities in all layers, even if a recent layer patches the
vulnerability in some way e.g. removes the affected package.

## Docker images and layers

## Walkthrough of the issue

### Install Clair

Just run `docker-compose up -f docker-compose.yml -d` to run two containers,
Clair and a postgres database. Then wait a considerable amount of time (hours)
for the database to be populated with vulnerability data from CVE databases.

There is a gotcha in the docker-compose.yml provided by the Clair repo - it
references the image `quay.io/coreos/clair-git:latest` which is not a stable
release and the v1 API didn't work when I used that image, so it's changed to
`quay.io/coreos/clair:v2.0.1` in docker-compose.yml in this repo.

### Install paclair and scan image

Paclair is a command line tool for interacting with the Clair API to scan an
image. Run:
- `pip install paclair`
- `paclair --conf paclair.conf Docker nginx:1.12.0 push`
- `paclair --conf paclair.conf Docker nginx:1.12.0 analyse 2>&1 > /dev/null | python3 get-vulnerable-packages.py`

This outputs a list of vulnerable packages and versions. For this, I'm going to
pick on libtiff5, which appears to be used in nginx in the
`ngx_http_image_filter_module` which transforms images on the fly. Let's say
this module is not needed and we'd like to remove it to remove a potential
attack vector.

### Remove the package and rescan

There's a simple Dockerfile in this repository which starts from nginx:1.12.0
and removes the package. Run (substituting your docker username):
- `docker build -t karlhopkinsonturrell/nginx:1.12.0-hardened .`
- `docker push karlhopkinsonturrell/nginx:1.12.0-hardened`

Then repeat the scan:

- `paclair --conf paclair.conf Docker karlhopkinsonturrell/nginx:1.12.0-hardened push`
- `paclair --conf paclair.conf Docker karlhopkinsonturrell/nginx:1.12.0-hardened analyse 2>&1 > /dev/null | python3 get-vulnerable-packages.py`

