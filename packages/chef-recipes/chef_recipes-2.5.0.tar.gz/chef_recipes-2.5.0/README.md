# 🍽️ Chef

A simple, customizable recipe management app.

A simple FastAPI + SQLAlchemy app + VueJS frontend.
Frontend app is built and bundled together with the python build downloadable from PyPI -> the entire app can be run with a single command.
It's also built as a single container and can be easily hosted (with little tweaks) on GCP Cloud Run.

## Installation

```shell
curl https://raw.githubusercontent.com/xyzjonas/chef/master/install.sh | bash
```

or install the package yourself

```shell
pip install chef-recipes
chef --help
```


or run with docker:

```shell
docker run -p 8000:8000 -v ~/.chef:/chef/data scotch3840/chef:latest
```


## Build & Development
### Migrations
migrations are included in the build package, symbolic link to the alembic.ini is in the repository root
```shell
# schema changes
alembic revision --autogenerate -m "<... message ...>"

# upgrade the target database - accoring to $DATABASE_URI
alembic upgrade head

# ...or can be executed from the built script - i.e. without the sources
chef migrate-db
```
### Build
1. Poetry: build the standalone Python package
```shell
cd ./src/js/chef
npm run build
cd -
poetry build
```
```shell
poetry publish
```
2. Build the docker image
```shell
docker build . -t scotch3840/chef
```
```shell
docker push scotch3840/chef
```

---------

...or run on GCP using `scotch3840/misc:chef-gcp` image (PostgreSQL):
> ! second generation execution environment required.
- `BUCKET`: name of your GCP/CloudStorage bucket.
- `MNT_DIR`: target where the bucket will be mounted.
- `IMAGES_FOLDER`: where the app will be looking for and storing uploaded images, has to be somewhere inside your bucket.
- `DATABASE_URI`: specify your posgres or possibly put an sqlite file in the bucket as well.
