## Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Install and start the virtual environment

Before all, install the virtual environment. on the root folder, type the command bellow.

```shell
python -m venv .venv
```

To start the created venv:

```shell
. .venv/bin/activate
```

## Saving packages

Before any commit, save the packages installed, typing the command bellow:

```shell
pip freeze > requirements.txt
```

## Install packages

```shell
pip install -r requirements.txt
```

## Start migrations

```shell
flask db init
```

## Run migrations

```shell
flask db migrate
```

## Apply migrations

```shell
flask db upgrade
```
