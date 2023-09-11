# DSW2Seek

## Project overview

dsw2seek is a python web application that uses Data Management Plans (DMPs) from DSW to create projects in FAIRDOM-SEEK.

## Important resources

DSW test environment: https://dsw-test.elixir.no/ \
DSW SDK: https://github.com/ds-wizard/dsw-sdk

Seek API documentation: https://docs.seek4science.org/tech/api/ \
Examples using the Seek API: https://docs.seek4science.org/help/user-guide/api.html \
Seek for Docker: https://docs.seek4science.org/tech/docker

## Project setup

### Docker

First, create the following 4 volumes in Docker:

```
docker volume create --name=seek-filestore
docker volume create --name=seek-mysql-db
docker volume create --name=seek-solr-data
docker volume create --name=seek-cache
```

Run `docker-compose` in the root directory of this project:

```
docker-compose -f docker/docker-compose.yml up
```

### Environment variables

Create a file `.env` in the root directory of the project. Fill in the following variables:

```
SEEK_USERNAME=<username>
SEEK_PASSWORD=<password>
```

These are the credentials for your local instance of Seek running in Docker.

## Seek API

Example request to the Seek API:

```
GET http://localhost:3000/projects/1 HTTP/1.1
Accept: application/vnd.api+json
Accept-Charset: ISO-8859-1
Authorization: Basic <credentials>
Content-Type: application/vnd.api+json
```

The authorization credentials are the base64-encoding of the string `<username>:<password>`.
